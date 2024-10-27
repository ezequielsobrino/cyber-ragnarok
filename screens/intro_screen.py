import pygame
from screens.base_screen import BaseScreen
from config.settings import GameType

class IntroScreen(BaseScreen):
    def __init__(self, width: int, height: int, fps: int, assets_manager):
        super().__init__(width, height, fps, assets_manager)
        self.game_titles = {
            GameType.TIC_TAC_TOE: "Cyber Ragnarok - Tic Tac Toe",
            GameType.CHECKERS: "Cyber Ragnarok - Battle Checkers"
        }
        
        # Efectos específicos para cada juego
        self.game_colors = {
            GameType.TIC_TAC_TOE: {
                'title': self.NEON_BLUE,
                'energy': self.THUNDER_PURPLE,
                'vs': self.BLOOD_NEON,
                'vs_effect': self.ENERGY_ORANGE
            },
            GameType.CHECKERS: {
                'title': self.NORDIC_GOLD,
                'energy': self.RUNE_GREEN,
                'vs': self.PLASMA_BLUE,
                'vs_effect': self.THUNDER_PURPLE
            }
        }

    def render(self, model1_name: str, model2_name: str, game_type: GameType = GameType.TIC_TAC_TOE):
        self.screen.fill(self.RAVEN_BLACK)
        
        # Load model images
        model1_img = self.assets_manager.load_model_image(model1_name)
        model2_img = self.assets_manager.load_model_image(model2_name)
        
        # Draw models with base effects
        self._draw_model_images(model1_img, model2_img)
        
        # Get game-specific colors
        colors = self.game_colors[game_type]
        
        # Create a more epic title with effects
        title = self.font_big.render(self.game_titles[game_type], True, colors['title'])
        title_rect = title.get_rect(center=(self.width//2, self.height//8))
        
        # Add energy field effect to title
        self._draw_energy_field(title_rect.inflate(40, 20), colors['energy'], self.time)
        
        # Add extra effects for checkers
        if game_type == GameType.CHECKERS:
            # Add corona effect for el título
            crown_rect = title_rect.inflate(60, 30)
            self._draw_crown_effect(crown_rect)
        
        self.screen.blit(title, title_rect)
        
        # Make VS text more dramatic
        vs_text = self.font_big.render("VS", True, colors['vs'])
        vs_rect = vs_text.get_rect(center=(self.width//2, self.height * 0.75))
        
        # Add lightning effect around VS
        self._draw_lightning_effect(vs_rect.inflate(60, 30), colors['vs_effect'])
        self.screen.blit(vs_text, vs_rect)
        
        return self.screen
    
    def _draw_crown_effect(self, rect):
        """Draw a crown-like effect for Checkers title"""
        # Points for a simple crown shape
        points = [
            (rect.left + rect.width * 0.2, rect.bottom),
            (rect.left + rect.width * 0.35, rect.top),
            (rect.left + rect.width * 0.5, rect.bottom),
            (rect.left + rect.width * 0.65, rect.top),
            (rect.left + rect.width * 0.8, rect.bottom)
        ]
        
        # Draw the crown outline with energy effect
        pygame.draw.lines(
            self.screen,
            self.NORDIC_GOLD,
            False,
            points,
            3
        )
        
        # Add energy particles around the crown points
        for point in points:
            self._draw_energy_field(
                pygame.Rect(point[0]-10, point[1]-10, 20, 20),
                self.NORDIC_GOLD,
                self.time * 1.5
            )