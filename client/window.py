
import logging

import tkinter as tk

import context
import client


log = logging.getLogger(__name__)


def refresh_online_users(current_user):
    window = context.get_window()
    authenticated_frame = context.get_frame('authenticated')

    users = client.get_online_users()

    labels = []
    for lbl, button in labels:
        lbl.destroy()
        button.destroy()

    for idx, user in enumerate(users):
        if idx <= 10:
            lbl = tk.Label(authenticated_frame, text=user)
            lbl.grid(row=3 + idx, column=0, columnspan=2)

            open_chat_button = tk.Button(authenticated_frame,
                                         text="Open",
                                         command=lambda f=current_user, t=user: show_chat_page(f, t))
            open_chat_button.grid(row=3 + idx, column=2, columnspan=2)

            labels.append((lbl, open_chat_button))
        else:
            break

    window.after(5000, lambda: refresh_online_users(current_user))


def refresh_active_chats(current_user):
    window = context.get_window()
    authenticated_frame = context.get_frame('authenticated')

    users = client.get_active_chats()

    labels = []
    for lbl, button in labels:
        lbl.destroy()
        button.destroy()

    for idx, user in enumerate(users):
        if idx <= 10:
            lbl = tk.Label(authenticated_frame, text=user)
            lbl.grid(row=3 + idx, column=5, columnspan=2)

            open_chat_button = tk.Button(authenticated_frame,
                                         text="Open",
                                         command=lambda f=current_user, t=user: show_chat_page(f, t))
            open_chat_button.grid(row=3 + idx, column=7, columnspan=2)

            labels.append((lbl, open_chat_button))
        else:
            break

    window.after(5000, lambda: refresh_active_chats(current_user))


def show_main_page(username):
    window = context.get_window()

    authenticated_frame = tk.Frame(window)
    authenticated_frame.grid(row=0, column=0, sticky="nsew")

    label = tk.Label(authenticated_frame, text=f"Hello {username}!")
    label.grid(row=0, column=0, columnspan=3)

    label = tk.Label(authenticated_frame, text="Online Users")
    label.grid(row=2, column=0, columnspan=4)

    label = tk.Label(authenticated_frame, text="Active Chats")
    label.grid(row=2, column=5, columnspan=4)

    def logout_action():
        context.delete_token()
        show_login_page()

    # Create logout button
    logout = tk.Button(authenticated_frame,
                       text="Logout",
                       command=logout_action)
    logout.grid(row=0, column=4, columnspan=2)

    authenticated_frame.tkraise()
    context.set_frame('authenticated', authenticated_frame)

    refresh_online_users(username)
    refresh_active_chats(username)


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


def refresh_chat_page(username):
    chat_content = client.view_chat(username)

    chat_frame = context.get_frame(f'chat_{username}')

    buff = 2

    for idx, chat_entry in enumerate(chat_content):
        label = tk.Label(chat_frame, text=chat_entry['uname_from'])
        label.grid(row=buff + 1 + 3 * idx, column=0, columnspan=3)

        label = tk.Label(chat_frame, text=chat_entry['message'])
        label.grid(row=buff + 2 + 3 * idx, column=0, columnspan=3)

        label = tk.Label(chat_frame, text=' ')
        label.grid(row=buff + 3 + 3 * idx, column=0, columnspan=3)

    context.get_window().after(1000, lambda: refresh_chat_page(username))


def show_chat_page(host, remote):
    window = context.get_window()

    chat_frame = tk.Frame(window)
    context.set_frame(f'chat_{remote}', chat_frame)
    chat_frame.grid(row=0, column=0, sticky="nsew")

    label = tk.Label(chat_frame, text=f"Chat with {remote}")
    label.grid(row=0, column=0, columnspan=3)

    exit_button = tk.Button(chat_frame,
                            text="Exit",
                            command=lambda: show_main_page(host))
    exit_button.grid(row=0, column=3)

    message_label = tk.Label(chat_frame, text="Message:")
    message_label.grid(row=1, column=0)
    message_entry = tk.Entry(message_label)
    message_entry.grid(row=1, column=1, columnspan=3)

    # Create login button
    def send_chat_action():
        message = message_entry.get()
        client.send_message(remote, message)
        message_entry.delete(0, tk.END)

        # action

    send_button = tk.Button(chat_frame,
                             text="Send!",
                             command=send_chat_action)
    send_button.grid(row=1, column=4)

    chat_frame.tkraise()

    refresh_chat_page(remote)


def initialize():
    # create tkinter window
    window = tk.Tk()
    # save in global context
    context.set_window(window)

    # title window
    window.title("TCP Chat Client")

    show_login_page()

    window.mainloop()
