"""
SVG board generator for the Omok game.
Creates an interactive SVG representation of the game board.
"""

from typing import Optional, Tuple
from game_state import GameState, Player


class SVGBoardGenerator:
    """Generates SVG representation of the Omok board."""
    
    def __init__(self):
        """Initialize the SVG generator."""
        self.board_size = GameState.BOARD_SIZE
        self.cell_size = 30
        self.margin = 40
        self.board_width = (self.board_size - 1) * self.cell_size
        self.board_height = (self.board_size - 1) * self.cell_size
        self.svg_width = self.board_width + 2 * self.margin
        self.svg_height = self.board_height + 2 * self.margin + 60  # Extra space for status
        
    def generate_board_svg(self, game_state: GameState) -> str:
        """
        Generate SVG representation of the game board.
        
        Args:
            game_state: Current game state
            
        Returns:
            str: SVG content
        """
        svg_parts = []
        
        # SVG header
        svg_parts.append(f'''<svg width="{self.svg_width}" height="{self.svg_height}" 
                           xmlns="http://www.w3.org/2000/svg">''')
        
        # Background
        svg_parts.append(f'''<rect width="{self.svg_width}" height="{self.svg_height}" 
                           fill="#f5f5dc" stroke="none"/>''')
        
        # Board background
        board_x = self.margin
        board_y = self.margin
        svg_parts.append(f'''<rect x="{board_x - 10}" y="{board_y - 10}" 
                           width="{self.board_width + 20}" height="{self.board_height + 20}" 
                           fill="#daa520" stroke="#8b4513" stroke-width="2"/>''')
        
        # Grid lines
        self._add_grid_lines(svg_parts, board_x, board_y)
        
        # Star points (traditional Omok board markings)
        self._add_star_points(svg_parts, board_x, board_y)
        
        # Column and row labels
        self._add_labels(svg_parts, board_x, board_y)
        
        # Stones
        self._add_stones(svg_parts, board_x, board_y, game_state)
        
        # Last move indicator
        if game_state.last_move:
            self._add_last_move_indicator(svg_parts, board_x, board_y, game_state.last_move)
        
        # Game status
        self._add_game_status(svg_parts, game_state)
        
        # SVG footer
        svg_parts.append('</svg>')
        
        return '\n'.join(svg_parts)
        
    def _add_grid_lines(self, svg_parts: list, board_x: int, board_y: int) -> None:
        """Add grid lines to the SVG."""
        # Vertical lines
        for i in range(self.board_size):
            x = board_x + i * self.cell_size
            svg_parts.append(f'''<line x1="{x}" y1="{board_y}" 
                               x2="{x}" y2="{board_y + self.board_height}" 
                               stroke="#8b4513" stroke-width="1"/>''')
        
        # Horizontal lines
        for i in range(self.board_size):
            y = board_y + i * self.cell_size
            svg_parts.append(f'''<line x1="{board_x}" y1="{y}" 
                               x2="{board_x + self.board_width}" y2="{y}" 
                               stroke="#8b4513" stroke-width="1"/>''')
    
    def _add_star_points(self, svg_parts: list, board_x: int, board_y: int) -> None:
        """Add star points (traditional board markings) to the SVG."""
        # Star points at positions (3,3), (3,11), (7,7), (11,3), (11,11)
        star_positions = [(3, 3), (3, 11), (7, 7), (11, 3), (11, 11)]
        
        for row, col in star_positions:
            x = board_x + col * self.cell_size
            y = board_y + row * self.cell_size
            svg_parts.append(f'''<circle cx="{x}" cy="{y}" r="3" 
                               fill="#8b4513"/>''')
    
    def _add_labels(self, svg_parts: list, board_x: int, board_y: int) -> None:
        """Add column and row labels to the SVG."""
        # Column labels (A-O)
        for i in range(self.board_size):
            x = board_x + i * self.cell_size
            y = board_y - 15
            letter = chr(ord('A') + i)
            svg_parts.append(f'''<text x="{x}" y="{y}" text-anchor="middle" 
                               font-family="Arial, sans-serif" font-size="12" 
                               font-weight="bold" fill="#8b4513">{letter}</text>''')
        
        # Row labels (1-15)
        for i in range(self.board_size):
            x = board_x - 15
            y = board_y + i * self.cell_size + 5
            number = str(i + 1)
            svg_parts.append(f'''<text x="{x}" y="{y}" text-anchor="middle" 
                               font-family="Arial, sans-serif" font-size="12" 
                               font-weight="bold" fill="#8b4513">{number}</text>''')
    
    def _add_stones(self, svg_parts: list, board_x: int, board_y: int, 
                   game_state: GameState) -> None:
        """Add stones to the SVG."""
        stone_radius = 12
        
        for row in range(self.board_size):
            for col in range(self.board_size):
                cell_value = game_state.board[row][col]
                if cell_value == Player.EMPTY.value:
                    continue
                    
                x = board_x + col * self.cell_size
                y = board_y + row * self.cell_size
                
                if cell_value == Player.BLACK.value:
                    # Black stone with gradient
                    svg_parts.extend([
                        f'''<defs>
                            <radialGradient id="blackGradient_{row}_{col}" 
                                          cx="0.3" cy="0.3" r="0.7">
                                <stop offset="0%" stop-color="#444444"/>
                                <stop offset="100%" stop-color="#000000"/>
                            </radialGradient>
                        </defs>''',
                        f'''<circle cx="{x}" cy="{y}" r="{stone_radius}" 
                           fill="url(#blackGradient_{row}_{col})" 
                           stroke="#000000" stroke-width="1"/>'''
                    ])
                else:  # White stone
                    # White stone with gradient
                    svg_parts.extend([
                        f'''<defs>
                            <radialGradient id="whiteGradient_{row}_{col}" 
                                          cx="0.3" cy="0.3" r="0.7">
                                <stop offset="0%" stop-color="#ffffff"/>
                                <stop offset="100%" stop-color="#e0e0e0"/>
                            </radialGradient>
                        </defs>''',
                        f'''<circle cx="{x}" cy="{y}" r="{stone_radius}" 
                           fill="url(#whiteGradient_{row}_{col})" 
                           stroke="#000000" stroke-width="1"/>'''
                    ])
    
    def _add_last_move_indicator(self, svg_parts: list, board_x: int, board_y: int, 
                                last_move: Tuple[int, int]) -> None:
        """Add indicator for the last move."""
        row, col = last_move
        x = board_x + col * self.cell_size
        y = board_y + row * self.cell_size
        
        # Red circle around the last move
        svg_parts.append(f'''<circle cx="{x}" cy="{y}" r="16" 
                           fill="none" stroke="#ff0000" stroke-width="2" 
                           opacity="0.8"/>''')
    
    def _add_game_status(self, svg_parts: list, game_state: GameState) -> None:
        """Add game status text to the SVG."""
        status_y = self.svg_height - 30
        center_x = self.svg_width // 2
        
        # Status background
        svg_parts.append(f'''<rect x="10" y="{status_y - 20}" 
                           width="{self.svg_width - 20}" height="40" 
                           fill="#ffffff" stroke="#cccccc" stroke-width="1" 
                           rx="5"/>''')
        
        # Status text
        status_text = game_state.get_status_message()
        svg_parts.append(f'''<text x="{center_x}" y="{status_y}" text-anchor="middle" 
                           font-family="Arial, sans-serif" font-size="16" 
                           font-weight="bold" fill="#333333">{status_text}</text>''')


def generate_svg_file(output_file: str = "board.svg") -> bool:
    """
    Generate SVG file for the current game state.
    
    Args:
        output_file: Output SVG file path
        
    Returns:
        bool: True if generation was successful, False otherwise
    """
    try:
        # Load current game state
        game_state = GameState()
        game_state.load_state()
        
        # Generate SVG
        generator = SVGBoardGenerator()
        svg_content = generator.generate_board_svg(game_state)
        
        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(svg_content)
            
        print(f"SVG board generated: {output_file}")
        return True
        
    except Exception as e:
        print(f"Error generating SVG: {e}")
        return False


if __name__ == "__main__":
    generate_svg_file()