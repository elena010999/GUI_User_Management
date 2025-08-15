#!/usr/bin/env python3
import subprocess
import tkinter as tk
from tkinter import simpledialog, messagebox

# Single hidden root for all dialogs
_root = tk.Tk()
_root.withdraw()


# ------------------- Helper Functions -------------------

def run_pkexec(cmd, success_msg="", error_msg=""):
    """Run a command with pkexec and show success/error message."""
    try:
        subprocess.run(["pkexec"] + cmd, check=True)
        if success_msg:
            messagebox.showinfo("Success", success_msg)
    except subprocess.CalledProcessError:
        details = f"{error_msg}\n\nExit Code: {e.returncode}\nError: {e.stderr.strip()}"
        print(details)  # show in terminal for debugging
        messagebox.showerror("Error", details)


def get_all_users():
    """Return a list of normal system usernames (UID >= 1000)."""
    users = []
    with open("/etc/passwd", "r") as f:
        for line in f:
            parts = line.strip().split(":")
            if int(parts[2]) >= 1000:
                users.append(parts[0])
    return users


def get_all_groups():
    """Return a list of all groups on the system."""
    groups = []
    with open("/etc/group", "r") as f:
        for line in f:
            groups.append(line.split(":")[0])
    return groups


def multi_picklist(title, prompt, options):
    """Return list of selected items from a multi-select checklist."""
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


# ------------------- User Actions -------------------

def create_user():
    users = get_all_users()
    groups = get_all_groups()

    top = tk.Toplevel(_root)
    top.title("Create New User")
    top.geometry("400x500")  # fixed height
    top.resizable(False, False)

    tk.Label(top, text="Username:").pack(pady=5)
    username_var = tk.StringVar()
    username_entry = tk.Entry(top, textvariable=username_var)
    username_entry.pack(pady=5, fill="x", padx=10)

    tk.Label(top, text="Shell (optional):").pack(pady=5)
    shell_var = tk.StringVar()
    shell_entry = tk.Entry(top, textvariable=shell_var)
    shell_entry.pack(pady=5, fill="x", padx=10)

    tk.Label(top, text="Select Groups:").pack(pady=5)

    # Scrollable frame for groups
    group_frame = tk.Frame(top)
    group_frame.pack(fill="both", expand=True, padx=10)

    canvas = tk.Canvas(group_frame)
    scrollbar = tk.Scrollbar(group_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    group_vars = {}
    for g in groups:
        var = tk.IntVar()
        cb = tk.Checkbutton(scrollable_frame, text=g, variable=var)
        cb.pack(anchor="w")
        group_vars[g] = var

    def on_submit():
        username = username_var.get().strip()
        shell = shell_var.get().strip() or None
        selected_groups = [g for g, var in group_vars.items() if var.get() == 1]

        if not username:
            messagebox.showerror("Error", "Username is required!")
            return

        if username in users:
            messagebox.showerror("Error", f"User '{username}' already exists!")
            return

        cmd = ["useradd", username]
        if shell:
            cmd += ["-s", shell]

        if not selected_groups:
            # create a default group same as username
            cmd += ["-G", username]
        else:
            cmd += ["-G", ",".join(selected_groups)]

        try:
            subprocess.run(["pkexec"] + cmd, check=True)
            messagebox.showinfo("Success", f"User '{username}' created successfully!")
            top.destroy()
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", f"Failed to create user '{username}'. Make sure you have sudo privileges.")

    submit_btn = tk.Button(top, text="Create User", command=on_submit)
    submit_btn.pack(pady=10)




def modify_user(username):
    options = ["Change Shell", "Change Username", "Change Home Directory"]
    choice = simpledialog.askstring("Modify User", f"Select modification for {username} (Shell/Username/Home):", parent=_root)
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


def delete_user(username):
    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{username}'?")
    if not confirm:
        return
    run_pkexec(["deluser", "--remove-home", username], f"User '{username}' deleted successfully!", f"Failed to delete user '{username}'.")


def change_password(username):
    run_pkexec(["passwd", username], f"Password changed successfully for '{username}'!", f"Failed to change password for '{username}'.")


def lock_unlock_user(username):
    # Check current status
    try:
        result = subprocess.run(["passwd", "-S", username], capture_output=True, text=True)
        status = result.stdout.split()[1]
        action = "unlock" if status == "L" else "lock"
    except:
        messagebox.showerror("Error", f"Cannot read status for '{username}'")
        return

    cmd = ["usermod", "-U" if action == "unlock" else "-L", username]
    run_pkexec(cmd, f"User '{username}' {action}ed successfully!", f"Failed to {action} user '{username}'.")


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
            run_pkexec(["usermod", "-aG", g, u], f"Added {u} to {g}", f"Failed to add {u} to {g}")


def list_users_shells():
    users = []
    with open("/etc/passwd", "r") as f:
        for line in f:
            parts = line.strip().split(":")
            if int(parts[2]) >= 1000:
                users.append(f"{parts[0]} → {parts[-1]}")
    messagebox.showinfo("Users and Shells", "\n".join(users) if users else "No users found.")

