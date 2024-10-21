import tkinter as tk
from tkinter import ttk
import random
from typing import List, Optional
from PIL import Image, ImageTk

from tic_tac_toe_brain import TicTacToeBrain

class TicTacToeCompetition:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic-Tac-Toe Brain Competition")
        self.master.geometry("800x600")
        self.master.configure(bg="#f0f0f0")

        self.brain1 = TicTacToeBrain()
        self.brain2 = TicTacToeBrain()
        self.current_player = 'X'
        self.board = [' '] * 9
        self.game_count = 0
        self.brain1_wins = 0
        self.brain2_wins = 0
        self.draws = 0

        self.load_images()
        self.create_widgets()
        self.update_stats()
        self.play_game()

    def load_images(self):
        # Load background image
        self.bg_image = Image.open("tic_tac_toe_board.png")
        self.bg_image = self.bg_image.resize((400, 400), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Load X and O images
        self.x_image = Image.open("x_image.png")
        self.x_image = self.x_image.resize((100, 100), Image.LANCZOS)
        self.x_photo = ImageTk.PhotoImage(self.x_image)

        self.o_image = Image.open("o_image.png")
        self.o_image = self.o_image.resize((100, 100), Image.LANCZOS)
        self.o_photo = ImageTk.PhotoImage(self.o_image)

    def create_widgets(self):
        # Main frame
        self.main_frame = tk.Frame(self.master, bg="#f0f0f0")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Game board (left side)
        self.board_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.board_frame.pack(side=tk.LEFT, padx=20, pady=20)

        self.canvas = tk.Canvas(self.board_frame, width=400, height=400, highlightthickness=0)
        self.canvas.pack()

        # Draw background image
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo)

        self.buttons = []
        for i in range(9):
            x = (i % 3) * 133 + 66
            y = (i // 3) * 133 + 66
            btn = self.canvas.create_rectangle(x-50, y-50, x+50, y+50, fill='', outline='')
            self.buttons.append(btn)

        # Right side frame
        self.right_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.right_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Statistics
        self.stats_frame = tk.Frame(self.right_frame, bg="#f0f0f0")
        self.stats_frame.pack(pady=10)

        self.stats_label = tk.Label(self.stats_frame, text="", font=('Arial', 12), bg="#f0f0f0")
        self.stats_label.pack()

        # Control buttons
        self.control_frame = tk.Frame(self.right_frame, bg="#f0f0f0")
        self.control_frame.pack(pady=10)

        self.play_button = ttk.Button(self.control_frame, text="Play Next Game", command=self.play_game)
        self.play_button.pack(pady=5)

        self.reset_button = ttk.Button(self.control_frame, text="Reset Stats", command=self.reset_stats)
        self.reset_button.pack(pady=5)

    def update_board(self):
        for i, symbol in enumerate(self.board):
            x = (i % 3) * 133 + 66
            y = (i // 3) * 133 + 66
            if symbol == 'X':
                self.canvas.create_image(x, y, image=self.x_photo)
            elif symbol == 'O':
                self.canvas.create_image(x, y, image=self.o_photo)

    def update_stats(self):
        stats_text = f"Games: {self.game_count}\nBrain 1 Wins: {self.brain1_wins}\nBrain 2 Wins: {self.brain2_wins}\nDraws: {self.draws}"
        self.stats_label.config(text=stats_text)

    def reset_stats(self):
        self.game_count = 0
        self.brain1_wins = 0
        self.brain2_wins = 0
        self.draws = 0
        self.update_stats()

    def play_game(self):
        self.board = [' '] * 9
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo)
        self.current_player = 'X' if self.game_count % 2 == 0 else 'O'
        self.game_count += 1
        self.play_turn()

    def play_turn(self):
        winner = self.check_winner()
        if winner or ' ' not in self.board:
            self.end_game(winner)
            return

        current_brain = self.brain1 if self.current_player == 'X' else self.brain2
        move, _, _ = current_brain.get_move(self.board, self.current_player)
        self.board[move] = self.current_player
        self.update_board()

        self.current_player = 'O' if self.current_player == 'X' else 'X'
        self.master.after(500, self.play_turn)

    def check_winner(self) -> Optional[str]:
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' ':
                return self.board[combo[0]]
        return None

    def end_game(self, winner: Optional[str]):
        if winner:
            if winner == 'X':
                self.brain1_wins += 1
            else:
                self.brain2_wins += 1
        else:
            self.draws += 1
        self.update_stats()

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeCompetition(root)
    root.mainloop()