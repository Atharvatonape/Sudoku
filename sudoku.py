import tkinter as tk
import pandas as pd
import tkinter.messagebox as mssg
import time
import login


def create_grid(frame, puzzle):
    global entries
    entries = []

    # Validation command
    vcmd = (frame.register(validate_input), '%P')

    for row in range(9):
        row_entries = []
        for col in range(9):
            value = puzzle[row][col]
            entry = tk.Entry(frame, width=2, font=('Arial', 18), justify='center', validate="key", validatecommand=vcmd)
            entry.grid(row=row, column=col, stick="nsew", padx=1, pady=1)
            if value != 0:
                entry.insert(tk.END, str(value))
                entry.config(state='readonly')
            row_entries.append(entry)
        entries.append(row_entries)

def create_button(frame, text, command, row, column, columnspan):
    """Helper function to create a styled button."""
    button = tk.Button(frame, text=text, command=command,
                       bg='#4CAF50', fg='white',  # Green background with white text
                       font=('Helvetica', 12, 'bold'),
                       borderwidth=0,  # Flat design
                       highlightthickness=0,  # Remove border highlight
                       relief='flat')  # Flat relief for modern look
    button.grid(row=row, column=column, columnspan=columnspan, sticky="ew", padx=5, pady=5)

    # Adding hover effect
    button.bind("<Enter>", lambda e, b=button: b.configure(bg='#45a049'))  # Darker shade on hover
    button.bind("<Leave>", lambda e, b=button: b.configure(bg='#4CAF50'))  # Original color when not hovered

    return button

def submit_answers():
    """Locks only the filled cells to prevent further changes."""
    for row_entries in entries:
        for entry in row_entries:
            if entry.get() and entry.cget('state') != 'readonly':
                entry.config(state='readonly')
                entry.user_filled = True  # Mark the entry as filled by the user

def clear_answers():
    """Clears the entries filled by the user."""
    for row_entries in entries:
        for entry in row_entries:
            if hasattr(entry, 'user_filled') and entry.user_filled:
                entry.delete(0, tk.END)
                entry.config(state='normal')
                entry.user_filled = False  # Reset the marker

def check_answers(sudoku_solution):
    """Checks the answers against the solution and updates cell colors."""
    for row in range(9):
        for col in range(9):
            entry = entries[row][col]
            if entry.cget('state') != 'readonly':  # Check only user-filled cells
                try:
                    user_value = int(entry.get())
                    correct_value = sudoku_solution[row][col]
                    if user_value == correct_value:
                        entry.config(bg='light green')
                    else:
                        entry.config(bg='red')
                except ValueError:
                    # If the cell is empty or non-integer, do nothing
                    pass

def update_timer(label):
    """ Update the timer every second """
    global start_time
    if start_time:
        elapsed_time = time.time() - start_time
        label.config(text=time.strftime('%H:%M:%S', time.gmtime(elapsed_time)))
        label.after(1000, lambda: update_timer(label))

def start_timer(label):
    """ Start the timer """
    global start_time
    start_time = time.time()
    update_timer(label)

def start_sudoku_game():
    main()  # Assuming main sets up your game
    start_timer(timer_label)  # Start the timer


def new_game(app):
    """Starts a new Sudoku game."""
    pass  # Logic for starting a new game goes here
    ans = mssg.askyesno("Do you really want to restart the game")
    if ans:
        app.destroy()
        main()

def reset_game(app):
    """Resets the current Sudoku puzzle."""
    pass  # Logic for resetting the game goes here
    ans = mssg.askyesno("Do you really want to go back to login")
    if ans:
        app.destroy()
        login.login_up()
        

def quit_game(app):
    """Quits the Sudoku game."""
    app.destroy()

def validate_input(P):
    """Validate that the entry is an integer or empty."""
    if P.isdigit() or P == "":
        return True
    else:
        show_alert()
        return False

def show_alert():
    """Show an alert message when non-integer input is detected."""
    tk.messagebox.showinfo("Invalid Input", "Only integers are accepted")

def confirm_check_all(sudoku_solution):
    """Ask the user for confirmation to check all answers."""
    response = tk.messagebox.askyesno("Confirm", "Do you want to reveal all answers?")
    if response:
        check_all_answers(sudoku_solution)

def check_all_answers(sudoku_solution):
   for row in range(9):
        for col in range(9):
            entry = entries[row][col]
            if entry.cget('state') != 'readonly':  # Check only user-filled cells
                try:
                    user_value = int(entry.get())
                    correct_value = sudoku_solution[row][col]
                    if user_value == correct_value:
                        #entry.config(state='normal')
                        entry.config(bg='light green')
                        #entry.config(state='readonly')
                    else:
                        entry.config(bg='red')
                except ValueError:
                    correct_value = sudoku_solution[row][col]
                    entry.config(bg= 'Yellow')
                    entry.insert(tk.END, str(correct_value))
                    #entry.config(state='readonly')


sudoku_solution = None 

def main():
    global sudoku_solution, start_time, rounds_played, filled_boxes_count, quit_time
    # Initialize global variables
    rounds_played = 0
    filled_boxes_count = 0
    quit_time = None
    start_time = None

    # Initialize the Tkinter window
    app = tk.Tk()
    app.title("Sudoku Game")
    app.geometry('600x700')
    app.configure(bg='#f0f0f0')
    frame = tk.Frame(app, bg='#e0e0e0', padx=20, pady=20)
    frame.pack(expand=True, padx=20, pady=20)

    # Read the Sudoku puzzle and create the grid layout
    sudoku_df = pd.read_csv("challenges\sudoku_puzzle.csv", header=None)
    sudoku_puzzle = sudoku_df.values.tolist()
    create_grid(frame, sudoku_puzzle)

    # Timer label
    timer_label = tk.Label(frame, text="00:00:00", font=('Helvetica', 14))
    timer_label.grid(row=11, column=0, columnspan=9, sticky="ew")

    # Create buttons and other components
    btn_new = create_button(frame, 'New', lambda: new_game(app), 9, 0, 2)
    btn_reset = create_button(frame, 'Reset', lambda: reset_game(app), 9, 2, 2)
    btn_submit = create_button(frame, 'Submit', submit_answers, 9, 4, 2)
    btn_quit = create_button(frame, 'Quit', lambda: quit_game(app), 9, 6, 2 )
    btn_clear = create_button(frame, 'Clear', lambda: clear_answers(), 9, 8, 2)
    btn_check = create_button(frame, 'Check', lambda: check_answers(sudoku_solution), 10, 2, 2)
    btn_check_all = create_button(frame, 'Check ALL', lambda: confirm_check_all(sudoku_solution), 10, 4, 3)

    # Read the Sudoku solution
    sudoku_solution_df = pd.read_csv("challenges\sudoku_solution.csv", header=None)
    sudoku_solution = sudoku_solution_df.values.tolist()

    # Ask the user to start the game
    # //Add a new button functionality to it
    # start_game = tk.messagebox.askyesno("Start Game", "Do you want to start the Sudoku game?")
    # if start_game:
    #     # Start the timer and begin the game
    start_timer(timer_label)
    
    #     # Handle the case where the user chooses not to start the game
    #     # For example, you could display a welcome message or instructions

    # # Start the Tkinter main loop
    app.mainloop()

if __name__ == "__main__":
    main()

