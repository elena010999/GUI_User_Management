#!/usr/bin/env python3
from tkinter import messagebox
from logic.helper_functions import run_pkexec

def delete_user(username):
    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{username}'?")
    if not confirm:
        return

    run_pkexec(
        ["deluser", "--remove-home", username],
        f"User '{username}' deleted successfully!",
        f"Failed to delete user '{username}'."
    )

