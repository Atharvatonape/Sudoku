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
    """
    Main function to set up the Tkinter window and run the application.
    """
    global sudoku_solution
    app = tk.Tk()
    app.title("Sudoku Game")
    app.geometry('600x700')
    # Set a modern background color
    app.configure(bg='#f0f0f0')  # Light grey background

    # Create a frame with a slightly different background color for contrast
    frame = tk.Frame(app, bg='#e0e0e0', padx=20, pady=20)  # Slightly darker shade
    frame.pack(expand=True, padx=20, pady=20)  # Consistent padding for neat layout


     # Read the Sudoku puzzle from CSV
    sudoku_df = pd.read_csv("challenges\sudoku_puzzle.csv", header=None)
    sudoku_puzzle = sudoku_df.values.tolist()

    # Create the Sudoku grid layout inside the frame
    create_grid(frame, sudoku_puzzle)

    # Creating buttons for new game, reset, submit, and quit
    btn_new = create_button(frame, 'New', new_game, 9, 0, 2)
    btn_reset = create_button(frame, 'Reset', reset_game, 9, 2, 2)
    btn_submit = create_button(frame, 'Submit', submit_answers, 9, 4, 2)
    btn_quit = create_button(frame, 'Quit',lambda: quit_game(app), 9, 6, 2)
    btn_clear = create_button(frame, 'Clear',lambda: clear_answers, 9, 8, 2)
    btn_check = create_button(frame, 'Check', lambda:check_answers(sudoku_solution), 10, 2, 2)
    btn_check_all = create_button(frame, 'Check ALL', lambda:confirm_check_all(sudoku_solution), 10, 4, 3)
   

    # btn_new = tk.Button(frame, text='New', command=new_game)
    # btn_new.grid(row=9, column=0, columnspan=2, sticky="ew")

    # btn_reset = tk.Button(frame, text='Reset', command=reset_game)
    # btn_reset.grid(row=9, column=2, columnspan=2, sticky="ew")

    # btn_submit = tk.Button(frame, text='Submit', command=submit_answers)
    # btn_submit.grid(row=9, column=4, columnspan=2, sticky="ew")

    # btn_quit = tk.Button(frame, text='Quit', command=lambda: quit_game(app))
    # btn_quit.grid(row=9, column=6, columnspan=3, sticky="ew")

    # # Inside the main function, after creating other buttons
    # btn_clear = tk.Button(frame, text='Clear', command=clear_answers)
    # btn_clear.grid(row=9, column=8, columnspan=2, sticky="ew")

    # Inside the main function, after creating other buttons
    # Inside the main function
    sudoku_solution_df = pd.read_csv("challenges\sudoku_solution.csv", header=None)
    sudoku_solution = sudoku_solution_df.values.tolist()

    # btn_check = tk.Button(frame, text='Check', command=lambda: check_answers(sudoku_solution))
    # btn_check.grid(row=10, column=4, columnspan=2, sticky="ew")

    # # Inside the main function, after creating other buttons
    # btn_check_all = tk.Button(frame, text='Check All', command=lambda: confirm_check_all(sudoku_solution))
    # btn_check_all.grid(row=10, column=6, columnspan=2, sticky="ew")





    # Start the Tkinter event loop
    app.mainloop()

if __name__ == "__main__":
    main()
