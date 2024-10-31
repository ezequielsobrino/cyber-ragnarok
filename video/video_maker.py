# video/video_maker.py
import cv2
import os
import pygame
import logging
from datetime import datetime
from moviepy.editor import VideoFileClip, AudioFileClip
from config.settings import GameType
from screens.intro_screen import IntroScreen
from screens.game_screen import GameScreen
from screens.round_screen import RoundScreen
from screens.winner_screen import WinnerScreen
from assets.assets_manager import AssetsManager

class VideoMaker:
    def __init__(self, width=1280, height=720, fps=30, game_type=GameType.TIC_TAC_TOE):
        self.logger = logging.getLogger(__name__)
        self.width = width
        self.height = height
        self.fps = fps
        self.game_type = game_type
        
        # Initialize pygame
        if not pygame.get_init():
            pygame.init()
        
        # Set up the display (hidden)
        if pygame.display.get_surface() is None:
            pygame.display.set_mode((width, height), pygame.HIDDEN)
        
        # Initialize assets and screens
        self.assets_manager = AssetsManager("assets", width, height)
        self._init_screens()
        
        # Initialize video writing
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.temp_video_path = f"temp_video_{timestamp}.mp4"
        self.final_output_path = None
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video_writer = None
    
    def _init_screens(self):
        self.intro_screen = IntroScreen(self.width, self.height, self.fps, self.assets_manager)
        self.game_screen = GameScreen(self.width, self.height, self.fps, self.assets_manager)
        self.round_screen = RoundScreen(self.width, self.height, self.fps, self.assets_manager)
        self.winner_screen = WinnerScreen(self.width, self.height, self.fps, self.assets_manager)
    
    def start_video(self, output_path):
        self.final_output_path = output_path
        self.video_writer = cv2.VideoWriter(
            self.temp_video_path,
            self.fourcc,
            self.fps,
            (self.width, self.height)
        )
    
    def _write_frame(self, surface):
        view = pygame.surfarray.array3d(surface)
        view = view.transpose([1, 0, 2])
        view = cv2.cvtColor(view, cv2.COLOR_RGB2BGR)
        self.video_writer.write(view)

    def create_intro(self, model1_name, model2_name, duration_seconds=5):
        frames = int(duration_seconds * self.fps)
        for _ in range(frames):
            surface = self.intro_screen.render(
                model1_name,
                model2_name,
                self.game_type
            )
            self._write_frame(surface)
    
    def render_game(self, game, model1_name, model2_name, model1_metrics=None, model2_metrics=None, frame_duration=1):
        frames = int(frame_duration * self.fps)
        for _ in range(frames):
            surface = self.game_screen.render(
                game=game,
                model1_name=model1_name,
                model2_name=model2_name,
                model1_metrics=model1_metrics,
                model2_metrics=model2_metrics
            )
            self._write_frame(surface)
    
    def create_round_intro(self, round_num, model1_score, model2_score, ties, model1_name, model2_name, duration_seconds=3):
        frames = int(duration_seconds * self.fps)
        for _ in range(frames):
            surface = self.round_screen.render(
                round_num,
                model1_score,
                model2_score,
                ties,
                model1_name,
                model2_name
            )
            self._write_frame(surface)
    
    def create_winner_announcement(self, winner_name, score1, score2, ties, model1_name, model2_name, duration_seconds=5):
        frames = int(duration_seconds * self.fps)
        for _ in range(frames):
            surface = self.winner_screen.render(
                winner_name,
                score1,
                score2,
                ties,
                model1_name,
                model2_name
            )
            self._write_frame(surface)
    
    def close(self):
        self.logger.info("Closing video maker and finalizing video with audio")
        try:
            # Close video writer
            if self.video_writer:
                self.video_writer.release()
            
            # Add background music using moviepy
            video = VideoFileClip(self.temp_video_path)
            background_music = AudioFileClip(os.path.join("assets", "video_music.mp3"))
            
            # Loop the music if it's shorter than the video
            if background_music.duration < video.duration:
                repeats = int(video.duration / background_music.duration) + 1
                background_music = AudioFileClip(os.path.join("assets", "video_music.mp3")).loop(repeats)
            
            # Trim music if it's longer than video
            background_music = background_music.subclip(0, video.duration)
            
            # Set music volume
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
            
            # Quit pygame
            pygame.quit()
            
        except Exception as e:
            self.logger.error(f"Error during video finalization: {str(e)}", exc_info=True)
            raise