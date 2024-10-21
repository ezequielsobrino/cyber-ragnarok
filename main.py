import pygame
import sys
import random
from typing import List, Optional

from tic_tac_toe_brain import TicTacToeBrain

class TicTacToeCompetition:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("Tic-Tac-Toe Brain Competition")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 48)

        self.brain1 = None
        self.brain2 = None
        self.current_player = 'X'
        self.board = [' '] * 9
        self.game_count = 0
        self.brain1_wins = 0
        self.brain2_wins = 0
        self.draws = 0

        self.total_games = 10
        self.model_choice = "Llama-3.1-70b-versatile"

        self.player_colors = {
            'X': (255, 87, 51),    # Bright red
            'O': (52, 152, 219)    # Bright blue
        }
        self.wood_tint = (193, 154, 107)

        self.load_images()
        self.create_buttons()

        self.state = "setup"  # Can be "setup", "playing", or "finished"
        
    def load_images(self):
        # Load and tint the background image
        self.bg_image = pygame.image.load("tic_tac_toe_board.png")
        self.bg_image = pygame.transform.scale(self.bg_image, (500, 500))
        self.bg_image = self.apply_wood_tint(self.bg_image)

        self.x_image = pygame.image.load("x_image.png")
        self.x_image = pygame.transform.scale(self.x_image, (130, 130))

        self.o_image = pygame.image.load("o_image.png")
        self.o_image = pygame.transform.scale(self.o_image, (130, 130))

    def apply_wood_tint(self, surface):
        tinted_surface = surface.copy()
        tinted_surface.fill(self.wood_tint, special_flags=pygame.BLEND_RGB_MULT)
        return tinted_surface

    def create_buttons(self):
        self.start_button = pygame.Rect(800, 500, 250, 60)
        self.quit_button = pygame.Rect(800, 580, 250, 60)

    def draw_setup_screen(self):
        self.screen.fill((44, 62, 80))  # Dark blue background

        # Draw title
        title = self.title_font.render("Tic-Tac-Toe Brain Competition", True, (236, 240, 241))
        self.screen.blit(title, (300, 50))

        # Draw model selection
        model_text = self.font.render("Model: " + self.model_choice, True, (236, 240, 241))
        self.screen.blit(model_text, (400, 150))

        # Draw game count selection
        games_text = self.font.render(f"Number of games: {self.total_games}", True, (236, 240, 241))
        self.screen.blit(games_text, (400, 250))

        # Draw buttons
        pygame.draw.rect(self.screen, (46, 204, 113), self.start_button, border_radius=10)
        start_text = self.font.render("Start Competition", True, (236, 240, 241))
        self.screen.blit(start_text, (self.start_button.x + 30, self.start_button.y + 15))

        pygame.draw.rect(self.screen, (231, 76, 60), self.quit_button, border_radius=10)
        quit_text = self.font.render("Quit Game", True, (236, 240, 241))
        self.screen.blit(quit_text, (self.quit_button.x + 65, self.quit_button.y + 15))

    def draw_game_screen(self):
        self.screen.fill((44, 62, 80))  # Dark blue background

        # Draw the wood-tinted game board
        self.screen.blit(self.bg_image, (50, 100))

        # Draw X and O on the board
        for i, symbol in enumerate(self.board):
            x = (i % 3) * 165 + 135
            y = (i // 3) * 165 + 185
            if symbol in ['X', 'O']:
                self.draw_tinted_piece(symbol, x, y)

        # Draw statistics with player colors
        stats = [
            ("Games Played", f"{self.game_count}", (236, 240, 241)),
            (f"{self.model_choice}", f"Wins: {self.brain1_wins}", self.player_colors['X']),
            (f"{self.model_choice}", f"Wins: {self.brain2_wins}", self.player_colors['O']),
            ("Draws", f"{self.draws}", (236, 240, 241))
        ]
        for i, (label, value, color) in enumerate(stats):
            label_text = self.font.render(label, True, color)
            value_text = self.font.render(value, True, color)
            self.screen.blit(label_text, (700, 150 + i * 60))
            self.screen.blit(value_text, (1000, 150 + i * 60))

    def draw_tinted_piece(self, symbol, x, y):
        image = self.x_image if symbol == 'X' else self.o_image
        color = self.player_colors[symbol]
        
        # Create a copy of the image and fill it with the player's color
        tinted_image = image.copy()
        tinted_image.fill(color, special_flags=pygame.BLEND_RGBA_MULT)
        
        # Add a glow effect
        glow_surface = pygame.Surface((150, 150), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (*color, 100), (75, 75), 65)
        self.screen.blit(glow_surface, (x - 75, y - 75))
        
        # Draw the tinted image
        self.screen.blit(tinted_image, (x - 65, y - 65))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == "setup":
                    if self.start_button.collidepoint(event.pos):
                        self.start_game()
                    elif self.quit_button.collidepoint(event.pos):
                        return False
        return True

    def start_game(self):
        self.brain1 = TicTacToeBrain(self.model_choice)
        self.brain2 = TicTacToeBrain(self.model_choice)
        self.state = "playing"
        self.play_game()

    def play_game(self):
        self.board = [' '] * 9
        self.current_player = 'X' if self.game_count % 2 == 0 else 'O'
        self.game_count += 1
        self.play_turn()

    def play_turn(self):
        winner = self.check_winner()
        if winner or ' ' not in self.board:
            self.end_game(winner)
            return

        current_brain = self.brain1 if self.current_player == 'X' else self.brain2
        move, _, _ = current_brain.get_move(self.board, self.current_player)
        self.board[move] = self.current_player

        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_winner(self) -> Optional[str]:
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' ':
                return self.board[combo[0]]
        return None

    def end_game(self, winner: Optional[str]):
        if winner:
            if winner == 'X':
                self.brain1_wins += 1
            else:
                self.brain2_wins += 1
        else:
            self.draws += 1

        if self.game_count < self.total_games:
            self.play_game()
        else:
            self.state = "finished"

    def run(self):
        running = True
        while running:
            running = self.handle_events()

            if self.state == "setup":
                self.draw_setup_screen()
            elif self.state in ["playing", "finished"]:
                self.draw_game_screen()
                if self.state == "playing":
                    self.play_turn()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = TicTacToeCompetition()
    game.run()