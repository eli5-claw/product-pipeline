// Chaos Mode - Popup Script
// popup.js

// DOM Elements
const chaosCountEl = document.getElementById('chaosCount');
const chaosPointsEl = document.getElementById('chaosPoints');
const achievementCountEl = document.getElementById('achievementCount');
const enabledToggle = document.getElementById('enabledToggle');
const chaosLevel = document.getElementById('chaosLevel');
const chaosLevelValue = document.getElementById('chaosLevelValue');
const personaSelect = document.getElementById('personaSelect');
const achievementsContainer = document.getElementById('achievements');
const triggerBtn = document.getElementById('triggerChaos');

// Load settings and stats
document.addEventListener('DOMContentLoaded', () => {
  loadSettings();
  loadStats();
});

// Load settings
function loadSettings() {
  chrome.runtime.sendMessage({ action: 'GET_SETTINGS' }, (settings) => {
    if (settings) {
      enabledToggle.checked = settings.enabled !== false;
      chaosLevel.value = settings.chaosLevel || 5;
      chaosLevelValue.textContent = chaosLevel.value;
      personaSelect.value = settings.persona || 'gen-z';
    }
  });
}

// Load stats
function loadStats() {
  chrome.runtime.sendMessage({ action: 'GET_STATS' }, (stats) => {
    if (stats) {
      chaosCountEl.textContent = stats.totalChaosEvents || 0;
      chaosPointsEl.textContent = stats.chaosPoints || 0;
      achievementCountEl.textContent = (stats.achievements || []).length;
      
      updateAchievements(stats.achievements || []);
    }
  });
}

// Update achievements display
function updateAchievements(unlockedAchievements) {
  const allAchievements = [
    { id: 'tornado', icon: '🌪️', name: 'Tornado' },
    { id: 'roasted', icon: '💀', name: 'Roasted' },
    { id: 'dancer', icon: '🎵', name: 'Dancer' },
    { id: 'chaos-god', icon: '🔥', name: 'Chaos God' }
  ];
  
  achievementsContainer.innerHTML = allAchievements.map(ach => {
    const isUnlocked = unlockedAchievements.includes(ach.id);
    return `
      <span class="badge ${isUnlocked ? '' : 'locked'}" title="${isUnlocked ? 'Unlocked!' : 'Locked'}">
        ${ach.icon} ${ach.name}
      </span>
    `;
  }).join('');
}

// Save settings
function saveSettings() {
  const settings = {
    enabled: enabledToggle.checked,
    chaosLevel: parseInt(chaosLevel.value),
    persona: personaSelect.value
  };
  
  chrome.runtime.sendMessage({
    action: 'UPDATE_SETTINGS',
    settings: settings
  });
}

// Event Listeners
enabledToggle.addEventListener('change', saveSettings);

chaosLevel.addEventListener('input', (e) => {
  chaosLevelValue.textContent = e.target.value;
  saveSettings();
});

personaSelect.addEventListener('change', saveSettings);

triggerBtn.addEventListener('click', () => {
  chrome.runtime.sendMessage({ action: 'TRIGGER_CHAOS_NOW' }, () => {
    // Visual feedback
    triggerBtn.textContent = '🎉 Chaos Triggered!';
    triggerBtn.style.background = '#4CAF50';
    
    setTimeout(() => {
      triggerBtn.textContent = '🎲 Trigger Chaos Now';
      triggerBtn.style.background = 'white';
    }, 2000);
    
    // Refresh stats after a moment
    setTimeout(loadStats, 1000);
  });
});

// Refresh stats periodically
setInterval(loadStats, 5000);
