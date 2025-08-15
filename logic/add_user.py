#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox, ttk
from logic.helper_functions import _root, run_pkexec, get_all_users
import subprocess

# ======= Get available shells dynamically =======
def get_available_shells():
    shells = []
    with open("/etc/shells", "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                shells.append(line)
    return shells

# ======= CREATE USER WINDOW =======
def create_user():
    users = get_all_users()
    shells = get_available_shells()

    top = tk.Toplevel(_root)
    top.title("Create New User")
    top.geometry("400x300")
    top.resizable(False, False)

    # Username
    tk.Label(top, text="Username:").pack(pady=5)
    username_var = tk.StringVar()
    tk.Entry(top, textvariable=username_var).pack(pady=5, fill="x", padx=10)

    # Shell selection
    tk.Label(top, text="Shell (optional):").pack(pady=5)
    shell_var = tk.StringVar()
    shell_combo = ttk.Combobox(top, textvariable=shell_var, values=shells, state="readonly")
    shell_combo.pack(pady=5, fill="x", padx=10)
    shell_combo.set("/bin/bash")  # default

    # Submit button
    def on_submit():
        username = username_var.get().strip()
        shell = shell_var.get().strip() or None

        if not username:
            messagebox.showerror("Error", "Username is required!")
            return
        if username in users:
            messagebox.showerror("Error", f"User '{username}' already exists!")
            return

        cmd = ["useradd", username]
        if shell:
            cmd += ["-s", shell]

        # Default group = username
        cmd += ["-G", username]

        run_pkexec(cmd,
                   f"User '{username}' created successfully!",
                   f"Failed to create user '{username}'. Make sure you have sudo privileges.")
        top.destroy()

    tk.Button(top, text="Create User", command=on_submit).pack(pady=10)

