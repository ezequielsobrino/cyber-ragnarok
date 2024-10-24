from screens.base_screen import BaseScreen


class WinnerScreen(BaseScreen):
    def render(self, winner_name: str, score1: int, score2: int, ties: int, model1_name: str, model2_name: str):
        self.screen.fill((0, 0, 0))
        
        # Load model images
        model1_img = self.assets_manager.load_model_image(model1_name)
        model2_img = self.assets_manager.load_model_image(model2_name)
        
        winner = 'X' if winner_name == model1_name else 'O' if winner_name == model2_name else None
        self._draw_model_images(model1_img, model2_img, winner, True)
        
        if winner_name == "Tie":
            title = self.font_big.render("It's a Tie!", True, self.GOLDEN)
        else:
            title = self.font_big.render(f"{winner_name} Wins!", True, self.GOLDEN)
        
        score_text = self.font.render(f"Final Score: {score1} - {score2} (Ties: {ties})", True, self.TEXT_COLOR)
        
        self.screen.blit(title, (self.width//2 - title.get_width()//2, self.height//3))
        self.screen.blit(score_text, (self.width//2 - score_text.get_width()//2, self.height//2))
        
        return self.screen