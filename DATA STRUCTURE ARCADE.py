from flask import Flask, render_template_string, send_file
import os

app = Flask(__name__)

# --- CONFIGURATION: LOCAL MUSIC ---
# 1. Place your .mp3 file in the same folder as this script.
# 2. Update the filename below to match your file.
MUSIC_FILENAME = '/home/mahmad1499/Downloads/retro-arcade-game-music-297305.mp3' 

# --- RETRO ARCADE TEMPLATE ---
APP_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DATA STRUCTURE ARCADE</title>
    
    <!-- Retro Pixel Font -->
    <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>

    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        arcade: ['"Press Start 2P"', 'cursive'],
                    },
                    colors: {
                        arcade: {
                            black: '#050505',
                            dark: '#0a0a12',
                            cyan: '#0ff',
                            magenta: '#f0f',
                            yellow: '#ff0',
                            green: '#0f0',
                        }
                    },
                    animation: {
                        'pulse-fast': 'pulse 0.1s infinite',
                    }
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

        /* --- HYPER-REALISTIC CRT SHADER EFFECTS --- */
        #monitor-casing {
            width: 100%;
            height: 100%;
            position: relative;
            background: #000;
            overflow: hidden;
        }

        /* Screen curvature and vignette */
        #crt-overlay {
            position: absolute;
            inset: 0;
            background: radial-gradient(circle, rgba(0,0,0,0) 60%, rgba(0,0,0,0.4) 90%, rgba(0,0,0,1) 100%);
            z-index: 100;
            pointer-events: none;
            box-shadow: inset 0 0 5rem rgba(0,0,0,0.75);
        }

        /* Scanlines */
        #crt-scanlines {
            position: absolute;
            inset: 0;
            background: linear-gradient(
                to bottom,
                rgba(255,255,255,0),
                rgba(255,255,255,0) 50%,
                rgba(0,0,0,0.2) 50%,
                rgba(0,0,0,0.2)
            );
            background-size: 100% 4px;
            z-index: 99;
            pointer-events: none;
            animation: scrollScanlines 10s linear infinite;
        }

        /* RGB Shift (Chromatic Aberration) */
        .rgb-effect {
            text-shadow: 2px 0 rgba(255,0,0,0.7), -2px 0 rgba(0,0,255,0.7);
        }

        /* Screen Flicker */
        @keyframes flicker {
            0% { opacity: 0.98; }
            5% { opacity: 0.95; }
            10% { opacity: 0.98; }
            15% { opacity: 1; }
            20% { opacity: 0.98; }
            25% { opacity: 0.99; }
            30% { opacity: 0.95; }
            100% { opacity: 0.99; }
        }
        #game-content {
            animation: flicker 0.15s infinite;
            filter: contrast(1.2) brightness(1.1) saturate(1.2);
            width: 100%;
            height: 100%;
            position: relative;
        }

        @keyframes scrollScanlines {
            0% { background-position: 0 0; }
            100% { background-position: 0 100%; }
        }

        /* --- GAME ENTITIES --- */
        .player-ship {
            position: absolute;
            bottom: 20px;
            transform: translateX(-50%) rotate(-45deg);
            filter: drop-shadow(0 0 10px #0ff);
            z-index: 50;
            pointer-events: none;
            /* ZERO transition for instant response */
            transition: none !important; 
        }

        .falling-entity {
            position: absolute;
            z-index: 40;
            filter: drop-shadow(0 0 8px currentColor);
        }

        .projectile {
            position: absolute;
            width: 4px;
            height: 16px;
            background: #0ff;
            box-shadow: 0 0 10px #0ff, 0 0 20px #0ff;
            z-index: 45;
            border-radius: 2px;
        }

        .particle {
            position: absolute;
            width: 4px;
            height: 4px;
            background: #ff0;
            pointer-events: none;
            z-index: 60;
        }

        /* --- UI LAYOUT --- */
        #ui-layer {
            position: absolute;
            inset: 0;
            z-index: 80;
            pointer-events: none;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        #ui-layer * {
            pointer-events: auto;
        }

        .retro-panel {
            border: 2px solid #fff;
            background: rgba(10, 10, 18, 0.85);
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.2), inset 0 0 20px rgba(0,0,0,0.8);
            backdrop-filter: blur(4px);
            padding: 1rem;
        }

        .neon-text {
            color: #fff;
            text-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 20px #0ff, 0 0 40px #0ff;
        }

        .blink { animation: blinker 1s steps(2, start) infinite; }
        @keyframes blinker { to { visibility: hidden; } }

        /* Stack Visuals */
        .stack-item {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            border: 4px solid white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            position: relative;
            margin-bottom: 0.5rem;
            transition: transform 0.2s;
            box-shadow: inset -5px -5px 10px rgba(0,0,0,0.5);
        }
        
        /* Queue Visuals */
        .queue-item {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            border: 4px solid white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            position: relative;
            margin-right: 0.5rem; /* Horizontal spacing */
            transition: transform 0.2s;
            box-shadow: inset -5px -5px 10px rgba(0,0,0,0.5);
        }

        /* Realistic Physics Animations */
        @keyframes physicsDrop {
            0% { transform: translateY(-300px); }
            60% { transform: translateY(20px); }
            80% { transform: translateY(-10px); }
            100% { transform: translateY(0); }
        }
        .animate-physics-drop {
            animation: physicsDrop 0.5s cubic-bezier(0.25, 1, 0.5, 1) forwards;
        }
        
        @keyframes physicsSlideLeft {
            0% { transform: translateX(300px); opacity: 0; }
            60% { transform: translateX(-20px); opacity: 1; }
            80% { transform: translateX(10px); }
            100% { transform: translateX(0); }
        }
        .animate-physics-slide {
            animation: physicsSlideLeft 0.5s cubic-bezier(0.25, 1, 0.5, 1) forwards;
        }

        @keyframes physicsPop {
            0% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.4); opacity: 0.8; filter: brightness(2); }
            100% { transform: scale(0); opacity: 0; }
        }
        .animate-physics-pop {
            animation: physicsPop 0.4s ease-in forwards;
        }

        /* Screen Shake Class */
        .shake-screen {
            animation: shake 0.3s cubic-bezier(.36,.07,.19,.97) both;
        }
        @keyframes shake {
            10%, 90% { transform: translate3d(-2px, 0, 0); }
            20%, 80% { transform: translate3d(4px, 0, 0); }
            30%, 50%, 70% { transform: translate3d(-6px, 0, 0); }
            40%, 60% { transform: translate3d(6px, 0, 0); }
        }

        /* --- TECH LOGOS RETRO CONTAINER --- */
        #tech-logos {
            position: absolute;
            bottom: 2rem;
            right: 2rem;
            display: flex;
            align-items: center;
            gap: 1.5rem;
            z-index: 150;
            pointer-events: none;
            background: rgba(0, 0, 0, 0.9);
            border: 2px solid white;
            padding: 8px 16px;
            box-shadow: 4px 4px 0px #000;
        }
        .tech-icon-wrapper {
            background: rgba(255, 255, 255, 0.05);
            border: 2px solid rgba(255,255,255,0.2);
            border-radius: 8px;
            padding: 8px;
            transition: transform 0.2s, border-color 0.2s;
        }
        .tech-icon-wrapper:hover {
            transform: scale(1.1);
            border-color: #fff;
            background: rgba(255, 255, 255, 0.15);
        }

        .tech-icon {
            width: 36px; 
            height: 36px;
            /* Ultra High Contrast Filters */
            filter: drop-shadow(0 0 5px currentColor);
            object-fit: contain;
        }
    </style>
</head>
<body>

    <div id="monitor-casing">
        <div id="crt-scanlines"></div>
        <div id="crt-overlay"></div>
        
        <div id="game-content" onclick="handleGlobalClick(event)">
            <!-- Stars Background -->
            <div id="stars" class="absolute inset-0 z-0 opacity-50"></div>

            <!-- Player Ship -->
            <div id="player-ship" class="player-ship text-cyan-400 hidden">
                <i data-lucide="rocket" class="w-16 h-16"></i>
            </div>

            <!-- Game Entities Container (Projectiles, Enemies, Particles) -->
            <div id="entities-layer" class="absolute inset-0 z-10 pointer-events-none"></div>

            <!-- UI Layer -->
            <div id="ui-layer">
                <!-- Content injected via JS -->
            </div>

            <!-- TECH STACK ICONS (High Contrast) -->
            <div id="tech-logos">
                <!-- Python (Bright Neon Yellow) -->
                <div class="tech-icon-wrapper border-yellow-500/50">
                    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" class="tech-icon" alt="Python">
                </div>
                
                <!-- JS (Neon Yellow) -->
                <div class="tech-icon-wrapper border-yellow-300/50">
                    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg" class="tech-icon" alt="JS">
                </div>
                
                <!-- CSS (Neon Blue) -->
                <div class="tech-icon-wrapper border-blue-500/50">
                    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg" class="tech-icon" alt="CSS">
                </div>

                 <!-- VS Code (Neon Sky Blue) -->
                <div class="tech-icon-wrapper border-sky-400/50">
                    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vscode/vscode-original.svg" class="tech-icon" alt="VS Code">
                </div>
            </div>

            <!-- GAME OVER MODAL (Re-added) -->
            <div id="game-over-modal" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/90 hidden">
                <div class="retro-panel p-8 text-center max-w-lg w-full border-red-500 shadow-[0_0_20px_rgba(239,68,68,0.5)]">
                    <h1 class="text-4xl text-red-500 mb-6 neon-text" style="text-shadow: 0 0 10px red;">GAME OVER</h1>
                    
                    <div class="mb-6 space-y-2">
                        <p class="text-gray-400 text-xs uppercase">Cause of Death</p>
                        <p id="game-over-reason" class="text-white text-lg blink"></p>
                    </div>

                    <div class="flex justify-between items-center bg-gray-900/50 p-4 mb-8 border border-gray-700">
                        <div class="text-center">
                            <div class="text-xs text-gray-500">SCORE</div>
                            <div id="final-score" class="text-2xl text-yellow-400">000000</div>
                        </div>
                        <div class="text-center">
                            <div class="text-xs text-gray-500">BEST</div>
                            <div id="final-highscore" class="text-xl text-white">000000</div>
                        </div>
                    </div>

                    <button onclick="closeGameOver()" class="arcade-btn px-8 py-4 text-green-400 border-green-500 w-full hover:bg-green-900/20 text-sm">
                        INSERT COIN TO CONTINUE
                    </button>
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
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            const now = audioCtx.currentTime;

            if (type === 'shoot') {
                osc.type = 'square';
                osc.frequency.setValueAtTime(880, now);
                osc.frequency.exponentialRampToValueAtTime(100, now + 0.15);
                gain.gain.setValueAtTime(0.1, now);
                gain.gain.linearRampToValueAtTime(0, now + 0.15);
                osc.start(); osc.stop(now + 0.15);
            } else if (type === 'explosion') {
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(100, now);
                osc.frequency.linearRampToValueAtTime(10, now + 0.3);
                gain.gain.setValueAtTime(0.2, now);
                gain.gain.exponentialRampToValueAtTime(0.01, now + 0.3);
                osc.start(); osc.stop(now + 0.3);
            } else if (type === 'coin') {
                osc.type = 'sine';
                osc.frequency.setValueAtTime(1200, now);
                osc.frequency.setValueAtTime(1600, now + 0.1);
                gain.gain.setValueAtTime(0.1, now);
                gain.gain.linearRampToValueAtTime(0, now + 0.3);
                osc.start(); osc.stop(now + 0.3);
            } else if (type === 'push') {
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(200, now);
                osc.frequency.linearRampToValueAtTime(400, now + 0.1);
                gain.gain.setValueAtTime(0.1, now);
                gain.gain.linearRampToValueAtTime(0, now + 0.1);
                osc.start(); osc.stop(now + 0.1);
            } else if (type === 'startup') {
                // Retro Boot Sound
                osc.type = 'square';
                osc.frequency.setValueAtTime(110, now);
                osc.frequency.linearRampToValueAtTime(880, now + 0.5);
                gain.gain.setValueAtTime(0.1, now);
                gain.gain.linearRampToValueAtTime(0, now + 0.5);
                osc.start(); osc.stop(now + 0.5);
            }
        }

        // --- BACKGROUND MUSIC (File Based) ---
        function startMusic() {
            if (bgmAudio) return; // Already loaded
            
            // Using the specific file configured in Python variable
            bgmAudio = new Audio('/music');
            bgmAudio.loop = true;
            bgmAudio.volume = 0.5;
            
            // Try to play
            bgmAudio.play().then(() => {
                console.log("Music started");
            }).catch(e => {
                console.log("Autoplay blocked - waiting for interaction");
            });
        }

        function stopMusic() {
            if (bgmAudio) {
                bgmAudio.pause();
                bgmAudio.currentTime = 0;
            }
        }
    </script>

    <!-- LOGIC -->
    <script>
        const state = {
            view: 'landing',
            credits: 0,
            score: 0,
            highScore: 0,
            
            // Logic
            gameType: null, // 'stack' or 'queue'
            dataItems: [], // Shared array for stack/queue
            maxSize: 6,
            logs: [],
            
            // Game Loop
            lastTime: 0,
            enemySpawnTimer: 0,
            
            // Entities
            projectiles: [],
            enemies: [],
            particles: [], // For explosions
            
            // Gameplay
            lives: 3,
            gameActive: true, // Entities update in background?
            
            // Mission (Game Mode)
            mission: null,
            missionTimer: 100
        };

        const colors = ['#ef4444', '#22c55e', '#3b82f6', '#eab308', '#a855f7']; // Tailwind colors hex

        // --- CORE GAME LOOP (PHYSICS) ---
        function startLoop() {
            // Mouse Tracking
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

            // Only update physics if game over modal is NOT showing
            const modal = document.getElementById('game-over-modal');
            if (!modal || modal.classList.contains('hidden')) {
                updatePhysics(dt);
                
                // Mission Timer
                if (state.view === 'game' && state.mission) {
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

            // 1. Spawn Enemies (Landing Page Only)
            if (state.view === 'landing') {
                state.enemySpawnTimer += dt;
                if (state.enemySpawnTimer > 1000) {
                    spawnEnemy();
                    state.enemySpawnTimer = 0;
                }
            }

            // 2. Update Projectiles
            for (let i = state.projectiles.length - 1; i >= 0; i--) {
                const p = state.projectiles[i];
                p.y -= 0.8 * dt; // Speed
                if (p.y < -50) state.projectiles.splice(i, 1);
            }

            // 3. Update Enemies
            for (let i = state.enemies.length - 1; i >= 0; i--) {
                const e = state.enemies[i];
                e.y += 0.3 * dt; // Fall speed
                
                // Collision with Ship (Landing only)
                if (state.view === 'landing') {
                    const ship = document.getElementById('player-ship');
                    if (ship) {
                        const shipRect = ship.getBoundingClientRect();
                        // Simple distance check approximation
                        const dx = e.x - (shipRect.left + shipRect.width/2);
                        const dy = e.y - (shipRect.top + shipRect.height/2);
                        if (Math.sqrt(dx*dx + dy*dy) < 40) {
                            createExplosion(e.x, e.y, e.color);
                            triggerScreenShake();
                            playSound('explosion');
                            state.enemies.splice(i, 1);
                            gameOver("SHIP DESTROYED");
                            continue;
                        }
                    }
                }

                if (e.y > height + 50) state.enemies.splice(i, 1);
            }

            // 4. Update Particles (Gravity Physics)
            for (let i = state.particles.length - 1; i >= 0; i--) {
                const p = state.particles[i];
                p.x += p.vx * (dt/16);
                p.y += p.vy * (dt/16);
                p.vy += 0.5 * (dt/16); // Gravity
                p.life -= 0.02 * (dt/16);
                if (p.life <= 0) state.particles.splice(i, 1);
            }

            // 5. Check Bullet Collisions
            state.projectiles.forEach((p, pIdx) => {
                state.enemies.forEach((e, eIdx) => {
                    const dx = p.x - e.x;
                    const dy = p.y - e.y;
                    if (Math.sqrt(dx*dx + dy*dy) < 30) {
                        // HIT
                        createExplosion(e.x, e.y, e.color);
                        playSound('explosion');
                        state.enemies.splice(eIdx, 1);
                        state.projectiles.splice(pIdx, 1);
                        state.score += 100;
                        updateScore();
                    }
                });
            });
        }

        function spawnEnemy() {
            const icons = ['ghost', 'skull', 'bug', 'alien'];
            const color = colors[Math.floor(Math.random() * colors.length)];
            const icon = icons[Math.floor(Math.random() * icons.length)];
            
            state.enemies.push({
                x: Math.random() * window.innerWidth,
                y: -50,
                color: color,
                icon: icon,
                id: Math.random()
            });
        }

        function createExplosion(x, y, color) {
            // Spawn 15 particles
            for(let i=0; i<15; i++) {
                state.particles.push({
                    x: x, y: y,
                    vx: (Math.random() - 0.5) * 15,
                    vy: (Math.random() - 0.5) * 15 - 5, // Upward bias
                    color: color,
                    life: 1.0
                });
            }
        }

        function triggerScreenShake() {
            const content = document.getElementById('game-content');
            content.classList.remove('shake-screen');
            void content.offsetWidth; // reflow
            content.classList.add('shake-screen');
        }

        function renderEntities() {
            const layer = document.getElementById('entities-layer');
            let html = '';

            // Projectiles
            state.projectiles.forEach(p => {
                html += `<div class="projectile" style="left: ${p.x}px; top: ${p.y}px;"></div>`;
            });

            // Enemies
            state.enemies.forEach(e => {
                html += `<div class="falling-entity" style="left: ${e.x}px; top: ${e.y}px; color: ${e.color}">
                    <i data-lucide="${e.icon}" class="w-10 h-10"></i>
                </div>`;
            });

            // Particles
            state.particles.forEach(p => {
                html += `<div class="particle" style="left: ${p.x}px; top: ${p.y}px; background-color: ${p.color}; opacity: ${p.life}"></div>`;
            });

            layer.innerHTML = html;
            if (state.enemies.length > 0) lucide.createIcons();
        }

        // --- INPUT HANDLING ---
        function handleGlobalClick(e) {
            // Ensure music starts on any interaction
            startMusic();

            // Only shoot on landing page and not when clicking UI buttons
            if (state.view === 'landing' && !e.target.closest('button') && !e.target.closest('.interactive-card')) {
                const ship = document.getElementById('player-ship');
                if(!ship) return;
                
                // Spawn projectile at ship location
                const rect = ship.getBoundingClientRect();
                state.projectiles.push({
                    x: rect.left + rect.width/2,
                    y: rect.top
                });
                playSound('shoot');
            }
        }

        // --- GAME LOGIC ---
        function insertCoin() {
            startMusic(); // Ensure music starts
            state.credits++;
            playSound('coin');
            renderUI();
        }

        function startGame(type) {
            startMusic();
            if (state.credits > 0) {
                state.credits--;
                state.view = 'game';
                state.gameType = type; // 'stack' or 'queue'
                state.score = 0;
                state.lives = 3;
                state.dataItems = [];
                state.mission = null;
                // Clear enemies so we can focus on game
                state.enemies = []; 
                state.projectiles = [];
                renderUI();
                generateMission();
            } else {
                alert("INSERT COIN!");
            }
        }

        function setView(v) {
            state.view = v;
            renderUI();
        }

        function gameOver(reason) {
            playSound('explosion');
            triggerScreenShake();
            // Show custom modal
            const modal = document.getElementById('game-over-modal');
            const reasonEl = document.getElementById('game-over-reason');
            const scoreEl = document.getElementById('final-score');
            const highEl = document.getElementById('final-highscore');
            
            if(state.score > state.highScore) state.highScore = state.score;
            
            reasonEl.innerText = reason;
            scoreEl.innerText = state.score.toString().padStart(6,'0');
            highEl.innerText = state.highScore.toString().padStart(6,'0');
            
            modal.classList.remove('hidden');
        }
        
        function closeGameOver() {
            const modal = document.getElementById('game-over-modal');
            modal.classList.add('hidden');
            state.view = 'landing';
            state.enemies = [];
            state.projectiles = [];
            renderUI();
        }

        function updateScore() {
            const el = document.getElementById('score-el');
            if(el) el.innerText = state.score.toString().padStart(6,'0');
        }

        // --- COMMANDER LOGIC (STACK & QUEUE) ---
        function generateMission() {
            let ops;
            if (state.gameType === 'stack') {
                ops = ['PUSH', 'POP', 'PEEK'];
            } else {
                ops = ['ENQUEUE', 'DEQUEUE', 'FRONT'];
            }
            
            let op = ops[Math.floor(Math.random() * ops.length)];
            
            if (state.dataItems.length === 0) {
                op = state.gameType === 'stack' ? 'PUSH' : 'ENQUEUE';
            }
            if (state.dataItems.length >= state.maxSize) {
                op = state.gameType === 'stack' ? 'POP' : 'DEQUEUE';
            }

            let val = null;
            if (op === 'PUSH' || op === 'ENQUEUE') val = Math.floor(Math.random()*100).toString(16).toUpperCase();

            state.mission = { op, val };
            state.missionTimer = 100;
            renderUI(); // Update mission text
        }

        function failMission(reason) {
            playSound('explosion');
            triggerScreenShake();
            state.lives--;
            addLog(`FAIL: ${reason}`);
            if(state.lives <= 0) {
                gameOver("OUT OF LIVES");
            } else {
                generateMission();
                renderUI();
            }
        }

        function updateMissionUI() {
            const bar = document.getElementById('timer-bar');
            if(bar) bar.style.width = `${state.missionTimer}%`;
        }

        // --- DATA OPERATIONS ---
        function handleAdd(e) {
            // PUSH or ENQUEUE
            if(e) e.preventDefault();
            
            startMusic();
            const input = document.getElementById('dataInput');
            
            // Auto-fill logic
            const addOp = state.gameType === 'stack' ? 'PUSH' : 'ENQUEUE';

            if(state.mission && state.mission.op === addOp && !input.value) {
                input.value = state.mission.val;
            }

            const val = input.value.trim();
            if(!val) return;

            if(state.dataItems.length < state.maxSize) {
                playSound('push');
                const color = colors[Math.floor(Math.random() * colors.length)];
                
                // Stack: Add to top (start of array)
                // Queue: Add to rear (start of array, visualization handles order)
                // For simplified logic: Array[0] is always "Top" or "Rear" visually newly added
                state.dataItems.unshift({ id: Date.now(), val, color, isNew: true });
                
                // Check Mission
                if(state.mission && state.mission.op === addOp) {
                    state.score += 50;
                    playSound('coin');
                    generateMission();
                } else if(state.mission) {
                    failMission("WRONG MOVE");
                }

                renderUI();
                input.value = '';
                document.getElementById('dataInput').focus();
                setTimeout(() => { if(state.dataItems[0]) state.dataItems[0].isNew = false; }, 500);
            } else {
                playSound('error');
            }
        }

        function handleRemove() {
            // POP or DEQUEUE
            startMusic();
            if(state.dataItems.length > 0) {
                
                let targetEl;
                if (state.gameType === 'stack') {
                    // Stack Pop: Remove from Top (first element in DOM)
                    const container = document.getElementById('visual-container');
                    targetEl = container.firstElementChild;
                } else {
                    // Queue Dequeue: Remove from Front (last element in DOM visually? No, queue flows)
                    // Let's say items enter right and leave left.
                    // Visualizer renders array. map((item, i))
                    // If queue, items move towards exit.
                    // Let's remove the "oldest" item which is at the end of the array if we unshift new ones?
                    // Wait, unshift adds to index 0. So index length-1 is oldest.
                    // Stack: Pop removes index 0 (Top).
                    // Queue: Dequeue removes index length-1 (Front).
                    
                    const container = document.getElementById('visual-container');
                    targetEl = container.lastElementChild; 
                }

                if(targetEl) targetEl.classList.add('animate-physics-pop');

                playSound('push'); 
                setTimeout(() => {
                    const removeOp = state.gameType === 'stack' ? 'POP' : 'DEQUEUE';
                    
                    if (state.gameType === 'stack') {
                        state.dataItems.shift();
                    } else {
                        state.dataItems.pop();
                    }
                    
                    if(state.mission && state.mission.op === removeOp) {
                        state.score += 50;
                        playSound('coin');
                        generateMission();
                    } else if(state.mission) {
                        failMission("WRONG MOVE");
                    }
                    renderUI();
                }, 300);
            } else {
                playSound('error');
            }
        }

        function handleInspect() {
            // PEEK or FRONT
            startMusic();
            if(state.dataItems.length > 0) {
                playSound('peek');
                
                const inspectOp = state.gameType === 'stack' ? 'PEEK' : 'FRONT';
                
                if(state.mission && state.mission.op === inspectOp) {
                    state.score += 50;
                    playSound('coin');
                    generateMission();
                } else if(state.mission) {
                    failMission("WRONG MOVE");
                }
            } else {
                playSound('error');
            }
        }

        function handleClear() {
            state.dataItems = [];
            renderUI();
        }

        function addLog(msg) {
            state.logs.unshift(msg);
            if(state.logs.length > 5) state.logs.pop();
        }

        // --- MAIN RENDERER ---
        function renderUI() {
            const root = document.getElementById('ui-layer');
            const playerShip = document.getElementById('player-ship');

            if (state.view === 'landing') {
                if(playerShip) playerShip.classList.remove('hidden'); 
                root.innerHTML = `
                    <div class="text-center z-50">
                        <div class="mb-12 p-8 retro-panel">
                            <h1 class="text-5xl md:text-7xl mb-4 neon-text rgb-effect animate-pulse">DATA STRUCTURE<br>ARCADE</h1>
                            <div class="mt-8">
                                <button onclick="insertCoin()" class="arcade-btn px-8 py-4 text-green-400 text-xl border-green-500 blink hover:scale-105 transition-transform">
                                    ${state.credits > 0 ? `CREDITS: ${state.credits}` : 'INSERT COIN'}
                                </button>
                            </div>
                        </div>

                        <div class="flex gap-8 justify-center">
                            <div class="retro-panel p-6 cursor-pointer hover:bg-white/10 transition-transform hover:-translate-y-2 interactive-card" onclick="startGame('stack')">
                                <div class="text-yellow-400 text-3xl mb-2">LVL 1</div>
                                <div class="text-white text-xl">STACKS</div>
                                <div class="text-green-400 text-xs mt-2">${state.credits > 0 ? 'READY' : 'LOCKED'}</div>
                            </div>
                            <div class="retro-panel p-6 cursor-pointer hover:bg-white/10 transition-transform hover:-translate-y-2 interactive-card" onclick="startGame('queue')">
                                <div class="text-cyan-400 text-3xl mb-2">LVL 2</div>
                                <div class="text-white text-xl">QUEUES</div>
                                <div class="text-green-400 text-xs mt-2">${state.credits > 0 ? 'READY' : 'LOCKED'}</div>
                            </div>
                             <div class="retro-panel p-6 opacity-50">
                                <div class="text-gray-500 text-3xl mb-2">LVL 3</div>
                                <div class="text-gray-500">LISTS</div>
                                <div class="text-red-500 text-xs mt-2"><i data-lucide="lock" class="inline w-3"></i></div>
                            </div>
                        </div>
                    </div>
                `;
            } else {
                if(playerShip) playerShip.classList.add('hidden'); 
                
                const isStack = state.gameType === 'stack';
                const addLabel = isStack ? 'PUSH' : 'ENQUEUE';
                const removeLabel = isStack ? 'POP' : 'DEQUEUE';
                const inspectLabel = isStack ? 'PEEK' : 'FRONT';
                
                // --- VISUALIZATION GENERATION ---
                let visualHtml = '';
                
                if (isStack) {
                    // STACK: Vertical Tube
                    visualHtml = state.dataItems.map((item, i) => `
                        <div class="stack-item ${item.isNew ? 'animate-physics-drop' : ''}" 
                             style="border-color: ${item.color}; color: ${item.color}; box-shadow: 0 0 10px ${item.color}">
                            ${item.val}
                            ${i===0 ? '<span class="absolute -right-16 text-xs text-white"><< TOP</span>' : ''}
                        </div>
                    `).join('');
                } else {
                    // QUEUE: Horizontal Conveyor
                    // Items added to Rear (Left side here? Or Right? Let's say flow is Right -> Left)
                    // New items unshifted to array start. Oldest at end.
                    // Visual: [Newest] [..] [..] [Oldest (Front)]
                    // Let's render horizontally.
                    visualHtml = state.dataItems.map((item, i) => `
                         <div class="queue-item ${item.isNew ? 'animate-physics-slide' : ''}" 
                             style="border-color: ${item.color}; color: ${item.color}; box-shadow: 0 0 10px ${item.color}">
                            ${item.val}
                            ${i===state.dataItems.length-1 ? '<span class="absolute -bottom-8 text-xs text-white">FRONT</span>' : ''}
                            ${i===0 ? '<span class="absolute -top-8 text-xs text-white">REAR</span>' : ''}
                        </div>
                    `).join('');
                }

                const hearts = '❤️'.repeat(state.lives);
                
                let missionText = "WAITING...";
                if(state.mission) {
                    missionText = `CPU: ${state.mission.op}`;
                    if(state.mission.val) missionText += ` [${state.mission.val}]`;
                }
                
                // THEORY TEXT
                let theoryHtml = '';
                if(isStack) {
                    theoryHtml = `
                        <p class="text-xs leading-6 text-gray-300">
                            1. <strong>LIFO:</strong> Last In, First Out.<br>
                            2. <strong>Push:</strong> Add to TOP (O(1)).<br>
                            3. <strong>Pop:</strong> Remove TOP (O(1)).<br>
                            4. Don't overflow the buffer!
                        </p>`;
                } else {
                    theoryHtml = `
                         <p class="text-xs leading-6 text-gray-300">
                            1. <strong>FIFO:</strong> First In, First Out.<br>
                            2. <strong>Enqueue:</strong> Add to REAR (O(1)).<br>
                            3. <strong>Dequeue:</strong> Remove FRONT (O(1)).<br>
                            4. Keep the line moving!
                        </p>`;
                }

                root.innerHTML = `
                    <div class="w-full max-w-6xl p-4 h-full flex flex-col">
                        <!-- HUD -->
                        <div class="flex justify-between items-center mb-6 retro-panel p-4">
                            <button onclick="setView('landing')" class="arcade-btn px-4 py-2 text-xs">EXIT</button>
                            <div class="flex-1 mx-8">
                                <div class="text-yellow-400 text-xl text-center mb-1 blink font-bold">${missionText}</div>
                                <div class="w-full h-2 bg-gray-700 rounded-full overflow-hidden">
                                    <div id="timer-bar" class="h-full bg-green-500" style="width: ${state.missionTimer}%"></div>
                                </div>
                            </div>
                            <div class="text-right">
                                <div class="text-xs text-gray-400">SCORE</div>
                                <div id="score-el" class="text-2xl text-yellow-400">${state.score.toString().padStart(6,'0')}</div>
                                <div class="text-lg mt-1">${hearts}</div>
                            </div>
                        </div>

                        <div class="grid grid-cols-12 gap-8 flex-1">
                            <!-- Controls -->
                            <div class="col-span-4 flex flex-col gap-4">
                                <div class="retro-panel p-4">
                                    <h2 class="text-cyan-400 mb-4 text-sm">>> ${isStack ? 'STACK_OPS' : 'QUEUE_OPS'}</h2>
                                    <form onsubmit="handleAdd(event)" class="flex gap-2 mb-4">
                                        <input id="dataInput" type="text" maxlength="4" class="w-full bg-black border-2 border-green-500 text-green-500 p-2 outline-none uppercase font-bold" placeholder="DATA" autocomplete="off" autofocus>
                                        <button onclick="handleAdd()" class="arcade-btn bg-blue-900 px-4 hover:bg-blue-800 text-xs">${addLabel}</button>
                                    </form>
                                    <div class="grid grid-cols-2 gap-4">
                                        <button onclick="handleRemove()" class="arcade-btn bg-red-900 py-4 hover:bg-red-800 text-xs">${removeLabel}</button>
                                        <button onclick="handleInspect()" class="arcade-btn bg-purple-900 py-4 hover:bg-purple-800 text-xs">${inspectLabel}</button>
                                    </div>
                                    <button onclick="handleClear()" class="arcade-btn w-full mt-4 py-2 text-xs opacity-70">CLEAR MEMORY</button>
                                </div>
                                <div class="retro-panel p-4 flex-1 overflow-hidden">
                                    <h3 class="text-xs text-gray-500 mb-2">SYSTEM_LOGS</h3>
                                    <div class="text-xs text-green-400 font-mono flex flex-col gap-1">
                                        ${state.logs.map(l => `<span>> ${l}</span>`).join('')}
                                    </div>
                                </div>
                            </div>

                            <!-- Visualization Area -->
                            <div class="col-span-5 flex flex-col items-center justify-end relative">
                                <div class="absolute inset-x-0 bottom-0 top-10 border-4 border-white/50 bg-white/5 backdrop-blur-sm rounded-xl flex ${isStack ? 'flex-col justify-end' : 'flex-row items-center justify-center'} p-4 overflow-hidden">
                                    <div class="absolute top-2 left-2 text-xs text-gray-500">MAX: ${state.maxSize}</div>
                                    <div id="visual-container" class="w-full flex ${isStack ? 'flex-col items-center' : 'flex-row items-center justify-center gap-2'}">
                                        ${visualHtml}
                                    </div>
                                    ${state.dataItems.length === 0 ? '<div class="absolute text-gray-600 animate-pulse">NO_DATA</div>' : ''}
                                </div>
                            </div>

                            <!-- Info -->
                            <div class="col-span-3 retro-panel h-fit">
                                <h2 class="text-yellow-500 mb-4 text-sm">>> MISSION_GUIDE</h2>
                                ${theoryHtml}
                                <br>
                                <p class="text-xs text-red-400">WARNING: Failed ops decrease HP.</p>
                            </div>
                        </div>
                    </div>
                `;
            }
            lucide.createIcons();
        }

        // Generate stars
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

        // Init
        setTimeout(initStars, 100);
        // Play startup sound
        setTimeout(() => playSound('startup'), 500);
        startLoop();
        renderUI();

    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(APP_TEMPLATE)

@app.route('/music')
def serve_music():
    try:
        return send_file(MUSIC_FILENAME)
    except FileNotFoundError:
        return "Music file not found", 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)