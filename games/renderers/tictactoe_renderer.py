import pygame

from games.renderers.base_renderer import BoardRenderer


class TicTacToeRenderer(BoardRenderer):
    """Renderer for Tic Tac Toe game"""
    
    BOARD_COLOR = (222, 184, 135)  # Beige
    GRID_COLOR = (169, 169, 169)   # Dark Gray
    X_COLOR = (76, 153, 0)         # Green
    O_COLOR = (0, 105, 148)        # Blue
    
    @property
    def rows(self) -> int:
        return 3
    
    @property
    def cols(self) -> int:
        return 3
    
    def draw_board(self, surface: pygame.Surface) -> None:
        """Draw the Tic Tac Toe board"""
        # Draw board background
        pygame.draw.rect(
            surface,
            self.BOARD_COLOR,
            (self.offset_x, self.offset_y, self.board_width, self.board_height)
        )
        
        # Draw grid lines
        for i in range(1, 3):
            # Vertical lines
            pygame.draw.line(
                surface,
                self.GRID_COLOR,
                (self.offset_x + i * self.cell_size, self.offset_y),
                (self.offset_x + i * self.cell_size, self.offset_y + self.board_height),
                3
            )
            # Horizontal lines
            pygame.draw.line(
                surface,
                self.GRID_COLOR,
                (self.offset_x, self.offset_y + i * self.cell_size),
                (self.offset_x + self.board_width, self.offset_y + i * self.cell_size),
                3
            )
    
    def draw_piece(self, surface: pygame.Surface, position: int, piece: str) -> None:
        """Draw an X or O piece on the board"""
        if piece not in ['X', 'O'] or position >= len(self.cell_positions):
            return
            
        x, y = self.cell_positions[position]
        piece_size = int(min(self.board_width, self.board_height) * 0.25)
        padding = piece_size * 0.2
        
        if piece == 'X':
            # Draw X
            pygame.draw.line(
                surface,
                self.X_COLOR,
                (x + padding, y + padding),
                (x + piece_size - padding, y + piece_size - padding),
                4
            )
            pygame.draw.line(
                surface,
                self.X_COLOR,
                (x + piece_size - padding, y + padding),
                (x + padding, y + piece_size - padding),
                4
            )
        else:  # O
            # Draw O
            pygame.draw.circle(
                surface,
                self.O_COLOR,
                (x + piece_size // 2, y + piece_size // 2),
                (piece_size - padding * 2) // 2,
                4
            )