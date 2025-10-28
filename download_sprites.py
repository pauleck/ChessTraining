#!/usr/bin/env python3
"""
Helper script to download chess piece sprites.
Run this to automatically download and set up chess piece graphics.
"""

import urllib.request
import sys

def download_sprite_sheet():
    """Download a chess piece sprite sheet."""

    # List of possible sprite sheet URLs
    sprite_urls = [
        # Wikimedia Commons - reliable source
        "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Chess_Pieces_Sprite.svg/600px-Chess_Pieces_Sprite.svg.png",
        # OpenGameArt
        "https://opengameart.org/sites/default/files/chess_pieces_sprite.png",
        # Alternative sources
        "https://raw.githubusercontent.com/lichess-org/lila/master/public/piece/cburnett/wK.svg",
    ]

    print("Chess Piece Sprite Downloader")
    print("=" * 50)
    print()
    print("Attempting to download chess piece sprite sheet...")
    print()

    for i, url in enumerate(sprite_urls, 1):
        try:
            print(f"Trying source {i}/{len(sprite_urls)}: {url[:60]}...")

            urllib.request.urlretrieve(url, "chess_pieces.png")

            print("✓ Successfully downloaded sprite sheet!")
            print("  Saved as: chess_pieces.png")
            print()
            print("You can now run chess_trainer.py and it will use the sprite graphics.")
            return True

        except Exception as e:
            print(f"✗ Failed: {e}")
            continue

    print()
    print("=" * 50)
    print("Could not automatically download sprite sheet.")
    print()
    print("Manual download instructions:")
    print("1. Open your web browser")
    print("2. Search for 'chess pieces sprite sheet PNG'")
    print("3. Download a sprite sheet you like")
    print("4. Save it as 'chess_pieces.png' in this directory")
    print()
    print("Recommended sprite sheet layout:")
    print("  - 6 columns x 2 rows (King, Queen, Bishop, Knight, Rook, Pawn)")
    print("  - First row: White pieces")
    print("  - Second row: Black pieces")
    print()
    print("The game will work fine without sprites using Unicode characters!")
    return False

if __name__ == "__main__":
    download_sprite_sheet()
