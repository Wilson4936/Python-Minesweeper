import tkinter as tk
import random
import time


class Minesweeper_Easy:
    def __init__(self, master):
        self.master = master
        self.master.title("Minesweeper")

        self.board_size = 8
        self.num_mines = 10
        self.flags_remaining = self.num_mines
        self.time_remaining = 600  # 10 minutes in seconds

        self.board = [[0] * self.board_size for _ in range(self.board_size)]
        self.mine_locations = []
        self.buttons = [[None] * self.board_size for _ in range(self.board_size)]

        self.create_widgets()
        self.place_mines()
        self.update_flags_remaining()
        self.update_timer()

    def create_widgets(self):
        self.flag_timer_frame = tk.Frame(self.master)
        self.flag_timer_frame.pack()

        self.flag_label = tk.Label(self.flag_timer_frame, text=f"Flags: {self.flags_remaining}")
        self.flag_label.pack(side=tk.LEFT, padx=(10, 5))

        self.timer_label = tk.Label(self.flag_timer_frame, text="Timer: 10:00", fg='red', bg='black', relief=tk.SOLID,
                                    bd=2)
        self.timer_label.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.board_frame = tk.Frame(self.master, bd=4, relief=tk.SOLID)
        self.board_frame.pack()

        for row in range(self.board_size):
            for col in range(self.board_size):
                button = tk.Button(self.board_frame, width=2, height=1)
                button.grid(row=row, column=col)
                button.bind('<Button-1>', lambda event, r=row, c=col: self.click_cell(event, r, c))
                button.bind('<Button-3>', lambda event, r=row, c=col: self.flag_cell(event, r, c))
                self.buttons[row][col] = button

    def place_mines(self):
        mines = 0
        while mines < self.num_mines:
            row = random.randint(0, self.board_size - 1)
            col = random.randint(0, self.board_size - 1)

            if self.board[row][col] != -1:
                self.board[row][col] = -1
                self.mine_locations.append((row, col))
                mines += 1

        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] != -1:
                    self.board[row][col] = self.count_adjacent_mines(row, col)

    def count_adjacent_mines(self, row, col):
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                if 0 <= row + dr < self.board_size and 0 <= col + dc < self.board_size and self.board[row + dr][
                    col + dc] == -1:
                    count += 1
        return count

    def click_cell(self, event, row, col):
        if self.board[row][col] == -1:
            self.game_over(row, col)
        else:
            self.reveal_cell(row, col)
            if self.check_win():
                self.game_win()

    def flag_cell(self, event, row, col):
        button = self.buttons[row][col]
        if button['state'] == tk.NORMAL:
            if self.flags_remaining > 0:
                button['text'] = '🚩'
                button['state'] = tk.DISABLED
                self.flags_remaining -= 1
                self.update_flags_remaining()

    def reveal_cell(self, row, col):
        button = self.buttons[row][col]
        value = self.board[row][col]

        if button['state'] == tk.NORMAL:
            button['state'] = tk.DISABLED
            button['relief'] = tk.SUNKEN

            if value == 0:
                button['text'] = ''
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        if 0 <= row + dr < self.board_size and 0 <= col + dc < self.board_size:
                            self.reveal_cell(row + dr, col + dc)
            else:
                button['text'] = str(value)

    def game_over(self, row, col):
        for r, c in self.mine_locations:
            button = self.buttons[r][c]
            button['text'] = '💣'
            button['fg'] = 'red'
            button['bg'] = 'red'

        self.disable_all_buttons()
        self.timer_label.after_cancel(self.timer_id)

        # Create game over screen
        game_over_window = tk.Toplevel(self.master)
        game_over_window.title("Game Over")

        game_over_label = tk.Label(game_over_window, text="Game Over! The mine has exploded.", font=("Arial", 16, "bold"))
        game_over_label.pack(padx=20, pady=20)

    def game_win(self):
        self.disable_all_buttons()
        self.timer_label.after_cancel(self.timer_id)

        # Create game win screen
        game_win_window = tk.Toplevel(self.master)
        game_win_window.title("Congratulations!")

        game_win_label = tk.Label(game_win_window, text="You win! 😊\nExit the program to play again.",
                                  font=("Arial", 16, "bold"))
        game_win_label.pack(padx=20, pady=20)

    def disable_all_buttons(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                button = self.buttons[row][col]
                button['state'] = tk.DISABLED

    def update_flags_remaining(self):
        self.flag_label['text'] = f"Flags: {self.flags_remaining}"

    def update_timer(self):
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        self.timer_label['text'] = f"Timer: {minutes:02d}:{seconds:02d}"

        if self.time_remaining > 0:
            self.time_remaining -= 1
            self.timer_id = self.timer_label.after(1000, self.update_timer)
        else:
            self.game_over(None, None)

    def check_win(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                button = self.buttons[row][col]
                if button['state'] != tk.DISABLED and self.board[row][col] != -1:
                    return False
        return True


class Minesweeper_Medium:
    def __init__(self, master):
        self.master = master
        self.master.title("Minesweeper")

        self.board_size = 16
        self.num_mines = 40
        self.flags_remaining = self.num_mines
        self.time_remaining = 300  # 5 minutes in seconds

        self.board = [[0] * self.board_size for _ in range(self.board_size)]
        self.mine_locations = []
        self.buttons = [[None] * self.board_size for _ in range(self.board_size)]

        self.create_widgets()
        self.place_mines()
        self.update_flags_remaining()
        self.update_timer()

    def create_widgets(self):
        self.flag_timer_frame = tk.Frame(self.master)
        self.flag_timer_frame.pack()

        self.flag_label = tk.Label(self.flag_timer_frame, text=f"Flags: {self.flags_remaining}")
        self.flag_label.pack(side=tk.LEFT, padx=(10, 5))

        self.timer_label = tk.Label(self.flag_timer_frame, text="Timer: 10:00", fg='red', bg='black', relief=tk.SOLID,
                                    bd=2)
        self.timer_label.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.board_frame = tk.Frame(self.master, bd=4, relief=tk.SOLID)
        self.board_frame.pack()

        for row in range(self.board_size):
            for col in range(self.board_size):
                button = tk.Button(self.board_frame, width=2, height=1)
                button.grid(row=row, column=col)
                button.bind('<Button-1>', lambda event, r=row, c=col: self.click_cell(event, r, c))
                button.bind('<Button-3>', lambda event, r=row, c=col: self.flag_cell(event, r, c))
                self.buttons[row][col] = button

    def place_mines(self):
        mines = 0
        while mines < self.num_mines:
            row = random.randint(0, self.board_size - 1)
            col = random.randint(0, self.board_size - 1)

            if self.board[row][col] != -1:
                self.board[row][col] = -1
                self.mine_locations.append((row, col))
                mines += 1

        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] != -1:
                    self.board[row][col] = self.count_adjacent_mines(row, col)

    def count_adjacent_mines(self, row, col):
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                if 0 <= row + dr < self.board_size and 0 <= col + dc < self.board_size and self.board[row + dr][
                    col + dc] == -1:
                    count += 1
        return count

    def click_cell(self, event, row, col):
        if self.board[row][col] == -1:
            self.game_over(row, col)
        else:
            self.reveal_cell(row, col)
            if self.check_win():
                self.game_win()

    def flag_cell(self, event, row, col):
        button = self.buttons[row][col]
        if button['state'] == tk.NORMAL:
            if self.flags_remaining > 0:
                button['text'] = '🚩'
                button['state'] = tk.DISABLED
                self.flags_remaining -= 1
                self.update_flags_remaining()

    def reveal_cell(self, row, col):
        button = self.buttons[row][col]
        value = self.board[row][col]

        if button['state'] == tk.NORMAL:
            button['state'] = tk.DISABLED
            button['relief'] = tk.SUNKEN

            if value == 0:
                button['text'] = ''
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        if 0 <= row + dr < self.board_size and 0 <= col + dc < self.board_size:
                            self.reveal_cell(row + dr, col + dc)
            else:
                button['text'] = str(value)

    def game_over(self, row, col):
        for r, c in self.mine_locations:
            button = self.buttons[r][c]
            button['text'] = '💣'
            button['fg'] = 'red'
            button['bg'] = 'red'

        self.disable_all_buttons()
        self.timer_label.after_cancel(self.timer_id)

        # Create game over screen
        game_over_window = tk.Toplevel(self.master)
        game_over_window.title("Game Over")

        game_over_label = tk.Label(game_over_window, text="Game Over! You hit a bomb.", font=("Arial", 16, "bold"))
        game_over_label.pack(padx=20, pady=20)

    def game_win(self):
        self.disable_all_buttons()
        self.timer_label.after_cancel(self.timer_id)

        # Create game win screen
        game_win_window = tk.Toplevel(self.master)
        game_win_window.title("Congratulations!")

        game_win_label = tk.Label(game_win_window, text="You win! 😊\nExit the program to play again.",
                                  font=("Arial", 16, "bold"))
        game_win_label.pack(padx=20, pady=20)

    def disable_all_buttons(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                button = self.buttons[row][col]
                button['state'] = tk.DISABLED

    def update_flags_remaining(self):
        self.flag_label['text'] = f"Flags: {self.flags_remaining}"

    def update_timer(self):
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        self.timer_label['text'] = f"Timer: {minutes:02d}:{seconds:02d}"

        if self.time_remaining > 0:
            self.time_remaining -= 1
            self.timer_id = self.timer_label.after(1000, self.update_timer)
        else:
            self.game_over(None, None)

    def check_win(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                button = self.buttons[row][col]
                if button['state'] != tk.DISABLED and self.board[row][col] != -1:
                    return False
        return True


class Minesweeper_Hard:
    def __init__(self, master):
        self.master = master
        self.master.title("Minesweeper")

        self.board_size = 32
        self.num_mines = 99
        self.flags_remaining = self.num_mines
        self.time_remaining = 60  # 1 minute in seconds

        self.board = [[0] * self.board_size for _ in range(self.board_size)]
        self.mine_locations = []
        self.buttons = [[None] * self.board_size for _ in range(self.board_size)]

        self.create_widgets()
        self.place_mines()
        self.update_flags_remaining()
        self.update_timer()

    def create_widgets(self):
        self.flag_timer_frame = tk.Frame(self.master)
        self.flag_timer_frame.pack()

        self.flag_label = tk.Label(self.flag_timer_frame, text=f"Flags: {self.flags_remaining}")
        self.flag_label.pack(side=tk.LEFT, padx=(10, 5))

        self.timer_label = tk.Label(self.flag_timer_frame, text="Timer: 10:00", fg='red', bg='black', relief=tk.SOLID,
                                    bd=2)
        self.timer_label.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.board_frame = tk.Frame(self.master, bd=4, relief=tk.SOLID)
        self.board_frame.pack()

        for row in range(self.board_size):
            for col in range(self.board_size):
                button = tk.Button(self.board_frame, width=2, height=1)
                button.grid(row=row, column=col)
                button.bind('<Button-1>', lambda event, r=row, c=col: self.click_cell(event, r, c))
                button.bind('<Button-3>', lambda event, r=row, c=col: self.flag_cell(event, r, c))
                self.buttons[row][col] = button

    def place_mines(self):
        mines = 0
        while mines < self.num_mines:
            row = random.randint(0, self.board_size - 1)
            col = random.randint(0, self.board_size - 1)

            if self.board[row][col] != -1:
                self.board[row][col] = -1
                self.mine_locations.append((row, col))
                mines += 1

        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] != -1:
                    self.board[row][col] = self.count_adjacent_mines(row, col)

    def count_adjacent_mines(self, row, col):
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                if 0 <= row + dr < self.board_size and 0 <= col + dc < self.board_size and self.board[row + dr][
                    col + dc] == -1:
                    count += 1
        return count

    def click_cell(self, event, row, col):
        if self.board[row][col] == -1:
            self.game_over(row, col)
        else:
            self.reveal_cell(row, col)
            if self.check_win():
                self.game_win()

    def flag_cell(self, event, row, col):
        button = self.buttons[row][col]
        if button['state'] == tk.NORMAL:
            if self.flags_remaining > 0:
                button['text'] = '🚩'
                button['state'] = tk.DISABLED
                self.flags_remaining -= 1
                self.update_flags_remaining()

    def reveal_cell(self, row, col):
        button = self.buttons[row][col]
        value = self.board[row][col]

        if button['state'] == tk.NORMAL:
            button['state'] = tk.DISABLED
            button['relief'] = tk.SUNKEN

            if value == 0:
                button['text'] = ''
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        if 0 <= row + dr < self.board_size and 0 <= col + dc < self.board_size:
                            self.reveal_cell(row + dr, col + dc)
            else:
                button['text'] = str(value)

    def game_over(self, row, col):
        for r, c in self.mine_locations:
            button = self.buttons[r][c]
            button['text'] = '💣'
            button['fg'] = 'red'
            button['bg'] = 'red'

        self.disable_all_buttons()
        self.timer_label.after_cancel(self.timer_id)

        # Create game over screen
        game_over_window = tk.Toplevel(self.master)
        game_over_window.title("Game Over")

        game_over_label = tk.Label(game_over_window, text="Game Over! You hit a bomb.", font=("Arial", 16, "bold"))
        game_over_label.pack(padx=20, pady=20)

    def game_win(self):
        self.disable_all_buttons()
        self.timer_label.after_cancel(self.timer_id)

        # Create game win screen
        game_win_window = tk.Toplevel(self.master)
        game_win_window.title("Congratulations!")

        game_win_label = tk.Label(game_win_window, text="You win! 😊\nExit the program to play again.",
                                  font=("Arial", 16, "bold"))
        game_win_label.pack(padx=20, pady=20)

    def disable_all_buttons(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                button = self.buttons[row][col]
                button['state'] = tk.DISABLED

    def update_flags_remaining(self):
        self.flag_label['text'] = f"Flags: {self.flags_remaining}"

    def update_timer(self):
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        self.timer_label['text'] = f"Timer: {minutes:02d}:{seconds:02d}"

        if self.time_remaining > 0:
            self.time_remaining -= 1
            self.timer_id = self.timer_label.after(1000, self.update_timer)
        else:
            self.game_over(None, None)

    def check_win(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                button = self.buttons[row][col]
                if button['state'] != tk.DISABLED and self.board[row][col] != -1:
                    return False
        return True


def open_difficulty_screen():
    # Hide current screen
    title_label.pack_forget()
    play_button.pack_forget()
    settings_button.pack_forget()
    help_button.pack_forget()
    quit_button.pack_forget()

    # Create difficulty screen
    difficulty_label.pack()
    easy_button.pack()
    medium_button.pack()
    hard_button.pack()
    main_menu_button_difficulty.pack()


def open_help_screen():
    # Hide current screen
    title_label.pack_forget()
    play_button.pack_forget()
    settings_button.pack_forget()
    help_button.pack_forget()
    quit_button.pack_forget()

    # Create help screen
    help_title_label.pack()
    help_text_label.pack()
    main_menu_button_help.pack()


def open_settings_screen():
    # Hide current screen
    title_label.pack_forget()
    play_button.pack_forget()
    settings_button.pack_forget()
    help_button.pack_forget()
    quit_button.pack_forget()

    # Create settings screen
    settings_title_label.pack()
    volume_up_button.pack()
    volume_down_button.pack()
    volume_mute_button.pack()
    main_menu_button_settings.pack()


def open_main_menu():
    # Hide current screens buttons
    difficulty_label.pack_forget()
    easy_button.pack_forget()
    medium_button.pack_forget()
    hard_button.pack_forget()
    main_menu_button_difficulty.pack_forget()

    help_title_label.pack_forget()
    help_text_label.pack_forget()
    main_menu_button_help.pack_forget()

    settings_title_label.pack_forget()
    volume_up_button.pack_forget()
    volume_down_button.pack_forget()
    volume_mute_button.pack_forget()
    main_menu_button_settings.pack_forget()

    # Show main menu buttons
    title_label.pack()
    play_button.pack(anchor="center")
    settings_button.pack(anchor="center")
    help_button.pack(anchor="center")
    quit_button.pack(anchor="center")


def easy_difficulty(difficulty):
    difficulty_label.pack_forget()
    easy_button.pack_forget()
    medium_button.pack_forget()
    hard_button.pack_forget()
    main_menu_button_difficulty.pack_forget()

    print(f"Selected difficulty: {difficulty}")
    game = Minesweeper_Easy(root)
    quit_button.pack()


def medium_difficulty(difficulty):
    difficulty_label.pack_forget()
    easy_button.pack_forget()
    medium_button.pack_forget()
    hard_button.pack_forget()
    main_menu_button_difficulty.pack_forget()

    print(f"Selected difficulty: {difficulty}")
    game = Minesweeper_Medium(root)
    quit_button.pack()


def hard_difficulty(difficulty):
    difficulty_label.pack_forget()
    easy_button.pack_forget()
    medium_button.pack_forget()
    hard_button.pack_forget()
    main_menu_button_difficulty.pack_forget()

    print(f"Selected difficulty: {difficulty}")
    game = Minesweeper_Hard(root)
    quit_button.pack()


def quit_game():
    root.destroy()


# Create main window
root = tk.Tk()
root.title("Minesweeper")

# Set window size
root.geometry("400x300")

# Create title label
title_label = tk.Label(root, text="Minesweeper💣", font=("Arial", 24, "bold"))

# Create buttons
play_button = tk.Button(root, text="Play", command=open_difficulty_screen, width=15, height=2)
settings_button = tk.Button(root, text="Settings", command=open_settings_screen, width=15, height=2)
help_button = tk.Button(root, text="Help", command=open_help_screen, width=15, height=2)
quit_button = tk.Button(root, text="Quit", command=quit_game, width=15, height=2)

# Create difficulty screen
difficulty_label = tk.Label(root, text="Difficulty", font=("Arial", 24, "bold"))
easy_button = tk.Button(root, text="Easy", command=lambda: easy_difficulty("Easy"), width=15, height=2, fg='green')
medium_button = tk.Button(root, text="Medium", command=lambda: medium_difficulty("Medium"), width=15, height=2,
                          fg='yellow')
hard_button = tk.Button(root, text="Hard", command=lambda: hard_difficulty("Hard"), width=15, height=2, fg='red')
main_menu_button_difficulty = tk.Button(root, text="Main Menu", command=open_main_menu, width=15, height=2)

# Create help screen
help_title_label = tk.Label(root, text="HELP", font=("Arial", 24, "bold"))
help_text_label = tk.Label(root, text='''The objective of minesweeper is to clear a minefield under an allocated time without detonating any hidden mines using numerical hints from neighbouring mines.

To reveal a tile, click the left mouse button.

To flag a suspected mine, click the right mouse button.''', justify="left", wraplength=300, padx=10, pady=10)
main_menu_button_help = tk.Button(root, text="Main Menu", command=open_main_menu, width=15, height=2)

# Create the settings screen
settings_title_label = tk.Label(root, text="Settings", font=("Arial", 24, "bold"))
volume_up_button = tk.Button(root, text="Volume 🔊", width=15, height=2)
volume_down_button = tk.Button(root, text="Volume 🔈", width=15, height=2)
volume_mute_button = tk.Button(root, text="Volume 🔇", width=15, height=2)
main_menu_button_settings = tk.Button(root, text="Main Menu", command=open_main_menu, width=15, height=2)

# Place the buttons in the window
title_label.pack()
play_button.pack(anchor="center")
settings_button.pack(anchor="center")
help_button.pack(anchor="center")
quit_button.pack(anchor="center")

# Hide the difficulty, help and settings screens initially
difficulty_label.pack_forget()
easy_button.pack_forget()
medium_button.pack_forget()
hard_button.pack_forget()
main_menu_button_difficulty.pack_forget()

help_title_label.pack_forget()
help_text_label.pack_forget()
main_menu_button_help.pack_forget()

settings_title_label.pack_forget()
volume_up_button.pack_forget()
volume_down_button.pack_forget()
volume_mute_button.pack_forget()
main_menu_button_settings.pack_forget()

# Start the main loop
root.mainloop()