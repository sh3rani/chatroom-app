import os
import tkinter as tk
from tkinter import messagebox

# Global variables
logged_in_user = None
chat_list = []

# Function to register a new user
def register():
    username = entry_username.get()
    password = entry_password.get()

    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as file:
            users = file.readlines()
            for user in users:
                stored_username, _ = user.split(',')
                if stored_username.strip() == username:
                    messagebox.showwarning("Registration Failed", "Username already exists!")
                    return

    with open('users.txt', 'a') as file:
        file.write(f"{username},{password}\n")

    messagebox.showinfo("Registration Success", "Registration successful! You can now log in.")

# Function to log in an existing user
def login():
    global logged_in_user, chat_list
    username = entry_username.get()
    password = entry_password.get()

    if not os.path.exists('users.txt'):
        messagebox.showerror("Login Failed", "No users registered yet.")
        return

    with open('users.txt', 'r') as file:
        users = file.readlines()
        for user in users:
            stored_username, stored_password = user.strip().split(',')
            if stored_username == username and stored_password == password:
                logged_in_user = username  # Save logged-in user
                messagebox.showinfo("Login Success", "Login successful!")
                load_user_chat()  # Load user's chat data
                return

    messagebox.showerror("Login Failed", "Invalid username or password.")

# Function to load user chat data
def load_user_chat():
    global chat_list

    login_frame.pack_forget()  # Hide the login frame
    toggle_menu()  # Toggle menu to be shown

    chat_frame = tk.Frame(root)
    chat_frame.pack(expand=True, fill=tk.BOTH)

    welcome_label = tk.Label(chat_frame, text=f"Home", font=("Arial", 20))
    welcome_label.pack(pady=20)

# Function to save user chat data
def save_user_chat():
    if not logged_in_user:
        return

    user_file = f"{logged_in_user}_chat.txt"
    with open(user_file, "w") as file:
        for chat in chat_list:
            file.write(f'{chat["Number"]}|{chat["Name"]}\n')

# Function to toggle the menu
def toggle_menu():
    
    def collapse_toggle_menu():
        toggle_menu_fm.destroy()
        toggle_btn.config(text='☰')
        toggle_btn.config(command=toggle_menu)

    toggle_menu_fm = tk.Frame(root, bg='#158aff')
    options_frame = tk.Frame(root, bg='#158aff')

    home_btn = tk.Button(toggle_menu_fm, text='Home', font=('Bold'), bd=0, bg='#158aff', fg='white',
                         activebackground='#158aff', activeforeground='white')
    home_btn.place(x=10, y=20)

    Chatrooms_btn = tk.Button(toggle_menu_fm, text='Chatroom', bg='#158aff', fg='white',
                               font=('Bold', 20), bd=0, activebackground='#158aff', activeforeground='white')
    Chatrooms_btn.place(x=10, y=60)

    Settings_btn = tk.Button(toggle_menu_fm, text='Settings', bg='#158aff', fg='white',
                             font=('Bold', 20), bd=0, activebackground='#158aff', activeforeground='white')
    Settings_btn.place(x=10, y=100)

    window_height = root.winfo_height()
    toggle_menu_fm.place(x=0, y=50, height=window_height, width=200)

    toggle_btn.config(text='x')
    toggle_btn.config(command=collapse_toggle_menu)

def logout():
    global logged_in_user
    logged_in_user = None
    try:
        head_Frame.destroy()
        toggle_menu_fm.destroy()
    except:
        pass
    create_login_frame()



# Function to create the top frame
def top_frame():

    global toggle_btn, head_Frame
    # If the frame already exists, destroy it to avoid duplication
    try:
        head_Frame.destroy()
    except:
        pass
    head_Frame = tk.Frame(root, bg='#158aff', highlightbackground='White', highlightthickness=1)

    toggle_btn = tk.Button(head_Frame, text='☰', command=toggle_menu)
    toggle_btn.pack(side=tk.LEFT)

    title_lb = tk.Label(head_Frame, text='Chats', bg='#158aff', font=('Bold', 20))
    title_lb.pack(side=tk.LEFT)
    head_Frame.pack(side=tk.TOP, fill=tk.X)
    head_Frame.pack_propagate(False)
    head_Frame.configure(height=50)

# Function to create the login frame
def create_login_frame():
    global entry_username, entry_password, login_frame

    login_frame = tk.Frame(root)
    login_frame.pack(expand=True)

    label_username = tk.Label(login_frame, text="Username:")
    label_username.pack()

    entry_username = tk.Entry(login_frame)
    entry_username.pack(pady=10)

    label_password = tk.Label(login_frame, text="Password:")
    label_password.pack()

    entry_password = tk.Entry(login_frame, show="*")
    entry_password.pack(pady=10)

    btn_login = tk.Button(login_frame, text="Login", command=login)
    btn_login.pack(pady=5)

    btn_register = tk.Button(login_frame, text="Register", command=register)
    btn_register.pack(pady=5)



# Main window setup
root = tk.Tk()
root.title("Chatroom App")
root.attributes('-fullscreen', True)
root.configure(background='#FFFFFF')

# Create the top frame
top_frame()

# Create the login page frame initially
create_login_frame()

# Bind the Escape key to toggle fullscreen mode
root.bind("<Escape>", lambda e: root.attributes("-fullscreen", not root.attributes("-fullscreen")))

# Start the Tkinter event loop
root.mainloop()
