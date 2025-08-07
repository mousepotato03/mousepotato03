#!/usr/bin/env python3
"""
Updated README.md utility script using SVG base64 embedding.
Completely eliminates GitHub raw URL caching issues by embedding SVG directly.
"""

import base64
import json
import re
import os
import sys
from pathlib import Path


def read_svg_file(svg_path):
    """Read SVG file content"""
    try:
        with open(svg_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"ERROR: SVG file not found at {svg_path}")
        return None


def svg_to_base64(svg_content):
    """Convert SVG content to base64 data URI"""
    # Encode SVG content to base64
    svg_bytes = svg_content.encode('utf-8')
    base64_encoded = base64.b64encode(svg_bytes).decode('utf-8')
    
    # Create data URI
    data_uri = f"data:image/svg+xml;base64,{base64_encoded}"
    return data_uri


def get_current_game_info(game_state_path):
    """Get current game information for status display"""
    try:
        with open(game_state_path, 'r', encoding='utf-8') as file:
            game_state = json.load(file)
        
        move_count = game_state.get('move_count', 0)
        current_player = game_state.get('current_player', 'black')
        game_status = game_state.get('game_status', 'ongoing')
        winner = game_state.get('winner', None)
        
        if game_status == 'finished' and winner:
            status_text = f"Game Over - {winner.title()} Wins! (Total moves: {move_count})"
        else:
            next_move = move_count + 1
            status_text = f"Current turn: {current_player.title()} (Move #{next_move})"
            
        return status_text
    except Exception as e:
        print(f"Warning: Could not read game state: {e}")
        return "Current turn: Black (Move #1)"


def update_readme_with_embedded_svg():
    """
    Update README.md with embedded SVG using base64 encoding.
    This completely eliminates caching issues.
    
    Returns:
        bool: True if update was successful, False otherwise
    """
    try:
        # File paths
        svg_path = Path("board.svg")
        readme_path = Path("README.md")
        game_state_path = Path("game_state.json")
        
        # Check if files exist
        if not svg_path.exists():
            print(f"ERROR: {svg_path} not found!")
            return False
        
        if not readme_path.exists():
            print(f"ERROR: {readme_path} not found!")
            return False
        
        # Read SVG content
        svg_content = read_svg_file(svg_path)
        if not svg_content:
            return False
        
        # Convert to base64
        svg_data_uri = svg_to_base64(svg_content)
        print(f"[OK] SVG converted to base64 (length: {len(svg_data_uri)} characters)")
        
        # Get current game status
        game_status = get_current_game_info(game_state_path)
        
        # Read README content
        with open(readme_path, 'r', encoding='utf-8') as file:
            readme_content = file.read()
        
        # Create the new SVG img tag with embedded data
        new_svg_line = f'![Omok Game Board](data:image/svg+xml;base64,{svg_data_uri.split(",")[1]})'
        
        # Pattern to match existing SVG image line (both external URL and embedded versions)
        svg_patterns = [
            r'!\[Omok Game Board\]\(https://raw\.githubusercontent\.com/[^)]+\)',  # External URL
            r'!\[Omok Game Board\]\(data:image/svg\+xml;base64,[^)]+\)'  # Existing embedded
        ]
        
        # Try to replace existing SVG reference
        updated = False
        for pattern in svg_patterns:
            if re.search(pattern, readme_content):
                readme_content = re.sub(pattern, new_svg_line, readme_content)
                updated = True
                print("[OK] Successfully replaced existing SVG reference with embedded version")
                break
        
        if not updated:
            print("Warning: Could not find existing SVG reference pattern")
            return False
        
        # Write updated content back to file
        with open(readme_path, 'w', encoding='utf-8') as file:
            file.write(readme_content)
        
        print(f"[OK] README.md updated with embedded SVG")
        print(f"[OK] Game Status: {game_status}")
        print("[SUCCESS] SVG embedding completed - no more caching issues!")
        return True
        
    except Exception as e:
        print(f"ERROR updating README: {e}")
        return False


def main():
    """
    Main entry point for README update using SVG embedding.
    This replaces the old cache-busting method with a permanent solution.
    """
    print("=== README Update with SVG Embedding ===")
    print("Updating README.md with embedded SVG to eliminate caching issues...")
    
    success = update_readme_with_embedded_svg()
    
    if success:
        print("\n[COMPLETE] README.md has been updated with embedded SVG!")
        print("[INFO] The game board will now update immediately without any caching delays")
    else:
        print("\n[FAILED] Could not update README.md")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()