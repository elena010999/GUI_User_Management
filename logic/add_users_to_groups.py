#!/usr/bin/env python3
from tkinter import messagebox
from logic.helper_functions import run_pkexec, get_all_groups, multi_picklist

def add_user_to_group(user_list):
    groups = get_all_groups()
    if not groups:
        messagebox.showerror("Error", "No groups found!")
        return

    selected_groups = multi_picklist("Select Groups", "Select groups to add selected users:", groups)
    if not selected_groups:
        return

    for u in user_list:
        for g in selected_groups:
            run_pkexec(
                ["usermod", "-aG", g, u],
                f"Added {u} to {g}",
                f"Failed to add {u} to {g}"
            )

