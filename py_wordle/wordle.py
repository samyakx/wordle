import tkinter as tk
from tkinter import messagebox
import random

# --- CONFIGURATION & COLORS ---
GREEN = "#6aaa64"
YELLOW = "#c9b458"
GRAY = "#787c7e"
BLACK = "#121213"
WHITE = "#ffffff"
EMPTY = "#3a3a3c"

# A small sample list. You can expand this or load from a text file.
WORDS = ["APPLE", "BEACH", "BRAIN", "CLOUD", "DRIVE", "FLAME", "GHOST", "HOUSE", "LIGHT", "PLANT"]

class WordleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Wordle (Mac)")
        self.root.geometry("400x600")
        self.root.configure(bg=BLACK)

        self.target_word = random.choice(WORDS).upper()
        self.current_guess_num = 0
        self.current_guess_str = ""
        self.cells = []
        
        self._setup_ui()
        self.root.bind("<Key>", self._handle_keypress)

    def _setup_ui(self):
        """Creates the 5x6 grid for guesses."""
        title_label = tk.Label(self.root, text="WORDLE", font=("Helvetica", 36, "bold"), 
                              bg=BLACK, fg=WHITE, pady=20)
        title_label.pack()

        grid_frame = tk.Frame(self.root, bg=BLACK)
        grid_frame.pack(pady=10)

        for row in range(6):
            row_cells = []
            for col in range(5):
                cell = tk.Label(grid_frame, text="", font=("Helvetica", 30, "bold"),
                               width=2, height=1, fg=WHITE, bg=BLACK,
                               highlightbackground=EMPTY, highlightthickness=2, relief="flat")
                cell.grid(row=row, column=col, padx=3, pady=3)
                row_cells.append(cell)
            self.cells.append(row_cells)

    def _handle_keypress(self, event):
        key = event.keysym.upper()
        
        # Handle Backspace
        if key == "BACKSPACE":
            if len(self.current_guess_str) > 0:
                self.current_guess_str = self.current_guess_str[:-1]
                self._update_grid()

        # Handle Enter
        elif key == "RETURN":
            if len(self.current_guess_str) == 5:
                self._submit_guess()
            else:
                # Shake or warning could go here
                pass

        # Handle Letters
        elif len(key) == 1 and key.isalpha():
            if len(self.current_guess_str) < 5:
                self.current_guess_str += key
                self._update_grid()

    def _update_grid(self):
        """Updates the visual text in the current row."""
        row = self.cells[self.current_guess_num]
        # Clear row first (visualizing backspaces)
        for i, cell in enumerate(row):
            if i < len(self.current_guess_str):
                cell.config(text=self.current_guess_str[i], highlightbackground=GRAY)
            else:
                cell.config(text="", highlightbackground=EMPTY)

    def _submit_guess(self):
        guess = self.current_guess_str
        result_colors = self._get_color_feedback(guess)
        
        # Apply colors to the UI
        row = self.cells[self.current_guess_num]
        for i, color in enumerate(result_colors):
            row[i].config(bg=color, highlightbackground=color)

        if guess == self.target_word:
            messagebox.showinfo("Wordle", f"Splendid! \n\n The word was {self.target_word}")
            self.root.destroy()
        elif self.current_guess_num == 5:
            messagebox.showinfo("Wordle", f"Game Over. \n\n The word was {self.target_word}")
            self.root.destroy()
        else:
            self.current_guess_num += 1
            self.current_guess_str = ""

    def _get_color_feedback(self, guess):
        """Logic for determining green, yellow, or gray."""
        result = [GRAY] * 5
        target_list = list(self.target_word)
        guess_list = list(guess)

        # First pass: Find Greens
        for i in range(5):
            if guess_list[i] == target_list[i]:
                result[i] = GREEN
                target_list[i] = None # Mark as used
                guess_list[i] = None

        # Second pass: Find Yellows
        for i in range(5):
            if guess_list[i] is not None and guess_list[i] in target_list:
                result[i] = YELLOW
                target_list[target_list.index(guess_list[i])] = None
                
        return result

if __name__ == "__main__":
    root = tk.Tk()
    game = WordleGame(root)
    root.mainloop()