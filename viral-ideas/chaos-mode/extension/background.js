// Chaos Mode - Background Script
// background.js

// Chaos event types
const CHAOS_EVENTS = {
  ROAST: 'roast',
  DANCE_BREAK: 'dance_break',
  MEME_FLOOD: 'meme_flood',
  TRIVIA: 'trivia',
  FORTUNE: 'fortune',
  PUPPY: 'puppy'
};

// Personas
const PERSONAS = {
  GEN_Z: {
    name: 'Chaotic Gen Z',
    greetings: ['bestie', 'bestie fr fr', 'no cap', "it's giving"],
    style: 'casual, internet slang, emojis'
  },
  DRILL_SERGEANT: {
    name: 'Drill Sergeant',
    greetings: ['MAGGOT', 'SOLDIER', 'RECRUIT'],
    style: 'aggressive, all caps, military'
  },
  SHAKESPEARE: {
    name: 'Dramatic Shakespeare',
    greetings: ['Dear friend', 'Noble worker', 'Fair user'],
    style: 'old english, dramatic, poetic'
  }
};

// Default settings
const DEFAULT_SETTINGS = {
  chaosLevel: 5, // 1-10
  persona: 'gen-z',
  enabled: true,
  workHours: { start: 9, end: 17 },
  doNotDisturb: false
};

// Initialize extension
chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.set({
    settings: DEFAULT_SETTINGS,
    stats: {
      totalChaosEvents: 0,
      chaosPoints: 0,
      achievements: [],
      lastChaosTime: null
    }
  });
  
  // Set up chaos alarm
  scheduleNextChaos();
});

// Schedule next chaos event
function scheduleNextChaos() {
  chrome.storage.local.get(['settings'], (result) => {
    const settings = result.settings || DEFAULT_SETTINGS;
    
    if (!settings.enabled || settings.doNotDisturb) {
      return;
    }
    
    // Random time between 15-60 minutes based on chaos level
    const minMinutes = 60 - (settings.chaosLevel * 5); // Level 10 = 10 min, Level 1 = 55 min
    const maxMinutes = 65 - (settings.chaosLevel * 5);
    const randomMinutes = Math.floor(Math.random() * (maxMinutes - minMinutes + 1)) + minMinutes;
    
    chrome.alarms.create('chaosTime', { delayInMinutes: randomMinutes });
  });
}

// Alarm listener
chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'chaosTime') {
    triggerChaos();
  }
});

// Trigger chaos event
async function triggerChaos() {
  const eventType = selectRandomEvent();
  
  // Get current tab
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  
  if (tab) {
    // Send chaos to content script
    chrome.tabs.sendMessage(tab.id, {
      action: 'TRIGGER_CHAOS',
      eventType: eventType,
      timestamp: Date.now()
    });
    
    // Update stats
    updateStats(eventType);
  }
  
  // Schedule next chaos
  scheduleNextChaos();
}

// Select random chaos event
function selectRandomEvent() {
  const events = Object.values(CHAOS_EVENTS);
  return events[Math.floor(Math.random() * events.length)];
}

// Update user stats
function updateStats(eventType) {
  chrome.storage.local.get(['stats'], (result) => {
    const stats = result.stats || { totalChaosEvents: 0, chaosPoints: 0, achievements: [] };
    
    stats.totalChaosEvents++;
    stats.lastChaosTime = Date.now();
    
    // Add chaos points
    const points = {
      [CHAOS_EVENTS.ROAST]: 25,
      [CHAOS_EVENTS.DANCE_BREAK]: 100,
      [CHAOS_EVENTS.MEME_FLOOD]: 50,
      [CHAOS_EVENTS.TRIVIA]: 75,
      [CHAOS_EVENTS.FORTUNE]: 10,
      [CHAOS_EVENTS.PUPPY]: 30
    };
    
    stats.chaosPoints += points[eventType] || 10;
    
    // Check achievements
    checkAchievements(stats);
    
    chrome.storage.local.set({ stats });
  });
}

// Check for new achievements
function checkAchievements(stats) {
  const newAchievements = [];
  
  if (stats.totalChaosEvents >= 5 && !stats.achievements.includes('tornado')) {
    newAchievements.push('tornado');
  }
  
  if (stats.totalChaosEvents >= 20 && !stats.achievements.includes('roasted')) {
    newAchievements.push('roasted');
  }
  
  if (stats.chaosPoints >= 1000 && !stats.achievements.includes('chaos-god')) {
    newAchievements.push('chaos-god');
  }
  
  if (newAchievements.length > 0) {
    stats.achievements.push(...newAchievements);
    
    // Notify user
    chrome.notifications.create({
      type: 'basic',
      iconUrl: 'icons/icon128.png',
      title: '🎉 Achievement Unlocked!',
      message: `You earned: ${newAchievements.join(', ')}`
    });
  }
}

// Listen for messages from popup/content
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'GET_SETTINGS') {
    chrome.storage.local.get(['settings'], (result) => {
      sendResponse(result.settings || DEFAULT_SETTINGS);
    });
    return true;
  }
  
  if (request.action === 'UPDATE_SETTINGS') {
    chrome.storage.local.set({ settings: request.settings }, () => {
      scheduleNextChaos();
      sendResponse({ success: true });
    });
    return true;
  }
  
  if (request.action === 'GET_STATS') {
    chrome.storage.local.get(['stats'], (result) => {
      sendResponse(result.stats || { totalChaosEvents: 0, chaosPoints: 0, achievements: [] });
    });
    return true;
  }
  
  if (request.action === 'TRIGGER_CHAOS_NOW') {
    triggerChaos();
    sendResponse({ success: true });
  }
});
