import pygame
from typing import List, Tuple
from games.renderers.base_renderer import BoardRenderer

class TicTacToeRenderer(BoardRenderer):
    """Renderer for Tic Tac Toe game with a minimal cyberpunk style"""
    
    # Updated colors to match character borders
    BOARD_COLOR = (10, 10, 20)      # Dark background
    GRID_COLOR = (0, 255, 255)      # Cyan for grid lines
    X_COLOR = (0, 255, 255)         # NEON_BLUE for X
    O_COLOR = (255, 20, 100)        # NEON_RED for O
    
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
        
        self.scaled_width = int(width * self.scale)
        self.scaled_height = int(height * self.scale)
        
        self.screen_offset_x = (width - self.scaled_width) // 2
        self.screen_offset_y = (height - self.scaled_height) // 2
        
        super().__init__(self.scaled_width, self.scaled_height)
    
    def draw_board(self, surface: pygame.Surface) -> None:
        """Draw the board with simple grid lines"""
        total_offset_x = self.screen_offset_x + self.offset_x
        total_offset_y = self.screen_offset_y + self.offset_y
        
        # Draw board background
        pygame.draw.rect(
            surface,
            self.BOARD_COLOR,
            (total_offset_x, total_offset_y, self.board_width, self.board_height)
        )
        
        # Draw solid grid lines
        for i in range(1, 3):
            # Vertical lines
            pygame.draw.line(
                surface,
                self.GRID_COLOR,
                (total_offset_x + i * self.cell_size, total_offset_y),
                (total_offset_x + i * self.cell_size, total_offset_y + self.board_height),
                2
            )
            
            # Horizontal lines
            pygame.draw.line(
                surface,
                self.GRID_COLOR,
                (total_offset_x, total_offset_y + i * self.cell_size),
                (total_offset_x + self.board_width, total_offset_y + i * self.cell_size),
                2
            )
    
    def draw_piece(self, surface: pygame.Surface, position: int, piece: str) -> None:
        """Draw X or O pieces with simple clean lines"""
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
            # Simple X with straight lines
            start_x = center_x - half_size + padding
            start_y = center_y - half_size + padding
            end_x = center_x + half_size - padding
            end_y = center_y + half_size - padding
            
            pygame.draw.line(surface, self.X_COLOR, 
                           (start_x, start_y), 
                           (end_x, end_y), 
                           line_thickness)
            pygame.draw.line(surface, self.X_COLOR, 
                           (end_x, start_y), 
                           (start_x, end_y), 
                           line_thickness)
        else:  # O
            # Simple circle instead of diamond
            radius = half_size - padding
            pygame.draw.circle(surface, self.O_COLOR, 
                             (center_x, center_y), 
                             radius, 
                             line_thickness)

    def draw_winning_line(self, surface: pygame.Surface, winning_line: List[int], color: Tuple[int, int, int]) -> None:
        """Draw a simple line through the winning cells"""
        if winning_line and len(winning_line) >= 2:
            start_cell = self.cell_positions[winning_line[0]]
            end_cell = self.cell_positions[winning_line[-1]]
            
            start_x = start_cell[0] + self.screen_offset_x
            start_y = start_cell[1] + self.screen_offset_y
            end_x = end_cell[0] + self.screen_offset_x
            end_y = end_cell[1] + self.screen_offset_y
            
            pygame.draw.line(surface, color, (start_x, start_y), (end_x, end_y), 4)