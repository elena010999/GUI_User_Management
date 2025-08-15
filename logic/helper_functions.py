#!/usr/bin/env python3
import subprocess
import tkinter as tk
from tkinter import messagebox

# Single hidden root for all dialogs
_root = tk.Tk()
_root.withdraw()


def run_pkexec(cmd, success_msg="", error_msg=""):
    """Run a command with pkexec and show success/error message."""
    try:
        result = subprocess.run(["pkexec"] + cmd, capture_output=True, text=True, check=True)
        if success_msg:
            messagebox.showinfo("Success", success_msg)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"{error_msg}\n\nDetails:\n{e.stderr}")


def get_all_users():
    users = []
    with open("/etc/passwd", "r") as f:
        for line in f:
            parts = line.strip().split(":")
            if int(parts[2]) >= 1000:
                users.append(parts[0])
    return users


def get_all_groups():
    groups = []
    with open("/etc/group", "r") as f:
        for line in f:
            groups.append(line.split(":")[0])
    return groups


def multi_picklist(title, prompt, options):
    top = tk.Toplevel(_root)
    top.title(title)
    tk.Label(top, text=prompt).pack(pady=5)

    vars = {o: tk.IntVar() for o in options}
    for o in options:
        tk.Checkbutton(top, text=o, variable=vars[o]).pack(anchor="w")

    def on_ok():
        top.destroy()

    tk.Button(top, text="OK", command=on_ok).pack(pady=5)
    top.grab_set()
    top.wait_window()

    return [o for o, var in vars.items() if var.get() == 1]

