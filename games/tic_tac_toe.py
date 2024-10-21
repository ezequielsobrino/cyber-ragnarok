import pygame


class TicTacToeGame:
    def __init__(self, game_manager, player_starts=True):
        self.game_manager = game_manager
        self.player_starts = player_starts
        self.current_player = 'X' if player_starts else 'O'
        self.board = ['' for _ in range(9)]
        self.winner = None
        self.game_over = False
        self.winning_line = None

        # Define window and board dimensions
        self.window_width = 1200
        self.window_height = 700
        self.board_width = 500  # Board width
        self.board_height = 500  # Board height
        
        # Centered board position
        self.board_x = (self.window_width - self.board_width) // 2
        self.board_y = (self.window_height - self.board_height) // 2

        # Calculate cell positions relative to centered board
        cell_spacing = self.board_width // 3
        self.cell_positions = [
            (self.board_x + cell_spacing * 0.5,     self.board_y + cell_spacing * 0.5),
            (self.board_x + cell_spacing * 1.5,     self.board_y + cell_spacing * 0.5),
            (self.board_x + cell_spacing * 2.5,     self.board_y + cell_spacing * 0.5),
            (self.board_x + cell_spacing * 0.5,     self.board_y + cell_spacing * 1.5),
            (self.board_x + cell_spacing * 1.5,     self.board_y + cell_spacing * 1.5),
            (self.board_x + cell_spacing * 2.5,     self.board_y + cell_spacing * 1.5),
            (self.board_x + cell_spacing * 0.5,     self.board_y + cell_spacing * 2.5),
            (self.board_x + cell_spacing * 1.5,     self.board_y + cell_spacing * 2.5),
            (self.board_x + cell_spacing * 2.5,     self.board_y + cell_spacing * 2.5)
        ]

        # If AI starts, make its move
        if not player_starts:
            self.make_ai_move()

    def handle_click(self, pos):
        if self.game_over or self.current_player != 'X':
            return

        # Verificar en qué celda se hizo clic
        for i, (x, y) in enumerate(self.cell_positions):
            cell_rect = pygame.Rect(x - 65, y - 65, 130, 130)
            if cell_rect.collidepoint(pos):
                if self.board[i] == '':  # Si la celda está vacía
                    self.board[i] = 'X'
                    if not self.check_winner():
                        self.current_player = 'O'
                        self.make_ai_move()
                break

    def make_ai_move(self):
        if self.game_over:
            return

        empty_cells = [i for i, cell in enumerate(self.board) if cell == '']
        if empty_cells:
            import random
            move = random.choice(empty_cells)
            self.board[move] = 'O'
            if not self.check_winner():
                self.current_player = 'X'

    def check_winner(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontales
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Verticales
            [0, 4, 8], [2, 4, 6]              # Diagonales
        ]

        for line in winning_combinations:
            if (self.board[line[0]] == self.board[line[1]] == self.board[line[2]] != ''):
                self.winner = self.board[line[0]]
                self.game_over = True
                self.winning_line = line
                return True

        if '' not in self.board:
            self.game_over = True
            self.winner = None
            return True

        return False

    def update(self):
        return self.game_over

    def draw(self, screen):
        # Draw background board
        screen.blit(self.game_manager.bg_image, (self.board_x, self.board_y))

        # Draw X's and O's
        for i, symbol in enumerate(self.board):
            x, y = self.cell_positions[i]
            if symbol == 'X':
                screen.blit(self.game_manager.x_image, (x - 65, y - 65))
            elif symbol == 'O':
                screen.blit(self.game_manager.o_image, (x - 65, y - 65))

        # If there's a winner, draw winning line
        if self.winning_line is not None:
            start_pos = self.cell_positions[self.winning_line[0]]
            end_pos = self.cell_positions[self.winning_line[2]]
            pygame.draw.line(screen, (255, 0, 0), start_pos, end_pos, 5)

        # Show game status message
        font = pygame.font.Font(None, 36)
        if self.game_over:
            if self.winner:
                text = f"{'Player' if self.winner == 'X' else 'AI'} wins!"
            else:
                text = "It's a tie!"
        else:
            text = f"{'Player' if self.current_player == 'X' else 'AI'}'s turn"
        
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.window_width // 2, self.board_y + self.board_height + 50))
        screen.blit(text_surface, text_rect)