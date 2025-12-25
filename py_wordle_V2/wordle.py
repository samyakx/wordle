import tkinter as tk
from tkinter import messagebox
import random

# --- CONFIGURATION & COLORS ---
GREEN = "#6aaa64"
YELLOW = "#c9b458"
GRAY = "#3a3a3c"   # Dark Gray for 'absent'
# We use a slightly lighter gray for the default keyboard state so it's visible against the black background
DEFAULT_KEY_BG = "#818384" 
BLACK = "#121213"
WHITE = "#ffffff"
EMPTY = "#3a3a3c"

WORDS = ["APPLE", "BEACH", "BRAIN", "CLOUD", "DRIVE", "FLAME", "GHOST", "HOUSE", "LIGHT", "PLANT"]

class WordleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Wordle")
        self.root.geometry("500x750")
        self.root.configure(bg=BLACK)

        self.target_word = random.choice(WORDS).upper()
        self.current_guess_num = 0
        self.current_guess_str = ""
        self.cells = []
        self.key_labels = {} # Stores references to keyboard labels

        self._setup_ui()
        self.root.bind("<Key>", self._handle_keypress)

    def _setup_ui(self):
        # Title
        tk.Label(self.root, text="WORDLE", font=("Helvetica", 36, "bold"), 
                 bg=BLACK, fg=WHITE, pady=20).pack()

        # Grid Frame
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

        # Keyboard UI
        self._setup_keyboard()

    def _setup_keyboard(self):
        kb_frame = tk.Frame(self.root, bg=BLACK)
        kb_frame.pack(pady=30)

        rows = [
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
            ["ENTER", "Z", "X", "C", "V", "B", "N", "M", "⌫"]
        ]

        for row in rows:
            row_frame = tk.Frame(kb_frame, bg=BLACK)
            row_frame.pack()
            for key in row:
                width = 5 if len(key) > 1 else 3
                
                # NOTE: Using Label instead of Button to force colors on Mac
                lbl = tk.Label(row_frame, text=key, font=("Helvetica", 14, "bold"),
                               width=width, height=2, fg=WHITE, bg=DEFAULT_KEY_BG)
                
                # Add a small border to make them look like keys
                lbl.pack(side="left", padx=2, pady=2)
                
                # Bind the click event
                lbl.bind("<Button-1>", lambda event, k=key: self._on_screen_key_click(k))
                
                if len(key) == 1:
                    self.key_labels[key] = lbl

    def _on_screen_key_click(self, key):
        """Maps virtual keyboard clicks to game logic."""
        class PseudoEvent:
            def __init__(self, k):
                self.keysym = "Return" if k == "ENTER" else ("BackSpace" if k == "⌫" else k)
        self._handle_keypress(PseudoEvent(key))

    def _handle_keypress(self, event):
        key = event.keysym.upper()
        if key == "BACKSPACE":
            if len(self.current_guess_str) > 0:
                self.current_guess_str = self.current_guess_str[:-1]
                self._update_grid()
        elif key in ["RETURN", "ENTER"]:
            if len(self.current_guess_str) == 5:
                self._submit_guess()
        elif len(key) == 1 and key.isalpha():
            if len(self.current_guess_str) < 5:
                self.current_guess_str += key
                self._update_grid()

    def _update_grid(self):
        row = self.cells[self.current_guess_num]
        for i, cell in enumerate(row):
            if i < len(self.current_guess_str):
                cell.config(text=self.current_guess_str[i], highlightbackground=DEFAULT_KEY_BG)
            else:
                cell.config(text="", highlightbackground=EMPTY)

    def _submit_guess(self):
        guess = self.current_guess_str
        result_colors = self._get_color_feedback(guess)
        
        row = self.cells[self.current_guess_num]
        for i, color in enumerate(result_colors):
            # Update the Grid
            row[i].config(bg=color, highlightbackground=color)
            
            # Update the Virtual Keyboard
            letter = guess[i]
            if letter in self.key_labels:
                self._update_key_color(self.key_labels[letter], color)

        if guess == self.target_word:
            messagebox.showinfo("Wordle", "Genius!")
            self.root.destroy()
        elif self.current_guess_num == 5:
            messagebox.showinfo("Wordle", f"The word was {self.target_word}")
            self.root.destroy()
        else:
            self.current_guess_num += 1
            self.current_guess_str = ""

    def _update_key_color(self, lbl, new_color):
        """Ensures we don't overwrite a Green key with Yellow/Gray."""
        current_color = lbl.cget("bg")
        
        # Priority: GREEN > YELLOW > GRAY > DEFAULT
        if current_color == GREEN:
            return
        if current_color == YELLOW and new_color == GRAY:
            return
            
        lbl.config(bg=new_color)

    def _get_color_feedback(self, guess):
        result = [GRAY] * 5
        target_list = list(self.target_word)
        guess_list = list(guess)

        # Pass 1: Green
        for i in range(5):
            if guess_list[i] == target_list[i]:
                result[i] = GREEN
                target_list[i] = None
                guess_list[i] = None

        # Pass 2: Yellow
        for i in range(5):
            if guess_list[i] is not None and guess_list[i] in target_list:
                result[i] = YELLOW
                target_list[target_list.index(guess_list[i])] = None
        return result

if __name__ == "__main__":
    root = tk.Tk()
    game = WordleGame(root)
    root.mainloop()