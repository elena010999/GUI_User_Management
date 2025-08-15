#!/usr/bin/env python3
from tkinter import simpledialog, messagebox
from logic.helper_functions import _root, run_pkexec

def modify_user(username):
    options = ["Change Shell", "Change Username", "Change Home Directory"]
    choice = simpledialog.askstring(
        "Modify User",
        f"Select modification for {username} (Shell/Username/Home):",
        parent=_root
    )
    if not choice or choice not in options:
        return

    cmd = ["usermod", username]

    if choice == "Change Shell":
        new_shell = simpledialog.askstring("Modify User", "Enter new shell:", parent=_root)
        if not new_shell: return
        cmd += ["-s", new_shell]

    elif choice == "Change Username":
        new_username = simpledialog.askstring("Modify User", "Enter new username:", parent=_root)
        if not new_username: return
        cmd += ["-l", new_username]

    elif choice == "Change Home Directory":
        new_home = simpledialog.askstring("Modify User", "Enter new home directory path:", parent=_root)
        if not new_home: return
        cmd += ["-d", new_home]

    run_pkexec(cmd, f"User '{username}' modified successfully!", f"Failed to modify user '{username}'.")

