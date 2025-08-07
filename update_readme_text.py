#!/usr/bin/env python3
"""
Update README.md with text-based board representation.
Replaces the SVG board section with Unicode/ASCII text board.
"""

import os
from typing import List, Optional
from generate_text_board import TextBoardGenerator


class ReadmeUpdater:
    """Updates README.md with current game board in text format."""
    
    README_FILE = "README.md"
    BOARD_START_MARKER = "### Current Game State"
    BOARD_END_MARKER = "### 📋 How to Play"
    
    def __init__(self):
        """Initialize the README updater."""
        self.generator = TextBoardGenerator()
        
    def update_readme(self) -> bool:
        """
        Update the README.md file with current game state.
        
        Returns:
            bool: True if update was successful, False otherwise
        """
        try:
            # Read current README content
            readme_content = self._read_readme()
            if readme_content is None:
                return False
                
            # Generate new board content
            new_board_content = self._generate_board_section()
            
            # Replace the board section
            updated_content = self._replace_board_section(readme_content, new_board_content)
            
            # Write back to file
            return self._write_readme(updated_content)
            
        except Exception as e:
            print(f"Error updating README: {e}")
            return False
            
    def _read_readme(self) -> Optional[List[str]]:
        """
        Read README.md file content.
        
        Returns:
            List of lines or None if error
        """
        try:
            if not os.path.exists(self.README_FILE):
                print(f"README file not found: {self.README_FILE}")
                return None
                
            with open(self.README_FILE, 'r', encoding='utf-8') as f:
                return f.readlines()
                
        except Exception as e:
            print(f"Error reading README: {e}")
            return None
            
    def _write_readme(self, content: List[str]) -> bool:
        """
        Write content back to README.md file.
        
        Args:
            content: List of lines to write
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(self.README_FILE, 'w', encoding='utf-8') as f:
                f.writelines(content)
            return True
            
        except Exception as e:
            print(f"Error writing README: {e}")
            return False
            
    def _generate_board_section(self) -> str:
        """
        Generate the new board section content.
        
        Returns:
            str: New board section with text representation
        """
        # Load current game state
        if not self.generator.game_state.load_state():
            return "Error: Could not load game state\n"
            
        board_text = self.generator.generate_board_text()
        status_text = self.generator.generate_status_message()
        
        # Create the complete section
        section_lines = [
            "### Current Game State\n",
            "\n",
            "```\n",
            f"{board_text}\n",
            "```\n",
            "\n",
            f"{status_text}\n",
            "\n"
        ]
        
        return "".join(section_lines)
        
    def _replace_board_section(self, content: List[str], new_section: str) -> List[str]:
        """
        Replace the board section in README content.
        
        Args:
            content: Current README content lines
            new_section: New board section to insert
            
        Returns:
            List of updated content lines
        """
        start_idx = None
        end_idx = None
        
        # Find the start and end markers
        for i, line in enumerate(content):
            if self.BOARD_START_MARKER in line:
                start_idx = i
            elif self.BOARD_END_MARKER in line and start_idx is not None:
                end_idx = i
                break
                
        if start_idx is None:
            print(f"Could not find start marker: {self.BOARD_START_MARKER}")
            return content
            
        if end_idx is None:
            print(f"Could not find end marker: {self.BOARD_END_MARKER}")
            return content
            
        # Replace the section
        updated_content = content[:start_idx]
        updated_content.extend(new_section.splitlines(keepends=True))
        updated_content.extend(content[end_idx:])
        
        return updated_content
        
    def preview_changes(self) -> str:
        """
        Preview what the new board section will look like.
        
        Returns:
            str: Preview of the new board section
        """
        try:
            return self._generate_board_section()
        except Exception as e:
            return f"Error generating preview: {e}"


def update_readme_with_text_board() -> bool:
    """
    Update README.md with current text-based board.
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        updater = ReadmeUpdater()
        
        print("Updating README.md with text board...")
        success = updater.update_readme()
        
        if success:
            print("README.md updated successfully!")
        else:
            print("Failed to update README.md")
            
        return success
        
    except Exception as e:
        print(f"Error in update process: {e}")
        return False


if __name__ == "__main__":
    # Test the updater
    updater = ReadmeUpdater()
    
    print("Preview of new board section:")
    print("=" * 50)
    print(updater.preview_changes())
    print("=" * 50)
    
    # Actually update the README
    success = update_readme_with_text_board()
    
    if not success:
        exit(1)