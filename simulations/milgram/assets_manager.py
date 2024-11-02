import os
import pygame
from typing import Dict, Tuple

class AssetsManager:
    def __init__(self, screen_size: Tuple[int, int]):
        self.screen_size = screen_size
        self.portraits: Dict[str, pygame.Surface] = {}
        self.sprites: Dict[str, pygame.Surface] = {}
        self.background: pygame.Surface = None
        self.load_all_assets()

    def load_and_scale(self, filename: str, size: Tuple[int, int]) -> pygame.Surface:
        try:
            path = os.path.join('simulations', 'milgram', 'assets', filename)
            image = pygame.image.load(path)
            return pygame.transform.scale(image, size)
        except pygame.error:
            surface = pygame.Surface(size)
            surface.fill((200, 200, 200))  # Default gray
            return surface

    def load_all_assets(self):
        # Load background
        self.background = self.load_and_scale('background.png', self.screen_size)
        
        # Load portraits
        portrait_size = (100, 100)
        for character in ['jarl', 'thrall', 'warrior']:
            self.portraits[character] = self.load_and_scale(
                f'{character}_portrait.png', 
                portrait_size
            )
        
        # Load sprites
        sprite_size = (200, 400)
        for character in ['jarl', 'thrall', 'warrior']:
            self.sprites[character] = self.load_and_scale(
                f'{character}_sprite.png', 
                sprite_size
            )