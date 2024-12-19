
import tkinter as tk
import context
import client
import logging


log = logging.getLogger(__name__)


def refresh_online_users():
    window = context.get_window()
    authenticated_frame = context.get_frame('authenticated')

    users = client.get_online_users()

    labels = []
    for lbl in labels:
        lbl.destroy()

    for idx, user in enumerate(users):
        if idx <= 10:
            lbl = tk.Label(authenticated_frame, text=user)
            lbl.grid(row=3 + idx, column=0, columnspan=2)
            labels.append(lbl)
        else:
            break

    window.after(5000, refresh_online_users)


def show_main_page(username):
    window = context.get_window()

    authenticated_frame = tk.Frame(window)
    authenticated_frame.grid(row=0, column=0, sticky="nsew")

    label = tk.Label(authenticated_frame, text=f"Hello {username}!")
    label.grid(row=0, column=0, columnspan=2)

    label = tk.Label(authenticated_frame, text="Online Users")
    label.grid(row=2, column=0, columnspan=2)

    def logout_action():
        context.delete_token()
        show_login_page()

    # Create logout button
    logout = tk.Button(authenticated_frame,
                       text="Logout",
                       command=logout_action)
    logout.grid(row=1, column=0, columnspan=2)

    authenticated_frame.tkraise()
    context.set_frame('authenticated', authenticated_frame)

    refresh_online_users()


def show_login_page():
    window = context.get_window()

    login_frame = tk.Frame(window)
    context.set_frame('login', login_frame)
    login_frame.grid(row=0, column=0, sticky="nsew")

    # Create labels and entry widgets
    username_label = tk.Label(login_frame, text="Username:")
    username_label.grid(row=1, column=0)
    username_entry = tk.Entry(login_frame)
    username_entry.grid(row=1, column=1)

    password_label = tk.Label(login_frame, text="Password:")
    password_label.grid(row=2, column=0)
    password_entry = tk.Entry(login_frame, show="*")  # Hide password characters
    password_entry.grid(row=2, column=1)

    # Create login button
    def login_button_action():
        username = username_entry.get()
        password = password_entry.get()

        log.info(f"Attempting login with {username}:{password}")

        if client.verify_credentials(username, password):
            show_main_page(username)
            username_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)
        else:
            label = tk.Label(login_frame, text="Bad login!")
            label.grid(row=0, column=0, columnspan=2)

    login_button = tk.Button(login_frame,
                             text="Login",
                             command=login_button_action)
    login_button.grid(row=3, column=0, columnspan=2)

    # Create account button
    def create_account_action():
        username = username_entry.get()
        password = password_entry.get()

        created, error = client.create_account(username, password)
        if created:
            show_main_page(username)
        else:
            label = tk.Label(login_frame, text=error)
            label.grid(row=0, column=0, columnspan=2)

        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)

    create_account_button = tk.Button(login_frame,
                                      text="Create Account",
                                      command=create_account_action)
    create_account_button.grid(row=4, column=0, columnspan=2)

    login_frame.tkraise()


def initialize():
    # create tkinter window
    window = tk.Tk()
    # save in global context
    context.set_window(window)

    # title window
    window.title("TCP Chat Client")

    show_login_page()

    window.mainloop()
