from screens.base_screen import BaseScreen

class RoundScreen(BaseScreen):
    def render(self, round_num: int, model1_score: int, model2_score: int, ties: int, 
               model1_name: str, model2_name: str, model1_metrics=None, model2_metrics=None):
        """Renders the round transition screen with dramatic effects and model metrics"""
        self.screen.fill(self.RAVEN_BLACK)
        
        # Draw models using ModelDisplay component with metrics
        self.model_display.render(
            self.screen,
            model1_name,
            model2_name,
            None,  # No winner during round transition
            False,
            model1_metrics,
            model2_metrics
        )
        
        # Enhanced round display with epic frame
        round_text = self.font_big.render(f"Round {round_num}", True, self.NEON_BLUE)
        round_rect = round_text.get_rect(center=(self.width//2, self.height//3))
        self._draw_epic_frame(round_rect.inflate(40, 20), self.PLASMA_BLUE)
        self.screen.blit(round_text, round_rect)
        
        # Score with energy field effect
        score_text = self.font.render(f"{model1_score} - {model2_score}", True, self.NORDIC_GOLD)
        score_rect = score_text.get_rect(center=(self.width//2, self.height//2))
        self._draw_energy_field(score_rect.inflate(60, 30), self.THUNDER_PURPLE, self.time)
        self.screen.blit(score_text, score_rect)
        
        # Ties counter with lightning effect
        ties_text = self.font.render(f"Ties: {ties}", True, self.RUNE_GREEN)
        ties_rect = ties_text.get_rect(center=(self.width//2, self.height * 0.8))
        self._draw_lightning_effect(ties_rect.inflate(40, 20), self.FROST_BLUE)
        self.screen.blit(ties_text, ties_rect)
        
        return self.screen