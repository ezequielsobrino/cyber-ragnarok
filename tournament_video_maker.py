import pygame
import cv2
import random
import logging
from datetime import datetime
from games.tic_tac_toe import TicTacToeGame

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'tournament_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)

class TournamentVideoMaker:
    def __init__(self, width=1920, height=1080, fps=30):
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Initializing TournamentVideoMaker with dimensions {width}x{height} at {fps} FPS")
        
        self.width = width
        self.height = height
        self.fps = fps
        self.font_size = int(height * 0.05)
        self.font_large = int(height * 0.08)
        
        # Define custom colors with alpha for overlay
        self.WOOD_COLOR = (222, 184, 135, 128)    # Tan/light wood color with alpha
        self.NATURE_GREEN = (76, 153, 0, 255)     # Natural green without transparency for X pieces
        self.SEA_BLUE = (0, 105, 148, 255)        # Sea blue without transparency for O pieces
        self.BLOOD_RED = (139, 0, 0)              # Blood red (no alpha needed)
        self.GOLDEN = (255, 215, 0)               # Golden (no alpha needed)
        
        try:
            # Initialize Pygame with a display mode
            pygame.init()
            pygame.display.set_mode((width, height))  # Necesario para convertir las imágenes
            self.screen = pygame.Surface((width, height))
            self.clock = pygame.time.Clock()
            self.font = pygame.font.Font(None, self.font_size)
            self.font_big = pygame.font.Font(None, self.font_large)
            self.logger.info("Pygame initialized successfully")
            
            # Load and tint game images
            self.logger.info("Loading and tinting game images...")
            
            # Load original images
            original_board = pygame.image.load('tic_tac_toe_board.png').convert_alpha()
            original_x = pygame.image.load('x_image.png').convert_alpha()
            original_o = pygame.image.load('o_image.png').convert_alpha()
            
            # Apply color overlays
            self.board_img = self._apply_color_overlay(original_board, self.WOOD_COLOR)
            self.x_img = self._apply_color_overlay(original_x, self.NATURE_GREEN)
            self.o_img = self._apply_color_overlay(original_o, self.SEA_BLUE)
            
            self.logger.info("Game images tinted successfully")
            
            # Scale images
            board_scale = min(width * 0.4 / self.board_img.get_width(), 
                            height * 0.6 / self.board_img.get_height())
            self.board_img = pygame.transform.scale(self.board_img, 
                (int(self.board_img.get_width() * board_scale),
                 int(self.board_img.get_height() * board_scale)))
            
            piece_size = int(min(self.board_img.get_width(), self.board_img.get_height()) * 0.25)
            self.x_img = pygame.transform.scale(self.x_img, (piece_size, piece_size))
            self.o_img = pygame.transform.scale(self.o_img, (piece_size, piece_size))
            
            # Calculate positions
            self.board_x = (width - self.board_img.get_width()) // 2
            self.board_y = (height - self.board_img.get_height()) // 2
            
            cell_width = self.board_img.get_width() // 3
            cell_height = self.board_img.get_height() // 3
            self.cell_positions = []
            for row in range(3):
                for col in range(3):
                    x = self.board_x + col * cell_width + cell_width // 2 - piece_size // 2
                    y = self.board_y + row * cell_height + cell_height // 2 - piece_size // 2
                    self.cell_positions.append((x, y))
            
            # Video writer setup
            self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.video_writer = None
            self.logger.info("Video writer initialized")
            
        except Exception as e:
            self.logger.error(f"Error during initialization: {str(e)}", exc_info=True)
            raise
    
    def create_intro(self, model1_name, model2_name, duration_seconds=5):
        self.logger.info(f"Creating intro sequence for {model1_name} vs {model2_name}")
        frames = int(duration_seconds * self.fps)
        try:
            for frame in range(frames):
                self.screen.fill((0, 0, 0))
                title = self.font_big.render("TicTacToe Tournament", True, (255, 255, 255))
                name1_text = self.font_big.render(model1_name, True, (255, 255, 255))
                name2_text = self.font_big.render(model2_name, True, (255, 255, 255))
                vs_text = self.font_big.render("VS", True, (255, 0, 0))
                
                self.screen.blit(title, (self.width//2 - title.get_width()//2, self.height//4))
                self.screen.blit(name1_text, (self.width//4 - name1_text.get_width()//2, self.height//2))
                self.screen.blit(vs_text, (self.width//2 - vs_text.get_width()//2, self.height//2))
                self.screen.blit(name2_text, (3*self.width//4 - name2_text.get_width()//2, self.height//2))
                
                self._write_frame()
            self.logger.info("Intro sequence created successfully")
        except Exception as e:
            self.logger.error(f"Error creating intro: {str(e)}", exc_info=True)
            raise

    def _apply_color_overlay(self, original_surface, overlay_color):
        """
        Applies a semi-transparent color overlay to the original surface
        """
        # Create a copy of the original surface
        result = original_surface.copy()
        
        # Create overlay surface with alpha
        overlay = pygame.Surface(original_surface.get_size(), pygame.SRCALPHA)
        overlay.fill(overlay_color)
        
        # Blit the overlay onto the result surface
        result.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        
        return result

    def render_game(self, game, frame_duration=1):
        self.logger.debug(f"Rendering game state: {game.board}")
        frames = int(frame_duration * self.fps)
        try:
            for _ in range(frames):
                self.screen.fill((0, 0, 0))
                
                # Draw tinted board
                self.screen.blit(self.board_img, (self.board_x, self.board_y))
                
                # Draw golden grid lines
                board_width = self.board_img.get_width()
                board_height = self.board_img.get_height()
                
                # Vertical lines
                for i in range(1, 3):
                    x = self.board_x + i * (board_width // 3)
                    pygame.draw.line(self.screen, self.GOLDEN,
                                   (x, self.board_y),
                                   (x, self.board_y + board_height),
                                   3)  # Increased thickness for better visibility
                
                # Horizontal lines
                for i in range(1, 3):
                    y = self.board_y + i * (board_height // 3)
                    pygame.draw.line(self.screen, self.GOLDEN,
                                   (self.board_x, y),
                                   (self.board_x + board_width, y),
                                   3)  # Increased thickness for better visibility
                
                # Draw pieces
                for i, piece in enumerate(game.board):
                    if piece == 'X':
                        self.screen.blit(self.x_img, self.cell_positions[i])
                    elif piece == 'O':
                        self.screen.blit(self.o_img, self.cell_positions[i])
                
                # Draw winning line
                if game.winning_line:
                    self.logger.debug(f"Drawing winning line: {game.winning_line}")
                    start_pos = (
                        self.cell_positions[game.winning_line[0]][0] + self.x_img.get_width()//2,
                        self.cell_positions[game.winning_line[0]][1] + self.x_img.get_height()//2
                    )
                    end_pos = (
                        self.cell_positions[game.winning_line[2]][0] + self.x_img.get_width()//2,
                        self.cell_positions[game.winning_line[2]][1] + self.x_img.get_height()//2
                    )
                    pygame.draw.line(self.screen, self.BLOOD_RED, start_pos, end_pos, 5)
                
                self._write_frame()
        except Exception as e:
            self.logger.error(f"Error rendering game: {str(e)}", exc_info=True)
            raise

    def create_round_intro(self, round_num, model1_score, model2_score, ties, duration_seconds=3):
        self.logger.info(f"Creating round {round_num} intro. Scores: {model1_score}-{model2_score} (Ties: {ties})")
        frames = int(duration_seconds * self.fps)
        try:
            for frame in range(frames):
                self.screen.fill((0, 0, 0))
                round_text = self.font_big.render(f"Round {round_num}", True, (255, 255, 255))
                score_text = self.font.render(f"Score: {model1_score} - {model2_score} (Ties: {ties})", True, (255, 255, 255))
                
                self.screen.blit(round_text, (self.width//2 - round_text.get_width()//2, self.height//3))
                self.screen.blit(score_text, (self.width//2 - score_text.get_width()//2, self.height//2))
                
                self._write_frame()
        except Exception as e:
            self.logger.error(f"Error creating round intro: {str(e)}", exc_info=True)
            raise
    
    def create_winner_announcement(self, winner_name, score1, score2, ties, duration_seconds=5):
        self.logger.info(f"Creating winner announcement. Winner: {winner_name}, Final score: {score1}-{score2} (Ties: {ties})")
        frames = int(duration_seconds * self.fps)
        try:
            for frame in range(frames):
                self.screen.fill((0, 0, 0))
                
                if winner_name == "Tie":
                    title = self.font_big.render("It's a Tie!", True, (255, 215, 0))
                else:
                    title = self.font_big.render(f"{winner_name} Wins!", True, (255, 215, 0))
                
                score_text = self.font.render(f"Final Score: {score1} - {score2} (Ties: {ties})", True, (255, 255, 255))
                
                self.screen.blit(title, (self.width//2 - title.get_width()//2, self.height//3))
                self.screen.blit(score_text, (self.width//2 - score_text.get_width()//2, self.height//2))
                
                self._write_frame()
        except Exception as e:
            self.logger.error(f"Error creating winner announcement: {str(e)}", exc_info=True)
            raise

    def start_video(self, output_path):
        self.logger.info(f"Starting video writing to {output_path}")
        try:
            self.video_writer = cv2.VideoWriter(
                output_path,
                self.fourcc,
                self.fps,
                (self.width, self.height)
            )
        except Exception as e:
            self.logger.error(f"Error starting video writer: {str(e)}", exc_info=True)
            raise

    def _write_frame(self):
        try:
            view = pygame.surfarray.array3d(self.screen)
            view = view.transpose([1, 0, 2])
            view = cv2.cvtColor(view, cv2.COLOR_RGB2BGR)
            self.video_writer.write(view)
        except Exception as e:
            self.logger.error(f"Error writing frame: {str(e)}", exc_info=True)
            raise

    def close(self):
        self.logger.info("Closing video maker")
        if self.video_writer:
            self.video_writer.release()
        pygame.quit()

def play_game(model1_starts):
    logger = logging.getLogger(__name__)
    logger.info(f"Starting new game. Model 1 starts: {model1_starts}")
    
    game = TicTacToeGame(model1_starts)
    
    while not game.game_over:
        valid_moves = game.get_valid_moves()
        if not valid_moves:
            logger.info("Game ended in a tie - no valid moves remaining")
            break
            
        move = random.choice(valid_moves)
        logger.debug(f"Player {game.current_player} making move at position {move}")
        game.make_move(move, game.current_player)
        
    logger.info(f"Game ended. Winner: {game.winner if game.winner else 'Tie'}")
    
    if game.winner == 'X':
        return 1  # Model 1 wins
    elif game.winner == 'O':
        return 2  # Model 2 wins
    else:
        return 0  # Tie

def main():
    logger = logging.getLogger(__name__)
    logger.info("Starting tournament")
    
    # Configuration
    MODEL1_NAME = "llama-3.1-70b-versatile"
    MODEL2_NAME = "llama-3.1-8b-instant"
    NUM_GAMES = 1
    
    model1_clean = MODEL1_NAME.replace("-", "_").replace(".", "_")
    model2_clean = MODEL2_NAME.replace("-", "_").replace(".", "_")
    OUTPUT_PATH = f"tournament_{model1_clean}_vs_{model2_clean}_{NUM_GAMES}games.mp4"
    
    logger.info(f"Tournament config: {MODEL1_NAME} vs {MODEL2_NAME}, {NUM_GAMES} games")
    
    try:
        # Initialize video maker
        video_maker = TournamentVideoMaker()
        video_maker.start_video(OUTPUT_PATH)
        
        # Create intro
        video_maker.create_intro(MODEL1_NAME, MODEL2_NAME)
        
        # Play games and record
        score1 = score2 = ties = 0
        for game_num in range(NUM_GAMES):
            logger.info(f"Starting game {game_num + 1} of {NUM_GAMES}")
            model1_starts = game_num % 2 == 0
            
            video_maker.create_round_intro(game_num + 1, score1, score2, ties)
            
            game = TicTacToeGame(model1_starts)
            while not game.game_over:
                valid_moves = game.get_valid_moves()
                if not valid_moves:
                    logger.info("No valid moves remaining")
                    break
                    
                move = random.choice(valid_moves)
                logger.debug(f"Move selected: {move}")
                game.make_move(move, game.current_player)
                video_maker.render_game(game, frame_duration=0.5)
            
            # Update scores
            if game.winner == 'X':
                score1 += 1
                logger.info(f"Game {game_num + 1} winner: Model 1")
            elif game.winner == 'O':
                score2 += 1
                logger.info(f"Game {game_num + 1} winner: Model 2")
            else:
                ties += 1
                logger.info(f"Game {game_num + 1} ended in tie")
            
            video_maker.render_game(game, frame_duration=2)
        
        # Show winner
        if score1 > score2:
            winner_name = MODEL1_NAME
        elif score2 > score1:
            winner_name = MODEL2_NAME
        else:
            winner_name = "Tie"
        
        logger.info(f"Tournament ended. Winner: {winner_name}")
        logger.info(f"Final scores - {MODEL1_NAME}: {score1}, {MODEL2_NAME}: {score2}, Ties: {ties}")
        
        video_maker.create_winner_announcement(winner_name, score1, score2, ties)
        
        # Cleanup
        video_maker.close()
        logger.info(f"Tournament video created successfully: {OUTPUT_PATH}")
        
    except Exception as e:
        logger.error(f"Tournament failed: {str(e)}", exc_info=True)
        raise
    finally:
        logger.info("Tournament process completed")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.getLogger(__name__).error("Fatal error in main", exc_info=True)
        raise