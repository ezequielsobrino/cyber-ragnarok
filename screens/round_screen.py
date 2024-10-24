from screens.base_screen import BaseScreen


class RoundScreen(BaseScreen):
    def render(self, round_num: int, model1_score: int, model2_score: int, ties: int, model1_name: str, model2_name: str):
        self.screen.fill((0, 0, 0))
        
        # Load model images
        model1_img = self.assets_manager.load_model_image(model1_name)
        model2_img = self.assets_manager.load_model_image(model2_name)
        
        self._draw_model_images(model1_img, model2_img)
        
        round_text = self.font_big.render(f"Round {round_num}", True, self.TEXT_COLOR)
        score_text = self.font.render(f"{model1_score} - {model2_score}", True, self.TEXT_COLOR)
        ties_text = self.font.render(f"Ties: {ties}", True, self.TEXT_COLOR)
        
        self.screen.blit(round_text, (self.width//2 - round_text.get_width()//2, self.height//3))
        self.screen.blit(score_text, (self.width//2 - score_text.get_width()//2, self.height//2))
        self.screen.blit(ties_text, (self.width//2 - ties_text.get_width()//2, self.height * 0.8))
        
        return self.screen