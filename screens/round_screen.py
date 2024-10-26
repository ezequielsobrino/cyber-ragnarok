from screens.base_screen import BaseScreen


class RoundScreen(BaseScreen):
    def render(self, round_num: int, model1_score: int, model2_score: int, ties: int, model1_name: str, model2_name: str):
        self.screen.fill(self.RAVEN_BLACK)
        
        # Load model images
        model1_img = self.assets_manager.load_model_image(model1_name)
        model2_img = self.assets_manager.load_model_image(model2_name)
        
        self._draw_model_images(model1_img, model2_img)
        
        # Enhanced round display
        round_text = self.font_big.render(f"Round {round_num}", True, self.NEON_BLUE)
        round_rect = round_text.get_rect(center=(self.width//2, self.height//3))
        self._draw_epic_frame(round_rect.inflate(40, 20), self.PLASMA_BLUE)
        self.screen.blit(round_text, round_rect)
        
        # Score with energy field
        score_text = self.font.render(f"{model1_score} - {model2_score}", True, self.NORDIC_GOLD)
        score_rect = score_text.get_rect(center=(self.width//2, self.height//2))
        self._draw_energy_field(score_rect.inflate(60, 30), self.THUNDER_PURPLE, self.time)
        self.screen.blit(score_text, score_rect)
        
        # Ties counter with rune effect
        ties_text = self.font.render(f"Ties: {ties}", True, self.RUNE_GREEN)
        ties_rect = ties_text.get_rect(center=(self.width//2, self.height * 0.8))
        self._draw_lightning_effect(ties_rect.inflate(40, 20), self.FROST_BLUE)
        self.screen.blit(ties_text, ties_rect)
        
        return self.screen