# Chess Trainer

A simple chess training application built with Python and Pygame. Play against a computer opponent that makes random legal moves.

## Features

- Full chess rule implementation (including castling, en passant, check, checkmate)
- Graphical 2D board with Unicode chess pieces
- Click to select piece, click again to move
- Choose to play as White or Black
- Computer opponent makes random legal moves
- Move validation and highlighting
- Game over detection (checkmate, stalemate, insufficient material)

## Requirements

- Python 3.7 or higher
- pygame (the only external dependency!)

## Installation

1. Install the required packages:

```bash
pip install -r requirements.txt
```

## Using Custom Chess Piece Graphics

By default, the game uses Unicode chess piece characters. For better graphics, you can add a chess piece sprite sheet:

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
