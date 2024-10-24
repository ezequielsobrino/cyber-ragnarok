from screens.base_screen import BaseScreen


class IntroScreen(BaseScreen):
    def render(self, model1_name: str, model2_name: str):
        self.screen.fill((0, 0, 0))
        
        # Load model images
        model1_img = self.assets_manager.load_model_image(model1_name)
        model2_img = self.assets_manager.load_model_image(model2_name)
        
        # Draw models
        self._draw_model_images(model1_img, model2_img)
        
        # Draw title
        title = self.font_big.render("Cyber Ragnarok - Tic Tac Toe", True, self.TEXT_COLOR)
        self.screen.blit(title, (self.width//2 - title.get_width()//2, self.height//8))
        
        # Draw VS text
        vs_text = self.font_big.render("VS", True, (255, 0, 0))
        vs_y = self.height * 0.75
        self.screen.blit(vs_text, (self.width//2 - vs_text.get_width()//2, vs_y))
        
        return self.screen