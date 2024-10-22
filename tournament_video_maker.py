import pygame
import cv2
import random
import logging
from datetime import datetime
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip
from pydub import AudioSegment
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'tournament_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)

class TicTacToeGame:
    def __init__(self, model1_starts=True):
        self.board = [' '] * 9
        self.current_player = 'X' if model1_starts else 'O'
        self.game_over = False
        self.winner = None
        self.winning_line = None

    def get_valid_moves(self):
        return [i for i, piece in enumerate(self.board) if piece == ' ']

    def make_move(self, position, player):
        if self.board[position] == ' ' and not self.game_over:
            self.board[position] = player
            if self._check_winner(player):
                self.game_over = True
                self.winner = player
            elif not self.get_valid_moves():
                self.game_over = True
            else:
                self.current_player = 'O' if player == 'X' else 'X'
            return True
        return False

    def _check_winner(self, player):
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontal
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Vertical
            [0, 4, 8], [2, 4, 6]              # Diagonal
        ]
        
        for line in win_combinations:
            if all(self.board[i] == player for i in line):
                self.winning_line = line
                return True
        return False

class TournamentVideoMaker:
    def __init__(self, width=1920, height=1080, fps=30):
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Initializing TournamentVideoMaker with dimensions {width}x{height} at {fps} FPS")
        
        # Initialize Pygame
        pygame.init()
        
        # Initialize temporary file paths
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.temp_video_path = f"temp_video_{timestamp}.mp4"
        self.final_output_path = None
        
        self.width = width
        self.height = height
        self.fps = fps
        self.font_size = int(height * 0.05)
        self.font_large = int(height * 0.08)
        
        self.WOOD_COLOR = (222, 184, 135, 128)
        self.NATURE_GREEN = (76, 153, 0, 255)
        self.SEA_BLUE = (0, 105, 148, 255)
        self.BLOOD_RED = (139, 0, 0)
        self.GOLDEN = (255, 215, 0)
        self.TEXT_COLOR = (255, 255, 255)
        
        try:
            pygame.init()
            pygame.display.set_mode((width, height))
            self.screen = pygame.Surface((width, height))
            self.clock = pygame.time.Clock()
            self.font = pygame.font.Font(None, self.font_size)
            self.font_big = pygame.font.Font(None, self.font_large)
            
            # Load and tint images
            original_board = pygame.image.load('tic_tac_toe_board.png').convert_alpha()
            original_x = pygame.image.load('x_image.png').convert_alpha()
            original_o = pygame.image.load('o_image.png').convert_alpha()
            
            self.board_img = self._apply_color_overlay(original_board, self.WOOD_COLOR)
            self.x_img = self._apply_color_overlay(original_x, self.NATURE_GREEN)
            self.o_img = self._apply_color_overlay(original_o, self.SEA_BLUE)
            
            board_scale = min(width * 0.4 / self.board_img.get_width(), 
                            height * 0.6 / self.board_img.get_height())
            self.board_img = pygame.transform.scale(self.board_img, 
                (int(self.board_img.get_width() * board_scale),
                 int(self.board_img.get_height() * board_scale)))
            
            piece_size = int(min(self.board_img.get_width(), self.board_img.get_height()) * 0.25)
            self.x_img = pygame.transform.scale(self.x_img, (piece_size, piece_size))
            self.o_img = pygame.transform.scale(self.o_img, (piece_size, piece_size))
            
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
            
            self.model1_img = None
            self.model2_img = None
            self.model1_name = None
            self.model2_name = None
            
            self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.video_writer = None
            
        except Exception as e:
            self.logger.error(f"Error during initialization: {str(e)}", exc_info=True)
            raise

    def _apply_color_overlay(self, original_surface, overlay_color):
        result = original_surface.copy()
        overlay = pygame.Surface(original_surface.get_size(), pygame.SRCALPHA)
        overlay.fill(overlay_color)
        result.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return result

    def _load_model_image(self, model_name):
        formatted_name = model_name.replace("-", "_").replace(".", "_") + ".png"
        try:
            image = pygame.image.load(formatted_name).convert_alpha()
            target_height = self.height * 0.8
            aspect_ratio = image.get_width() / image.get_height()
            target_width = int(target_height * aspect_ratio)
            
            max_width = self.width * 0.2
            if target_width > max_width:
                target_width = max_width
                target_height = int(target_width / aspect_ratio)
            
            return pygame.transform.scale(image, (target_width, int(target_height)))
        except Exception as e:
            self.logger.error(f"Error loading model image {formatted_name}: {str(e)}")
            placeholder = pygame.Surface((int(self.width * 0.2), int(self.height * 0.8)))
            placeholder.fill((50, 50, 50))
            return placeholder

    def _draw_model_names(self):
        """Helper method to consistently draw model names under images"""
        if self.model1_name and self.model2_name:
            margin = 20
            
            # Calculate positions for model 1 name
            name1_text = self.font.render(self.model1_name, True, self.TEXT_COLOR)
            name1_x = margin + (self.model1_img.get_width() - name1_text.get_width()) // 2
            name1_y = (self.height + self.model1_img.get_height()) // 2 + 20
            
            # Calculate positions for model 2 name
            name2_text = self.font.render(self.model2_name, True, self.TEXT_COLOR)
            name2_x = self.width - self.model2_img.get_width() - margin + (self.model2_img.get_width() - name2_text.get_width()) // 2
            name2_y = (self.height + self.model2_img.get_height()) // 2 + 20
            
            # Draw the names
            self.screen.blit(name1_text, (name1_x, name1_y))
            self.screen.blit(name2_text, (name2_x, name2_y))

    def _draw_model_images(self, winner=None, final_winner=False):
        if self.model1_img and self.model2_img:
            img_y = (self.height - self.model1_img.get_height()) // 2
            margin = 20
            border_thickness = 4

            # Model 1 borders
            border_rect_1 = pygame.Rect(
                margin - border_thickness,
                img_y - border_thickness,
                self.model1_img.get_width() + (border_thickness * 2),
                self.model1_img.get_height() + (border_thickness * 2)
            )
            pygame.draw.rect(self.screen, self.NATURE_GREEN, border_rect_1, border_thickness)

            if winner == 'X':
                winner_rect_1 = pygame.Rect(
                    margin - (border_thickness * 2),
                    img_y - (border_thickness * 2),
                    self.model1_img.get_width() + (border_thickness * 4),
                    self.model1_img.get_height() + (border_thickness * 4)
                )
                pygame.draw.rect(self.screen, self.GOLDEN, winner_rect_1, border_thickness)

                if final_winner:
                    final_rect_1 = pygame.Rect(
                        margin - (border_thickness * 3),
                        img_y - (border_thickness * 3),
                        self.model1_img.get_width() + (border_thickness * 6),
                        self.model1_img.get_height() + (border_thickness * 6)
                    )
                    pygame.draw.rect(self.screen, self.GOLDEN, final_rect_1, border_thickness)

            # Model 2 borders
            border_rect_2 = pygame.Rect(
                self.width - self.model2_img.get_width() - margin - border_thickness,
                img_y - border_thickness,
                self.model2_img.get_width() + (border_thickness * 2),
                self.model2_img.get_height() + (border_thickness * 2)
            )
            pygame.draw.rect(self.screen, self.SEA_BLUE, border_rect_2, border_thickness)

            if winner == 'O':
                winner_rect_2 = pygame.Rect(
                    self.width - self.model2_img.get_width() - margin - (border_thickness * 2),
                    img_y - (border_thickness * 2),
                    self.model2_img.get_width() + (border_thickness * 4),
                    self.model2_img.get_height() + (border_thickness * 4)
                )
                pygame.draw.rect(self.screen, self.GOLDEN, winner_rect_2, border_thickness)

                if final_winner:
                    final_rect_2 = pygame.Rect(
                        self.width - self.model2_img.get_width() - margin - (border_thickness * 3),
                        img_y - (border_thickness * 3),
                        self.model2_img.get_width() + (border_thickness * 6),
                        self.model2_img.get_height() + (border_thickness * 6)
                    )
                    pygame.draw.rect(self.screen, self.GOLDEN, final_rect_2, border_thickness)

            # Draw the actual images
            self.screen.blit(self.model1_img, (margin, img_y))
            self.screen.blit(self.model2_img, (self.width - self.model2_img.get_width() - margin, img_y))
            
            # Draw names under images
            self._draw_model_names()

    def create_intro(self, model1_name, model2_name, duration_seconds=5):
        self.logger.info(f"Creating intro sequence for {model1_name} vs {model2_name}")
        
        self.model1_name = model1_name
        self.model2_name = model2_name
        self.model1_img = self._load_model_image(model1_name)
        self.model2_img = self._load_model_image(model2_name)
        
        frames = int(duration_seconds * self.fps)
        try:
            for frame in range(frames):
                self.screen.fill((0, 0, 0))
                self._draw_model_images()
                
                title = self.font_big.render("Cyber Ragnarok - Tic Tac Toe", True, self.TEXT_COLOR)
                self.screen.blit(title, (self.width//2 - title.get_width()//2, self.height//8))
                
                vs_text = self.font_big.render("VS", True, (255, 0, 0))
                vs_y = self.height * 0.75
                self.screen.blit(vs_text, (self.width//2 - vs_text.get_width()//2, vs_y))
                
                self._write_frame()
        except Exception as e:
            self.logger.error(f"Error creating intro: {str(e)}", exc_info=True)
            raise

    def render_game(self, game, frame_duration=1):
        self.logger.debug(f"Rendering game state: {game.board}")
        frames = int(frame_duration * self.fps)
        try:
            for _ in range(frames):
                self.screen.fill((0, 0, 0))
                
                winner = game.winner if game.game_over else None
                self._draw_model_images(winner, False)
                
                self.screen.blit(self.board_img, (self.board_x, self.board_y))
                
                board_width = self.board_img.get_width()
                board_height = self.board_img.get_height()
                
                # Vertical lines
                for i in range(1, 3):
                    x = self.board_x + i * (board_width // 3)
                    pygame.draw.line(self.screen, self.GOLDEN,
                                (x, self.board_y),
                                (x, self.board_y + board_height),
                                3)
                
                # Horizontal lines
                for i in range(1, 3):
                    y = self.board_y + i * (board_height // 3)
                    pygame.draw.line(self.screen, self.GOLDEN,
                                (self.board_x, y),
                                (self.board_x + board_width, y),
                                3)
                
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
        self.logger.info(f"Creating round {round_num} intro")
        
        frames = int(duration_seconds * self.fps)
        try:
            for frame in range(frames):
                self.screen.fill((0, 0, 0))
                
                self._draw_model_images()
                
                round_text = self.font_big.render(f"Round {round_num}", True, self.TEXT_COLOR)
                score_text = self.font.render(f"{model1_score} - {model2_score}", True, self.TEXT_COLOR)
                ties_text = self.font.render(f"Ties: {ties}", True, self.TEXT_COLOR)
                
                self.screen.blit(round_text, (self.width//2 - round_text.get_width()//2, self.height//3))
                self.screen.blit(score_text, (self.width//2 - score_text.get_width()//2, self.height//2))
                self.screen.blit(ties_text, (self.width//2 - ties_text.get_width()//2, self.height * 0.8))
                
                self._write_frame()
        except Exception as e:
            self.logger.error(f"Error creating round intro: {str(e)}", exc_info=True)
            raise
    
    def create_winner_announcement(self, winner_name, score1, score2, ties, duration_seconds=5):
        self.logger.info(f"Creating winner announcement for {winner_name}")
        
        frames = int(duration_seconds * self.fps)
        try:
            for frame in range(frames):
                self.screen.fill((0, 0, 0))
                
                winner = 'X' if winner_name == self.model1_name else 'O' if winner_name == self.model2_name else None
                self._draw_model_images(winner, True)
                
                if winner_name == "Tie":
                    title = self.font_big.render("It's a Tie!", True, (255, 215, 0))
                else:
                    title = self.font_big.render(f"{winner_name} Wins!", True, (255, 215, 0))
                
                score_text = self.font.render(f"Final Score: {score1} - {score2} (Ties: {ties})", True, self.TEXT_COLOR)
                
                self.screen.blit(title, (self.width//2 - title.get_width()//2, self.height//3))
                self.screen.blit(score_text, (self.width//2 - score_text.get_width()//2, self.height//2))
                
                self._write_frame()
        except Exception as e:
            self.logger.error(f"Error creating winner announcement: {str(e)}", exc_info=True)
            raise

    def start_video(self, output_path):
        self.logger.info(f"Starting video writing to {output_path}")
        self.final_output_path = output_path
        try:
            self.video_writer = cv2.VideoWriter(
                self.temp_video_path,
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
        self.logger.info("Closing video maker and finalizing video with audio")
        try:
            # Close video writer
            if self.video_writer:
                self.video_writer.release()
            
            # Add background music using moviepy
            video = VideoFileClip(self.temp_video_path)
            background_music = AudioFileClip("video_music.mp3")
            
            # Loop the music if it's shorter than the video
            if background_music.duration < video.duration:
                repeats = int(video.duration / background_music.duration) + 1
                background_music = AudioFileClip("video_music.mp3").loop(repeats)
            
            # Trim music if it's longer than video
            background_music = background_music.subclip(0, video.duration)
            
            # Set music volume to 0.3 (30% of original volume)
            background_music = background_music.volumex(0.3)
            
            # Combine video with background music
            final_video = video.set_audio(background_music)
            final_video.write_videofile(self.final_output_path, codec='libx264')
            
            # Cleanup
            video.close()
            background_music.close()
            
            # Remove temporary files
            try:
                os.remove(self.temp_video_path)
            except Exception as e:
                self.logger.warning(f"Error removing temporary files: {str(e)}")
            
            pygame.quit()
            
        except Exception as e:
            self.logger.error(f"Error during video finalization: {str(e)}", exc_info=True)
            raise

def main():
    logger = logging.getLogger(__name__)
    logger.info("Starting tournament")
    
    # Configuration
    MODEL1_NAME = "llama-3.1-70b-versatile"
    MODEL2_NAME = "llama-3.1-8b-instant"
    NUM_GAMES = 10
    
    model1_clean = MODEL1_NAME.replace("-", "_").replace(".", "_")
    model2_clean = MODEL2_NAME.replace("-", "_").replace(".", "_")
    OUTPUT_PATH = f"tournament_{model1_clean}_vs_{model2_clean}_{NUM_GAMES}games.mp4"
    
    logger.info(f"Tournament config: {MODEL1_NAME} vs {MODEL2_NAME}, {NUM_GAMES} games")
    
    try:
        video_maker = TournamentVideoMaker()
        video_maker.start_video(OUTPUT_PATH)
        
        video_maker.create_intro(MODEL1_NAME, MODEL2_NAME)
        
        score1 = score2 = ties = 0
        for game_num in range(NUM_GAMES):
            logger.info(f"Starting game {game_num + 1} of {NUM_GAMES}")
            model1_starts = game_num % 2 == 0
            
            video_maker.create_round_intro(game_num + 1, score1, score2, ties)
            
            game = TicTacToeGame(model1_starts)
            while not game.game_over:
                valid_moves = game.get_valid_moves()
                if not valid_moves:
                    break
                    
                move = random.choice(valid_moves)
                game.make_move(move, game.current_player)
                video_maker.render_game(game, frame_duration=0.5)
            
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
        
        if score1 > score2:
            winner_name = MODEL1_NAME
        elif score2 > score1:
            winner_name = MODEL2_NAME
        else:
            winner_name = "Tie"
        
        logger.info(f"Tournament ended. Winner: {winner_name}")
        logger.info(f"Final scores - {MODEL1_NAME}: {score1}, {MODEL2_NAME}: {score2}, Ties: {ties}")
        
        video_maker.create_winner_announcement(winner_name, score1, score2, ties)
        
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