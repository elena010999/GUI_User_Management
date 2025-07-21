# ui/main_window.py

import tkinter as tk

class UserManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Linux User Manager")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        self.build_interface()

    def build_interface(self):
        # Username input
        tk.Label(self.root, text="Username:").pack(pady=(10, 0))
        self.username_entry = tk.Entry(self.root, width=30)
        self.username_entry.pack()

        # Buttons
        tk.Button(self.root, text="Add User", command=self.add_user).pack(pady=5)
        tk.Button(self.root, text="Delete User", command=self.delete_user).pack(pady=5)
        tk.Button(self.root, text="List Users", command=self.list_users).pack(pady=5)

        # Output box
        self.output_box = tk.Text(self.root, height=8, width=50)
        self.output_box.pack(pady=10)

    # Placeholder methods to be implemented
    def add_user(self):
        self.show_output("Add user clicked.")

    def delete_user(self):
        self.show_output("Delete user clicked.")

    def list_users(self):
        self.show_output("List users clicked.")

    def show_output(self, text):
        self.output_box.delete(1.0, tk.END)
        self.output_box.insert(tk.END, text)

