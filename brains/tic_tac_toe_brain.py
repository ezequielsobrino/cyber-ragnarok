import random
import re
from typing import List, Optional
from brains.base import BrainResponse
from brains.providers.base import LLMProvider

class TicTacToeBrain:
    def __init__(self, llm_provider: LLMProvider):
        self.llm_provider = llm_provider

    def analyze_board(self, board: List[str], current_player: str) -> dict:
        analysis = {
            'empty_cells': self.get_empty_cells(board),
            'player_positions': [i for i, cell in enumerate(board) if cell == current_player],
            'opponent_positions': [i for i, cell in enumerate(board) if cell != ' ' and cell != current_player],
            'winning_moves': self.get_winning_moves(board, current_player),
            'blocking_moves': self.get_blocking_moves(board, current_player),
            'fork_opportunities': self.get_fork_opportunities(board, current_player),
            'opponent_fork_threats': self.get_opponent_fork_threats(board, current_player)
        }
        return analysis

    def get_empty_cells(self, board: List[str]) -> List[int]:
        return [i for i, cell in enumerate(board) if cell == ' ']

    def get_winning_moves(self, board: List[str], player: str) -> List[int]:
        return self._get_critical_moves(board, player)

    def get_blocking_moves(self, board: List[str], player: str) -> List[int]:
        opponent = 'O' if player == 'X' else 'X'
        return self._get_critical_moves(board, opponent)

    def _get_critical_moves(self, board: List[str], player: str) -> List[int]:
        critical_moves = []
        for i in range(9):
            if board[i] == ' ':
                board_copy = board.copy()
                board_copy[i] = player
                if self.check_winner(board_copy) == player:
                    critical_moves.append(i)
        return critical_moves

    def get_fork_opportunities(self, board: List[str], player: str) -> List[int]:
        return self._get_fork_moves(board, player)

    def get_opponent_fork_threats(self, board: List[str], player: str) -> List[int]:
        opponent = 'O' if player == 'X' else 'X'
        return self._get_fork_moves(board, opponent)

    def _get_fork_moves(self, board: List[str], player: str) -> List[int]:
        fork_moves = []
        for i in range(9):
            if board[i] == ' ':
                board_copy = board.copy()
                board_copy[i] = player
                if len(self._get_critical_moves(board_copy, player)) >= 2:
                    fork_moves.append(i)
        return fork_moves

    def check_winner(self, board: List[str]) -> Optional[str]:
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Filas
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columnas
            [0, 4, 8], [2, 4, 6]  # Diagonales
        ]
        for combo in winning_combinations:
            if board[combo[0]] == board[combo[1]] == board[combo[2]] != ' ':
                return board[combo[0]]
        return None

    def get_move(self, board: List[str], current_player: str) -> BrainResponse:
        analysis = self.analyze_board(board, current_player)
        board_state = [str(i) if cell == ' ' else cell for i, cell in enumerate(board)]
    
        prompt = f"""You are an expert Tic-Tac-Toe player. Analyze the current game state and choose the best move.

Current Board:
+---+---+---+
| {board_state[0]} | {board_state[1]} | {board_state[2]} |
+---+---+---+
| {board_state[3]} | {board_state[4]} | {board_state[5]} |
+---+---+---+
| {board_state[6]} | {board_state[7]} | {board_state[8]} |
+---+---+---+
(Numbers represent empty cells, '{current_player}' = you, '{'O' if current_player == 'X' else 'X'}' = opponent)

Board Analysis:
1. Empty cells: {analysis['empty_cells']}
2. Your positions: {analysis['player_positions']}
3. Opponent's positions: {analysis['opponent_positions']}
4. Winning moves for you: {analysis['winning_moves']}
5. Blocking moves (opponent's winning moves): {analysis['blocking_moves']}
6. Fork opportunities for you: {analysis['fork_opportunities']}
7. Opponent's fork threats: {analysis['opponent_fork_threats']}

Move Priority:
1. Win if possible
2. Block opponent's winning move
3. Create a fork (two winning ways)
4. Block opponent's fork
5. Play center if available
6. Play a corner
7. Play any available side

Instructions:
- Analyze the board carefully
- Consider the move priorities
- Choose the best move based on the current game state
- Respond with ONLY the position number (0-8) for your chosen move. Without another comments
"""

        try:
            llm_response = self.llm_provider.get_completion(prompt)
            
            match = re.search(r'\b[0-8]\b', llm_response.content)
            if match:
                move = int(match.group())
                if move in analysis['empty_cells']:
                    return BrainResponse(
                        move=move,
                        raw_content=llm_response.content,
                        input_tokens=llm_response.input_tokens,
                        output_tokens=llm_response.output_tokens,
                        total_tokens=llm_response.total_tokens,
                        cost=llm_response.cost,
                        response_time=llm_response.response_time,
                        is_fallback=False
                    )

            # Fallback a movimiento aleatorio
            fallback_move = random.choice(analysis['empty_cells'])
            print(f"LLM provided an invalid move: {llm_response.content}. Falling back to random choice: {fallback_move}")
            return BrainResponse(
                move=fallback_move,
                raw_content=llm_response.content,
                input_tokens=llm_response.input_tokens,
                output_tokens=llm_response.output_tokens,
                total_tokens=llm_response.total_tokens,
                cost=llm_response.cost,
                response_time=llm_response.response_time,
                is_fallback=True
            )

        except Exception as e:
            # En caso de error, devolver un movimiento aleatorio con valores por defecto
            fallback_move = random.choice(analysis['empty_cells'])
            print(f"Error in get_move: {e}")
            return BrainResponse(
                move=fallback_move,
                raw_content=str(e),
                input_tokens=0,
                output_tokens=0,
                total_tokens=0,
                cost=0,
                response_time=0,
                is_fallback=True
            )