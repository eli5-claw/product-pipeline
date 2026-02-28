// Chaos Mode - Content Script
// content.js

// Roast templates
const ROAST_TEMPLATES = {
  'gen-z': [
    "bestie you've been staring at this screen for {minutes} mins and the grind is NOT giving what it's supposed to give 💀",
    "no cap, you've checked {site} {count} times. touch grass bestie 🌱",
    "it's giving... procrastination. major red flag 🚩",
    "the way you've typed {words} words in {minutes} mins is actually sending me",
    "bestie the productivity is not productive rn. vibe check: FAILED",
    "you've been 'working' for {hours} hours but i see you 👀"
  ],
  'drill-sergeant': [
    "MAGGOT! You've been sitting there for {minutes} MINUTES! DROP AND GIVE ME 20... SECONDS OF STRETCHING!",
    "SOLDIER! I see you've visited {site} {count} TIMES! THAT'S NOT WORK, THAT'S TREASON!",
    "RECRUIT! {words} words in {minutes} minutes?! MY GRANDMOTHER TYPES FASTER! AND SHE'S BEEN DEAD FOR 10 YEARS!",
    "WHAT DO WE HAVE HERE?! A SPECIALIST IN DOING ABSOLUTELY NOTHING! CONGRATULATIONS!",
    "YOU CALL THAT PRODUCTIVITY?! I'VE SEEN ROCKS WITH BETTER WORK ETHIC!",
    "GET UP! STRETCH! MOVE! OR SO HELP ME I WILL MAKE YOU DO BURPEES THROUGH THE SCREEN!"
  ],
  'shakespeare': [
    "To work, or not to work, that is the question. Alas, thou hast chosen... neither, for {minutes} minutes.",
    "O noble user, why dost thou visit {site} {count} times? 'Tis not the work of a focused mind.",
    "Hark! {words} words in {minutes} minutes? Even my quill moves with greater haste, and I am but a ghost!",
    "The slings and arrows of outrageous procrastination have found their mark in thee.",
    "Alas, poor user, I knew them well. A person of infinite jest, but finite productivity.",
    "Is this a spreadsheet I see before me? No, 'tis but {site}, beckoning thee to stray."
  ]
};

// Trivia questions
const TRIVIA_QUESTIONS = [
  { q: "What is the only food that never spoils?", a: "honey", options: ["salt", "honey", "sugar", "rice"] },
  { q: "How many hearts does an octopus have?", a: "three", options: ["one", "two", "three", "four"] },
  { q: "What is the shortest war in history?", a: "38 minutes", options: ["1 hour", "38 minutes", "2 days", "1 week"] },
  { q: "Which animal has the largest eyes?", a: "giant squid", options: ["elephant", "giant squid", "blue whale", "ostrich"] },
  { q: "What can you break without touching?", a: "a promise", options: ["glass", "silence", "a promise", "bread"] }
];

// Fortune cookies
const FORTUNES = [
  "You will send an email to the wrong person today. Check twice.",
  "Your next idea will be brilliant... or terrible. Only time will tell.",
  "The coffee you seek is in the kitchen you avoid walking to.",
  "A bug in your code will make you question everything. It's a semicolon.",
  "You will discover a new favorite song today. It will be stuck in your head for weeks.",
  "The meeting could have been an email. You know it. They know it.",
  "Your posture is atrocious. Sit up straight. Yes, you.",
  "You will find money in your pocket today. It will be a receipt.",
  "The answer you seek is on page 42. Of what? That's for you to discover.",
  "Your pet is plotting something. Trust no one. Especially not the cat."
];

// Meme URLs (placeholder - would fetch from API)
const MEME_URLS = [
  'https://i.imgflip.com/30b1gx.jpg', // Disaster girl
  'https://i.imgflip.com/1bij.jpg',   // One does not simply
  'https://i.imgflip.com/4t0m5.jpg',  // Change my mind
  'https://i.imgflip.com/26am.jpg',   // Y U No
  'https://i.imgflip.com/1otk96.jpg'  // Woman yelling at cat
];

// Listen for chaos triggers
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'TRIGGER_CHAOS') {
    handleChaosEvent(request.eventType);
  }
});

// Handle different chaos events
function handleChaosEvent(eventType) {
  switch(eventType) {
    case 'roast':
      showRoast();
      break;
    case 'dance_break':
      showDanceBreak();
      break;
    case 'meme_flood':
      showMemeFlood();
      break;
    case 'trivia':
      showTrivia();
      break;
    case 'fortune':
      showFortune();
      break;
    case 'puppy':
      showPuppy();
      break;
  }
}

// Show roast popup
function showRoast() {
  chrome.storage.local.get(['settings'], (result) => {
    const persona = result.settings?.persona || 'gen-z';
    const templates = ROAST_TEMPLATES[persona] || ROAST_TEMPLATES['gen-z'];
    
    // Get user activity (simplified - would track actual activity)
    const mockStats = {
      minutes: Math.floor(Math.random() * 60) + 10,
      site: ['Twitter', 'Reddit', 'YouTube'][Math.floor(Math.random() * 3)],
      count: Math.floor(Math.random() * 20) + 5,
      words: Math.floor(Math.random() * 100) + 10,
      hours: Math.floor(Math.random() * 4) + 1
    };
    
    let roast = templates[Math.floor(Math.random() * templates.length)];
    roast = roast.replace(/{(\w+)}/g, (match, key) => mockStats[key] || match);
    
    createChaosModal({
      title: '🔥 Chaos Mode Activated',
      content: roast,
      persona: persona,
      duration: 5000,
      type: 'roast'
    });
  });
}

// Show dance break
function showDanceBreak() {
  const modal = document.createElement('div');
  modal.className = 'chaos-overlay';
  modal.innerHTML = `
    <div class="chaos-modal dance-break">
      <h2>🎵 DANCE BREAK! 🎵</h2>
      <p>You must dance for 60 seconds to continue working</p>
      <div class="dance-timer">60</div>
      <div class="dance-animation">💃 🕺 💃 🕺</div>
      <button class="chaos-complete">I'm Dancing!</button>
    </div>
  `;
  
  document.body.appendChild(modal);
  
  let timeLeft = 60;
  const timer = setInterval(() => {
    timeLeft--;
    modal.querySelector('.dance-timer').textContent = timeLeft;
    if (timeLeft <= 0) {
      clearInterval(timer);
      closeChaosModal(modal);
    }
  }, 1000);
  
  modal.querySelector('.chaos-complete').addEventListener('click', () => {
    clearInterval(timer);
    closeChaosModal(modal);
  });
}

// Show meme flood
function showMemeFlood() {
  const overlay = document.createElement('div');
  overlay.className = 'chaos-overlay meme-flood';
  overlay.innerHTML = `
    <div class="meme-container">
      <h2>🖼️ MEME FLOOD! 🖼️</h2>
      <p>Click 10 memes to escape!</p>
      <div class="meme-counter">0 / 10</div>
    </div>
  `;
  
  document.body.appendChild(overlay);
  
  let clicked = 0;
  const spawnMeme = () => {
    const meme = document.createElement('img');
    meme.src = MEME_URLS[Math.floor(Math.random() * MEME_URLS.length)];
    meme.className = 'floating-meme';
    meme.style.left = Math.random() * 80 + '%';
    meme.style.top = Math.random() * 80 + '%';
    meme.style.transform = `rotate(${Math.random() * 30 - 15}deg)`;
    
    meme.addEventListener('click', () => {
      clicked++;
      overlay.querySelector('.meme-counter').textContent = `${clicked} / 10`;
      meme.remove();
      if (clicked >= 10) {
        closeChaosModal(overlay);
      }
    });
    
    overlay.appendChild(meme);
  };
  
  // Spawn initial memes
  for (let i = 0; i < 5; i++) spawnMeme();
  
  // Keep spawning
  const interval = setInterval(() => {
    if (clicked >= 10 || !document.body.contains(overlay)) {
      clearInterval(interval);
    } else {
      spawnMeme();
    }
  }, 2000);
}

// Show trivia
function showTrivia() {
  const question = TRIVIA_QUESTIONS[Math.floor(Math.random() * TRIVIA_QUESTIONS.length)];
  
  const modal = document.createElement('div');
  modal.className = 'chaos-overlay';
  modal.innerHTML = `
    <div class="chaos-modal trivia">
      <h2>❓ TRIVIA LOCKOUT! ❓</h2>
      <p>You've been working too hard. Answer 3 questions to continue!</p>
      <div class="trivia-question">${question.q}</div>
      <div class="trivia-options">
        ${question.options.map(opt => `
          <button class="trivia-option" data-answer="${opt === question.a}">${opt}</button>
        `).join('')}
      </div>
    </div>
  `;
  
  document.body.appendChild(modal);
  
  let correct = 0;
  modal.querySelectorAll('.trivia-option').forEach(btn => {
    btn.addEventListener('click', (e) => {
      if (e.target.dataset.answer === 'true') {
        correct++;
        e.target.style.background = '#4CAF50';
        if (correct >= 1) { // Simplified to 1 for MVP
          setTimeout(() => closeChaosModal(modal), 500);
        }
      } else {
        e.target.style.background = '#f44336';
        e.target.disabled = true;
      }
    });
  });
}

// Show fortune cookie
function showFortune() {
  const fortune = FORTUNES[Math.floor(Math.random() * FORTUNES.length)];
  
  createChaosModal({
    title: '🥠 Fortune Cookie',
    content: fortune,
    type: 'fortune',
    duration: 8000
  });
}

// Show emergency puppy
function showPuppy() {
  const modal = document.createElement('div');
  modal.className = 'chaos-overlay';
  modal.innerHTML = `
    <div class="chaos-modal puppy">
      <h2>🐾 EMERGENCY PUPPY! 🐾</h2>
      <p>You need this. 30 seconds of cuteness required.</p>
      <img src="https://place-puppy.com/300x300" alt="Cute puppy" class="puppy-img">
      <div class="puppy-timer">30</div>
    </div>
  `;
  
  document.body.appendChild(modal);
  
  let timeLeft = 30;
  const timer = setInterval(() => {
    timeLeft--;
    const timerEl = modal.querySelector('.puppy-timer');
    if (timerEl) timerEl.textContent = timeLeft;
    if (timeLeft <= 0) {
      clearInterval(timer);
      closeChaosModal(modal);
    }
  }, 1000);
}

// Helper: Create chaos modal
function createChaosModal({ title, content, type, duration = 5000 }) {
  const modal = document.createElement('div');
  modal.className = 'chaos-overlay';
  modal.innerHTML = `
    <div class="chaos-modal ${type}">
      <h2>${title}</h2>
      <div class="chaos-content">${content}</div>
      <button class="chaos-dismiss">Dismiss</button>
    </div>
  `;
  
  document.body.appendChild(modal);
  
  // Auto dismiss
  if (duration) {
    setTimeout(() => closeChaosModal(modal), duration);
  }
  
  // Manual dismiss
  modal.querySelector('.chaos-dismiss').addEventListener('click', () => {
    closeChaosModal(modal);
  });
}

// Helper: Close chaos modal
function closeChaosModal(modal) {
  modal.style.opacity = '0';
  setTimeout(() => modal.remove(), 300);
}

// Track user activity for better roasts
let activityStats = {
  keystrokes: 0,
  mouseMoves: 0,
  sitesVisited: {},
  startTime: Date.now()
};

document.addEventListener('keydown', () => activityStats.keystrokes++);
document.addEventListener('mousemove', () => activityStats.mouseMoves++);

// Track site visits
const currentSite = window.location.hostname;
activityStats.sitesVisited[currentSite] = (activityStats.sitesVisited[currentSite] || 0) + 1;
