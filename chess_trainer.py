#!/usr/bin/env python3
"""
Chess Training App - A simple chess game with pygame
Play against a computer that makes random legal moves.
"""

import pygame
import random
import sys
from typing import Optional, Tuple, List
from copy import deepcopy

# Constants
WINDOW_SIZE = 600
BOARD_SIZE = 8
SQUARE_SIZE = WINDOW_SIZE // BOARD_SIZE
FPS = 60

# Colors
LIGHT_SQUARE = (240, 217, 181)
DARK_SQUARE = (181, 136, 99)
SELECTED = (186, 202, 68)
VALID_MOVE = (130, 151, 105)
TEXT_COLOR = (50, 50, 50)
BG_COLOR = (40, 40, 40)
BUTTON_COLOR = (100, 100, 100)
BUTTON_HOVER = (130, 130, 130)

# Piece types
EMPTY = 0
PAWN = 1
KNIGHT = 2
BISHOP = 3
ROOK = 4
QUEEN = 5
KING = 6

# Piece colors
WHITE_PIECE = 1
BLACK_PIECE = -1


class ChessGame:
    """Main chess game class with complete chess rules."""

    def __init__(self):
        """Initialize the chess game."""
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 100))
        pygame.display.set_caption("Chess Trainer")
        self.clock = pygame.time.Clock()

        # Board is 8x8, each cell is (piece_type, color) or (EMPTY, 0)
        self.board = self.init_board()
        self.selected_square: Optional[Tuple[int, int]] = None
        self.valid_moves = []
        self.player_color = None  # WHITE_PIECE or BLACK_PIECE
        self.current_turn = WHITE_PIECE
        self.game_state = "color_selection"  # color_selection, playing, game_over
        self.status_message = "Choose your color"

        # Game state tracking
        self.castling_rights = {
            WHITE_PIECE: {"kingside": True, "queenside": True},
            BLACK_PIECE: {"kingside": True, "queenside": True}
        }
        self.en_passant_target = None
        self.king_positions = {WHITE_PIECE: (7, 4), BLACK_PIECE: (0, 4)}

        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        # Piece Unicode characters
        self.piece_symbols = {
            PAWN: {WHITE_PIECE: '♙', BLACK_PIECE: '♟'},
            KNIGHT: {WHITE_PIECE: '♘', BLACK_PIECE: '♞'},
            BISHOP: {WHITE_PIECE: '♗', BLACK_PIECE: '♝'},
            ROOK: {WHITE_PIECE: '♖', BLACK_PIECE: '♜'},
            QUEEN: {WHITE_PIECE: '♕', BLACK_PIECE: '♛'},
            KING: {WHITE_PIECE: '♔', BLACK_PIECE: '♚'}
        }

        self.piece_font = pygame.font.Font(None, 80)

    def init_board(self):
        """Initialize the chess board with starting position."""
        board = [[(EMPTY, 0) for _ in range(8)] for _ in range(8)]

        # Black pieces (row 0, 1)
        board[0] = [(ROOK, BLACK_PIECE), (KNIGHT, BLACK_PIECE), (BISHOP, BLACK_PIECE), (QUEEN, BLACK_PIECE),
                    (KING, BLACK_PIECE), (BISHOP, BLACK_PIECE), (KNIGHT, BLACK_PIECE), (ROOK, BLACK_PIECE)]
        board[1] = [(PAWN, BLACK_PIECE) for _ in range(8)]

        # White pieces (row 6, 7)
        board[6] = [(PAWN, WHITE_PIECE) for _ in range(8)]
        board[7] = [(ROOK, WHITE_PIECE), (KNIGHT, WHITE_PIECE), (BISHOP, WHITE_PIECE), (QUEEN, WHITE_PIECE),
                    (KING, WHITE_PIECE), (BISHOP, WHITE_PIECE), (KNIGHT, WHITE_PIECE), (ROOK, WHITE_PIECE)]

        return board

    def square_to_coords(self, row: int, col: int) -> Tuple[int, int]:
        """Convert board position to pixel coordinates."""
        if self.player_color == BLACK_PIECE:
            display_row = 7 - row
            display_col = 7 - col
        else:
            display_row = row
            display_col = col

        x = display_col * SQUARE_SIZE
        y = display_row * SQUARE_SIZE
        return x, y

    def coords_to_square(self, x: int, y: int) -> Optional[Tuple[int, int]]:
        """Convert pixel coordinates to board position."""
        if x < 0 or x >= WINDOW_SIZE or y < 0 or y >= WINDOW_SIZE:
            return None

        col = x // SQUARE_SIZE
        row = y // SQUARE_SIZE

        if self.player_color == BLACK_PIECE:
            row = 7 - row
            col = 7 - col

        return (row, col)

    def get_piece_moves(self, row: int, col: int) -> List[Tuple[int, int]]:
        """Get all pseudo-legal moves for a piece (not checking for checks)."""
        piece_type, color = self.board[row][col]
        if piece_type == EMPTY:
            return []

        moves = []

        if piece_type == PAWN:
            direction = -1 if color == WHITE_PIECE else 1
            start_row = 6 if color == WHITE_PIECE else 1

            # Forward move
            new_row = row + direction
            if 0 <= new_row < 8 and self.board[new_row][col][0] == EMPTY:
                moves.append((new_row, col))

                # Double move from starting position
                if row == start_row:
                    new_row2 = row + 2 * direction
                    if self.board[new_row2][col][0] == EMPTY:
                        moves.append((new_row2, col))

            # Captures
            for dcol in [-1, 1]:
                new_col = col + dcol
                new_row = row + direction
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target = self.board[new_row][new_col]
                    if target[0] != EMPTY and target[1] != color:
                        moves.append((new_row, new_col))
                    # En passant
                    elif self.en_passant_target == (new_row, new_col):
                        moves.append((new_row, new_col))

        elif piece_type == KNIGHT:
            knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
            for dr, dc in knight_moves:
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target = self.board[new_row][new_col]
                    if target[0] == EMPTY or target[1] != color:
                        moves.append((new_row, new_col))

        elif piece_type == BISHOP:
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            moves.extend(self.get_sliding_moves(row, col, directions, color))

        elif piece_type == ROOK:
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            moves.extend(self.get_sliding_moves(row, col, directions, color))

        elif piece_type == QUEEN:
            directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            moves.extend(self.get_sliding_moves(row, col, directions, color))

        elif piece_type == KING:
            king_moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            for dr, dc in king_moves:
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target = self.board[new_row][new_col]
                    if target[0] == EMPTY or target[1] != color:
                        moves.append((new_row, new_col))

            # Castling
            if self.castling_rights[color]["kingside"]:
                if self.board[row][5][0] == EMPTY and self.board[row][6][0] == EMPTY:
                    if not self.is_square_attacked(row, col, -color) and \
                       not self.is_square_attacked(row, 5, -color):
                        moves.append((row, 6))

            if self.castling_rights[color]["queenside"]:
                if self.board[row][3][0] == EMPTY and self.board[row][2][0] == EMPTY and \
                   self.board[row][1][0] == EMPTY:
                    if not self.is_square_attacked(row, col, -color) and \
                       not self.is_square_attacked(row, 3, -color):
                        moves.append((row, 2))

        return moves

    def get_sliding_moves(self, row: int, col: int, directions: List[Tuple[int, int]], color: int) -> List[Tuple[int, int]]:
        """Get moves for sliding pieces (bishop, rook, queen)."""
        moves = []
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                target = self.board[new_row][new_col]
                if target[0] == EMPTY:
                    moves.append((new_row, new_col))
                elif target[1] != color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
                new_row += dr
                new_col += dc
        return moves

    def is_square_attacked(self, row: int, col: int, by_color: int) -> bool:
        """Check if a square is attacked by a given color."""
        # Check all pieces of the attacking color
        for r in range(8):
            for c in range(8):
                piece_type, color = self.board[r][c]
                if color == by_color and piece_type != EMPTY:
                    # Get moves for this piece (without castling for kings)
                    if piece_type == KING:
                        king_moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
                        for dr, dc in king_moves:
                            if r + dr == row and c + dc == col:
                                return True
                    else:
                        moves = self.get_piece_moves(r, c)
                        if (row, col) in moves:
                            return True
        return False

    def is_in_check(self, color: int) -> bool:
        """Check if the given color's king is in check."""
        king_pos = self.king_positions[color]
        return self.is_square_attacked(king_pos[0], king_pos[1], -color)

    def get_legal_moves(self, row: int, col: int) -> List[Tuple[int, int]]:
        """Get all legal moves for a piece (checking for checks)."""
        piece_type, color = self.board[row][col]
        if piece_type == EMPTY or color != self.current_turn:
            return []

        pseudo_legal = self.get_piece_moves(row, col)
        legal = []

        for target_row, target_col in pseudo_legal:
            # Make the move temporarily
            original = self.board[target_row][target_col]
            self.board[target_row][target_col] = self.board[row][col]
            self.board[row][col] = (EMPTY, 0)

            # Update king position if moving king
            old_king_pos = None
            if piece_type == KING:
                old_king_pos = self.king_positions[color]
                self.king_positions[color] = (target_row, target_col)

            # Check if king is in check
            if not self.is_in_check(color):
                legal.append((target_row, target_col))

            # Undo the move
            self.board[row][col] = self.board[target_row][target_col]
            self.board[target_row][target_col] = original
            if old_king_pos:
                self.king_positions[color] = old_king_pos

        return legal

    def make_move(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        """Make a move on the board."""
        piece_type, color = self.board[from_row][from_col]

        # Handle en passant capture
        if piece_type == PAWN and (to_row, to_col) == self.en_passant_target:
            capture_row = from_row
            self.board[capture_row][to_col] = (EMPTY, 0)

        # Handle castling
        if piece_type == KING and abs(to_col - from_col) == 2:
            # Move the rook
            if to_col == 6:  # Kingside
                self.board[to_row][5] = self.board[to_row][7]
                self.board[to_row][7] = (EMPTY, 0)
            else:  # Queenside
                self.board[to_row][3] = self.board[to_row][0]
                self.board[to_row][0] = (EMPTY, 0)

        # Move the piece
        self.board[to_row][to_col] = self.board[from_row][from_col]
        self.board[from_row][from_col] = (EMPTY, 0)

        # Update king position
        if piece_type == KING:
            self.king_positions[color] = (to_row, to_col)
            self.castling_rights[color]["kingside"] = False
            self.castling_rights[color]["queenside"] = False

        # Update castling rights if rook moves
        if piece_type == ROOK:
            if from_row == 0 and from_col == 0:
                self.castling_rights[BLACK_PIECE]["queenside"] = False
            elif from_row == 0 and from_col == 7:
                self.castling_rights[BLACK_PIECE]["kingside"] = False
            elif from_row == 7 and from_col == 0:
                self.castling_rights[WHITE_PIECE]["queenside"] = False
            elif from_row == 7 and from_col == 7:
                self.castling_rights[WHITE_PIECE]["kingside"] = False

        # Set en passant target if pawn moved two squares
        self.en_passant_target = None
        if piece_type == PAWN and abs(to_row - from_row) == 2:
            self.en_passant_target = ((from_row + to_row) // 2, to_col)

        # Pawn promotion (auto-promote to queen)
        if piece_type == PAWN:
            if (color == WHITE_PIECE and to_row == 0) or (color == BLACK_PIECE and to_row == 7):
                self.board[to_row][to_col] = (QUEEN, color)

        # Switch turn
        self.current_turn = -self.current_turn
        return True

    def has_legal_moves(self, color: int) -> bool:
        """Check if the given color has any legal moves."""
        for row in range(8):
            for col in range(8):
                piece_type, piece_color = self.board[row][col]
                if piece_color == color:
                    if len(self.get_legal_moves(row, col)) > 0:
                        return True
        return False

    def check_game_over(self):
        """Check if the game is over and update status."""
        if not self.has_legal_moves(self.current_turn):
            if self.is_in_check(self.current_turn):
                winner = "White" if self.current_turn == BLACK_PIECE else "Black"
                self.status_message = f"Checkmate! {winner} wins!"
            else:
                self.status_message = "Stalemate! It's a draw."
            self.game_state = "game_over"
        elif self.is_in_check(self.current_turn):
            self.status_message = "Check!"

    def draw_board(self):
        """Draw the chess board."""
        for display_row in range(BOARD_SIZE):
            for display_col in range(BOARD_SIZE):
                # Determine square color
                is_light = (display_row + display_col) % 2 == 0
                color = LIGHT_SQUARE if is_light else DARK_SQUARE

                # Convert display position to board position
                if self.player_color == BLACK_PIECE:
                    row = 7 - display_row
                    col = 7 - display_col
                else:
                    row = display_row
                    col = display_col

                # Highlight selected square
                if self.selected_square == (row, col):
                    color = SELECTED
                # Highlight valid move squares
                elif (row, col) in self.valid_moves:
                    color = VALID_MOVE

                pygame.draw.rect(
                    self.screen,
                    color,
                    (display_col * SQUARE_SIZE, display_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                )

    def draw_pieces(self):
        """Draw the chess pieces."""
        for row in range(8):
            for col in range(8):
                piece_type, color = self.board[row][col]
                if piece_type != EMPTY:
                    x, y = self.square_to_coords(row, col)
                    symbol = self.piece_symbols[piece_type][color]

                    # Render piece
                    piece_color = (255, 255, 255) if color == WHITE_PIECE else (0, 0, 0)
                    piece_surface = self.piece_font.render(symbol, True, piece_color)
                    piece_rect = piece_surface.get_rect(center=(x + SQUARE_SIZE // 2, y + SQUARE_SIZE // 2))
                    self.screen.blit(piece_surface, piece_rect)

    def draw_status(self):
        """Draw status bar at the bottom."""
        pygame.draw.rect(self.screen, BG_COLOR, (0, WINDOW_SIZE, WINDOW_SIZE, 100))

        # Status message
        status_surface = self.small_font.render(self.status_message, True, (255, 255, 255))
        status_rect = status_surface.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE + 30))
        self.screen.blit(status_surface, status_rect)

        # Turn indicator
        if self.game_state == "playing":
            turn_text = "White's turn" if self.current_turn == WHITE_PIECE else "Black's turn"
            turn_surface = self.small_font.render(turn_text, True, (255, 255, 255))
            turn_rect = turn_surface.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE + 60))
            self.screen.blit(turn_surface, turn_rect)

    def draw_color_selection(self):
        """Draw color selection screen."""
        self.screen.fill(BG_COLOR)

        # Title
        title = self.font.render("Choose Your Color", True, (255, 255, 255))
        title_rect = title.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2 - 100))
        self.screen.blit(title, title_rect)

        # White button
        white_button = pygame.Rect(WINDOW_SIZE // 2 - 150, WINDOW_SIZE // 2, 120, 50)
        mouse_pos = pygame.mouse.get_pos()
        white_color = BUTTON_HOVER if white_button.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(self.screen, white_color, white_button, border_radius=5)
        white_text = self.font.render("White", True, (255, 255, 255))
        white_text_rect = white_text.get_rect(center=white_button.center)
        self.screen.blit(white_text, white_text_rect)

        # Black button
        black_button = pygame.Rect(WINDOW_SIZE // 2 + 30, WINDOW_SIZE // 2, 120, 50)
        black_color = BUTTON_HOVER if black_button.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(self.screen, black_color, black_button, border_radius=5)
        black_text = self.font.render("Black", True, (255, 255, 255))
        black_text_rect = black_text.get_rect(center=black_button.center)
        self.screen.blit(black_text, black_text_rect)

        return white_button, black_button

    def handle_click(self, pos: Tuple[int, int]):
        """Handle mouse click on the board."""
        if self.game_state != "playing":
            return

        # Check if it's player's turn
        if self.current_turn != self.player_color:
            return

        x, y = pos
        if y > WINDOW_SIZE:  # Clicked in status bar
            return

        clicked_square = self.coords_to_square(x, y)
        if clicked_square is None:
            return

        row, col = clicked_square

        # If a square is already selected
        if self.selected_square is not None:
            # Try to make a move
            if clicked_square in self.valid_moves:
                from_row, from_col = self.selected_square
                self.make_move(from_row, from_col, row, col)
                self.selected_square = None
                self.valid_moves = []
                self.check_game_over()

                # Computer's turn
                if self.game_state == "playing" and self.current_turn != self.player_color:
                    pygame.display.flip()
                    pygame.time.wait(500)
                    self.make_computer_move()
                return

            # Clicked on own piece, select it instead
            piece_type, piece_color = self.board[row][col]
            if piece_color == self.player_color:
                self.selected_square = (row, col)
                self.valid_moves = self.get_legal_moves(row, col)
                self.status_message = "Click destination square"
            else:
                self.selected_square = None
                self.valid_moves = []
        else:
            # Select a piece
            piece_type, piece_color = self.board[row][col]
            if piece_type != EMPTY and piece_color == self.player_color:
                self.selected_square = (row, col)
                self.valid_moves = self.get_legal_moves(row, col)
                if self.valid_moves:
                    self.status_message = "Click destination square"
                else:
                    self.status_message = "No legal moves for this piece"

    def make_computer_move(self):
        """Make a random legal move for the computer."""
        if self.game_state != "playing":
            return

        # Get all legal moves for computer
        all_moves = []
        for row in range(8):
            for col in range(8):
                piece_type, color = self.board[row][col]
                if color == self.current_turn:
                    moves = self.get_legal_moves(row, col)
                    for to_row, to_col in moves:
                        all_moves.append(((row, col), (to_row, to_col)))

        if all_moves:
            (from_row, from_col), (to_row, to_col) = random.choice(all_moves)
            self.make_move(from_row, from_col, to_row, to_col)
            self.status_message = f"Computer moved"
            self.check_game_over()

    def start_game(self, player_color: int):
        """Start the game with the selected color."""
        self.player_color = player_color
        self.game_state = "playing"
        self.status_message = "Your turn!" if player_color == WHITE_PIECE else "Computer's turn"

        # If player chose black, computer makes first move
        if player_color == BLACK_PIECE:
            pygame.time.wait(500)
            self.make_computer_move()

    def run(self):
        """Main game loop."""
        running = True

        while running:
            self.clock.tick(FPS)

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.game_state == "color_selection":
                        white_button, black_button = self.draw_color_selection()
                        if white_button.collidepoint(event.pos):
                            self.start_game(WHITE_PIECE)
                        elif black_button.collidepoint(event.pos):
                            self.start_game(BLACK_PIECE)

                    elif self.game_state == "playing":
                        self.handle_click(event.pos)

            # Draw everything
            if self.game_state == "color_selection":
                self.draw_color_selection()
            else:
                self.draw_board()
                self.draw_pieces()
                self.draw_status()

            pygame.display.flip()

        pygame.quit()
        sys.exit()


def main():
    """Run the chess trainer."""
    game = ChessGame()
    game.run()


if __name__ == "__main__":
    main()
