from flask import Flask, Response, send_file
import os

app = Flask(__name__)

# --- CONFIGURATION ---
MUSIC_FILENAME = '/home/mahmad1499/Downloads/retro-arcade-game-music-297305.mp3' 

# --- RETRO ARCADE TEMPLATE ---
APP_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DATA STRUCTURE ARCADE</title>
    
    <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>

    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: { arcade: ['"Press Start 2P"', 'cursive'] },
                    colors: { arcade: { black: '#050505', cyan: '#0ff', yellow: '#ff0' } },
                    animation: { 'pulse-fast': 'pulse 0.1s infinite' }
                }
            }
        }
    </script>

    <style>
        body {
            background-color: #000;
            color: #e0e0e0;
            overflow: hidden;
            font-family: 'Press Start 2P', cursive;
            margin: 0;
            height: 100vh;
            width: 100vw;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        /* --- CRT EFFECT --- */
        #monitor-casing { width: 100%; height: 100%; position: relative; background: #000; overflow: hidden; }
        
        #crt-overlay {
            position: absolute; inset: 0;
            background: radial-gradient(circle, rgba(0,0,0,0) 60%, rgba(0,0,0,0.4) 90%, rgba(0,0,0,1) 100%);
            z-index: 100; pointer-events: none; box-shadow: inset 0 0 5rem rgba(0,0,0,0.75);
        }

        #crt-scanlines {
            position: absolute; inset: 0;
            background: linear-gradient(to bottom, rgba(255,255,255,0), rgba(255,255,255,0) 50%, rgba(0,0,0,0.2) 50%, rgba(0,0,0,0.2));
            background-size: 100% 4px; z-index: 99; pointer-events: none;
            animation: scrollScanlines 10s linear infinite;
        }

        @keyframes scrollScanlines { 0% { background-position: 0 0; } 100% { background-position: 0 100%; } }
        @keyframes flicker { 0% { opacity: 0.98; } 50% { opacity: 0.95; } 100% { opacity: 0.99; } }

        #game-content {
            animation: flicker 0.15s infinite;
            filter: contrast(1.2) brightness(1.1) saturate(1.2);
            width: 100%; height: 100%; position: relative;
        }

        /* --- LAYERS --- */
        #game-layer { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 0; pointer-events: auto; }
        #ui-layer { position: absolute; inset: 0; z-index: 80; pointer-events: none; display: flex; flex-direction: column; justify-content: center; align-items: center; }
        #ui-layer * { pointer-events: auto; }

        /* --- ENTITIES --- */
        .player-ship { position: absolute; bottom: 20px; transform: translateX(-50%) rotate(-45deg); filter: drop-shadow(0 0 10px #0ff); z-index: 50; pointer-events: none; }
        .falling-entity { position: absolute; z-index: 40; filter: drop-shadow(0 0 8px currentColor); }
        .falling-coin { position: absolute; z-index: 42; filter: drop-shadow(0 0 8px #ffd700); color: #ffd700; font-size: 24px; animation: spin 1s linear infinite; }
        .projectile { position: absolute; width: 4px; height: 16px; background: #0ff; box-shadow: 0 0 10px #0ff; z-index: 45; }
        .particle { position: absolute; width: 4px; height: 4px; background: #ff0; pointer-events: none; z-index: 60; }

        /* --- VISUALS --- */
        .retro-panel {
            border: 2px solid #fff; background: rgba(10, 10, 18, 0.85);
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.2), inset 0 0 20px rgba(0,0,0,0.8);
            backdrop-filter: blur(4px); padding: 1rem;
        }
        .neon-text { color: #fff; text-shadow: 0 0 5px #fff, 0 0 20px #0ff; }
        .blink { animation: blinker 1s steps(2, start) infinite; }
        @keyframes blinker { to { visibility: hidden; } }
        @keyframes spin { 0% { transform: rotateY(0deg); } 100% { transform: rotateY(360deg); } }

        /* --- ANIMATIONS --- */
        @keyframes physicsDrop { 0% { transform: translateY(-300px); } 60% { transform: translateY(20px); } 100% { transform: translateY(0); } }
        .animate-physics-drop { animation: physicsDrop 0.5s cubic-bezier(0.25, 1, 0.5, 1) forwards; }

        @keyframes physicsPop { 0% { transform: scale(1); opacity: 1; } 50% { transform: scale(1.4); opacity: 0.8; filter: brightness(2); } 100% { transform: scale(0); opacity: 0; } }
        .animate-physics-pop { animation: physicsPop 0.4s ease-in forwards; }

        @keyframes slideInRight { 0% { transform: translateX(100px); opacity: 0; } 100% { transform: translateX(0); opacity: 1; } }
        .animate-slide-in { animation: slideInRight 0.4s ease-out forwards; }

        @keyframes slideOutLeft { 0% { transform: translateX(0); opacity: 1; } 100% { transform: translateX(-100px); opacity: 0; } }
        .animate-slide-out { animation: slideOutLeft 0.4s ease-in forwards; }

        @keyframes pulseBorder { 0%, 100% { border-color: rgba(255,255,255,0.3); } 50% { border-color: #fff; box-shadow: 0 0 15px #fff; } }
        .animate-pulse-border { animation: pulseBorder 0.5s ease-in-out; }
        
        @keyframes peekPulse { 0%, 100% { transform: scale(1); filter: brightness(1); } 50% { transform: scale(1.2); filter: brightness(2); box-shadow: 0 0 20px currentColor; } }
        .animate-peek { animation: peekPulse 0.6s ease-in-out; }

        .shake-screen { animation: shake 0.3s cubic-bezier(.36,.07,.19,.97) both; }
        @keyframes shake { 10%, 90% { transform: translate3d(-2px, 0, 0); } 20%, 80% { transform: translate3d(4px, 0, 0); } 30%, 50%, 70% { transform: translate3d(-6px, 0, 0); } 40%, 60% { transform: translate3d(6px, 0, 0); } }

        /* --- DATA ITEMS --- */
        .stack-item { width: 60px; height: 60px; border-radius: 50%; border: 4px solid white; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-bottom: 0.5rem; transition: transform 0.2s; }
        .queue-item { width: 60px; height: 60px; border-radius: 50%; border: 4px solid white; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 0.5rem; transition: transform 0.2s; }
        
        .circular-container { position: relative; width: 300px; height: 300px; border: 4px dashed rgba(255,255,255,0.2); border-radius: 50%; display: flex; justify-content: center; align-items: center; }
        .circular-slot { position: absolute; width: 50px; height: 50px; border: 2px solid rgba(255,255,255,0.3); border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 0.7rem; transition: all 0.3s; }
        
        .priority-item { width: 100%; height: 50px; border: 2px solid white; display: flex; justify-content: space-between; align-items: center; padding: 0 1rem; margin-bottom: 0.5rem; background: rgba(0,0,0,0.5); position: relative; transition: all 0.4s ease-out; }
        .priority-badge { background: #fff; color: #000; border-radius: 50%; width: 24px; height: 24px; display: flex; justify-content: center; align-items: center; font-size: 0.8rem; }

        /* --- TECH LOGOS --- */
        #tech-logos { position: absolute; bottom: 1rem; right: 1rem; display: flex; align-items: center; gap: 0.8rem; z-index: 150; pointer-events: none; background: rgba(0, 0, 0, 0.9); border: 1px solid white; padding: 6px 10px; box-shadow: 3px 3px 0px #000; }
        .tech-icon-wrapper { background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255,255,255,0.2); border-radius: 4px; padding: 4px; transition: transform 0.2s, border-color 0.2s; }
        .tech-icon-wrapper:hover { transform: scale(1.1); border-color: #fff; background: rgba(255, 255, 255, 0.15); }
        .tech-icon { width: 20px; height: 20px; filter: drop-shadow(0 0 3px currentColor); object-fit: contain; }
    </style>
</head>
<body>

    <div id="monitor-casing">
        <div id="crt-scanlines"></div>
        <div id="crt-overlay"></div>
        
        <div id="game-content" onclick="handleGlobalClick(event)">
            <div id="stars" class="absolute inset-0 z-0 opacity-50"></div>
            <div id="player-ship" class="player-ship text-cyan-400 hidden"><i data-lucide="rocket" class="w-16 h-16"></i></div>
            <div id="entities-layer" class="absolute inset-0 z-10 pointer-events-none"></div>
            <div id="ui-layer"></div>

            <!-- TECH LOGOS -->
            <div id="tech-logos">
                <div class="tech-icon-wrapper border-yellow-500/50"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" class="tech-icon" alt="Python"></div>
                <div class="tech-icon-wrapper border-yellow-300/50"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg" class="tech-icon" alt="JS"></div>
                <div class="tech-icon-wrapper border-blue-500/50"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg" class="tech-icon" alt="CSS"></div>
                <div class="tech-icon-wrapper border-sky-400/50"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vscode/vscode-original.svg" class="tech-icon" alt="VS Code"></div>
            </div>

            <!-- GAME OVER -->
            <div id="game-over-modal" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/90 hidden">
                <div class="retro-panel p-8 text-center max-w-lg w-full border-red-500 shadow-[0_0_20px_rgba(239,68,68,0.5)]">
                    <h1 class="text-4xl text-red-500 mb-6 neon-text">GAME OVER</h1>
                    <div class="mb-6 space-y-2"><p class="text-gray-400 text-xs uppercase">Cause of Death</p><p id="game-over-reason" class="text-white text-lg blink"></p></div>
                    <div class="flex justify-between items-center bg-gray-900/50 p-4 mb-8 border border-gray-700">
                        <div class="text-center"><div class="text-xs text-gray-500">SCORE</div><div id="final-score" class="text-2xl text-yellow-400">000000</div></div>
                        <div class="text-center"><div class="text-xs text-gray-500">BEST</div><div id="final-highscore" class="text-xl text-white">000000</div></div>
                    </div>
                    <button onclick="closeGameOver()" class="arcade-btn px-8 py-4 text-green-400 border-green-500 w-full hover:bg-green-900/20 text-sm cursor-pointer">INSERT COIN TO CONTINUE</button>
                </div>
            </div>
        </div>
    </div>

    <!-- AUDIO SYSTEM -->
    <script>
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        let bgmAudio = null;
        
        function playSound(type) {
            if (audioCtx.state === 'suspended') audioCtx.resume();
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.connect(gain); gain.connect(audioCtx.destination);
            const now = audioCtx.currentTime;

            if (type === 'shoot') {
                osc.type = 'square'; osc.frequency.setValueAtTime(880, now); osc.frequency.exponentialRampToValueAtTime(100, now + 0.15); gain.gain.setValueAtTime(0.1, now); gain.gain.linearRampToValueAtTime(0, now + 0.15); osc.start(); osc.stop(now + 0.15);
            } else if (type === 'explosion') {
                osc.type = 'sawtooth'; osc.frequency.setValueAtTime(100, now); osc.frequency.linearRampToValueAtTime(10, now + 0.3); gain.gain.setValueAtTime(0.2, now); gain.gain.exponentialRampToValueAtTime(0.01, now + 0.3); osc.start(); osc.stop(now + 0.3);
            } else if (type === 'coin') {
                osc.type = 'sine'; osc.frequency.setValueAtTime(1200, now); osc.frequency.setValueAtTime(1600, now + 0.1); gain.gain.setValueAtTime(0.1, now); gain.gain.linearRampToValueAtTime(0, now + 0.3); osc.start(); osc.stop(now + 0.3);
            } else if (type === 'push') {
                osc.type = 'triangle'; osc.frequency.setValueAtTime(200, now); osc.frequency.linearRampToValueAtTime(400, now + 0.1); gain.gain.setValueAtTime(0.1, now); gain.gain.linearRampToValueAtTime(0, now + 0.1); osc.start(); osc.stop(now + 0.1);
            } else if (type === 'peek') {
                osc.type = 'sine'; osc.frequency.setValueAtTime(600, now); gain.gain.setValueAtTime(0.1, now); gain.gain.linearRampToValueAtTime(0, now + 0.2); osc.start(); osc.stop(now + 0.2);
            } else if (type === 'startup') {
                osc.type = 'square'; osc.frequency.setValueAtTime(110, now); osc.frequency.linearRampToValueAtTime(880, now + 0.5); gain.gain.setValueAtTime(0.1, now); gain.gain.linearRampToValueAtTime(0, now + 0.5); osc.start(); osc.stop(now + 0.5);
            }
        }

        function startMusic() {
            if (bgmAudio) return;
            bgmAudio = new Audio('/music');
            bgmAudio.loop = true; bgmAudio.volume = 0.5;
            bgmAudio.play().catch(e => console.log("Autoplay blocked"));
        }
        function stopMusic() { if (bgmAudio) { bgmAudio.pause(); bgmAudio.currentTime = 0; } }
    </script>

    <!-- LOGIC -->
    <script>
        const state = {
            view: 'landing', credits: 0, score: 0, highScore: 0,
            gameType: 'stack', dataItems: [], maxSize: 6, logs: [],
            front: -1, rear: -1,
            lastTime: 0, enemySpawnTimer: 0, projectiles: [], enemies: [], coins: [], particles: [], lives: 3,
            mission: null, missionTimer: 100
        };

        const colors = ['#ef4444', '#22c55e', '#3b82f6', '#eab308', '#a855f7'];

        // --- GAME LOOP ---
        function startLoop() {
            document.addEventListener('mousemove', e => {
                const ship = document.getElementById('player-ship');
                if(ship && state.view === 'landing') {
                    ship.style.left = `${e.clientX}px`;
                    ship.style.transform = `translateX(-50%) rotate(-45deg)`;
                }
            });
            requestAnimationFrame(loop);
        }

        function loop(timestamp) {
            const dt = timestamp - state.lastTime;
            state.lastTime = timestamp;
            const modal = document.getElementById('game-over-modal');
            if (!modal || modal.classList.contains('hidden')) {
                updatePhysics(dt);
                if (state.view !== 'landing' && state.mission) {
                    state.missionTimer -= 0.05 * (dt / 16);
                    if (state.missionTimer <= 0) failMission("TIME UP");
                    updateMissionUI();
                }
            }
            renderEntities();
            requestAnimationFrame(loop);
        }

        function updatePhysics(dt) {
            const container = document.getElementById('monitor-casing');
            const height = container.clientHeight;
            if (state.view === 'landing') {
                state.enemySpawnTimer += dt;
                if (state.enemySpawnTimer > 1000) { 
                    if (Math.random() > 0.7) spawnCoin();
                    else spawnEnemy(); 
                    state.enemySpawnTimer = 0; 
                }
            }
            for (let i = state.projectiles.length - 1; i >= 0; i--) {
                const p = state.projectiles[i]; p.y -= 0.8 * dt; if (p.y < -50) state.projectiles.splice(i, 1);
            }
            for (let i = state.enemies.length - 1; i >= 0; i--) {
                const e = state.enemies[i]; e.y += 0.3 * dt;
                if (state.view === 'landing') {
                    const ship = document.getElementById('player-ship');
                    if (ship) {
                        const shipRect = ship.getBoundingClientRect();
                        const dx = e.x - (shipRect.left + shipRect.width/2);
                        const dy = e.y - (shipRect.top + shipRect.height/2);
                        if (Math.sqrt(dx*dx + dy*dy) < 40) {
                            createExplosion(e.x, e.y, e.color); triggerScreenShake(); playSound('explosion');
                            state.enemies.splice(i, 1); gameOver("SHIP DESTROYED"); continue;
                        }
                    }
                }
                if (e.y > height + 50) state.enemies.splice(i, 1);
            }
            for (let i = state.coins.length - 1; i >= 0; i--) {
                const c = state.coins[i]; c.y += 0.4 * dt; 
                if (c.y > height + 50) state.coins.splice(i, 1);
            }
            for (let i = state.particles.length - 1; i >= 0; i--) {
                const p = state.particles[i];
                p.x += p.vx * (dt/16); p.y += p.vy * (dt/16); p.vy += 0.5 * (dt/16); p.life -= 0.02 * (dt/16);
                if (p.life <= 0) state.particles.splice(i, 1);
            }
            state.projectiles.forEach((p, pIdx) => {
                state.enemies.forEach((e, eIdx) => {
                    const dx = p.x - e.x; const dy = p.y - e.y;
                    if (Math.sqrt(dx*dx + dy*dy) < 30) {
                        createExplosion(e.x, e.y, e.color); playSound('explosion');
                        state.enemies.splice(eIdx, 1); state.projectiles.splice(pIdx, 1);
                        state.score += 100; updateScore();
                    }
                });
                state.coins.forEach((c, cIdx) => {
                    const dx = p.x - c.x; const dy = p.y - c.y;
                    if (Math.sqrt(dx*dx + dy*dy) < 30) {
                        createExplosion(c.x, c.y, '#ffd700'); playSound('coin');
                        state.credits++;
                        state.coins.splice(cIdx, 1); state.projectiles.splice(pIdx, 1);
                        renderUI(); 
                    }
                });
            });
        }

        function spawnEnemy() {
            const icons = ['ghost', 'skull', 'bug', 'alien'];
            const color = colors[Math.floor(Math.random() * colors.length)];
            const icon = icons[Math.floor(Math.random() * icons.length)];
            state.enemies.push({ x: Math.random() * window.innerWidth, y: -50, color: color, icon: icon, id: Math.random() });
        }

        function spawnCoin() {
            state.coins.push({ x: Math.random() * window.innerWidth, y: -50, color: '#ffd700', id: Math.random() });
        }

        function createExplosion(x, y, color) {
            for(let i=0; i<15; i++) {
                state.particles.push({ x: x, y: y, vx: (Math.random() - 0.5) * 15, vy: (Math.random() - 0.5) * 15 - 5, color: color, life: 1.0 });
            }
        }

        function triggerScreenShake() {
            const content = document.getElementById('game-content');
            content.classList.remove('shake-screen');
            void content.offsetWidth; content.classList.add('shake-screen');
        }

        function renderEntities() {
            const layer = document.getElementById('entities-layer');
            let html = '';
            state.projectiles.forEach(p => { html += `<div class="projectile" style="left: ${p.x}px; top: ${p.y}px;"></div>`; });
            state.enemies.forEach(e => { html += `<div class="falling-entity" style="left: ${e.x}px; top: ${e.y}px; color: ${e.color}"><i data-lucide="${e.icon}" class="w-10 h-10"></i></div>`; });
            state.coins.forEach(c => { html += `<div class="falling-coin" style="left: ${c.x}px; top: ${c.y}px;"><i data-lucide="circle-dollar-sign" class="w-8 h-8"></i></div>`; });
            state.particles.forEach(p => { html += `<div class="particle" style="left: ${p.x}px; top: ${p.y}px; background-color: ${p.color}; opacity: ${p.life}"></div>`; });
            layer.innerHTML = html;
            if (state.enemies.length > 0 || state.coins.length > 0) lucide.createIcons();
        }

        function handleGlobalClick(e) {
            startMusic();
            if (state.view === 'landing' && !e.target.closest('button') && !e.target.closest('.interactive-card')) {
                const ship = document.getElementById('player-ship');
                if(!ship) return;
                const rect = ship.getBoundingClientRect();
                state.projectiles.push({ x: rect.left + rect.width/2, y: rect.top });
                playSound('shoot');
            }
        }

        function insertCoin() { startMusic(); state.credits++; playSound('coin'); renderUI(); }
        
        function startGame(type) {
            startMusic();
            if (state.credits > 0) {
                state.credits--;
                state.view = 'game'; state.gameType = type; state.score = 0; state.lives = 3; state.dataItems = [];
                if (type === 'circular') { state.dataItems = Array(state.maxSize).fill(null); state.front = -1; state.rear = -1; }
                state.mission = null; state.enemies = []; state.projectiles = []; state.coins = [];
                renderUI(); generateMission();
            } else {
                alert("SHOOT COINS TO GET CREDITS!");
            }
        }

        function setView(v) { state.view = v; renderUI(); }
        
        function gameOver(reason) {
            playSound('explosion'); triggerScreenShake();
            const modal = document.getElementById('game-over-modal');
            document.getElementById('game-over-reason').innerText = reason;
            document.getElementById('final-score').innerText = state.score.toString().padStart(6,'0');
            document.getElementById('final-highscore').innerText = state.highScore.toString().padStart(6,'0');
            modal.classList.remove('hidden');
        }

        function closeGameOver() {
            document.getElementById('game-over-modal').classList.add('hidden');
            state.view = 'landing'; state.enemies = []; state.projectiles = []; state.coins = [];
            renderUI();
        }

        function updateScore() {
            const el = document.getElementById('score-el');
            if(el) el.innerText = state.score.toString().padStart(6,'0');
        }

        function generateMission() {
            let ops;
            if (state.gameType === 'stack') ops = ['PUSH', 'POP', 'PEEK'];
            else if (state.gameType === 'queue') ops = ['ENQUEUE', 'DEQUEUE', 'FRONT'];
            else if (state.gameType === 'circular') ops = ['ENQUEUE', 'DEQUEUE'];
            else if (state.gameType === 'priority') ops = ['INSERT', 'EXTRACT'];
            let op = ops[Math.floor(Math.random() * ops.length)];
            
            if (state.gameType === 'stack' || state.gameType === 'queue' || state.gameType === 'priority') {
                if (state.dataItems.length === 0) op = ops[0]; 
                if (state.dataItems.length >= state.maxSize) op = ops[1]; 
            } else if (state.gameType === 'circular') {
                 const isFull = (state.front === 0 && state.rear === state.maxSize - 1) || (state.rear === (state.front - 1) % (state.maxSize - 1));
                 const isEmpty = state.front === -1;
                 if (isEmpty) op = 'ENQUEUE';
                 if (isFull) op = 'DEQUEUE';
            }

            let val = null;
            if (['PUSH', 'ENQUEUE', 'INSERT'].includes(op)) val = Math.floor(Math.random()*100).toString(16).toUpperCase();

            state.mission = { op, val }; state.missionTimer = 100; renderUI();
        }

        function failMission(reason) {
            playSound('explosion'); triggerScreenShake(); state.lives--; addLog(`FAIL: ${reason}`);
            if(state.lives <= 0) gameOver("OUT OF LIVES"); else { generateMission(); renderUI(); }
        }

        function updateMissionUI() {
            const bar = document.getElementById('timer-bar');
            if(bar) bar.style.width = `${state.missionTimer}%`;
        }

        function handleAdd(e) {
            if(e) e.preventDefault();
            startMusic();
            const input = document.getElementById('dataInput');
            const opName = state.gameType === 'stack' ? 'PUSH' : (state.gameType === 'priority' ? 'INSERT' : 'ENQUEUE');
            if(state.mission && state.mission.op === opName && !input.value) input.value = state.mission.val;
            const val = input.value.trim();
            if(!val) return;

            let success = false;
            const color = colors[Math.floor(Math.random() * colors.length)];
            const newItem = { id: Date.now(), val, color, isNew: true };

            if (state.gameType === 'circular') {
                if ((state.front === 0 && state.rear === state.maxSize - 1) || (state.rear === (state.front - 1) % (state.maxSize - 1))) {
                    playSound('error');
                } else {
                    if (state.front === -1) { state.front = 0; state.rear = 0; }
                    else if (state.rear === state.maxSize - 1 && state.front !== 0) { state.rear = 0; }
                    else { state.rear++; }
                    state.dataItems[state.rear] = newItem;
                    success = true;
                }
            } else if (state.gameType === 'priority') {
                 if (state.dataItems.length < state.maxSize) {
                     newItem.priority = Math.floor(Math.random() * 5) + 1;
                     state.dataItems.push(newItem);
                     state.dataItems.sort((a, b) => b.priority - a.priority);
                     success = true;
                 }
            } else {
                if (state.dataItems.length < state.maxSize) {
                    if (state.gameType === 'stack') state.dataItems.unshift(newItem); 
                    else state.dataItems.push(newItem); 
                    success = true;
                }
            }
            if (success) {
                playSound('push');
                if (state.mission && state.mission.op === opName) {
                    state.score += 50; playSound('coin'); generateMission();
                } else if(state.mission) failMission("WRONG MOVE");
                renderUI();
                input.value = '';
                document.getElementById('dataInput').focus();
            } else { playSound('error'); }
        }

        function handleRemove() {
            startMusic();
            let success = false;
            const opName = state.gameType === 'stack' ? 'POP' : (state.gameType === 'priority' ? 'EXTRACT' : 'DEQUEUE');
            
            // Animation Trigger Logic
            let targetEl = null;
            if (state.gameType === 'stack' && state.dataItems.length > 0) {
                 const container = document.getElementById('visual-container');
                 if(container) targetEl = container.firstElementChild; // Top is first in DOM for stack
            } else if (state.gameType === 'queue' && state.dataItems.length > 0) {
                 const container = document.getElementById('visual-container');
                 if(container) targetEl = container.firstElementChild; // Front is first in DOM for Queue map
            } else if (state.gameType === 'circular' && state.front !== -1) {
                 const container = document.querySelector('.circular-container');
                 if(container && container.children[state.front]) targetEl = container.children[state.front];
            } else if (state.gameType === 'priority' && state.dataItems.length > 0) {
                 const container = document.getElementById('visual-container');
                 if(container) targetEl = container.firstElementChild; // Highest priority is first
            }

            if(targetEl) {
                 if(state.gameType === 'queue') targetEl.classList.add('animate-slide-out');
                 else if(state.gameType === 'circular') targetEl.classList.add('animate-pulse-border');
                 else targetEl.classList.add('animate-physics-pop');
            }

            if (state.gameType === 'circular') {
                if (state.front === -1) { playSound('error'); }
                else {
                    setTimeout(() => {
                        state.dataItems[state.front] = null; 
                        if (state.front === state.rear) { state.front = -1; state.rear = -1; }
                        else if (state.front === state.maxSize - 1) { state.front = 0; }
                        else { state.front++; }
                        finishRemove(opName);
                    }, 300);
                }
            } else {
                if (state.dataItems.length > 0) {
                    setTimeout(() => {
                        if (state.gameType === 'stack') state.dataItems.shift(); 
                        else state.dataItems.shift(); 
                        finishRemove(opName);
                    }, 300);
                } else { playSound('error'); }
            }
        }

        function finishRemove(opName) {
             if (state.mission && state.mission.op === opName) {
                state.score += 50; playSound('coin'); generateMission();
            } else if(state.mission) failMission("WRONG MOVE");
            renderUI();
        }

        function handleInspect() {
             startMusic();
             const opName = state.gameType === 'stack' ? 'PEEK' : (state.gameType === 'priority' ? 'PEEK' : 'FRONT');
             
             // Animation Logic
             let targetEl = null;
             if (state.gameType === 'stack' && state.dataItems.length > 0) {
                 targetEl = document.getElementById('visual-container').firstElementChild;
             } else if (state.gameType === 'queue' && state.dataItems.length > 0) {
                 targetEl = document.getElementById('visual-container').firstElementChild;
             } else if (state.gameType === 'circular' && state.front !== -1) {
                 targetEl = document.querySelector('.circular-container').children[state.front];
             } else if (state.gameType === 'priority' && state.dataItems.length > 0) {
                 targetEl = document.getElementById('visual-container').firstElementChild;
             }

             if(targetEl) {
                 playSound('peek');
                 targetEl.classList.remove('animate-peek');
                 void targetEl.offsetWidth; 
                 targetEl.classList.add('animate-peek');
                 
                 if (state.mission && state.mission.op === opName) {
                        state.score += 50; playSound('coin'); generateMission();
                } else if(state.mission) failMission("WRONG MOVE");
             } else {
                 playSound('error');
             }
        }

        function handleClear() { state.dataItems = (state.gameType === 'circular' ? Array(state.maxSize).fill(null) : []); if(state.gameType==='circular'){state.front=-1;state.rear=-1;} renderUI(); }
        function addLog(msg) { state.logs.unshift(msg); if(state.logs.length > 5) state.logs.pop(); }

        function renderUI() {
            const root = document.getElementById('ui-layer');
            const playerShip = document.getElementById('player-ship');
            
            if(!root) return;

            if (state.view === 'landing') {
                if(playerShip) playerShip.classList.remove('hidden'); 
                root.innerHTML = `
                    <div class="text-center z-50">
                        <div class="mb-12 p-8 retro-panel">
                            <h1 class="text-5xl md:text-7xl mb-4 neon-text rgb-effect animate-pulse">DATA STRUCTURE<br>ARCADE</h1>
                            <div class="mt-8">
                                <div class="text-yellow-400 text-sm blink mt-4">SHOOT COINS TO GET CREDITS</div>
                                <div class="mt-2 text-green-400 text-xl">CREDITS: ${state.credits.toString().padStart(2, '0')}</div>
                            </div>
                        </div>

                        <div class="grid grid-cols-2 gap-8 justify-center max-w-4xl mx-auto">
                            <div class="retro-panel p-6 cursor-pointer hover:bg-white/10 transition-transform hover:-translate-y-2 interactive-card" onclick="startGame('stack')">
                                <div class="text-yellow-400 text-2xl mb-2">LVL 1: STACKS</div>
                                <div class="text-xs text-green-400 mt-2">${state.credits > 0 ? 'READY' : 'LOCKED'}</div>
                            </div>
                            <div class="retro-panel p-6 cursor-pointer hover:bg-white/10 transition-transform hover:-translate-y-2 interactive-card" onclick="startGame('queue')">
                                <div class="text-cyan-400 text-2xl mb-2">LVL 2: QUEUES</div>
                                <div class="text-xs text-green-400 mt-2">${state.credits > 0 ? 'READY' : 'LOCKED'}</div>
                            </div>
                            <div class="retro-panel p-6 cursor-pointer hover:bg-white/10 transition-transform hover:-translate-y-2 interactive-card" onclick="startGame('circular')">
                                <div class="text-purple-400 text-2xl mb-2">LVL 3: CIRCULAR</div>
                                <div class="text-xs text-green-400 mt-2">${state.credits > 0 ? 'READY' : 'LOCKED'}</div>
                            </div>
                            <div class="retro-panel p-6 cursor-pointer hover:bg-white/10 transition-transform hover:-translate-y-2 interactive-card" onclick="startGame('priority')">
                                <div class="text-red-400 text-2xl mb-2">LVL 4: PRIORITY</div>
                                <div class="text-xs text-green-400 mt-2">${state.credits > 0 ? 'READY' : 'LOCKED'}</div>
                            </div>
                        </div>
                    </div>
                `;
            } else {
                if(playerShip) playerShip.classList.add('hidden'); 
                
                let addLabel = 'PUSH', removeLabel = 'POP', inspectLabel = 'PEEK';
                let visualHtml = '';
                let guideHtml = '';
                let containerClass = "flex-col items-center justify-end"; 

                if (state.gameType === 'stack') {
                    visualHtml = state.dataItems.map((item, i) => `
                        <div class="stack-item ${item.isNew ? 'animate-physics-drop' : ''}" style="border-color: ${item.color}; color: ${item.color}; box-shadow: 0 0 10px ${item.color}">
                            ${item.val} ${i===0 ? '<span class="absolute -right-16 text-xs text-white"><< TOP</span>' : ''}
                        </div>
                    `).join('');
                    guideHtml = "<p class='text-[0.6rem] leading-4 text-gray-300'>1. <strong>LIFO</strong>: Last In, First Out.<br>2. <strong>PUSH</strong>: Add to TOP.<br>3. <strong>POP</strong>: Remove TOP.<br>4. <strong>PEEK</strong>: View TOP.</p>";
                } else if (state.gameType === 'queue') {
                    addLabel = 'ENQUEUE'; removeLabel = 'DEQUEUE'; inspectLabel = 'FRONT';
                    containerClass = "flex-row items-center justify-start overflow-x-auto";
                    visualHtml = state.dataItems.map((item, i) => `
                        <div class="queue-item ${item.isNew ? 'animate-slide-in' : ''}" style="border-color: ${item.color}; color: ${item.color}; margin-right: 10px;">
                            ${item.val}
                            ${i===0 ? '<span class="absolute -top-6 text-xs text-white">FRONT</span>' : ''}
                            ${i===state.dataItems.length-1 ? '<span class="absolute -bottom-6 text-xs text-white">REAR</span>' : ''}
                        </div>
                    `).join('');
                    guideHtml = "<p class='text-[0.6rem] leading-4 text-gray-300'>1. <strong>FIFO</strong>: First In, First Out.<br>2. <strong>ENQUEUE</strong>: Add to REAR.<br>3. <strong>DEQUEUE</strong>: Remove FRONT.<br>4. <strong>FRONT</strong>: View FRONT.</p>";
                } else if (state.gameType === 'circular') {
                    addLabel = 'ENQUEUE'; removeLabel = 'DEQUEUE'; inspectLabel = 'FRONT';
                    const angleStep = 360 / state.maxSize;
                    const radius = 100;
                    const itemsHtml = state.dataItems.map((item, i) => {
                         const angle = i * angleStep;
                         const content = item ? `<span style="color:${item.color}">${item.val}</span>` : '<span class="text-gray-700">.</span>';
                         const border = item ? `border-color:${item.color}; box-shadow:0 0 5px ${item.color}` : 'border-color:#333';
                         
                         let pointer = '';
                         if (i === state.front) pointer += '<span class="absolute -top-4 text-green-500 text-xs">F</span>';
                         if (i === state.rear) pointer += '<span class="absolute -bottom-4 text-red-500 text-xs">R</span>';

                         return `<div class="circular-slot ${item && item.isNew ? 'animate-pulse-border' : ''}" style="transform: rotate(${angle}deg) translate(${radius}px) rotate(-${angle}deg); ${border}">
                            ${content} ${pointer}
                         </div>`;
                    }).join('');
                    visualHtml = `<div class="circular-container">${itemsHtml}</div>`;
                    containerClass = "items-center justify-center";
                    guideHtml = "<p class='text-[0.6rem] leading-4 text-gray-300'>1. <strong>Circular</strong>: Connects End to Start.<br>2. <strong>Wrap Around</strong>: Rear moves to 0 if full.<br>3. <strong>Pointers</strong>: Uses modulo arithmetic.</p>";
                } else if (state.gameType === 'priority') {
                    addLabel = 'INSERT'; removeLabel = 'EXTRACT'; inspectLabel = 'PEEK';
                    visualHtml = state.dataItems.map((item, i) => `
                        <div class="priority-item ${item.isNew ? 'animate-slide-in' : ''}" style="border-color: ${item.color}; color: ${item.color}">
                            <span>${item.val}</span>
                            <div class="priority-badge">★${item.priority}</div>
                            ${i===0 ? '<span class="absolute -right-16 text-xs text-white"><< MAX</span>' : ''}
                        </div>
                    `).join('');
                    guideHtml = "<p class='text-[0.6rem] leading-4 text-gray-300'>1. <strong>Priority</strong>: High rank out first.<br>2. <strong>Insert</strong>: Sorted placement.<br>3. <strong>Extract</strong>: Remove highest priority.</p>";
                }

                const hearts = '❤️'.repeat(state.lives);
                let missionText = state.mission ? `CPU: ${state.mission.op} ${state.mission.val ? '['+state.mission.val+']' : ''}` : "WAITING";

                root.innerHTML = `
                    <div class="w-full max-w-6xl p-4 h-full flex flex-col">
                        <div class="flex justify-between items-center mb-6 retro-panel p-4">
                            <button onclick="setView('landing')" class="arcade-btn px-4 py-2 text-xs">EXIT</button>
                            <div class="flex-1 mx-8 text-center">
                                <div class="text-yellow-400 text-xl blink font-bold">${missionText}</div>
                                <div class="w-full h-2 bg-gray-700 rounded-full mt-2"><div id="timer-bar" class="h-full bg-green-500" style="width: ${state.missionTimer}%"></div></div>
                            </div>
                            <div class="text-right">
                                <div class="text-xs text-gray-400">SCORE</div>
                                <div class="text-2xl text-yellow-400">${state.score}</div>
                                <div class="text-lg">${hearts}</div>
                            </div>
                        </div>

                        <div class="grid grid-cols-12 gap-8 flex-1">
                            <div class="col-span-4 flex flex-col gap-4">
                                <div class="retro-panel p-4">
                                    <h2 class="text-cyan-400 mb-4 text-sm">>> INPUT</h2>
                                    <form onsubmit="handleAdd(event)" class="flex gap-2 mb-4">
                                        <input id="dataInput" type="text" maxlength="4" class="w-full bg-black border-2 border-green-500 text-green-500 p-2 outline-none uppercase font-bold" placeholder="DATA" autocomplete="off" autofocus>
                                        <button class="arcade-btn bg-blue-900 px-4">${addLabel}</button>
                                    </form>
                                    <div class="grid grid-cols-2 gap-4">
                                        <button onclick="handleRemove()" class="arcade-btn bg-red-900 py-4">${removeLabel}</button>
                                        <button onclick="handleInspect()" class="arcade-btn bg-purple-900 py-4">${inspectLabel}</button>
                                    </div>
                                    <button onclick="handleClear()" class="arcade-btn w-full mt-4 py-2 text-xs opacity-70">CLEAR</button>
                                </div>
                                <div class="retro-panel p-4 flex-1 overflow-hidden">
                                    <h3 class="text-xs text-gray-500 mb-2">SYSTEM_LOGS</h3>
                                    <div class="text-xs text-green-400 font-mono flex flex-col gap-1">
                                        ${state.logs.map(l => `<span>> ${l}</span>`).join('')}
                                    </div>
                                </div>
                            </div>

                            <div class="col-span-5 relative">
                                <div class="absolute inset-0 border-4 border-white/50 bg-white/5 backdrop-blur-sm rounded-xl flex ${containerClass} p-4 overflow-hidden">
                                    <div class="absolute top-2 left-2 text-xs text-gray-500">MAX: ${state.maxSize}</div>
                                    <div id="visual-container" class="w-full h-full flex ${containerClass}">
                                        ${visualHtml}
                                    </div>
                                </div>
                            </div>

                            <div class="col-span-3 retro-panel h-fit">
                                <h2 class="text-yellow-500 mb-4 text-sm">>> THEORY_DB</h2>
                                <div class="text-xs leading-6 text-gray-300">
                                    ${guideHtml}
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            }
            lucide.createIcons();
        }

        // --- INIT ---
        window.onload = function() {
            setTimeout(initStars, 100);
            setTimeout(() => playSound('startup'), 500);
            startLoop();
            renderUI();
        };

        function initStars() {
            const container = document.getElementById('stars');
            if(!container) return;
            for(let i=0; i<50; i++) {
                const s = document.createElement('div');
                s.className = 'absolute bg-white rounded-full';
                s.style.width = Math.random() * 2 + 'px';
                s.style.height = s.style.width;
                s.style.left = Math.random() * 100 + '%';
                s.style.top = Math.random() * 100 + '%';
                s.style.opacity = Math.random();
                container.appendChild(s);
            }
        }

    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return Response(APP_TEMPLATE, mimetype='text/html')

@app.route('/music')
def serve_music():
    try:
        return send_file(MUSIC_FILENAME)
    except FileNotFoundError:
        return "Music file not found", 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
