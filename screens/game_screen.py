import pygame
from screens.base_screen import BaseScreen

class GameScreen(BaseScreen):
    BLOOD_RED = (200, 0, 0)
    
    def __init__(self, width: int, height: int, fps: int, assets_manager):
        super().__init__(width, height, fps, assets_manager)
    
    def render(self, game, model1_name: str, model2_name: str):
        self.screen.fill((0, 0, 0))
        
        # Initialize renderer if not already initialized
        if game.renderer is None:
            game.initialize_renderer(self.width, self.height)
        
        # Load model images
        model1_img = self.assets_manager.load_model_image(model1_name)
        model2_img = self.assets_manager.load_model_image(model2_name)
        
        winner = game.winner if game.game_over else None
        self._draw_model_images(model1_img, model2_img, winner)
        
        # Draw board
        game.renderer.draw_board(self.screen)
        
        # Draw pieces
        for i, piece in enumerate(game.board):
            if piece != ' ':
                game.renderer.draw_piece(self.screen, i, piece)
        
        # Draw winning line if game is over
        if game.winning_line:
            game.renderer.draw_winning_line(self.screen, game.winning_line, self.BLOOD_RED)
        
        return self.screen