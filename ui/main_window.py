#!/usr/bin/env python3

import tkinter as tk
import ttkbootstrap as tb
from tkinter import messagebox
from logic.helper_functions import get_all_users
from logic.add_user import create_user
from logic.delete_user import delete_user
from logic.modify_user import modify_user
from logic.change_password import change_password
from logic.lock_unlock_user import lock_unlock_user
from logic.add_users_to_groups import add_user_to_group


class UserManagerApp(tb.Window):
    def __init__(self):
        super().__init__(themename="flatly")
        self.title("Linux User Manager")
        self.geometry("900x600")

        # Search box
        self.search_var = tk.StringVar()
        self.search_entry = tb.Entry(self, textvariable=self.search_var, width=40)
        self.search_entry.pack(pady=10)
        self.search_var.trace_add("write", self.on_search)

        # Frame for user list
        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Cache all users at startup for instant filtering
        self.all_users_cache = get_all_users()
        self.show_user_list(self.all_users_cache)

        # Menu buttons
        menu_frame = tk.Frame(self)
        menu_frame.pack(fill="x", pady=5)
        tb.Button(menu_frame, text="Add User", bootstyle="success", command=self.add_user_window).pack(side="left", padx=5)
        tb.Button(menu_frame, text="Refresh", bootstyle="info", command=self.refresh_user_list).pack(side="left", padx=5)

    # ====== SEARCH ======
    def on_search(self, *args):
        search_text = self.search_var.get().lower()
        filtered_users = [u for u in self.all_users_cache if search_text in u.lower()]
        self.show_user_list(filtered_users)

    # ====== RENDER USERS ======
    def show_user_list(self, users):
        # Clear old widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for username in users:
            row_frame = tk.Frame(self.scrollable_frame)
            row_frame.pack(fill="x", pady=2)

            tk.Label(row_frame, text=username, width=20, anchor="w").pack(side="left", padx=5)
            tb.Button(row_frame, text="Modify", bootstyle="info",
                      command=lambda u=username: self.modify_user(u)).pack(side="left", padx=2)
            tb.Button(row_frame, text="Delete", bootstyle="danger",
                      command=lambda u=username: self.delete_user(u)).pack(side="left", padx=2)
            tb.Button(row_frame, text="Password", bootstyle="warning",
                      command=lambda u=username: self.change_password(u)).pack(side="left", padx=2)
            tb.Button(row_frame, text="Lock/Unlock", bootstyle="secondary",
                      command=lambda u=username: self.lock_unlock_user(u)).pack(side="left", padx=2)
            tb.Button(row_frame, text="Add to Group", bootstyle="success",
                      command=lambda u=username: self.add_to_group([u])).pack(side="left", padx=2)

    # ====== REFRESH ======
    def refresh_user_list(self):
        self.all_users_cache = get_all_users()
        self.show_user_list(self.all_users_cache)

    # ====== USER ACTIONS ======
    def add_user_window(self):
        create_user()

    def modify_user(self, username):
        modify_user(username)
        self.refresh_user_list()

    def delete_user(self, username):
        delete_user(username)
        self.refresh_user_list()

    def change_password(self, username):
        change_password(self, username)

    def lock_unlock_user(self, username):
        # This can be improved to check status first
        lock_user(self, username)  # Or unlock_user depending on status

    def add_to_group(self, usernames):
        add_user_to_group(usernames)


if __name__ == "__main__":
    app = UserManagerApp()
    app.mainloop()

