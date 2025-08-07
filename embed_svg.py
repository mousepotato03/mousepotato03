#!/usr/bin/env python3
"""
SVG Base64 Embedding Script for Omok Game
Converts SVG to base64 and embeds directly in README to eliminate GitHub raw URL caching issues
"""

import base64
import json
import re
import os

def read_svg_file(svg_path):
    """Read SVG file content"""
    try:
        with open(svg_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: SVG file not found at {svg_path}")
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
        print(f"Error reading game state: {e}")
        return "Current turn: Black (Move #1)"

def update_readme_with_embedded_svg(readme_path, svg_data_uri, game_status):
    """Update README.md with embedded SVG and game status"""
    try:
        with open(readme_path, 'r', encoding='utf-8') as file:
            readme_content = file.read()
        
        # Create the new SVG img tag with embedded data
        new_svg_line = f'![Omok Game Board](data:image/svg+xml;base64,{svg_data_uri.split(",")[1]})'
        
        # Pattern to match the existing SVG image line
        svg_pattern = r'!\[Omok Game Board\]\([^)]+\)'
        
        # Replace the existing SVG reference
        if re.search(svg_pattern, readme_content):
            updated_content = re.sub(svg_pattern, new_svg_line, readme_content)
            print("[OK] Successfully replaced existing SVG reference with embedded version")
        else:
            print("Warning: Could not find existing SVG reference pattern")
            return False
        
        # Write updated content back to file
        with open(readme_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)
        
        print(f"[OK] README.md updated with embedded SVG")
        print(f"[OK] Game Status: {game_status}")
        return True
        
    except Exception as e:
        print(f"Error updating README: {e}")
        return False

def main():
    # File paths
    svg_path = "board.svg"
    readme_path = "README.md"
    game_state_path = "game_state.json"
    
    print("=== Omok Game SVG Embedding Tool ===")
    print("Converting SVG to embedded base64 format...")
    
    # Check if files exist
    if not os.path.exists(svg_path):
        print(f"Error: {svg_path} not found!")
        return False
    
    if not os.path.exists(readme_path):
        print(f"Error: {readme_path} not found!")
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
    
    # Update README
    success = update_readme_with_embedded_svg(readme_path, svg_data_uri, game_status)
    
    if success:
        print("\n[SUCCESS] SVG embedding completed!")
        print("[INFO] The README.md now displays the game board without any external URL dependencies")
        print("[INFO] This completely eliminates GitHub raw URL caching issues")
        return True
    else:
        print("\n[FAILED] Could not complete SVG embedding")
        return False

if __name__ == "__main__":
    main()