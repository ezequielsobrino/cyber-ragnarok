import pygame
import sys
import random
from typing import List, Optional

from tic_tac_toe_brain import TicTacToeBrain

class TicTacToeCompetition:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption("Tic-Tac-Toe Brain Competition")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

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

        self.load_images()
        self.create_buttons()

        self.state = "setup"  # Can be "setup", "playing", or "finished"

    def load_images(self):
        self.bg_image = pygame.image.load("tic_tac_toe_board.png")
        self.bg_image = pygame.transform.scale(self.bg_image, (450, 450))

        self.x_image = pygame.image.load("x_image.png")
        self.x_image = pygame.transform.scale(self.x_image, (120, 120))

        self.o_image = pygame.image.load("o_image.png")
        self.o_image = pygame.transform.scale(self.o_image, (120, 120))

    def create_buttons(self):
        self.start_button = pygame.Rect(700, 400, 200, 50)
        self.quit_button = pygame.Rect(700, 500, 200, 50)

    def draw_setup_screen(self):
        self.screen.fill((44, 62, 80))  # Dark blue background

        # Draw title
        title = self.font.render("Tic-Tac-Toe Brain Competition", True, (236, 240, 241))
        self.screen.blit(title, (250, 50))

        # Draw model selection
        model_text = self.font.render("Model: " + self.model_choice, True, (236, 240, 241))
        self.screen.blit(model_text, (100, 150))

        # Draw game count selection
        games_text = self.font.render(f"Number of games: {self.total_games}", True, (236, 240, 241))
        self.screen.blit(games_text, (100, 250))

        # Draw buttons
        pygame.draw.rect(self.screen, (46, 204, 113), self.start_button)
        start_text = self.font.render("Start", True, (236, 240, 241))
        self.screen.blit(start_text, (self.start_button.x + 70, self.start_button.y + 10))

        pygame.draw.rect(self.screen, (231, 76, 60), self.quit_button)
        quit_text = self.font.render("Quit", True, (236, 240, 241))
        self.screen.blit(quit_text, (self.quit_button.x + 75, self.quit_button.y + 10))

    def draw_game_screen(self):
        self.screen.fill((44, 62, 80))  # Dark blue background

        # Draw the game board
        self.screen.blit(self.bg_image, (50, 75))

        # Draw X and O on the board
        for i, symbol in enumerate(self.board):
            x = (i % 3) * 150 + 125
            y = (i // 3) * 150 + 150
            if symbol == 'X':
                self.screen.blit(self.x_image, (x - 60, y - 60))
            elif symbol == 'O':
                self.screen.blit(self.o_image, (x - 60, y - 60))

        # Draw statistics
        stats = [
            f"Games Played: {self.game_count}",
            f"Brain 1 (X) Wins: {self.brain1_wins}",
            f"Brain 2 (O) Wins: {self.brain2_wins}",
            f"Draws: {self.draws}"
        ]
        for i, stat in enumerate(stats):
            text = self.font.render(stat, True, (236, 240, 241))
            self.screen.blit(text, (600, 100 + i * 50))

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