# Chess Trainer

A chess training application available in both Python/Pygame and single-file HTML versions. Play against a computer opponent that makes random legal moves.

## Versions

### 1. HTML Version (chess_trainer.html)
**Single self-contained HTML file** - Just open in any modern web browser!

- No installation required
- Works offline
- Runs in any modern browser
- Mobile-friendly responsive design

### 2. Python Version (chess_trainer.py)
Desktop application using Pygame with optional sprite sheet support.

## Features

Both versions include:

- Full chess rule implementation (including castling, en passant, check, checkmate)
- Graphical 2D board with Unicode chess pieces
- Click to select piece, click again to move
- Choose to play as White or Black
- Computer opponent makes random legal moves
- Move validation and highlighting
- Game over detection (checkmate, stalemate, insufficient material)
- **Move history panel** showing all moves in standard algebraic notation (SAN)
- Check (+) and checkmate (#) symbols in move notation

## Quick Start

### HTML Version (Recommended for quick play):
```bash
# Just open the file in your browser
open chess_trainer.html
# or double-click chess_trainer.html
```

### Python Version:
```bash
# Install pygame
pip install pygame

# Run the game
python chess_trainer.py
```

## Using Custom Chess Piece Graphics (Python Version Only)

The Python version supports custom sprite sheets. The HTML version uses Unicode characters.

1. Download a chess piece sprite sheet (PNG format)
   - Example: https://spng.pngfind.com/pngs/s/692-6922125_chess-pieces-sprite-chess-pieces-sprite-sheet-hd.png
   - Or search for "chess pieces sprite sheet PNG" and download one you like

2. Save it as `chess_pieces.png` in the same directory as `chess_trainer.py`

3. The sprite sheet should be organized as:
   - **6 columns x 2 rows**: King, Queen, Bishop, Knight, Rook, Pawn (white on top, black on bottom)
   - **OR 2 columns x 6 rows**: White pieces in left column, black pieces in right column

The game will automatically detect and use the sprite sheet if present, otherwise it falls back to Unicode characters.

## How to Play

1. Run the game:

```bash
python chess_trainer.py
```

2. Choose your color (White or Black) at the start

3. Click on a piece to select it (highlighted in yellow-green)

4. Valid moves will be highlighted in darker green

5. Click on a highlighted square to move your piece

6. The computer will automatically make its move after yours

## Controls

- Mouse Click: Select piece and make moves
- Close Window: Exit the game

## Game Rules

All standard chess rules are implemented:
- Pawns move forward, capture diagonally, and can promote to queen at the end
- Knights move in L-shape
- Bishops move diagonally
- Rooks move horizontally or vertically
- Queens move in any direction
- Kings move one square in any direction
- Castling (kingside and queenside)
- En passant capture
- Check and checkmate detection

## Future Improvements

- Add a smarter AI opponent
- Add move history
- Add ability to undo moves
- Add timer
- Save/load games
- Better graphics with actual piece images
