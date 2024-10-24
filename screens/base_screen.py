import pygame
from abc import ABC, abstractmethod

class BaseScreen(ABC):
    def __init__(self, width: int, height: int, fps: int, assets_manager):
        self.width = width
        self.height = height
        self.fps = fps
        self.assets_manager = assets_manager
        self.screen = pygame.Surface((width, height))
        
        # Common colors
        self.WOOD_COLOR = (222, 184, 135, 128)
        self.NATURE_GREEN = (76, 153, 0, 255)
        self.SEA_BLUE = (0, 105, 148, 255)
        self.BLOOD_RED = (139, 0, 0)
        self.GOLDEN = (255, 215, 0)
        self.TEXT_COLOR = (255, 255, 255)
        
        # Common fonts
        self.original_font_size = int(height * 0.05)
        self.min_font_size = int(height * 0.02)
        self.font_large = int(height * 0.08)
        self.font = pygame.font.Font(None, self.original_font_size)
        self.font_big = pygame.font.Font(None, self.font_large)
        
    def _draw_model_images(self, model1_img, model2_img, winner=None, final_winner=False):
        if model1_img and model2_img:
            img_y = (self.height - model1_img.get_height()) // 2
            margin = 20
            border_thickness = 4

            # Model 1 borders
            border_rect_1 = pygame.Rect(
                margin - border_thickness,
                img_y - border_thickness,
                model1_img.get_width() + (border_thickness * 2),
                model1_img.get_height() + (border_thickness * 2)
            )
            pygame.draw.rect(self.screen, self.NATURE_GREEN, border_rect_1, border_thickness)

            # Handle winner highlighting
            if winner == 'X':
                winner_rect_1 = pygame.Rect(
                    margin - (border_thickness * 2),
                    img_y - (border_thickness * 2),
                    model1_img.get_width() + (border_thickness * 4),
                    model1_img.get_height() + (border_thickness * 4)
                )
                pygame.draw.rect(self.screen, self.GOLDEN, winner_rect_1, border_thickness)

                if final_winner:
                    final_rect_1 = pygame.Rect(
                        margin - (border_thickness * 3),
                        img_y - (border_thickness * 3),
                        model1_img.get_width() + (border_thickness * 6),
                        model1_img.get_height() + (border_thickness * 6)
                    )
                    pygame.draw.rect(self.screen, self.GOLDEN, final_rect_1, border_thickness)

            # Draw model 1
            self.screen.blit(model1_img, (margin, img_y))

            # Model 2 borders
            border_rect_2 = pygame.Rect(
                self.width - model2_img.get_width() - margin - border_thickness,
                img_y - border_thickness,
                model2_img.get_width() + (border_thickness * 2),
                model2_img.get_height() + (border_thickness * 2)
            )
            pygame.draw.rect(self.screen, self.SEA_BLUE, border_rect_2, border_thickness)

            # Handle winner highlighting
            if winner == 'O':
                winner_rect_2 = pygame.Rect(
                    self.width - model2_img.get_width() - margin - (border_thickness * 2),
                    img_y - (border_thickness * 2),
                    model2_img.get_width() + (border_thickness * 4),
                    model2_img.get_height() + (border_thickness * 4)
                )
                pygame.draw.rect(self.screen, self.GOLDEN, winner_rect_2, border_thickness)

                if final_winner:
                    final_rect_2 = pygame.Rect(
                        self.width - model2_img.get_width() - margin - (border_thickness * 3),
                        img_y - (border_thickness * 3),
                        model2_img.get_width() + (border_thickness * 6),
                        model2_img.get_height() + (border_thickness * 6)
                    )
                    pygame.draw.rect(self.screen, self.GOLDEN, final_rect_2, border_thickness)

            # Draw model 2
            self.screen.blit(model2_img, (self.width - model2_img.get_width() - margin, img_y))
    
    @abstractmethod
    def render(self, **kwargs):
        pass