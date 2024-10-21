import pygame
import sys

from games.tic_tac_toe import TicTacToeGame

class GameManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("Mini-Juegos")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 48)

        self.state = "main_menu"
        self.characters = [
            "llama-3.1-70b-versatile",
            "llama-3.1-8b-instant",
            "mixtral-8x7b-32768"
        ]
        self.selected_character = None
        self.selected_game = None
        self.current_round = 0
        self.total_rounds = 3  # Valor por defecto
        self.player_score = 0
        self.ai_score = 0
        self.player_starts = True  # Nueva variable para controlar quien empieza

        self.round_options = [1,2,3,4,5,6,7,8,9,10]  # Opciones de rounds disponibles
        self.selected_rounds_index = 0  # Índice para selección de rounds

        self.tic_tac_toe_game = None

        self.load_images()

    def load_images(self):
        self.bg_image = pygame.image.load("tic_tac_toe_board.png")
        self.bg_image = pygame.transform.scale(self.bg_image, (500, 500))
        self.x_image = pygame.image.load("x_image.png")
        self.x_image = pygame.transform.scale(self.x_image, (130, 130))
        self.o_image = pygame.image.load("o_image.png")
        self.o_image = pygame.transform.scale(self.o_image, (130, 130))

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click(event.pos)

    def handle_click(self, pos):
        if self.state == "main_menu":
            if self.button_rect(600, 300, 400, 50).collidepoint(pos):
                self.state = "character_select"
        elif self.state == "character_select":
            for i, char in enumerate(self.characters):
                if self.button_rect(600, 200 + i * 100, 400, 50).collidepoint(pos):
                    self.selected_character = char
                    self.state = "rounds_select"  # Nuevo estado para seleccionar rounds
        elif self.state == "rounds_select":
            # Botón para disminuir rounds
            if self.button_rect(400, 300, 50, 50).collidepoint(pos):
                self.selected_rounds_index = max(0, self.selected_rounds_index - 1)
                self.total_rounds = self.round_options[self.selected_rounds_index]
            # Botón para aumentar rounds
            elif self.button_rect(800, 300, 50, 50).collidepoint(pos):
                self.selected_rounds_index = min(len(self.round_options) - 1, self.selected_rounds_index + 1)
                self.total_rounds = self.round_options[self.selected_rounds_index]
            # Botón de confirmación
            elif self.button_rect(600, 400, 400, 50).collidepoint(pos):
                self.state = "game_select"
        elif self.state == "game_select":
            if self.button_rect(600, 300, 400, 50).collidepoint(pos):
                self.selected_game = "tic_tac_toe"
                self.tic_tac_toe_game = TicTacToeGame(self, self.player_starts)  # Pasar quien empieza
                self.state = "playing"
        elif self.state == "playing":
            if self.selected_game == "tic_tac_toe":
                self.tic_tac_toe_game.handle_click(pos)
        elif self.state == "round_stats":
            if self.button_rect(600, 500, 400, 50).collidepoint(pos):
                if self.current_round < self.total_rounds:
                    self.player_starts = not self.player_starts  # Alternar quien empieza
                    self.tic_tac_toe_game = TicTacToeGame(self, self.player_starts)
                    self.state = "playing"
                else:
                    self.state = "final_results"
        elif self.state == "final_results":
            if self.button_rect(600, 500, 400, 50).collidepoint(pos):
                self.__init__()

    def update(self):
        if self.state == "playing":
            if self.selected_game == "tic_tac_toe":
                game_over = self.tic_tac_toe_game.update()
                if game_over:
                    self.end_round()

    def end_round(self):
        self.current_round += 1
        if self.tic_tac_toe_game.winner == 'X':
            self.player_score += 1
        elif self.tic_tac_toe_game.winner == 'O':
            self.ai_score += 1
        self.state = "round_stats"

    def draw(self):
        self.screen.fill((44, 62, 80))  # Dark blue background

        if self.state == "main_menu":
            self.draw_main_menu()
        elif self.state == "character_select":
            self.draw_character_select()
        elif self.state == "rounds_select":
            self.draw_rounds_select()
        elif self.state == "game_select":
            self.draw_game_select()
        elif self.state == "playing":
            if self.selected_game == "tic_tac_toe":
                self.tic_tac_toe_game.draw(self.screen)
                # Mostrar información adicional
                model_text = self.font.render(f"Modelo: {self.selected_character}", True, (255, 255, 255))
                self.screen.blit(model_text, (20, 20))
                turn_text = self.font.render(f"Empieza: {'Jugador' if self.player_starts else 'IA'}", True, (255, 255, 255))
                self.screen.blit(turn_text, (20, 60))
        elif self.state == "round_stats":
            self.draw_round_stats()
        elif self.state == "final_results":
            self.draw_final_results()

    def draw_main_menu(self):
        title = self.title_font.render("Mini-Juegos", True, (255, 255, 255))
        title_rect = title.get_rect(center=(600, 100))
        self.screen.blit(title, title_rect)
        self.draw_button("Jugar", 600, 300, 400)

    def draw_character_select(self):
        title = self.title_font.render("Selecciona un modelo", True, (255, 255, 255))
        title_rect = title.get_rect(center=(600, 100))
        self.screen.blit(title, title_rect)
        
        for i, char in enumerate(self.characters):
            self.draw_button(char, 600, 200 + i * 100, 400)

    def draw_rounds_select(self):
        title = self.title_font.render("Selecciona el número de rounds", True, (255, 255, 255))
        title_rect = title.get_rect(center=(600, 100))
        self.screen.blit(title, title_rect)
        
        # Mostrar número actual de rounds
        rounds_text = self.title_font.render(str(self.total_rounds), True, (255, 255, 255))
        rounds_rect = rounds_text.get_rect(center=(600, 300))
        self.screen.blit(rounds_text, rounds_rect)
        
        # Botones - y +
        self.draw_button("-", 400, 300, 50, 50)
        self.draw_button("+", 800, 300, 50, 50)
        
        # Botón de confirmación
        self.draw_button("Confirmar", 600, 400, 400)

    def draw_game_select(self):
        title = self.title_font.render("Selecciona un juego", True, (255, 255, 255))
        title_rect = title.get_rect(center=(600, 100))
        self.screen.blit(title, title_rect)
        
        # Draw selected model
        model_text = self.font.render(f"Modelo seleccionado: {self.selected_character}", True, (255, 255, 255))
        model_rect = model_text.get_rect(center=(600, 200))
        self.screen.blit(model_text, model_rect)
        
        self.draw_button("Tic-Tac-Toe", 600, 300, 400)

    def draw_round_stats(self):
        title = self.title_font.render(f"Ronda {self.current_round} de {self.total_rounds}", True, (255, 255, 255))
        title_rect = title.get_rect(center=(600, 100))
        self.screen.blit(title, title_rect)
        
        model_text = self.font.render(f"Modelo: {self.selected_character}", True, (255, 255, 255))
        model_rect = model_text.get_rect(center=(600, 200))
        self.screen.blit(model_text, model_rect)
        
        score = self.font.render(f"Jugador: {self.player_score} - IA: {self.ai_score}", True, (255, 255, 255))
        score_rect = score.get_rect(center=(600, 300))
        self.screen.blit(score, score_rect)
        
        next_turn = self.font.render(f"Siguiente ronda empezará: {'IA' if self.player_starts else 'Jugador'}", True, (255, 255, 255))
        next_turn_rect = next_turn.get_rect(center=(600, 400))
        self.screen.blit(next_turn, next_turn_rect)
        
        self.draw_button("Siguiente", 600, 500, 400)

    def draw_final_results(self):
        title = self.title_font.render("Resultados Finales", True, (255, 255, 255))
        title_rect = title.get_rect(center=(600, 100))
        self.screen.blit(title, title_rect)
        
        model_text = self.font.render(f"Modelo: {self.selected_character}", True, (255, 255, 255))
        model_rect = model_text.get_rect(center=(600, 200))
        self.screen.blit(model_text, model_rect)
        
        score = self.font.render(f"Jugador: {self.player_score} - IA: {self.ai_score}", True, (255, 255, 255))
        score_rect = score.get_rect(center=(600, 300))
        self.screen.blit(score, score_rect)
        
        result = "¡Ganaste!" if self.player_score > self.ai_score else "¡La IA ganó!" if self.ai_score > self.player_score else "¡Empate!"
        result_text = self.font.render(result, True, (255, 255, 255))
        result_rect = result_text.get_rect(center=(600, 400))
        self.screen.blit(result_text, result_rect)
        
        self.draw_button("Volver al Menú", 600, 500, 400)

    def draw_button(self, text, x, y, width=200, height=50):
        button = self.button_rect(x, y, width, height)
        pygame.draw.rect(self.screen, (52, 152, 219), button)
        text_surf = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=button.center)
        self.screen.blit(text_surf, text_rect)

    def button_rect(self, x, y, width, height):
        return pygame.Rect(x - width//2, y - height//2, width, height)
