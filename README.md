# DATA-STRUCTURE-ARCADE-RETRO-VISUALISER 🕹️

A gamified 🕹️, retro-styled learning platform for Data Structures and Algorithms.

<img width="1351" height="652" alt="Screenshot from 2025-12-11 12-01-51" src="https://github.com/user-attachments/assets/fe0ae04f-37e1-40d2-a557-b0f4ced35782" />

# About The Project

This project reimagines standard Computer Science visualizations as an 80s arcade game. Instead of boring diagrams, users interact with a CRT-styled interface 📺 complete with scanlines, neon glows and synthesized sound effects. The application serves as both a visualizer and a game, challenging users to perform data operations (like Push, Pop, Enqueue, Dequeue) under time pressure while maintaining the correct data structure logic (LIFO vs. FIFO).

# Key Features

### 1. Retro Immersion 🕶️

**_CRT Simulation 📺:_** 

Hyper-realistic CSS shaders including screen curvature, scanlines, RGB chromatic aberration and screen flicker.

**_Audio Engine 🔊:_** 

A hybrid audio system using native Web Audio API for synthesized sound effects (shooting, explosions) and local file support for retro background music.

**_Visuals :_** "

Press Start 2P" pixel fonts, neon aesthetics and particle physics explosions.

### 2. Gamified Learning 🎮

**_Landing Page Shooter 🛸:_** 

The main menu features a playable "Space Invaders" style mini-game where the mouse controls a ship destroying falling bugs.

**_Coin System 🪙:_** 

Users must virtually "Insert Coin" to unlock levels.

**_CPU Missions 💾:_** 

A "Simon Says" mechanic where the CPU issues commands (e.g., "CPU: PUSH"). The player must execute the correct operation before the timer runs out.

**_Health & Score ❤️:_** 

Players have 3 lives. Wrong operations or overflows result in damage and screen shake effects.

### 3. Data Structure Modules 🧱

**_Level 1: Stacks (LIFO) :_** 

Visualized as a vertical data tube. Concepts covered: Push, Pop, Peek, Overflow, Underflow.

**_Level 2: Queues (FIFO) :_** 

Visualized as a horizontal conveyor belt. Concepts covered: Enqueue, Dequeue, Front.

# 🛠️ Core Technologies

This project uses a lightweight, single-file architecture designed for portability.

### Backend :

**_Python (Flask):_** 

Handles routing and serves the application template.

**_Jinja2:_** 

Used for dynamic template rendering.

### Frontend :

**_HTML5 & Vanilla JavaScript:_** 

Handles the game loop, physics engine (gravity, collisions), and DOM manipulation.

**_Tailwind CSS (CDN):_** 

Used for rapid UI layout and utility classes.

**_CSS3 Animations:_** 

Keyframes used for "physics-like" movements (bouncing drops, popping items) and CRT effects.

### Assets 📂:

**_Lucide Icons:_** 

Vector icons for game entities (ghosts, skulls, rockets).

**_Google Fonts:_** 

Retro pixel typography.

# How It Works (The Game Loop)

**_Physics Engine :_** 

A custom JavaScript loop runs via requestAnimationFrame. It calculates gravity, velocity, and collision detection for falling enemies and projectiles.

**_State Management :_** 

The app maintains a state object tracking the Stack/Queue arrays, Score, Credits, and active "Missions".

### Rendering :

**_Game Layer:_** 

Renders moving entities (ships, enemies) using absolute positioning based on physics calculations.

**_UI Layer:_** 

Renders the Data Structures (DOM elements) based on the state array. When the array changes, the UI updates instantly.

# Installation & Setup

Prerequisites: Ensure you have Python installed.

*_Install Flask:_*

#### _`pip install flask`_

*_Clone the repo Files:_*

#### _`git clone https://github.com/MAHMAD1499/DATA-STRUCTURE-ARCADE-RETRO-VISUALISER.git`_

*_Music Setup 🎵:_*

Place your own background music file in the project root.

Rename it to background_music.mp3 (or update the file name config in the script).

*_Run the App ._*

*_After successful execution of the code a link will be prompted in your terminal window. CLick on the link. A browser window will be popped with the project
._*
