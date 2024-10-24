# assets/assets_manager.py
import pygame
import os
import logging

class AssetsManager:
    def __init__(self, assets_path, width, height):
        self.logger = logging.getLogger(__name__)
        self.assets_path = assets_path
        self.width = width
        self.height = height
        
        # Initialize pygame display if not already initialized
        if not pygame.get_init():
            pygame.init()
        if pygame.display.get_surface() is None:
            pygame.display.set_mode((width, height), pygame.HIDDEN)
        
        self._load_assets()
        
    def _load_assets(self):
        try:
            # Load base images
            board = pygame.image.load(os.path.join(self.assets_path, 'tic_tac_toe_board.png')).convert_alpha()
            x_img = pygame.image.load(os.path.join(self.assets_path, 'x_image.png')).convert_alpha()
            o_img = pygame.image.load(os.path.join(self.assets_path, 'o_image.png')).convert_alpha()
            
            # Apply color overlays
            self.board_img = self._apply_color_overlay(board, (222, 184, 135, 128))
            self.x_img = self._apply_color_overlay(x_img, (76, 153, 0, 255))
            self.o_img = self._apply_color_overlay(o_img, (0, 105, 148, 255))
            
            # Scale images
            self._scale_images()
            
        except Exception as e:
            self.logger.error(f"Error loading assets: {str(e)}", exc_info=True)
            raise
    
    def _scale_images(self):
        # Scale board
        board_scale = min(self.width * 0.4 / self.board_img.get_width(), 
                         self.height * 0.6 / self.board_img.get_height())
        self.board_img = pygame.transform.scale(self.board_img, 
            (int(self.board_img.get_width() * board_scale),
             int(self.board_img.get_height() * board_scale)))
        
        # Scale pieces
        piece_size = int(min(self.board_img.get_width(), self.board_img.get_height()) * 0.25)
        self.x_img = pygame.transform.scale(self.x_img, (piece_size, piece_size))
        self.o_img = pygame.transform.scale(self.o_img, (piece_size, piece_size))
    
    def _apply_color_overlay(self, original_surface, overlay_color):
        result = original_surface.copy()
        overlay = pygame.Surface(original_surface.get_size(), pygame.SRCALPHA)
        overlay.fill(overlay_color)
        result.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return result
    
    def load_model_image(self, model_name):
        formatted_name = model_name.replace("-", "_").replace(".", "_") + ".png"
        try:
            image = pygame.image.load(os.path.join(self.assets_path, formatted_name)).convert_alpha()
            target_height = self.height * 0.8
            aspect_ratio = image.get_width() / image.get_height()
            target_width = int(target_height * aspect_ratio)
            
            max_width = self.width * 0.2
            if target_width > max_width:
                target_width = max_width
                target_height = int(target_width / aspect_ratio)
            
            return pygame.transform.scale(image, (target_width, int(target_height)))
        except Exception as e:
            self.logger.error(f"Error loading model image {formatted_name}: {str(e)}")
            placeholder = pygame.Surface((int(self.width * 0.2), int(self.height * 0.8)))
            placeholder.fill((50, 50, 50))
            return placeholder
    
    def get_board(self):
        return self.board_img
    
    def get_x(self):
        return self.x_img
    
    def get_o(self):
        return self.o_img