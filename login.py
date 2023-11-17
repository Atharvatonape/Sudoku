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
                if row[1] == username and row[2] == password:
                    return True
    return False

def register_user(name, username, password):
    # Append new user credentials to the file
    with open(CREDENTIALS_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, username, password])
    messagebox.showinfo("Registration Successful", "You can now login with your credentials.")

def on_login(username_entry, password_entry):
    username = username_entry.get()
    password = password_entry.get()
    if verify_login(username, password):
        login_window.destroy()
        sudoku.main()
    else:
        messagebox.showinfo("Login Failed", "Incorrect username or password")

def on_sign_up(name_entry, username_entry, password_entry, confirm_password_entry, captcha_entry):
    name = name_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()
    captcha = captcha_entry.get()

    if not (name and username and password and confirm_password):
        messagebox.showinfo("Error", "All fields must be filled out")
        return

    if password != confirm_password:
        messagebox.showinfo("Error", "Passwords do not match")
        return

    if captcha != "11":  # Simple captcha check
        messagebox.showinfo("Error", "Captcha is incorrect")
        return

    register_user(name, username, password)

def show_signup_window():
    signup_window = tk.Toplevel(login_window)
    signup_window.title("Sign Up")
    signup_window.geometry('300x300')

    tk.Label(signup_window, text="Name:").pack()
    name_entry = tk.Entry(signup_window)
    name_entry.pack()

    tk.Label(signup_window, text="Username:").pack()
    username_entry = tk.Entry(signup_window)
    username_entry.pack()

    tk.Label(signup_window, text="Password:").pack()
    password_entry = tk.Entry(signup_window, show="*")
    password_entry.pack()

    tk.Label(signup_window, text="Confirm Password:").pack()
    confirm_password_entry = tk.Entry(signup_window, show="*")
    confirm_password_entry.pack()

    tk.Label(signup_window, text="Captcha: 10 + 1 = ").pack()
    captcha_entry = tk.Entry(signup_window)
    captcha_entry.pack()

    sign_up_button = tk.Button(signup_window, text="Sign Up", command=lambda: on_sign_up(name_entry, username_entry, password_entry, confirm_password_entry, captcha_entry))
    sign_up_button.pack()

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

    sign_up_button = tk.Button(login_window, text="Sign Up", command=show_signup_window)
    sign_up_button.pack()

    login_window.mainloop()

if __name__ == "__main__":
    login()
