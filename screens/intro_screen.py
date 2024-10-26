from screens.base_screen import BaseScreen


class IntroScreen(BaseScreen):
    def render(self, model1_name: str, model2_name: str):
        self.screen.fill(self.RAVEN_BLACK)  # Usar el negro profundo cyberpunk
        
        # Load model images
        model1_img = self.assets_manager.load_model_image(model1_name)
        model2_img = self.assets_manager.load_model_image(model2_name)
        
        # Draw models with base effects
        self._draw_model_images(model1_img, model2_img)
        
        # Create a more epic title with effects
        title = self.font_big.render("Cyber Ragnarok - Tic Tac Toe", True, self.NEON_BLUE)
        title_rect = title.get_rect(center=(self.width//2, self.height//8))
        
        # Add energy field effect to title
        self._draw_energy_field(title_rect.inflate(40, 20), self.THUNDER_PURPLE, self.time)
        self.screen.blit(title, title_rect)
        
        # Make VS text more dramatic
        vs_text = self.font_big.render("VS", True, self.BLOOD_NEON)
        vs_rect = vs_text.get_rect(center=(self.width//2, self.height * 0.75))
        
        # Add lightning effect around VS
        self._draw_lightning_effect(vs_rect.inflate(60, 30), self.ENERGY_ORANGE)
        self.screen.blit(vs_text, vs_rect)
        
        return self.screen