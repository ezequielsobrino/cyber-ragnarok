import pygame
from typing import List, Tuple
from games.renderers.base_renderer import BoardRenderer

class TicTacToeRenderer(BoardRenderer):
    """Renderer for Tic Tac Toe game with a minimal cyberpunk style"""
    
    # Cyberpunk neon colors
    BOARD_COLOR = (10, 10, 20)      # Dark background
    GRID_COLOR = (0, 255, 255)      # Cyan for grid lines
    X_COLOR = (255, 50, 150)        # Hot pink for X
    O_COLOR = (0, 255, 150)         # Neon green for O
    
    @property
    def rows(self) -> int:
        return 3
    
    @property
    def cols(self) -> int:
        return 3
    
    def __init__(self, width: int, height: int):
        self.scale = 0.7
        self.full_width = width
        self.full_height = height
        
        # Calculate the scaled dimensions
        self.scaled_width = int(width * self.scale)
        self.scaled_height = int(height * self.scale)
        
        # Calculate global screen offsets
        self.screen_offset_x = (width - self.scaled_width) // 2
        self.screen_offset_y = (height - self.scaled_height) // 2
        
        super().__init__(self.scaled_width, self.scaled_height)
    
    def draw_board(self, surface: pygame.Surface) -> None:
        """Draw the cyberpunk board"""
        # Calculate total offsets
        total_offset_x = self.screen_offset_x + self.offset_x
        total_offset_y = self.screen_offset_y + self.offset_y
        
        # Draw board background
        pygame.draw.rect(
            surface,
            self.BOARD_COLOR,
            (total_offset_x, total_offset_y, self.board_width, self.board_height)
        )
        
        # Draw grid lines with dotted effect
        dot_size = 2
        dot_spacing = 8
        
        for i in range(1, 3):
            # Vertical dotted lines
            for y in range(total_offset_y, total_offset_y + self.board_height, dot_spacing):
                pygame.draw.rect(
                    surface,
                    self.GRID_COLOR,
                    (total_offset_x + i * self.cell_size - dot_size//2, y, dot_size, dot_size)
                )
            
            # Horizontal dotted lines
            for x in range(total_offset_x, total_offset_x + self.board_width, dot_spacing):
                pygame.draw.rect(
                    surface,
                    self.GRID_COLOR,
                    (x, total_offset_y + i * self.cell_size - dot_size//2, dot_size, dot_size)
                )
    
    def draw_piece(self, surface: pygame.Surface, position: int, piece: str) -> None:
        """Draw X or O pieces with cyberpunk style"""
        if piece not in ['X', 'O'] or position >= len(self.cell_positions):
            return
            
        center_x, center_y = self.cell_positions[position]
        piece_size = int(min(self.board_width, self.board_height) * 0.20)
        padding = piece_size * 0.2
        half_size = piece_size // 2
        line_thickness = 3
        
        # Adjust for screen offset
        center_x += self.screen_offset_x
        center_y += self.screen_offset_y
        
        if piece == 'X':
            # Draw X centered at the cell's center
            start_x = center_x - half_size + padding
            start_y = center_y - half_size + padding
            end_x = center_x + half_size - padding
            end_y = center_y + half_size - padding
            
            # Diagonal lines for X
            pygame.draw.line(surface, self.X_COLOR, 
                           (start_x, start_y), 
                           (end_x, end_y), 
                           line_thickness)
            pygame.draw.line(surface, self.X_COLOR, 
                           (end_x, start_y), 
                           (start_x, end_y), 
                           line_thickness)
        else:  # O
            # Draw O as a diamond centered at the cell's center
            diamond_size = piece_size - padding * 2
            half_diamond = diamond_size // 2
            
            points = [
                (center_x, center_y - half_diamond),  # top
                (center_x + half_diamond, center_y),  # right
                (center_x, center_y + half_diamond),  # bottom
                (center_x - half_diamond, center_y)   # left
            ]
            
            pygame.draw.lines(surface, self.O_COLOR, True, points, line_thickness)

    def draw_winning_line(self, surface: pygame.Surface, winning_line: List[int], color: Tuple[int, int, int]) -> None:
        """Draw a line through the winning cells"""
        if winning_line and len(winning_line) >= 2:
            # Get center positions of start and end cells
            start_cell = self.cell_positions[winning_line[0]]
            end_cell = self.cell_positions[winning_line[-1]]
            
            # Adjust for screen offset
            start_x = start_cell[0] + self.screen_offset_x
            start_y = start_cell[1] + self.screen_offset_y
            end_x = end_cell[0] + self.screen_offset_x
            end_y = end_cell[1] + self.screen_offset_y
            
            pygame.draw.line(surface, color, (start_x, start_y), (end_x, end_y), 5)