from typing import Dict, List, Tuple

import pygame
from simulations.milgram.assets_manager import AssetsManager
from simulations.milgram.dialog_manager import DialogManager
from simulations.milgram.game_state import GameState
from simulations.milgram.text_manager import TextManager


class Renderer:
    def __init__(self, screen_size: Tuple[int, int]):
        self.screen = pygame.display.set_mode(screen_size)
        self.screen_width, self.screen_height = screen_size  # 1792 x 1024
        
        # Initialize managers
        self.assets = AssetsManager(screen_size)
        self.text_manager = TextManager()
        self.dialog_manager = DialogManager(screen_size)
        
        # Colors
        self.colors = {
            'terminal': (0, 255, 0),
            'alert': (255, 0, 0),
            'black': (0, 0, 0),
            'gray': (200, 200, 200)
        }

    def update_text_animation(self) -> bool:
        """Delegate text animation update to text manager"""
        return self.text_manager.update_text_animation()

    @property
    def is_animating(self) -> bool:
        """Delegate animation state check to text manager"""
        return self.text_manager.is_animating

    def draw_scene(self, scene: Dict, state: GameState) -> List[pygame.Rect]:
        # Draw background
        self.screen.blit(self.assets.background, (0, 0))
        
        # Calculate character positions for 1792x1024 screen
        # Assuming each character sprite is about 300px wide
        character_width = 300
        total_characters = 3
        total_spacing = self.screen_width - (character_width * total_characters)
        spacing = total_spacing // (total_characters + 1)
        
        # Base vertical position - placing characters near bottom but above UI elements
        base_y = self.screen_height - 450  # This leaves space for dialog and choices
        
        # Define fixed positions with metaphorical meaning
        sprite_positions = {
            'thrall': (spacing, base_y),  # Player/subject on left
            'jarl': (spacing * 2 + character_width, base_y),  # Authority in middle
            'warrior': (spacing * 3 + character_width * 2, base_y)  # Victim on right
        }
        
        # Draw all characters (always visible)
        for character, position in sprite_positions.items():
            sprite = self.assets.sprites[character]
            self.screen.blit(sprite, position)
            
            # Highlight current speaker with a subtle effect
            if scene.get('speaker') == character:
                sprite_rect = sprite.get_rect(topleft=position)
                highlight_rect = sprite_rect.inflate(20, 20)
                pygame.draw.rect(self.screen, self.colors['terminal'], highlight_rect, 2)
        
        # Draw dialog
        self.dialog_manager.draw_dialog(
            self.screen,
            scene,
            self.text_manager,
            self.assets.portraits,
            state.authority_level
        )
        
        # Draw interface text
        if 'interface_text' in scene:
            interface_rect = pygame.Rect(20, self.screen_height - 200, 300, 100)
            pygame.draw.rect(self.screen, self.colors['black'], interface_rect)
            pygame.draw.rect(self.screen, self.colors['terminal'], interface_rect, 1)
            self.text_manager.draw_text(
                self.screen,
                scene['interface_text'],
                (30, self.screen_height - 190),
                self.colors['terminal'],
                280
            )
        
        # Draw status - adjusted position for widescreen
        status_text = f"Autoridad: {state.authority_level}/{state.MAX_AUTHORITY}"
        self.text_manager.draw_text(
            self.screen,
            status_text,
            (self.screen_width - 250, 30),
            self.colors['terminal']
        )
        
        # Draw choices
        if not self.is_animating and scene.get('requires_choice', False):
            return self.draw_choices([
                ('Obedecer', True),
                ('Resistir', False)
            ])
        return []

    def draw_choices(self, choices: List[Tuple[str, bool]]) -> List[pygame.Rect]:
        rects = []
        button_width = 200
        spacing = 50
        start_x = (self.screen_width - (button_width * 2 + spacing)) // 2
        y = self.screen_height - 100
        
        for i, (text, _) in enumerate(choices):
            x = start_x + (button_width + spacing) * i
            surface = self.text_manager.font.render(text, True, self.colors['terminal'])
            rect = surface.get_rect(center=(x + button_width//2, y))
            
            pygame.draw.rect(self.screen, (20, 40, 20), rect.inflate(40, 20))
            pygame.draw.rect(self.screen, self.colors['terminal'], rect.inflate(40, 20), 2)
            
            self.screen.blit(surface, rect)
            rects.append(rect.inflate(40, 20))
        
        return rects

    def show_ending(self, text: str):
        fade_surface = pygame.Surface(self.screen.get_size())
        fade_surface.fill(self.colors['black'])
        
        for alpha in range(0, 255, 5):
            self.screen.blit(fade_surface, (0, 0))
            fade_surface.set_alpha(alpha)
            pygame.display.flip()
            pygame.time.wait(20)
        
        self.screen.fill(self.colors['black'])
        self.text_manager.start_text_animation(text)
        
        while self.is_animating:
            self.screen.fill(self.colors['black'])
            self.text_manager.draw_text(
                self.screen,
                text,
                (50, 200),
                self.colors['terminal'],
                animated=True
            )
            self.update_text_animation()
            pygame.display.flip()
            pygame.time.wait(20)
        
        pygame.time.wait(5000)