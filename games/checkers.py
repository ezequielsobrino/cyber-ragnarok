from games.renderers.checkers_renderer import CheckersRenderer
from typing import List, Tuple, Optional

class CheckersGame:
    def __init__(self, model1_starts=True):
        # Initialize empty board (8x8)
        self.board = [' '] * 64
        self.current_player = 'b' if model1_starts else 'w'  # 'b' for black, 'w' for white
        self.game_over = False
        self.winner = None
        self.renderer = None
        self.selected_piece = None
        self.possible_moves = []
        self._initialize_board()
    
    def _initialize_board(self):
        # Place black pieces (top of board)
        for i in range(24):
            row = i // 8
            col = i % 8
            if (row + col) % 2 == 1:  # Only on dark squares
                self.board[i] = 'b'
        
        # Place white pieces (bottom of board)
        for i in range(40, 64):
            row = i // 8
            col = i % 8
            if (row + col) % 2 == 1:  # Only on dark squares
                self.board[i] = 'w'
    
    def initialize_renderer(self, width: int, height: int):
        self.renderer = CheckersRenderer(width, height)

    def get_valid_moves(self, position: int) -> List[Tuple[int, List[int]]]:
        """Returns list of valid moves for a piece. Each move is a tuple of (target_position, captured_pieces)"""
        if not self._is_valid_position(position) or self.board[position].lower() != self.current_player:
            return []

        moves = []
        piece = self.board[position]
        is_king = piece.isupper()

        # Define movement directions
        directions = []
        if piece.lower() == 'b' or is_king:  # Black pieces and kings can move down
            directions.extend([9, 7])  # Down-right, down-left
        if piece.lower() == 'w' or is_king:  # White pieces and kings can move up
            directions.extend([-7, -9])  # Up-right, up-left

        # Check normal moves
        for direction in directions:
            target = position + direction
            if self._is_valid_move(position, target):
                moves.append((target, []))

        # Check jumps (captures)
        jumps = self._get_jumps(position)
        moves.extend(jumps)

        return moves

    def _get_jumps(self, position: int, captured: List[int] = None) -> List[Tuple[int, List[int]]]:
        """Recursively find all possible jump sequences from a position"""
        if captured is None:
            captured = []

        jumps = []
        piece = self.board[position]
        is_king = piece.isupper()

        # Define jump directions
        directions = []
        if piece.lower() == 'b' or is_king:
            directions.extend([(18, 9), (14, 7)])  # Down-right, down-left
        if piece.lower() == 'w' or is_king:
            directions.extend([(-14, -7), (-18, -9)])  # Up-right, Up-left

        for jump_dir, step_dir in directions:
            target = position + jump_dir
            step_pos = position + step_dir
            
            if (self._is_valid_position(target) and self._is_valid_position(step_pos) and
                self.board[target] == ' ' and
                self.board[step_pos].lower() == ('w' if self.current_player == 'b' else 'b') and
                step_pos not in captured):
                
                # Valid jump found
                new_captured = captured + [step_pos]
                jumps.append((target, new_captured))
                
                # Look for multiple jumps
                temp_board = self.board.copy()
                temp_board[position] = ' '
                temp_board[step_pos] = ' '
                temp_board[target] = piece
                
                # Recursively find more jumps
                more_jumps = self._get_jumps(target, new_captured)
                jumps.extend(more_jumps)

        return jumps

    def _is_valid_position(self, position: int) -> bool:
        """Check if a position is within the board boundaries"""
        if position < 0 or position >= 64:
            return False
        row = position // 8
        col = position % 8
        return (row + col) % 2 == 1  # Only dark squares are valid

    def _is_valid_move(self, start: int, target: int) -> bool:
        """Check if a non-jumping move is valid"""
        if not self._is_valid_position(target) or self.board[target] != ' ':
            return False
        
        start_row = start // 8
        start_col = start % 8
        target_row = target // 8
        target_col = target % 8
        
        # Check if move is diagonal and one square
        return abs(target_row - start_row) == 1 and abs(target_col - start_col) == 1

    def make_move(self, start: int, target: int) -> bool:
        """Make a move on the board"""
        valid_moves = self.get_valid_moves(start)
        move = next((move for move in valid_moves if move[0] == target), None)
        
        if not move:
            return False
            
        # Execute move
        piece = self.board[start]
        self.board[start] = ' '
        self.board[target] = piece
        
        # Remove captured pieces
        for captured in move[1]:
            self.board[captured] = ' '
        
        # Check for king promotion
        if self._should_promote(target):
            self.board[target] = self.board[target].upper()
        
        # Switch players
        self.current_player = 'w' if self.current_player == 'b' else 'b'
        
        # Check for game over
        if self._check_winner():
            self.game_over = True
            self.winner = 'b' if self.current_player == 'w' else 'w'
        
        return True

    def _should_promote(self, position: int) -> bool:
        """Check if a piece should be promoted to king"""
        row = position // 8
        piece = self.board[position]
        return (piece == 'b' and row == 7) or (piece == 'w' and row == 0)

    def _check_winner(self) -> bool:
        """Check if the current player has any valid moves left"""
        for i, piece in enumerate(self.board):
            if piece.lower() == self.current_player:
                if self.get_valid_moves(i):
                    return False
        return True

    def get_piece_position(self, screen_pos: Tuple[int, int]) -> Optional[int]:
        """Convert screen coordinates to board position"""
        if not self.renderer:
            return None
        board_pos = self.renderer.get_board_position(screen_pos)
        if board_pos:
            row, col = board_pos
            return row * 8 + col
        return None

    def select_piece(self, position: int) -> bool:
        """Select a piece and calculate its possible moves"""
        if self.board[position].lower() != self.current_player:
            return False
            
        self.selected_piece = position
        valid_moves = self.get_valid_moves(position)
        self.possible_moves = [(move[0] // 8, move[0] % 8) for move in valid_moves]
        
        if self.renderer:
            self.renderer.set_selected(position // 8, position % 8)
            self.renderer.set_possible_moves(self.possible_moves)
        
        return True

    def clear_selection(self):
        """Clear the current selection and possible moves"""
        self.selected_piece = None
        self.possible_moves = []
        if self.renderer:
            self.renderer.clear_selected()
            self.renderer.clear_possible_moves()
