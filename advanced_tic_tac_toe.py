import tkinter as tk
from tkinter import messagebox, simpledialog
import random
from functools import partial

class AdvancedTicTacToe:
    def _init_(self):
        self.window = tk.Tk()
        self.window.title("Advanced Tic Tac Toe")
        
        self.board_size = 5
        self.win_length = 4
        self.player_symbol = "X"
        self.ai_symbol = "O"
        self.difficulty = "medium"
        self.player_score = 0
        self.ai_score = 0
        
        self.buttons = []
        self.game_over = False
        self.move_count = 0
        
        self.setup_menu()
        self.setup_board()
        self.setup_scoreboard()
        
        self.choose_difficulty()
        self.choose_symbol()
    
    def setup_menu(self):
        menu_bar = tk.Menu(self.window)
        self.window.config(menu=menu_bar)
        
        game_menu = tk.Menu(menu_bar, tearoff=0)
        game_menu.add_command(label="New Game", command=self.reset_game)
        game_menu.add_command(label="Set Difficulty", command=self.choose_difficulty)
        game_menu.add_command(label="Change Symbol", command=self.choose_symbol)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.window.quit)
        menu_bar.add_cascade(label="Game", menu=game_menu)
    
    def setup_board(self):
        board_frame = tk.Frame(self.window)
        board_frame.pack(pady=10)
        
        for row in range(self.board_size):
            button_row = []
            for col in range(self.board_size):
                button = tk.Button(
                    board_frame,
                    text="",
                    font=("Helvetica", 20),
                    width=4,
                    height=2,
                    bg="lightgray",
                    command=partial(self.handle_click, row, col)
                )
                button.grid(row=row, column=col, padx=2, pady=2)
                button_row.append(button)
            self.buttons.append(button_row)
    
    def setup_scoreboard(self):
        score_frame = tk.Frame(self.window)
        score_frame.pack(pady=10)
        
        tk.Label(score_frame, text="Player:", font=("Helvetica", 12)).grid(row=0, column=0)
        self.player_score_label = tk.Label(score_frame, text=str(self.player_score), font=("Helvetica", 12))
        self.player_score_label.grid(row=0, column=1, padx=10)
        
        tk.Label(score_frame, text="AI:", font=("Helvetica", 12)).grid(row=0, column=2)
        self.ai_score_label = tk.Label(score_frame, text=str(self.ai_score), font=("Helvetica", 12))
        self.ai_score_label.grid(row=0, column=3, padx=10)
    
    def choose_difficulty(self):
        difficulty = simpledialog.askstring(
            "Difficulty",
            "Choose difficulty (easy/medium/hard):",
            parent=self.window
        )
        if difficulty and difficulty.lower() in ["easy", "medium", "hard"]:
            self.difficulty = difficulty.lower()
    
    def choose_symbol(self):
        symbol = simpledialog.askstring(
            "Symbol Selection",
            "Choose your symbol (X/O):",
            parent=self.window
        )
        if symbol and symbol.upper() in ["X", "O"]:
            self.player_symbol = symbol.upper()
            self.ai_symbol = "O" if self.player_symbol == "X" else "X"
    
    def handle_click(self, row, col):
        if not self.game_over and self.buttons[row][col]["text"] == "":
            self.make_move(row, col, self.player_symbol)
            if not self.check_game_over():
                self.ai_move()
    
    def make_move(self, row, col, player):
        self.buttons[row][col]["text"] = player
        self.buttons[row][col]["bg"] = "lightgreen" if player == self.player_symbol else "salmon"
        self.move_count += 1
    
    def ai_move(self):
        if self.difficulty == "easy":
            self.random_move()
        elif self.difficulty == "medium":
            self.smart_move()
        else:
            self.minimax_move()
    
    def random_move(self):
        empty_cells = [(i, j) for i in range(self.board_size) 
                      for j in range(self.board_size) if self.buttons[i][j]["text"] == ""]
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.make_move(row, col, self.ai_symbol)
            self.check_game_over()
    
    def smart_move(self):
        # Try to win or block player
        move = self.find_winning_move(self.ai_symbol) or \
               self.find_winning_move(self.player_symbol) or \
               self.find_best_move()
        if move:
            self.make_move(*move, self.ai_symbol)
            self.check_game_over()
    
    def find_winning_move(self, symbol):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.buttons[i][j]["text"] == "":
                    self.buttons[i][j]["text"] = symbol
                    if self.check_win(symbol):
                        self.buttons[i][j]["text"] = ""
                        return (i, j)
                    self.buttons[i][j]["text"] = ""
        return None
    
    def find_best_move(self):
        best_score = -float('inf')
        best_move = None
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.buttons[i][j]["text"] == "":
                    self.buttons[i][j]["text"] = self.ai_symbol
                    score = self.evaluate_board()
                    self.buttons[i][j]["text"] = ""
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        return best_move or self.random_move()
    
    def evaluate_board(self):
        score = 0
        # Evaluate all possible lines
        for line in self.get_all_lines():
            ai_count = line.count(self.ai_symbol)
            player_count = line.count(self.player_symbol)
            empty_count = line.count("")
            
            if ai_count == 3 and empty_count == 1: score += 100
            elif ai_count == 2 and empty_count == 2: score += 10
            if player_count == 3 and empty_count == 1: score -= 80
            elif player_count == 2 and empty_count == 2: score -= 8
        return score
    
    def get_all_lines(self):
        lines = []
        # Rows
        for row in self.buttons:
            for i in range(len(row) - self.win_length + 1):
                lines.append([cell["text"] for cell in row[i:i+self.win_length]])
        # Columns
        for col in range(self.board_size):
            for i in range(self.board_size - self.win_length + 1):
                lines.append([self.buttons[i+k][col]["text"] for k in range(self.win_length)])
        # Diagonals
        for i in range(self.board_size - self.win_length + 1):
            for j in range(self.board_size - self.win_length + 1):
                lines.append([self.buttons[i+k][j+k]["text"] for k in range(self.win_length)])
                lines.append([self.buttons[i+k][j+self.win_length-1-k]["text"] for k in range(self.win_length)])
        return lines
    
    def minimax_move(self):
        best_score = -float('inf')
        best_move = None
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.buttons[i][j]["text"] == "":
                    self.buttons[i][j]["text"] = self.ai_symbol
                    score = self.minimax(False, 0)
                    self.buttons[i][j]["text"] = ""
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        if best_move:
            self.make_move(*best_move, self.ai_symbol)
            self.check_game_over()
    
    def minimax(self, is_maximizing, depth):
        if self.check_win(self.ai_symbol):
            return 1
        if self.check_win(self.player_symbol):
            return -1
        if self.move_count == self.board_size**2:
            return 0
        
        if is_maximizing:
            best_score = -float('inf')
            for i in range(self.board_size):
                for j in range(self.board_size):
                    if self.buttons[i][j]["text"] == "":
                        self.buttons[i][j]["text"] = self.ai_symbol
                        score = self.minimax(False, depth+1)
                        self.buttons[i][j]["text"] = ""
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(self.board_size):
                for j in range(self.board_size):
                    if self.buttons[i][j]["text"] == "":
                        self.buttons[i][j]["text"] = self.player_symbol
                        score = self.minimax(True, depth+1)
                        self.buttons[i][j]["text"] = ""
                        best_score = min(score, best_score)
            return best_score
    
    def check_win(self, symbol):
        # Check all possible winning lines
        for line in self.get_all_lines():
            if all(cell == symbol for cell in line):
                return True
        return False
    
    def check_game_over(self):
        if self.check_win(self.player_symbol):
            self.player_score += 1
            self.player_score_label.config(text=str(self.player_score))
            self.game_over = True
            messagebox.showinfo("Game Over", "Congratulations! You win!")
            return True
        if self.check_win(self.ai_symbol):
            self.ai_score += 1
            self.ai_score_label.config(text=str(self.ai_score))
            self.game_over = True
            messagebox.showinfo("Game Over", "AI wins!")
            return True
        if self.move_count == self.board_size**2:
            self.game_over = True
            messagebox.showinfo("Game Over", "It's a draw!")
            return True
        return False
    
    def reset_game(self):
        for row in self.buttons:
            for button in row:
                button.config(text="", bg="lightgray")
        self.game_over = False
        self.move_count = 0
        if self.ai_symbol == "X":
            self.ai_move()
    
    def run(self):
        self.window.mainloop()

if _name_ == "_main_":
    game = AdvancedTicTacToe()
    game.run()
