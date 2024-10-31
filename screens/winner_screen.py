from screens.base_screen import BaseScreen

class WinnerScreen(BaseScreen):
    def render(self, winner_name: str, score1: int, score2: int, ties: int, 
               model1_name: str, model2_name: str, model1_metrics=None, model2_metrics=None):
        """Renders the winner screen with epic victory effects and final metrics"""
        self.screen.fill(self.RAVEN_BLACK)
        
        winner = 'X' if winner_name == model1_name else 'O' if winner_name == model2_name else None
        
        # Draw models using ModelDisplay component with winner effects and metrics
        self.model_display.render(
            self.screen,
            model1_name,
            model2_name,
            winner,
            True,  # final_winner=True for extra victory effects
            model1_metrics,
            model2_metrics
        )
        
        # Epic title with effects
        if winner_name == "Tie":
            title = self.font_big.render("It's a Tie!", True, self.NORDIC_GOLD)
        else:
            title = self.font_big.render(f"{winner_name} Wins!", True, self.NORDIC_GOLD)
        
        title_rect = title.get_rect(center=(self.width//2, self.height//3))
        
        # Add dramatic effects to title
        self._draw_lightning_effect(title_rect.inflate(80, 40), self.THUNDER_PURPLE)
        self._draw_energy_field(title_rect.inflate(60, 30), self.NEON_BLUE, self.time)
        self.screen.blit(title, title_rect)
        
        # Score with epic frame
        score_text = self.font.render(f"Final Score: {score1} - {score2} (Ties: {ties})", True, self.FROST_BLUE)
        score_rect = score_text.get_rect(center=(self.width//2, self.height//2))
        
        self._draw_epic_frame(score_rect.inflate(40, 20), self.PLASMA_BLUE)
        self.screen.blit(score_text, score_rect)
        
        # Add continuous victory particles if there's a winner
        if winner is not None:  # If not a tie
            self._add_victory_particles(title_rect)
            self._draw_particles()
        
        return self.screen