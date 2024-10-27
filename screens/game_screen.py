import pygame
from games.tic_tac_toe import TicTacToeGame
from screens.base_screen import BaseScreen

class GameScreen(BaseScreen):
    def __init__(self, width: int, height: int, fps: int, assets_manager):
        super().__init__(width, height, fps, assets_manager)
    
    def _get_cell_center(self, game, cell_index):
        """Calcula el centro de una celda dado su índice"""
        if isinstance(game, TicTacToeGame):
            row = cell_index // 3
            col = cell_index % 3
            cell_width = game.renderer.board_width // 3
            cell_height = game.renderer.board_width // 3
        else:  # CheckersGame
            row = cell_index // 8
            col = cell_index % 8
            cell_width = game.renderer.board_width // 8
            cell_height = game.renderer.board_width // 8
        
        # Calculamos la posición del tablero en el centro de la pantalla
        board_x = (self.width - game.renderer.board_width) // 2
        board_y = (self.height - game.renderer.board_width) // 2
        
        # Calculamos el centro de la celda
        x = board_x + (col * cell_width) + (cell_width // 2)
        y = board_y + (row * cell_height) + (cell_height // 2)
        
        return (x, y)

    def render(self, game, model1_name: str, model2_name: str):
        self.screen.fill(self.RAVEN_BLACK)
        
        if game.renderer is None:
            game.initialize_renderer(self.width, self.height)
        
        # Load model images
        model1_img = self.assets_manager.load_model_image(model1_name)
        model2_img = self.assets_manager.load_model_image(model2_name)
        
        winner = game.winner if game.game_over else None
        self._draw_model_images(model1_img, model2_img, winner)
        
        # Draw board with energy field effect
        board_rect = pygame.Rect(
            (self.width - game.renderer.board_width) // 2,
            (self.height - game.renderer.board_width) // 2,
            game.renderer.board_width,
            game.renderer.board_width
        )
        self._draw_energy_field(board_rect, self.FROST_BLUE, self.time)
        
        # Draw board
        game.renderer.draw_board(self.screen)
        
        # Draw pieces with enhanced effects
        for i, piece in enumerate(game.board):
            if piece != ' ':
                game.renderer.draw_piece(self.screen, i, piece)
                pos = self._get_cell_center(game, i)
                
                # Apply appropriate effects based on piece type
                if isinstance(game, TicTacToeGame):
                    if piece == 'X':
                        self._draw_lightning_effect(
                            pygame.Rect(pos[0]-20, pos[1]-20, 40, 40),
                            self.NEON_BLUE
                        )
                    else:
                        self._draw_energy_field(
                            pygame.Rect(pos[0]-20, pos[1]-20, 40, 40),
                            self.NEON_RED,
                            self.time
                        )
                else:  # CheckersGame
                    if piece.lower() == 'b':
                        self._draw_lightning_effect(
                            pygame.Rect(pos[0]-20, pos[1]-20, 40, 40),
                            self.NEON_BLUE
                        )
                    else:
                        self._draw_energy_field(
                            pygame.Rect(pos[0]-20, pos[1]-20, 40, 40),
                            self.NEON_RED,
                            self.time
                        )
                    
                    # Add special effect for kings
                    if piece.isupper():
                        self._draw_energy_field(
                            pygame.Rect(pos[0]-25, pos[1]-25, 50, 50),
                            self.NORDIC_GOLD,
                            self.time * 1.5
                        )
        
        # Draw winning effects
        if game.game_over and game.winner:
            if isinstance(game, TicTacToeGame) and hasattr(game, 'winning_line'):
                # Draw winning line for Tic-tac-toe
                game.renderer.draw_winning_line(self.screen, game.winning_line, self.BLOOD_NEON)
                start_pos = self._get_cell_center(game, game.winning_line[0])
                end_pos = self._get_cell_center(game, game.winning_line[-1])
                rect = pygame.Rect(
                    min(start_pos[0], end_pos[0]),
                    min(start_pos[1], end_pos[1]),
                    abs(end_pos[0] - start_pos[0]) or 40,
                    abs(end_pos[1] - start_pos[1]) or 40
                )
            else:
                # Draw victory effect for Checkers
                rect = board_rect.inflate(-board_rect.width//4, -board_rect.height//4)
                
            self._add_victory_particles(rect)
            self._draw_particles()
        
        return self.screen