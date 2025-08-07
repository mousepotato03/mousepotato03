#!/usr/bin/env python3
"""
Utility script to update README.md with cache-busting URLs for SVG images.
This ensures that updated board.svg files are immediately visible in GitHub.
"""

import re
import sys
import time
from pathlib import Path


def update_readme_cache_busting():
    """
    Update README.md to include cache-busting parameter for SVG URLs.
    
    Returns:
        bool: True if update was successful, False otherwise
    """
    try:
        readme_path = Path('README.md')
        
        if not readme_path.exists():
            print("ERROR: README.md not found")
            return False
            
        # Generate timestamp for cache busting
        timestamp = int(time.time())
        print(f"Generated cache-busting timestamp: {timestamp}")
        
        # Read current content
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Define pattern to match SVG URL with or without existing cache-busting parameter
        pattern = r'https://raw\.githubusercontent\.com/mousepotato03/mousepotato03/main/board\.svg(\?v=[^)]*)?'
        replacement = f'https://raw.githubusercontent.com/mousepotato03/mousepotato03/main/board.svg?v={timestamp}'
        
        # Check if pattern exists
        if not re.search(pattern, content):
            print("ERROR: SVG URL pattern not found in README.md")
            return False
            
        # Replace the URL
        updated_content = re.sub(pattern, replacement, content)
        
        # Write back to file
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
            
        print(f"Successfully updated README.md with cache-busting parameter: v={timestamp}")
        return True
        
    except Exception as e:
        print(f"ERROR updating README.md: {e}")
        return False


def main():
    """Main entry point."""
    success = update_readme_cache_busting()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()