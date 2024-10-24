import pygame
from screens.base_screen import BaseScreen


class GameScreen(BaseScreen):
    def __init__(self, width: int, height: int, fps: int, assets_manager):
        super().__init__(width, height, fps, assets_manager)
        self._setup_board()
    
    def _setup_board(self):
        self.board_img = self.assets_manager.get_board()
        self.board_x = (self.width - self.board_img.get_width()) // 2
        self.board_y = (self.height - self.board_img.get_height()) // 2
        
        cell_width = self.board_img.get_width() // 3
        cell_height = self.board_img.get_height() // 3
        piece_size = int(min(self.board_img.get_width(), self.board_img.get_height()) * 0.25)
        
        self.cell_positions = []
        for row in range(3):
            for col in range(3):
                x = self.board_x + col * cell_width + cell_width // 2 - piece_size // 2
                y = self.board_y + row * cell_height + cell_height // 2 - piece_size // 2
                self.cell_positions.append((x, y))
    
    def render(self, game, model1_name: str, model2_name: str):
        self.screen.fill((0, 0, 0))
        
        # Load model images
        model1_img = self.assets_manager.load_model_image(model1_name)
        model2_img = self.assets_manager.load_model_image(model2_name)
        
        winner = game.winner if game.game_over else None
        self._draw_model_images(model1_img, model2_img, winner)
        
        # Draw board and pieces
        self.screen.blit(self.board_img, (self.board_x, self.board_y))
        
        # Draw pieces
        for i, piece in enumerate(game.board):
            if piece == 'X':
                self.screen.blit(self.assets_manager.get_x(), self.cell_positions[i])
            elif piece == 'O':
                self.screen.blit(self.assets_manager.get_o(), self.cell_positions[i])
        
        # Draw winning line if game is over
        if game.winning_line:
            start_pos = (
                self.cell_positions[game.winning_line[0]][0] + self.assets_manager.get_x().get_width()//2,
                self.cell_positions[game.winning_line[0]][1] + self.assets_manager.get_x().get_height()//2
            )
            end_pos = (
                self.cell_positions[game.winning_line[2]][0] + self.assets_manager.get_x().get_width()//2,
                self.cell_positions[game.winning_line[2]][1] + self.assets_manager.get_x().get_height()//2
            )
            pygame.draw.line(self.screen, self.BLOOD_RED, start_pos, end_pos, 5)
        
        return self.screen