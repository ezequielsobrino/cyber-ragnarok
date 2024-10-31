import logging
from datetime import datetime
import os
import random
from brains.providers.factory import ProviderFactory
from brains.tic_tac_toe_brain import TicTacToeBrain
from brains.checkers_brain import CheckersBrain
from games.tic_tac_toe import TicTacToeGame
from games.checkers import CheckersGame
from video.video_maker import VideoMaker
from config.settings import MatchConfig, VideoConfig, GameType
from dataclasses import dataclass

@dataclass
class ModelMetrics:
    total_cost: float = 0
    total_tokens: int = 0
    total_time: float = 0
    total_moves: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    valid_moves: int = 0
    invalid_moves: int = 0
    fallback_moves: int = 0

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
        
        # Métricas separadas por modelo
        self.model1_metrics = ModelMetrics()
        self.model2_metrics = ModelMetrics()
        
        # Map game types to their respective classes
        self.game_classes = {
            GameType.TIC_TAC_TOE: (TicTacToeGame, TicTacToeBrain),
            GameType.CHECKERS: (CheckersGame, CheckersBrain)
        }

    def _setup_logger(self):
        logs_dir = 'logs'
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = os.path.join(logs_dir, f'match_{timestamp}.log')

        logger = logging.getLogger(__name__)
        if not logger.handlers:
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler(log_filename),
                    logging.StreamHandler()
                ]
            )
            logger.info(f"Log file created at: {log_filename}")
        
        return logger

    def _initialize_brains(self):
        provider_factory = ProviderFactory()
        
        model1_provider = provider_factory.create_provider(
            self.config.MODEL1_NAME,
            self.config.MODEL1_PROVIDER
        )
        model2_provider = provider_factory.create_provider(
            self.config.MODEL2_NAME,
            self.config.MODEL2_PROVIDER
        )
        
        game_class, brain_class = self.game_classes[self.config.GAME_TYPE]
        
        self.model1_brain = brain_class(llm_provider=model1_provider)
        self.model2_brain = brain_class(llm_provider=model2_provider)

    def _get_output_path(self):
        model1_clean = self.config.MODEL1_NAME.replace("-", "_").replace(".", "_")
        model2_clean = self.config.MODEL2_NAME.replace("-", "_").replace(".", "_")
        game_type = self.config.GAME_TYPE.value
        return f"{game_type}_match_{model1_clean}_vs_{model2_clean}_{self.config.NUM_GAMES}games.mp4"

    def _update_metrics(self, response, metrics: ModelMetrics, is_valid_move: bool, is_fallback: bool):
        metrics.total_cost += response.cost
        metrics.total_tokens += response.total_tokens
        metrics.total_time += response.response_time
        metrics.total_moves += 1
        metrics.input_tokens += response.input_tokens
        metrics.output_tokens += response.output_tokens
        
        if is_valid_move:
            metrics.valid_moves += 1
        else:
            metrics.invalid_moves += 1
        
        if is_fallback:
            metrics.fallback_moves += 1

    def _make_move(self, game):
        is_model1 = game.current_player in ['X', 'b']
        current_brain = self.model1_brain if is_model1 else self.model2_brain
        current_model = self.config.MODEL1_NAME if is_model1 else self.config.MODEL2_NAME
        current_metrics = self.model1_metrics if is_model1 else self.model2_metrics
        
        self.logger.info(f"{current_model}'s turn")
        
        if self.config.GAME_TYPE == GameType.CHECKERS:
            movable_pieces = []
            for i in range(64):
                if game.board[i].lower() == game.current_player:
                    valid_moves = game.get_valid_moves(i)
                    if valid_moves:
                        movable_pieces.append(i)
            
            if not movable_pieces:
                return
            
            response = current_brain.get_move(game.board, game.current_player)
            
            self.logger.info(
                f"LLM Metrics - Tokens: {response.input_tokens}/{response.output_tokens} "
                f"(total: {response.total_tokens}), Cost: ${response.cost:.2e}, "
            )
            
            if response.move is None:
                self._update_metrics(response, current_metrics, False, True)
                return
                
            start, target = response.move
            valid_moves = game.get_valid_moves(start)
            valid_targets = [m[0] for m in valid_moves]
            
            is_valid = start in movable_pieces and target in valid_targets
            
            if is_valid:
                game.make_move(start, target)
                self.logger.info(f"{current_model} moved piece from {start} to {target}")
            else:
                start = random.choice(movable_pieces)
                valid_moves = game.get_valid_moves(start)
                target, _ = random.choice(valid_moves)
                game.make_move(start, target)
                self.logger.warning(
                    f"Invalid move suggested. Using random move from {start} to {target} instead. "
                    f"Original response: {response.raw_content}"
                )
            
            self._update_metrics(response, current_metrics, is_valid, not is_valid)
        
        else:  # TIC_TAC_TOE
            valid_moves = game.get_valid_moves()
            if not valid_moves:
                return
                
            response = current_brain.get_move(game.board, game.current_player)
            
            self.logger.info(
                f"LLM Metrics - Tokens: {response.input_tokens}/{response.output_tokens} "
                f"(total: {response.total_tokens}), Cost: ${response.cost:.2e}, "
                f"Time: {response.response_time:.3f}s"
            )
            
            is_valid = response.move in valid_moves
            
            if is_valid:
                game.make_move(response.move, game.current_player)
                self.logger.info(f"{current_model} placed at position {response.move}")
            else:
                move = random.choice(valid_moves)
                game.make_move(move, game.current_player)
                self.logger.warning(
                    f"Invalid move suggested. Using random move {move} instead. "
                    f"Original response: {response.raw_content}"
                )
            
            self._update_metrics(response, current_metrics, is_valid, response.is_fallback)

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
        
        game_class = self.game_classes[self.config.GAME_TYPE][0]
        game = game_class(model1_starts)
        
        while not game.game_over:
            self._make_move(game)
            self.video_maker.render_game(
                game=game,
                model1_name=self.config.MODEL1_NAME,
                model2_name=self.config.MODEL2_NAME,
                model1_metrics=self.model1_metrics,
                model2_metrics=self.model2_metrics,
                frame_duration=VideoConfig.MOVE_DURATION
            )
            
        self._update_scores(game)
        self.video_maker.render_game(
            game=game,
            model1_name=self.config.MODEL1_NAME,
            model2_name=self.config.MODEL2_NAME,
            model1_metrics=self.model1_metrics,
            model2_metrics=self.model2_metrics,
            frame_duration=VideoConfig.END_GAME_DURATION
        )

    def _get_metrics_summary(self, metrics: ModelMetrics, model_name: str) -> str:
        if metrics.total_moves == 0:
            return f"{model_name}: No moves made"
        
        avg_time = metrics.total_time / metrics.total_moves
        avg_tokens = metrics.total_tokens / metrics.total_moves
        avg_cost = metrics.total_cost / metrics.total_moves
        
        return (
            f"{model_name}:\n"
            f"  Moves: {metrics.total_moves} "
            f"(Valid: {metrics.valid_moves}, Invalid: {metrics.invalid_moves}, Fallback: {metrics.fallback_moves})\n"
            f"  Tokens: {metrics.total_tokens} "
            f"(Input: {metrics.input_tokens}, Output: {metrics.output_tokens})\n"
            f"  Cost: ${metrics.total_cost:.2e}\n"
            f"  Averages per move:\n"
            f"    - Response Time: {avg_time:.3f}s\n"
            f"    - Tokens: {avg_tokens:.1f}\n"
            f"    - Cost: ${avg_cost:.2e}\n"
            f"  Move Accuracy: {(metrics.valid_moves/metrics.total_moves*100):.1f}%"
        )

    def _update_scores(self, game):
        if game.winner in ['X', 'b']:
            self.score1 += 1
            self.logger.info(f"Winner: {self.config.MODEL1_NAME}")
        elif game.winner in ['O', 'w']:
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
        self.logger.info(f"Starting {self.config.GAME_TYPE.value} match between {self.config.MODEL1_NAME} " +
                    f"({self.config.MODEL1_PROVIDER.value}) and {self.config.MODEL2_NAME} " +
                    f"({self.config.MODEL2_PROVIDER.value})")
        self.logger.info(f"Number of games: {self.config.NUM_GAMES}")
        
        try:     
            self._initialize_brains()
            output_path = self._get_output_path()
            
            self.video_maker = VideoMaker(
                width=VideoConfig.WIDTH,
                height=VideoConfig.HEIGHT,
                fps=VideoConfig.FPS,
                game_type=self.config.GAME_TYPE
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
            self.logger.info(
                f"Final scores - {self.config.MODEL1_NAME}: {self.score1}, "
                f"{self.config.MODEL2_NAME}: {self.score2}, Ties: {self.ties}"
            )

            # Resumen comparativo de métricas
            self.logger.info("\nMatch Summary:")
            self.logger.info("=" * 50)
            self.logger.info(self._get_metrics_summary(self.model1_metrics, self.config.MODEL1_NAME))
            self.logger.info("-" * 50)
            self.logger.info(self._get_metrics_summary(self.model2_metrics, self.config.MODEL2_NAME))
            self.logger.info("=" * 50)
            
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