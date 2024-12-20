
import logging

import tkinter as tk

import context
import client
from exception import ServerException

log = logging.getLogger(__name__)


def poll_online_users(current_user):

    authenticated_frame = context.get_frame('authenticated')

    if authenticated_frame is None:
        # if frame no longer exists in global context, stop polling
        return

    # retrieve list of online users from server
    users = client.get_online_users()

    labels = []
    for lbl, button in labels:
        lbl.destroy()
        button.destroy()

    for idx, user in enumerate(users[:10]):
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

    # poll every 5 seconds
    context.get_window().after(5000, lambda: poll_online_users(current_user))


def poll_active_chats(current_user):

    authenticated_frame = context.get_frame('authenticated')
    if authenticated_frame is None:
        # if frame no longer exists in global context, stop polling
        return

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

    # poll every 5 seconds
    context.get_window().after(5000, lambda: poll_active_chats(current_user))


def refresh_chat_page(username):
    chat_frame = context.get_frame(f'chat_{username}')
    if chat_frame is None:
        # if frame no longer exists in global context, stop polling
        return

    chat_content = client.view_chat(username)

    # display all chat content on screen
    buff = 2
    for idx, chat_entry in enumerate(chat_content):
        label = tk.Label(chat_frame, text=chat_entry['uname_from'])
        label.grid(row=buff + 1 + 3 * idx, column=0, columnspan=3)

        label = tk.Label(chat_frame, text=chat_entry['message'])
        label.grid(row=buff + 2 + 3 * idx, column=0, columnspan=3)

        label = tk.Label(chat_frame, text=' ')
        label.grid(row=buff + 3 + 3 * idx, column=0, columnspan=3)

    # poll every second
    context.get_window().after(1000, lambda: refresh_chat_page(username))


def show_main_page(username):
    window = context.get_window()

    # init frame
    authenticated_frame = tk.Frame(window)
    authenticated_frame.grid(row=0, column=0, sticky="nsew")
    context.set_frame('authenticated', authenticated_frame)

    # init page text
    label = tk.Label(authenticated_frame, text=f"Hello {username}!")
    label.grid(row=0, column=0, columnspan=3)

    label = tk.Label(authenticated_frame, text="Online Users")
    label.grid(row=2, column=0, columnspan=4)

    label = tk.Label(authenticated_frame, text="Active Chats")
    label.grid(row=2, column=5, columnspan=4)

    # Create logout button
    def logout_action():
        context.delete_token()
        authenticated_frame.destroy()
        context.set_frame('authenticated', None)
        show_login_page()

    logout = tk.Button(authenticated_frame,
                       text="Logout",
                       command=logout_action)
    logout.grid(row=0, column=4, columnspan=2)

    # display frame
    authenticated_frame.tkraise()

    # begin polling server
    poll_online_users(username)
    poll_active_chats(username)


def show_login_page():
    # retrieve window from global context
    window = context.get_window()
    # initialize login frame
    login_frame = tk.Frame(window)
    login_frame.grid(row=0, column=0, sticky="nsew")
    # save in global context
    context.set_frame('login', login_frame)

    # init error tracking
    current_error_label = tk.Label(login_frame, text="")
    current_error_label.grid(row=0, column=0, columnspan=3)

    # create login form
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
            username_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)
            login_frame.destroy()
            context.set_frame('login', None)
            show_main_page(username)
        else:
            # error output
            current_error_label.configure(text="Bad Username/Password")

    login_button = tk.Button(login_frame,
                             text="Login",
                             command=login_button_action)
    login_button.grid(row=3, column=0, columnspan=2)

    # Create account button
    def create_account_action():
        username = username_entry.get()
        password = password_entry.get()

        try:
            if client.create_account(username, password):
                username_entry.delete(0, tk.END)
                password_entry.delete(0, tk.END)
                login_frame.destroy()
                context.set_frame('login', None)
                show_main_page(username)
        except ServerException as e:
            # error output
            current_error_label.configure(text=e.message)

    create_account_button = tk.Button(login_frame,
                                      text="Create Account",
                                      command=create_account_action)
    create_account_button.grid(row=4, column=0, columnspan=2)

    # display login frame on screen
    login_frame.tkraise()


def show_chat_page(host_username, target_username):
    window = context.get_window()

    # init chat window frame
    chat_frame = tk.Frame(window)
    context.set_frame(f'chat_{target_username}', chat_frame)
    chat_frame.grid(row=0, column=0, sticky="nsew")

    label = tk.Label(chat_frame, text=f"Chat with {target_username}")
    label.grid(row=0, column=0, columnspan=3)

    # message field
    message_label = tk.Label(chat_frame, text="Message:")
    message_label.grid(row=1, column=0)
    message_entry = tk.Entry(message_label)
    message_entry.grid(row=1, column=1, columnspan=3)

    # exit button
    def exit_action():
        # on exit chat window, destroy chat frame
        chat_frame.destroy()
        context.set_frame(f'chat_{target_username}', None)
        # open main page
        show_main_page(host_username)

    exit_button = tk.Button(chat_frame,
                            text="Exit",
                            command=exit_action)
    exit_button.grid(row=0, column=3)

    # send chat button
    def send_chat_action():
        # on send, retrieve message
        message = message_entry.get()
        # send
        client.send_message(target_username, message)
        # and clear message field
        message_entry.delete(0, tk.END)

    send_button = tk.Button(chat_frame,
                            text="Send!",
                            command=send_chat_action)
    send_button.grid(row=1, column=4)

    # display chat window page
    chat_frame.tkraise()

    # begin pulling
    refresh_chat_page(target_username)


def initialize():
    # create tkinter window
    window = tk.Tk()
    # save in global context
    context.set_window(window)
    # set window title
    window.title("TCP Chat Client")
    # display login page (entry)
    show_login_page()
    # start tkinter application
    window.mainloop()
