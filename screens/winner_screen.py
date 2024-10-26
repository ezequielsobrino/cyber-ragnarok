from screens.base_screen import BaseScreen


class WinnerScreen(BaseScreen):
    def render(self, winner_name: str, score1: int, score2: int, ties: int, model1_name: str, model2_name: str):
        self.screen.fill(self.RAVEN_BLACK)  # Usar el negro profundo cyberpunk
        
        # Load model images
        model1_img = self.assets_manager.load_model_image(model1_name)
        model2_img = self.assets_manager.load_model_image(model2_name)
        
        winner = 'X' if winner_name == model1_name else 'O' if winner_name == model2_name else None
        self._draw_model_images(model1_img, model2_img, winner, True)
        
        # Título con efectos épicos
        if winner_name == "Tie":
            title = self.font_big.render("It's a Tie!", True, self.NORDIC_GOLD)
        else:
            title = self.font_big.render(f"{winner_name} Wins!", True, self.NORDIC_GOLD)
        
        title_rect = title.get_rect(center=(self.width//2, self.height//3))
        
        # Añadir efectos dramáticos al título
        self._draw_lightning_effect(title_rect.inflate(80, 40), self.THUNDER_PURPLE)
        self._draw_energy_field(title_rect.inflate(60, 30), self.NEON_BLUE, self.time)
        self.screen.blit(title, title_rect)
        
        # Score con efectos
        score_text = self.font.render(f"Final Score: {score1} - {score2} (Ties: {ties})", True, self.FROST_BLUE)
        score_rect = score_text.get_rect(center=(self.width//2, self.height//2))
        
        # Marco épico para el score
        self._draw_epic_frame(score_rect.inflate(40, 20), self.PLASMA_BLUE)
        self.screen.blit(score_text, score_rect)
        
        # Añadir partículas de victoria continuas
        if winner != None:  # Si hay un ganador (no es empate)
            self._add_victory_particles(title_rect)
            self._draw_particles()
        
        return self.screen