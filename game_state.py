"""
Game state management for the Omok game.
Handles loading, saving, and manipulating the game state.
"""

import json
import os
from typing import Dict, List, Optional, Tuple, Union
from enum import Enum


class Player(Enum):
    """Enumeration for players."""
    BLACK = "black"
    WHITE = "white"
    EMPTY = "empty"


class GameStatus(Enum):
    """Enumeration for game status."""
    ONGOING = "ongoing"
    BLACK_WINS = "black_wins"
    WHITE_WINS = "white_wins"
    DRAW = "draw"


class GameState:
    """Manages the state of the Omok game."""
    
    BOARD_SIZE = 15
    STATE_FILE = "game_state.json"
    
    def __init__(self):
        """Initialize the game state."""
        self.board: List[List[str]] = []
        self.current_player: Player = Player.BLACK
        self.game_status: GameStatus = GameStatus.ONGOING
        self.move_count: int = 0
        self.winner: Optional[Player] = None
        self.last_move: Optional[Tuple[int, int]] = None
        
    def reset_game(self) -> None:
        """Reset the game to initial state."""
        self.board = [[Player.EMPTY.value for _ in range(self.BOARD_SIZE)] 
                     for _ in range(self.BOARD_SIZE)]
        self.current_player = Player.BLACK
        self.game_status = GameStatus.ONGOING
        self.move_count = 0
        self.winner = None
        self.last_move = None
        
    def load_state(self) -> bool:
        """
        Load game state from JSON file.
        
        Returns:
            bool: True if state was loaded successfully, False otherwise.
        """
        try:
            if not os.path.exists(self.STATE_FILE):
                self.reset_game()
                self.save_state()
                return True
                
            with open(self.STATE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            self.board = data.get('board', [])
            self.current_player = Player(data.get('current_player', Player.BLACK.value))
            self.game_status = GameStatus(data.get('game_status', GameStatus.ONGOING.value))
            self.move_count = data.get('move_count', 0)
            self.winner = Player(data['winner']) if data.get('winner') else None
            self.last_move = tuple(data['last_move']) if data.get('last_move') else None
            
            # Validate board size
            if len(self.board) != self.BOARD_SIZE or any(len(row) != self.BOARD_SIZE for row in self.board):
                self.reset_game()
                self.save_state()
                
            return True
            
        except (json.JSONDecodeError, KeyError, ValueError, TypeError) as e:
            print(f"Error loading game state: {e}")
            self.reset_game()
            self.save_state()
            return False
            
    def save_state(self) -> bool:
        """
        Save current game state to JSON file.
        
        Returns:
            bool: True if state was saved successfully, False otherwise.
        """
        try:
            data = {
                'board': self.board,
                'current_player': self.current_player.value,
                'game_status': self.game_status.value,
                'move_count': self.move_count,
                'winner': self.winner.value if self.winner else None,
                'last_move': list(self.last_move) if self.last_move else None
            }
            
            with open(self.STATE_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
                
            return True
            
        except (OSError, TypeError) as e:
            print(f"Error saving game state: {e}")
            return False
            
    def parse_coordinate(self, coord_str: str) -> Optional[Tuple[int, int]]:
        """
        Parse coordinate string to board indices.
        
        Args:
            coord_str: Coordinate string like "A,1" or "H,8"
            
        Returns:
            Tuple of (row, col) indices or None if invalid
        """
        try:
            coord_str = coord_str.strip().upper()
            if ',' not in coord_str:
                return None
                
            parts = coord_str.split(',')
            if len(parts) != 2:
                return None
                
            col_char, row_str = parts[0].strip(), parts[1].strip()
            
            # Convert column letter to index (A=0, B=1, ..., O=14)
            if len(col_char) != 1 or not col_char.isalpha():
                return None
                
            col = ord(col_char) - ord('A')
            if col < 0 or col >= self.BOARD_SIZE:
                return None
                
            # Convert row number to index (1=0, 2=1, ..., 15=14)
            if not row_str.isdigit():
                return None
                
            row = int(row_str) - 1
            if row < 0 or row >= self.BOARD_SIZE:
                return None
                
            return (row, col)
            
        except (ValueError, IndexError):
            return None
            
    def is_valid_move(self, row: int, col: int) -> bool:
        """
        Check if a move is valid.
        
        Args:
            row: Row index (0-14)
            col: Column index (0-14)
            
        Returns:
            bool: True if move is valid, False otherwise
        """
        if self.game_status != GameStatus.ONGOING:
            return False
            
        if row < 0 or row >= self.BOARD_SIZE or col < 0 or col >= self.BOARD_SIZE:
            return False
            
        return self.board[row][col] == Player.EMPTY.value
        
    def make_move(self, row: int, col: int) -> bool:
        """
        Make a move on the board.
        
        Args:
            row: Row index (0-14)
            col: Column index (0-14)
            
        Returns:
            bool: True if move was successful, False otherwise
        """
        if not self.is_valid_move(row, col):
            return False
            
        # Place the stone
        self.board[row][col] = self.current_player.value
        self.last_move = (row, col)
        self.move_count += 1
        
        # Check for win
        if self.check_win(row, col):
            self.winner = self.current_player
            self.game_status = (GameStatus.BLACK_WINS if self.current_player == Player.BLACK 
                              else GameStatus.WHITE_WINS)
        elif self.move_count >= self.BOARD_SIZE * self.BOARD_SIZE:
            self.game_status = GameStatus.DRAW
        else:
            # Switch players
            self.current_player = (Player.WHITE if self.current_player == Player.BLACK 
                                 else Player.BLACK)
            
        return True
        
    def check_win(self, row: int, col: int) -> bool:
        """
        Check if the current player has won after placing a stone at (row, col).
        
        Args:
            row: Row index where the stone was placed
            col: Column index where the stone was placed
            
        Returns:
            bool: True if current player has won, False otherwise
        """
        player = self.current_player.value
        directions = [
            (0, 1),   # horizontal
            (1, 0),   # vertical
            (1, 1),   # diagonal \
            (1, -1)   # diagonal /
        ]
        
        for dr, dc in directions:
            count = 1  # Count the stone just placed
            
            # Count in positive direction
            r, c = row + dr, col + dc
            while (0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE and 
                   self.board[r][c] == player):
                count += 1
                r += dr
                c += dc
                
            # Count in negative direction
            r, c = row - dr, col - dc
            while (0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE and 
                   self.board[r][c] == player):
                count += 1
                r -= dr
                c -= dc
                
            # Check if we have 5 in a row
            if count >= 5:
                return True
                
        return False
        
    def get_board_display(self) -> str:
        """
        Get a text representation of the board.
        
        Returns:
            str: Text representation of the board
        """
        lines = []
        lines.append("   " + " ".join(chr(ord('A') + i) for i in range(self.BOARD_SIZE)))
        
        for i, row in enumerate(self.board):
            row_num = str(i + 1).rjust(2)
            row_display = []
            
            for cell in row:
                if cell == Player.BLACK.value:
                    row_display.append("●")
                elif cell == Player.WHITE.value:
                    row_display.append("○")
                else:
                    row_display.append("·")
                    
            lines.append(f"{row_num} " + " ".join(row_display))
            
        return "\n".join(lines)
        
    def get_status_message(self) -> str:
        """
        Get current game status message.
        
        Returns:
            str: Status message
        """
        if self.game_status == GameStatus.BLACK_WINS:
            return "Black wins!"
        elif self.game_status == GameStatus.WHITE_WINS:
            return "White wins!"
        elif self.game_status == GameStatus.DRAW:
            return "It's a draw!"
        else:
            current = "Black" if self.current_player == Player.BLACK else "White"
            return f"Current turn: {current} (Move #{self.move_count + 1})"