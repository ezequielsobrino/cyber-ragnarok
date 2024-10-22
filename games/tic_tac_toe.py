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