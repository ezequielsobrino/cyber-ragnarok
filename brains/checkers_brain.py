from typing import List
from brains.providers.base import LLMProvider
from brains.tic_tac_toe_brain import BrainResponse
from games.checkers import CheckersGame

class CheckersBrain:
    def __init__(self, llm_provider: LLMProvider):
        self.llm_provider = llm_provider

    def analyze_board(self, board: List[str], current_player: str) -> dict:
        """Analyze the current board state"""
        return {
            'player_pieces': self._count_pieces(board, current_player),
            'opponent_pieces': self._count_pieces(board, 'w' if current_player == 'b' else 'b'),
            'player_kings': self._count_kings(board, current_player),
            'opponent_kings': self._count_kings(board, 'w' if current_player == 'b' else 'b'),
            'player_positions': self._get_piece_positions(board, current_player),
            'opponent_positions': self._get_piece_positions(board, 'w' if current_player == 'b' else 'b'),
            'control_center': self._evaluate_center_control(board, current_player),
            'back_row_strength': self._evaluate_back_row(board, current_player)
        }

    def _count_pieces(self, board: List[str], player: str) -> int:
        """Count the number of pieces for a player"""
        return sum(1 for piece in board if piece.lower() == player)

    def _count_kings(self, board: List[str], player: str) -> int:
        """Count the number of kings for a player"""
        return sum(1 for piece in board if piece == player.upper())

    def _get_piece_positions(self, board: List[str], player: str) -> List[int]:
        """Get positions of all pieces for a player"""
        return [i for i, piece in enumerate(board) if piece.lower() == player]

    def _evaluate_center_control(self, board: List[str], player: str) -> float:
        """Evaluate control of the center squares"""
        center_squares = [27, 28, 35, 36]
        center_pieces = sum(1 for pos in center_squares if board[pos].lower() == player)
        return center_pieces / len(center_squares)

    def _evaluate_back_row(self, board: List[str], player: str) -> float:
        """Evaluate strength of back row defense"""
        back_row = range(56, 64) if player == 'w' else range(8)
        back_pieces = sum(1 for pos in back_row if board[pos].lower() == player)
        return back_pieces / 4  # 4 possible back row pieces

    def get_move(self, board: List[str], current_player: str) -> BrainResponse:
        """Get the best move for the current player"""
        analysis = self.analyze_board(board, current_player)
        
        # Create board visualization for the LLM
        board_visual = self._create_board_visual(board)
        
        prompt = f"""You are an expert Checkers player. Analyze the current game state and choose the best move.

Current Board:
{board_visual}

Board Analysis:
1. Your pieces (regular): {analysis['player_pieces'] - analysis['player_kings']}
2. Your kings: {analysis['player_kings']}
3. Opponent pieces (regular): {analysis['opponent_pieces'] - analysis['opponent_kings']}
4. Opponent kings: {analysis['opponent_kings']}
5. Center control: {analysis['control_center']:.2f}
6. Back row strength: {analysis['back_row_strength']:.2f}

You are playing as {current_player.upper()} pieces.
Lowercase letters (b/w) represent regular pieces.
Uppercase letters (B/W) represent kings.

Available moves are provided as "start_position:target_position".
Choose the best move considering:
1. Capturing opponent pieces when possible
2. Protecting your pieces from capture
3. Controlling the center
4. Creating kings
5. Maintaining back row defense

Respond with ONLY the chosen move in format "start:target" (e.g., "23:32"). No other text.
"""

        try:
            game = CheckersGame()  # Temporary game instance for move validation
            game.board = board.copy()
            game.current_player = current_player
            
            available_moves = []
            for start_pos in analysis['player_positions']:
                valid_moves = game.get_valid_moves(start_pos)
                for move, captures in valid_moves:
                    available_moves.append(f"{start_pos}:{move}")
            
            if not available_moves:
                return BrainResponse(
                    move=None,
                    raw_content="No valid moves available",
                    input_tokens=0,
                    output_tokens=0,
                    total_tokens=0,
                    cost=0,
                    response_time=0,
                    is_fallback=True
                )
                
            # Add available moves to prompt
            prompt += f"\nAvailable moves: {', '.join(available_moves)}"
            
            # Get move from LLM
            response = self.llm_provider.get_completion(prompt)
            
            # Parse response
            start, target = map(int, response.content.strip().split(':'))
            
            # Validate move
            if any(move.startswith(f"{start}:{target}") for move in available_moves):
                return BrainResponse(
                    move=(start, target),
                    raw_content=response.content,
                    input_tokens=response.input_tokens,
                    output_tokens=response.output_tokens,
                    total_tokens=response.total_tokens,
                    cost=response.cost,
                    response_time=response.response_time,
                    is_fallback=False
                )
            
            # Fallback to first valid move if LLM response is invalid
            fallback = available_moves[0].split(':')
            return BrainResponse(
                move=(int(fallback[0]), int(fallback[1])),
                raw_content=response.content,
                input_tokens=response.input_tokens,
                output_tokens=response.output_tokens,
                total_tokens=response.total_tokens,
                cost=response.cost,
                response_time=response.response_time,
                is_fallback=True
            )
            
        except Exception as e:
            print(f"Error in get_move: {e}")
            # Fallback to first valid move
            for start_pos in analysis['player_positions']:
                valid_moves = game.get_valid_moves(start_pos)
                if valid_moves:
                    return BrainResponse(
                        move=(start_pos, valid_moves[0][0]),
                        raw_content=str(e),
                        input_tokens=0,
                        output_tokens=0,
                        total_tokens=0,
                        cost=0,
                        response_time=0,
                        is_fallback=True
                    )
            return BrainResponse(
                move=None,
                raw_content=str(e),
                input_tokens=0,
                output_tokens=0,
                total_tokens=0,
                cost=0,
                response_time=0,
                is_fallback=True
            )

    def _create_board_visual(self, board: List[str]) -> str:
        """Create a visual representation of the board for the LLM"""
        visual = "  0 1 2 3 4 5 6 7\n"
        for row in range(8):
            visual += f"{row} "
            for col in range(8):
                pos = row * 8 + col
                piece = board[pos]
                if piece == ' ':
                    visual += '.' if (row + col) % 2 == 1 else ' '
                else:
                    visual += piece
                visual += ' '
            visual += '\n'
        return visual
