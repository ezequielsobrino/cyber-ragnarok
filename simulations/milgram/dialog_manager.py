from typing import Dict, Tuple
import pygame

from simulations.milgram.text_manager import TextManager


class DialogManager:
    def __init__(self, screen_size: Tuple[int, int]):
        self.dialog_height = 180
        self.dialog_padding = 20
        self.dialog_surface = pygame.Surface(
            (screen_size[0] - 40, self.dialog_height), 
            pygame.SRCALPHA
        )
        self.dialog_bg_color = (0, 0, 0, 180)
        self.screen_width = screen_size[0]

    def draw_dialog(self, screen: pygame.Surface, scene: Dict, text_manager: TextManager, 
                   portraits: Dict[str, pygame.Surface], authority_level: int):
        if 'text' not in scene:
            return

        dialog_rect = pygame.Rect(20, 20, self.screen_width - 40, self.dialog_height)
        self.dialog_surface.fill(self.dialog_bg_color)
        screen.blit(self.dialog_surface, dialog_rect)

        text_start_x = 30 + self.dialog_padding
        if 'speaker' in scene:
            portrait_pos = (30, 30)
            screen.blit(portraits[scene['speaker']], portrait_pos)
            text_start_x = 150

        text_color = (255, 0, 0) if authority_level > 0 else (200, 200, 200)
        max_text_width = self.screen_width - (text_start_x + 40 + self.dialog_padding)
        text_manager.draw_text(
            screen,
            scene['text'],
            (text_start_x, 40),
            text_color,
            max_text_width,
            animated=True
        )