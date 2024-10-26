from abc import ABC, abstractmethod
import pygame
from typing import Tuple, List, Optional

class BoardRenderer(ABC):
    """Base class for board game renderers"""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.cell_size = min(width // self.cols, height // self.rows)
        self.board_width = self.cell_size * self.cols
        self.board_height = self.cell_size * self.rows
        # Calculate offset to center the board
        self.offset_x = (width - self.board_width) // 2
        self.offset_y = (height - self.board_height) // 2
        # Store cell positions for game logic
        self.cell_positions = self._calculate_cell_positions()
    
    def _calculate_cell_positions(self) -> List[Tuple[int, int]]:
        """Calculate the position of each cell's center"""
        positions = []
        piece_size = int(min(self.board_width, self.board_height) * 0.25)
        for row in range(self.rows):
            for col in range(self.cols):
                x = self.offset_x + col * self.cell_size + self.cell_size // 2 - piece_size // 2
                y = self.offset_y + row * self.cell_size + self.cell_size // 2 - piece_size // 2
                positions.append((x, y))
        return positions

    @property
    @abstractmethod
    def rows(self) -> int:
        """Number of rows in the board"""
        pass

    @property
    @abstractmethod
    def cols(self) -> int:
        """Number of columns in the board"""
        pass

    @abstractmethod
    def draw_board(self, surface: pygame.Surface) -> None:
        """Draw the empty board"""
        pass

    @abstractmethod
    def draw_piece(self, surface: pygame.Surface, position: int, piece: str) -> None:
        """Draw a game piece at the specified position"""
        pass

    def draw_winning_line(self, surface: pygame.Surface, winning_line: List[int], color: Tuple[int, int, int]) -> None:
        """Draw a line through the winning cells"""
        if winning_line and len(winning_line) >= 2:
            piece_size = int(min(self.board_width, self.board_height) * 0.25)
            start_pos = (
                self.cell_positions[winning_line[0]][0] + piece_size//2,
                self.cell_positions[winning_line[0]][1] + piece_size//2
            )
            end_pos = (
                self.cell_positions[winning_line[-1]][0] + piece_size//2,
                self.cell_positions[winning_line[-1]][1] + piece_size//2
            )
            pygame.draw.line(surface, color, start_pos, end_pos, 5)