#!/usr/bin/env python3
"""
Text-based board generator for the Omok game.
Generates ASCII/Unicode representation of the game board.
"""

from typing import Optional, Tuple, List
from game_state import GameState, Player


class TextBoardGenerator:
    """Generates text-based representation of the Omok board."""
    
    # Simple ASCII characters for better compatibility
    HORIZONTAL_LINE = "-"
    VERTICAL_LINE = "|"
    TOP_LEFT = "+"
    TOP_RIGHT = "+"
    BOTTOM_LEFT = "+"
    BOTTOM_RIGHT = "+"
    CROSS = "+"
    T_DOWN = "+"
    T_UP = "+"
    T_RIGHT = "+"
    T_LEFT = "+"
    
    # Game pieces
    BLACK_STONE = "●"
    WHITE_STONE = "○"
    EMPTY_SPOT = "·"
    LAST_MOVE_MARKER = "🔴"  # For marking the last move
    
    def __init__(self, game_state: Optional[GameState] = None):
        """
        Initialize the text board generator.
        
        Args:
            game_state: Optional GameState object. If None, creates a new one.
        """
        self.game_state = game_state or GameState()
        
    def generate_board_text(self) -> str:
        """
        Generate the complete text representation of the board.
        
        Returns:
            str: Complete board text with coordinates and status
        """
        if not self.game_state.load_state():
            return "Error: Could not load game state"
            
        lines = []
        
        # Add column headers (A-O) with proper spacing
        header_chars = []
        for i in range(GameState.BOARD_SIZE):
            header_chars.append(f" {chr(ord('A') + i)} ")
        header = "   " + "".join(header_chars)
        lines.append(header)
        
        # Add board rows with content
        for row_idx in range(GameState.BOARD_SIZE):
            row_num = str(row_idx + 1).rjust(2)
            row_display = []
            
            for col_idx in range(GameState.BOARD_SIZE):
                cell_content = self._get_cell_content(row_idx, col_idx)
                row_display.append(cell_content)
                
            row_line = f"{row_num} " + "".join(row_display)
            lines.append(row_line)
        
        return "\n".join(lines)
        
    def _get_cell_content(self, row: int, col: int) -> str:
        """
        Get the content for a specific cell.
        
        Args:
            row: Row index (0-14)
            col: Column index (0-14)
            
        Returns:
            str: Character representing the cell content
        """
        cell_value = self.game_state.board[row][col]
        
        # Check if this is the last move position
        is_last_move = (self.game_state.last_move and 
                       self.game_state.last_move[0] == row and 
                       self.game_state.last_move[1] == col)
        
        if cell_value == Player.BLACK.value:
            return "[●]" if is_last_move else " ● "
        elif cell_value == Player.WHITE.value:
            return "[○]" if is_last_move else " ○ "
        else:
            return " · "
            
    def generate_status_message(self) -> str:
        """
        Generate the current game status message.
        
        Returns:
            str: Formatted status message
        """
        if not self.game_state.load_state():
            return "Error: Could not load game state"
            
        status_lines = []
        
        # Game status
        status_lines.append(f"**Game Status:** {self.game_state.get_status_message()}")
        
        # Move count
        status_lines.append(f"**Moves played:** {self.game_state.move_count}")
        
        # Last move
        if self.game_state.last_move:
            row, col = self.game_state.last_move
            coord_str = f"{chr(ord('A') + col)},{row + 1}"
            last_player = "Black" if self.game_state.move_count % 2 == 1 else "White"
            status_lines.append(f"**Last move:** {last_player} at {coord_str}")
        
        # Game result or next turn
        if self.game_state.winner:
            status_lines.append(f"**Winner:** {self.game_state.winner.value.title()}")
        elif self.game_state.move_count >= GameState.BOARD_SIZE * GameState.BOARD_SIZE:
            status_lines.append("**Result:** Draw - Board is full")
        else:
            next_player = "Black" if self.game_state.current_player == Player.BLACK else "White"
            status_lines.append(f"**Next turn:** {next_player}")
        
        return "\n".join(status_lines)
        
    def generate_complete_display(self) -> str:
        """
        Generate the complete display including board and status.
        
        Returns:
            str: Complete formatted display
        """
        board_text = self.generate_board_text()
        status_text = self.generate_status_message()
        
        return f"```\n{board_text}\n```\n\n{status_text}"


if __name__ == "__main__":
    # Test the generator
    generator = TextBoardGenerator()
    print("\nGenerated board:")
    print(generator.generate_complete_display())