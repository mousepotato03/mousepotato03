#!/usr/bin/env python3
"""
Main game logic handler for the GitHub Actions Omok game.
Processes moves from GitHub issues and manages the game flow.
"""

import sys
import argparse
import re
from typing import Optional
from game_state import GameState, GameStatus
from update_readme_text import update_readme_with_text_board


class OmokGameHandler:
    """Main handler for Omok game operations."""
    
    def __init__(self):
        """Initialize the game handler."""
        self.game_state = GameState()
        
    def reset_game(self) -> bool:
        """
        Reset the game to initial state.
        
        Returns:
            bool: True if reset was successful, False otherwise
        """
        try:
            print("Resetting game...")
            self.game_state.reset_game()
            
            if not self.game_state.save_state():
                print("Failed to save reset state")
                return False
                
            if not update_readme_with_text_board():
                print("Failed to update README with text board after reset")
                return False
                
            print("Game reset successfully!")
            print(f"Status: {self.game_state.get_status_message()}")
            return True
            
        except Exception as e:
            print(f"Error resetting game: {e}")
            return False
            
    def process_move(self, issue_title: str, issue_number: Optional[int] = None) -> bool:
        """
        Process a move from GitHub issue title.
        
        Args:
            issue_title: Title of the GitHub issue
            issue_number: Issue number for reference
            
        Returns:
            bool: True if move was processed successfully, False otherwise
        """
        try:
            print(f"Processing move from issue: '{issue_title}'")
            if issue_number:
                print(f"Issue number: {issue_number}")
                
            # Load current game state
            if not self.game_state.load_state():
                print("Failed to load game state")
                return False
                
            # Check if game is already finished
            if self.game_state.game_status != GameStatus.ONGOING:
                print(f"Game is already finished: {self.game_state.get_status_message()}")
                print("Use workflow dispatch with reset=true to start a new game")
                return False
                
            # Parse coordinates from issue title
            coords = self._parse_move_from_title(issue_title)
            if not coords:
                print("Invalid move format. Expected format: 'A,1', 'A 1', 'A1', or 'Play at A,1'")
                print("Valid coordinates: A-O (columns), 1-15 (rows)")
                return False
                
            row, col = coords
            coord_str = f"{chr(ord('A') + col)},{row + 1}"
            print(f"Parsed coordinates: {coord_str} (row={row}, col={col})")
            
            # Validate and make the move
            if not self.game_state.is_valid_move(row, col):
                if self.game_state.board[row][col] != "empty":
                    print(f"Position {coord_str} is already occupied!")
                else:
                    print(f"Invalid move at {coord_str}")
                return False
                
            # Make the move
            current_player = self.game_state.current_player.value
            if not self.game_state.make_move(row, col):
                print(f"Failed to make move at {coord_str}")
                return False
                
            print(f"Move successful! {current_player.title()} stone placed at {coord_str}")
            
            # Save updated state
            if not self.game_state.save_state():
                print("Failed to save game state")
                return False
                
            # Update README with text board
            if not update_readme_with_text_board():
                print("Failed to update README with text board")
                return False
                
            # Print game status
            print(f"Status: {self.game_state.get_status_message()}")
            
            # Check for game end
            if self.game_state.game_status != GameStatus.ONGOING:
                if self.game_state.winner:
                    print(f"{self.game_state.winner.value.title()} wins the game!")
                else:
                    print("Game ended in a draw!")
                print("Use workflow dispatch with reset=true to start a new game")
            else:
                next_player = self.game_state.current_player.value
                print(f"Next turn: {next_player.title()}")
                
            return True
            
        except Exception as e:
            print(f"Error processing move: {e}")
            return False
            
    def _parse_move_from_title(self, title: str) -> Optional[tuple]:
        """
        Parse move coordinates from issue title.
        
        Args:
            title: Issue title string
            
        Returns:
            Tuple of (row, col) or None if parsing failed
        """
        # Remove common prefixes and clean the title
        title = title.strip()
        
        # Try different patterns to extract coordinates (prioritize simple formats)
        patterns = [
            r'([A-O]),\s*(\d+)',              # "A,1" (simple comma format)
            r'([A-O])\s+(\d+)',               # "A 1" (space format)
            r'([A-O])(\d+)',                  # "A1" (no separator)
            r'play\s+at\s+([A-O]),\s*(\d+)',  # "Play at A,1"
            r'move\s+([A-O]),\s*(\d+)',       # "Move A,1"
            r'place\s+([A-O]),\s*(\d+)',      # "Place A,1"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, title, re.IGNORECASE)
            if match:
                col_char = match.group(1).upper()
                row_str = match.group(2)
                
                coord_str = f"{col_char},{row_str}"
                return self.game_state.parse_coordinate(coord_str)
                
        return None
        
    def show_status(self) -> bool:
        """
        Show current game status.
        
        Returns:
            bool: True if status was shown successfully, False otherwise
        """
        try:
            if not self.game_state.load_state():
                print("Failed to load game state")
                return False
                
            print("Current Game Status:")
            print(f"Status: {self.game_state.get_status_message()}")
            print(f"Moves played: {self.game_state.move_count}")
            
            if self.game_state.last_move:
                row, col = self.game_state.last_move
                coord_str = f"{chr(ord('A') + col)},{row + 1}"
                print(f"Last move: {coord_str}")
                
            print("\nBoard:")
            print(self.game_state.get_board_display())
            
            return True
            
        except Exception as e:
            print(f"Error showing status: {e}")
            return False


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description='Omok Game Handler')
    parser.add_argument('--reset', action='store_true', 
                       help='Reset the game to initial state')
    parser.add_argument('--move', type=str, 
                       help='Process a move from issue title')
    parser.add_argument('--issue-number', type=int, 
                       help='GitHub issue number for reference')
    parser.add_argument('--status', action='store_true', 
                       help='Show current game status')
    
    args = parser.parse_args()
    
    # Create game handler
    handler = OmokGameHandler()
    
    success = False
    
    if args.reset:
        success = handler.reset_game()
    elif args.move:
        success = handler.process_move(args.move, args.issue_number)
    elif args.status:
        success = handler.show_status()
    else:
        # Default: show status
        success = handler.show_status()
        
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()