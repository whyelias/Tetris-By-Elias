# Tetris-By-Elias
A classic Tetris clone built in Python with Pygame, featuring smooth gameplay, scoring, leveling, and a modern twist with a piece hold/swap system.

Features: 
- Core Gameplay: Classic Tetris mechanics with 7 tetrominoes
- Dynamic Difficulty: Game speeds up as the player clears lines and levels up
- Scoring System: Rewards for clearing multiple lines at once (single, double, triple, Tetris)
- Piece Hold/Swap: Save a piece with C and swap it in later with X

User Interface:
- Left panel shows the held piece
- Right panel shows the next piece, current score, level, and lines cleared
- Title + Game Over Screens

Controls:
- Arrow Keys → Move and rotate pieces
- Spacebar → Hard drop
- C → Hold current piece
- X → Swap held piece with current piece
- ESC → Quit

Uses: 
- Python 3
- Pygame

How to Play:
  1. Clone the repo:
     
    git clone https://github.com/<your-username>/tetris-by-tovar.git
    cd tetris-by-tovar
    
  2. Install dependencies:

    pip install pygame

  3. Run the game:

    python tetris.py
