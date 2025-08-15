#!/usr/bin/env python3
from tkinter import messagebox
from logic.helper_functions import get_all_users, get_all_groups

def list_users_shells():
    users = []
    with open("/etc/passwd", "r") as f:
        for line in f:
            parts = line.strip().split(":")
            if int(parts[2]) >= 1000:
                users.append(f"{parts[0]} → {parts[-1]}")
    messagebox.showinfo("Users and Shells", "\n".join(users) if users else "No users found.")

