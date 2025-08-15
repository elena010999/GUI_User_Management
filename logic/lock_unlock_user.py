#!/usr/bin/env python3
from tkinter import messagebox
from logic.helper_functions import run_pkexec
import subprocess

def lock_unlock_user(username):
    try:
        result = subprocess.run(["passwd", "-S", username], capture_output=True, text=True)
        status = result.stdout.split()[1]
        action = "unlock" if status == "L" else "lock"
    except:
        messagebox.showerror("Error", f"Cannot read status for '{username}'")
        return

    cmd = ["usermod", "-U" if action == "unlock" else "-L", username]
    run_pkexec(cmd, f"User '{username}' {action}ed successfully!", f"Failed to {action} user '{username}'.")

