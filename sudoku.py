import tkinter as tk
import pandas as pd
import tkinter.messagebox


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



def new_game():
    """Starts a new Sudoku game."""
    pass  # Logic for starting a new game goes here

def reset_game():
    """Resets the current Sudoku puzzle."""
    pass  # Logic for resetting the game goes here

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

def confirm_check_all():
    """Ask the user for confirmation to check all answers."""
    response = tk.messagebox.askyesno("Confirm", "Do you want to reveal all answers?")
    if response:
        check_all_answers()

def check_all_answers():
    """Reveals all answers, marking correct and incorrect ones."""
    for row in range(9):
        for col in range(9):
            entry = entries[row][col]
            correct_value = sudoku_solution[row][col]

            if entry.cget('state') != 'readonly':  # Check only user-filled cells
                try:
                    user_value = int(entry.get())
                    if user_value == correct_value:
                        entry.config(bg='light green')
                    else:
                        entry.config(bg='red')
                except ValueError:
                    # If the cell is empty or non-integer, mark it as wrong
                    entry.config(bg='red')
            
            # Update the entry with the correct value and make it readonly
            entry.delete(0, tk.END)
            entry.insert(0, str(correct_value))
            entry.config(state='readonly')



sudoku_solution = None 

def main():
    """
    Main function to set up the Tkinter window and run the application.
    """
    global sudoku_solution
    app = tk.Tk()
    app.title("Sudoku Game")


    # Read the Sudoku puzzle from CSV
    sudoku_df = pd.read_csv("challenges\sudoku_puzzle.csv", header=None)
    sudoku_puzzle = sudoku_df.values.tolist()



    # Create a frame to hold the Sudoku grid and buttons
    frame = tk.Frame(app)
    frame.pack(expand=True)

    # Create the Sudoku grid layout inside the frame
    create_grid(frame, sudoku_puzzle)

    # Creating buttons for new game, reset, submit, and quit
    btn_new = tk.Button(frame, text='New', command=new_game)
    btn_new.grid(row=9, column=0, columnspan=2, sticky="ew")

    btn_reset = tk.Button(frame, text='Reset', command=reset_game)
    btn_reset.grid(row=9, column=2, columnspan=2, sticky="ew")

    btn_submit = tk.Button(frame, text='Submit', command=submit_answers)
    btn_submit.grid(row=9, column=4, columnspan=2, sticky="ew")

    btn_quit = tk.Button(frame, text='Quit', command=lambda: quit_game(app))
    btn_quit.grid(row=9, column=6, columnspan=3, sticky="ew")

    # Inside the main function, after creating other buttons
    btn_clear = tk.Button(frame, text='Clear', command=clear_answers)
    btn_clear.grid(row=9, column=8, columnspan=2, sticky="ew")

    # Inside the main function, after creating other buttons
    # Inside the main function
    sudoku_solution_df = pd.read_csv("challenges\sudoku_solution.csv", header=None)
    sudoku_solution = sudoku_solution_df.values.tolist()

    btn_check = tk.Button(frame, text='Check', command=lambda: check_answers(sudoku_solution))
    btn_check.grid(row=10, column=4, columnspan=2, sticky="ew")

    # Inside the main function, after creating other buttons
    btn_check_all = tk.Button(frame, text='Check All', command=confirm_check_all)
    btn_check_all.grid(row=10, column=6, columnspan=2, sticky="ew")




    # Start the Tkinter event loop
    app.mainloop()

if __name__ == "__main__":
    main()
