#!/usr/bin/env python

import logging
import tkinter as tk

import context
import client


def handle_login(username, password):
    logging.info(f"Attempting login with {username}:{password}")

    if client.verify_credentials(username, password):
        init_authenticated_page(username).tkraise()
    else:
        frame = init_login_page()
        label = tk.Label(frame, text="Bad login!")
        label.grid(row=0, column=0, columnspan=2)


def handle_logout():
    context.delete_token()
    init_login_page().tkraise()


def handle_create_account(username, password):
    created, error = client.create_account(username, password)
    if created:
        init_authenticated_page(username).tkraise()
    else:
        frame = init_login_page()
        label = tk.Label(frame, text=error)
        label.grid(row=0, column=0, columnspan=2)


def init_login_page():
    window = context.get_window()

    login_frame = tk.Frame(window)
    context.add_frame('login', login_frame)
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
        handle_login(username_entry.get(), password_entry.get())
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)

    login_button = tk.Button(login_frame,
                             text="Login",
                             command=login_button_action)
    login_button.grid(row=3, column=0, columnspan=2)

    # Create account button
    def create_account_action():
        handle_create_account(username_entry.get(), password_entry.get())
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)

    create_account_button = tk.Button(login_frame,
                                      text="Create Account",
                                      command=create_account_action)
    create_account_button.grid(row=4, column=0, columnspan=2)

    return login_frame


def init_authenticated_page(username):
    window = context.get_window()

    authenticated_frame = tk.Frame(window)
    context.add_frame('authenticated', authenticated_frame)
    authenticated_frame.grid(row=0, column=0, sticky="nsew")

    label = tk.Label(authenticated_frame, text=f"Hello {username}!")
    label.grid(row=0, column=0, columnspan=2)

    # Create logout button
    logout = tk.Button(authenticated_frame,
                       text="Logout",
                       command=handle_logout)
    logout.grid(row=1, column=0, columnspan=2)

    return authenticated_frame


def main():
    logging.basicConfig(level=logging.DEBUG)

    # create tkinter window
    window = tk.Tk()
    # save in global context
    context.set_window(window)

    # title window
    window.title("TCP Chat Client")

    init_login_page().tkraise()

    window.mainloop()


if __name__ == "__main__":
    main()
