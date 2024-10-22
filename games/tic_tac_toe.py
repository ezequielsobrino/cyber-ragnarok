class TicTacToeGame:
    def __init__(self, player1_starts=True):
        self.current_player = 'X' if player1_starts else 'O'
        self.board = ['' for _ in range(9)]
        self.winner = None
        self.game_over = False
        self.winning_line = None
        
    def make_move(self, position, player):
        if self.board[position] == '' and not self.game_over:
            self.board[position] = player
            if not self.check_winner():
                self.current_player = 'O' if player == 'X' else 'X'
            return True
        return False
    
    def get_valid_moves(self):
        return [i for i, cell in enumerate(self.board) if cell == '']
    
    def check_winner(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontales
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Verticales
            [0, 4, 8], [2, 4, 6]              # Diagonales
        ]

        for line in winning_combinations:
            if (self.board[line[0]] == self.board[line[1]] == self.board[line[2]] != ''):
                self.winner = self.board[line[0]]
                self.game_over = True
                self.winning_line = line
                return True

        if '' not in self.board:
            self.game_over = True
            self.winner = None
            return True

        return False