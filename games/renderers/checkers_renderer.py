import pygame

from games.renderers.base_renderer import BoardRenderer


class CheckersRenderer(BoardRenderer):
    # Colors
    LIGHT_SQUARE = (255, 206, 158)  # Light brown
    DARK_SQUARE = (209, 139, 71)    # Dark brown
    BLACK_PIECE = (40, 40, 40)      # Dark gray
    WHITE_PIECE = (215, 215, 215)   # Light gray
    HIGHLIGHT_COLOR = (124, 252, 0)  # LawnGreen
    CROWN_COLOR = (255, 215, 0)     # Gold
    POSSIBLE_MOVE = (144, 238, 144) # Light green
    
    @property
    def rows(self) -> int:
        return 8
    
    @property
    def cols(self) -> int:
        return 8
    
    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        self.selected_piece = None
        self.possible_moves = []
    
    def draw_board(self, surface: pygame.Surface) -> None:
        # Draw board background
        for row in range(self.rows):
            for col in range(self.cols):
                x = self.offset_x + col * self.cell_size
                y = self.offset_y + row * self.cell_size
                color = self.LIGHT_SQUARE if (row + col) % 2 == 0 else self.DARK_SQUARE
                
                # Draw square
                pygame.draw.rect(
                    surface,
                    color,
                    (x, y, self.cell_size, self.cell_size)
                )
                
                # Highlight selected piece
                if self.selected_piece == (row, col):
                    pygame.draw.rect(
                        surface,
                        self.HIGHLIGHT_COLOR,
                        (x, y, self.cell_size, self.cell_size),
                        3
                    )
                
                # Show possible moves
                if (row, col) in self.possible_moves:
                    radius = self.cell_size // 6
                    pygame.draw.circle(
                        surface,
                        self.POSSIBLE_MOVE,
                        (x + self.cell_size // 2, y + self.cell_size // 2),
                        radius
                    )
    
    def draw_piece(self, surface: pygame.Surface, position: int, piece: str) -> None:
        if not piece:
            return
            
        row = position // 8
        col = position % 8
        x = self.offset_x + col * self.cell_size
        y = self.offset_y + row * self.cell_size
        
        # Calculate piece dimensions
        padding = self.cell_size * 0.15
        radius = (self.cell_size - padding * 2) // 2
        center_x = x + self.cell_size // 2
        center_y = y + self.cell_size // 2
        
        piece_color = self.BLACK_PIECE if piece.lower() == 'b' else self.WHITE_PIECE
        highlight_color = (80, 80, 80) if piece.lower() == 'b' else (255, 255, 255)
        
        # Draw main piece circle
        pygame.draw.circle(
            surface,
            piece_color,
            (center_x, center_y),
            radius
        )
        
        # Add highlight effect
        pygame.draw.circle(
            surface,
            highlight_color,
            (center_x - radius//3, center_y - radius//3),
            radius//3
        )
        
        # Draw crown for kings (uppercase pieces)
        if piece.isupper():
            crown_points = [
                (center_x - radius//2, center_y + radius//4),
                (center_x - radius//4, center_y - radius//4),
                (center_x, center_y + radius//4),
                (center_x + radius//4, center_y - radius//4),
                (center_x + radius//2, center_y + radius//4)
            ]
            pygame.draw.lines(
                surface,
                self.CROWN_COLOR,
                False,
                crown_points,
                3
            )
    
    def set_selected(self, row: int, col: int) -> None:
        """Set the currently selected piece"""
        self.selected_piece = (row, col)
    
    def clear_selected(self) -> None:
        """Clear the currently selected piece"""
        self.selected_piece = None
    
    def set_possible_moves(self, moves: List[Tuple[int, int]]) -> None:
        """Set the possible moves for the currently selected piece"""
        self.possible_moves = moves
    
    def clear_possible_moves(self) -> None:
        """Clear the possible moves"""
        self.possible_moves = []

    def get_board_position(self, screen_pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """Convert screen coordinates to board position"""
        x, y = screen_pos
        # Adjust for board offset
        x -= self.offset_x
        y -= self.offset_y
        
        if 0 <= x < self.board_width and 0 <= y < self.board_height:
            col = x // self.cell_size
            row = y // self.cell_size
            return (row, col)
        return None