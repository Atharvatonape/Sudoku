import tkinter as tk
from tkinter import messagebox
import sudoku
import csv
import os

# File to store user credentials
CREDENTIALS_FILE = 'credentials.csv'

def verify_login(username, password):
    # Check credentials in the file
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == username and row[1] == password:
                    return True
    return False

def register_user(username, password):
    # Append new user credentials to the file
    with open(CREDENTIALS_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, password])
    messagebox.showinfo("Registration Successful", "You can now login with your credentials.")

def on_login(username_entry, password_entry):
    username = username_entry.get()
    password = password_entry.get()
    if verify_login(username, password):
        login_window.destroy()
        sudoku.main()
    else:
        messagebox.showinfo("Login Failed", "Incorrect username or password")

def on_sign_up(username_entry, password_entry):
    username = username_entry.get()
    password = password_entry.get()
    if username and password:
        register_user(username, password)
    else:
        messagebox.showinfo("Error", "Username and password cannot be empty")

def login():
    global login_window
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry('300x200')

    tk.Label(login_window, text="Username:").pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    tk.Label(login_window, text="Password:").pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    login_button = tk.Button(login_window, text="Login", command=lambda: on_login(username_entry, password_entry))
    login_button.pack()

    sign_up_button = tk.Button(login_window, text="Sign Up", command=lambda: on_sign_up(username_entry, password_entry))
    sign_up_button.pack()

    login_window.mainloop()

if __name__ == "__main__":
    login()
