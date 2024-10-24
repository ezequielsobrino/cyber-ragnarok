# main.py
import logging
from datetime import datetime
import os
import random
from brains.providers.factory import ProviderFactory
from brains.tic_tac_toe_brain import TicTacToeBrain
from games.tic_tac_toe import TicTacToeGame
from video.video_maker import VideoMaker
from config.settings import MatchConfig, VideoConfig

class AIMatch:
    def __init__(self, config: MatchConfig):
        self.config = config
        self.logger = self._setup_logger()
        self.video_maker = None
        self.model1_brain = None
        self.model2_brain = None
        self.score1 = 0
        self.score2 = 0
        self.ties = 0

    def _setup_logger(self):
        logger = logging.getLogger(__name__)
        if not logger.handlers:
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler(f'match_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
                    logging.StreamHandler()
                ]
            )
        return logger

    def _initialize_brains(self):
        provider_factory = ProviderFactory()
        
        # Create providers with specific model names and types
        model1_provider = provider_factory.create_provider(
            self.config.MODEL1_NAME,
            self.config.MODEL1_PROVIDER
        )
        model2_provider = provider_factory.create_provider(
            self.config.MODEL2_NAME,
            self.config.MODEL2_PROVIDER
        )
        
        self.model1_brain = TicTacToeBrain(llm_provider=model1_provider)
        self.model2_brain = TicTacToeBrain(llm_provider=model2_provider)

    def _get_output_path(self):
        model1_clean = self.config.MODEL1_NAME.replace("-", "_").replace(".", "_")
        model2_clean = self.config.MODEL2_NAME.replace("-", "_").replace(".", "_")
        return f"match_{model1_clean}_vs_{model2_clean}_{self.config.NUM_GAMES}games.mp4"

    def _play_single_game(self, game_num):
        self.logger.info(f"Starting game {game_num + 1} of {self.config.NUM_GAMES}")
        self.logger.info(f"Model 1 ({self.config.MODEL1_NAME}) vs Model 2 ({self.config.MODEL2_NAME})")
        
        model1_starts = game_num % 2 == 0
        
        self.video_maker.create_round_intro(
            game_num + 1, 
            self.score1, 
            self.score2, 
            self.ties,
            self.config.MODEL1_NAME,
            self.config.MODEL2_NAME,
            duration_seconds=VideoConfig.ROUND_INTRO_DURATION
        )
        
        game = TicTacToeGame(model1_starts)
        while not game.game_over:
            self._make_move(game)
            self.video_maker.render_game(
                game,
                self.config.MODEL1_NAME,
                self.config.MODEL2_NAME,
                frame_duration=VideoConfig.MOVE_DURATION
            )
            
        self._update_scores(game)
        self.video_maker.render_game(
            game,
            self.config.MODEL1_NAME,
            self.config.MODEL2_NAME,
            frame_duration=VideoConfig.END_GAME_DURATION
        )
        
    def _make_move(self, game):
        valid_moves = game.get_valid_moves()
        if not valid_moves:
            return

        current_brain = self.model1_brain if game.current_player == 'X' else self.model2_brain
        current_model = self.config.MODEL1_NAME if game.current_player == 'X' else self.config.MODEL2_NAME
        
        self.logger.info(f"{current_model}'s turn")
        move = current_brain.get_move(game.board, game.current_player)
        
        if move not in valid_moves:
            self.logger.warning(f"Invalid move {move} suggested by {current_model}. Using random move instead.")
            move = random.choice(valid_moves)
        
        game.make_move(move, game.current_player)
        self.logger.info(f"{current_model} placed at position {move}")

    def _update_scores(self, game):
        if game.winner == 'X':
            self.score1 += 1
            self.logger.info(f"Winner: {self.config.MODEL1_NAME}")
        elif game.winner == 'O':
            self.score2 += 1
            self.logger.info(f"Winner: {self.config.MODEL2_NAME}")
        else:
            self.ties += 1
            self.logger.info("Game ended in tie")

    def _determine_winner(self):
        if self.score1 > self.score2:
            return self.config.MODEL1_NAME
        elif self.score2 > self.score1:
            return self.config.MODEL2_NAME
        return "Tie"

    def run(self):
        self.logger.info(f"Starting match between {self.config.MODEL1_NAME} ({self.config.MODEL1_PROVIDER.value}) and " +
                      f"{self.config.MODEL2_NAME} ({self.config.MODEL2_PROVIDER.value})")
        self.logger.info(f"Number of games: {self.config.NUM_GAMES}")
        
        try:
            self._initialize_brains()
            output_path = self._get_output_path()
            
            self.video_maker = VideoMaker(
                width=VideoConfig.WIDTH,
                height=VideoConfig.HEIGHT,
                fps=VideoConfig.FPS
            )
            self.video_maker.start_video(output_path)
            self.video_maker.create_intro(
                self.config.MODEL1_NAME,
                self.config.MODEL2_NAME,
                duration_seconds=VideoConfig.INTRO_DURATION
            )
            
            for game_num in range(self.config.NUM_GAMES):
                self._play_single_game(game_num)
            
            winner_name = self._determine_winner()
            self.logger.info(f"Match ended. Winner: {winner_name}")
            self.logger.info(f"Final scores - {self.config.MODEL1_NAME}: {self.score1}, " +
                         f"{self.config.MODEL2_NAME}: {self.score2}, Ties: {self.ties}")
            
            self.video_maker.create_winner_announcement(
                winner_name,
                self.score1,
                self.score2,
                self.ties,
                self.config.MODEL1_NAME,
                self.config.MODEL2_NAME,
                duration_seconds=VideoConfig.WINNER_ANNOUNCEMENT_DURATION
            )
            self.video_maker.close()
            
            self.logger.info(f"Match video created successfully: {output_path}")
            
        except Exception as e:
            self.logger.error(f"Match failed: {str(e)}", exc_info=True)
            raise
        finally:
            self.logger.info("Match process completed")

if __name__ == "__main__":
    try:
        config = MatchConfig()
        match = AIMatch(config)
        match.run()
    except Exception as e:
        logging.getLogger(__name__).error("Fatal error in main", exc_info=True)
        raise