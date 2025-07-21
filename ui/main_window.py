import tkinter as tk
from tkinter import messagebox

class UserManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Linux User Manager")
        self.root.geometry("1500x1600")
        self.root.resizable(False, False)

        self.build_interface()

    def build_interface(self):
        # Buttons frame
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Add User", width=20, command=self.show_add_user_form).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Modify User", width=20, command=lambda: self.show_simple_input("Modify User", "Username")).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="Delete User", width=20, command=lambda: self.show_simple_input("Delete User", "Username")).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Change Password", width=20, command=lambda: self.show_simple_input("Change Password", "Username")).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="Lock User Account", width=20, command=lambda: self.show_simple_input("Lock User Account", "Username")).grid(row=2, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Unlock User Account", width=20, command=lambda: self.show_simple_input("Unlock User Account", "Username")).grid(row=2, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="Add User to Group", width=20, command=lambda: self.show_group_input()).grid(row=3, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="List Users & Shells", width=20, command=self.list_users).grid(row=3, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="Check if User Exists", width=20, command=lambda: self.show_simple_input("Check User Exists", "Username")).grid(row=4, column=0, padx=5, pady=5)

        # Output box
        self.output_box = tk.Text(self.root, height=10, width=60)
        self.output_box.pack(pady=10)

        # Form frame for dynamic inputs
        self.form_frame = tk.Frame(self.root)
        self.form_frame.pack(pady=10)

    def clear_form(self):
        for widget in self.form_frame.winfo_children():
            widget.destroy()

    def show_add_user_form(self):
        self.clear_form()

        tk.Label(self.form_frame, text="Add New User", font=("Arial", 14, "bold")).pack(pady=5)

        # Username
        tk.Label(self.form_frame, text="Username:").pack(anchor="w")
        self.username_entry = tk.Entry(self.form_frame, width=30)
        self.username_entry.pack()

        # Password
        tk.Label(self.form_frame, text="Password:").pack(anchor="w", pady=(10,0))
        self.password_entry = tk.Entry(self.form_frame, show="*", width=30)
        self.password_entry.pack()

        # Group
        tk.Label(self.form_frame, text="Group (leave blank to create new):").pack(anchor="w", pady=(10,0))
        self.group_entry = tk.Entry(self.form_frame, width=30)
        self.group_entry.pack()

        # Shell selection with default
        tk.Label(self.form_frame, text="Shell:").pack(anchor="w", pady=(10,0))
        self.shell_var = tk.StringVar(value="/bin/bash")
        shells = ["/bin/bash", "/bin/sh", "/bin/zsh", "/bin/dash"]
        self.shell_menu = tk.OptionMenu(self.form_frame, self.shell_var, *shells)
        self.shell_menu.pack()

        # Submit button
        tk.Button(self.form_frame, text="Create User", command=self.add_user_submit).pack(pady=15)

    def add_user_submit(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        group = self.group_entry.get().strip()
        shell = self.shell_var.get()

        if not username or not password:
            messagebox.showerror("Input Error", "Username and password are required.")
            return

        # Here you would call backend logic to add user with these parameters
        # For now, just show a summary:
        output = (f"Creating user:\n"
                  f"Username: {username}\n"
                  f"Password: {'*' * len(password)}\n"
                  f"Group: {group if group else '(new group)'}\n"
                  f"Shell: {shell}")
        self.output_box.delete(1.0, tk.END)
        self.output_box.insert(tk.END, output)

        # Clear form if you want
        # self.clear_form()

    def show_simple_input(self, action_name, label_text):
        self.clear_form()
        tk.Label(self.form_frame, text=action_name, font=("Arial", 14, "bold")).pack(pady=5)
        tk.Label(self.form_frame, text=f"{label_text}:").pack(anchor="w")
        self.simple_entry = tk.Entry(self.form_frame, width=30)
        self.simple_entry.pack()
        tk.Button(self.form_frame, text="Submit", command=lambda: self.simple_submit(action_name)).pack(pady=10)

    def simple_submit(self, action_name):
        value = self.simple_entry.get().strip()
        if not value:
            messagebox.showerror("Input Error", "Input cannot be empty.")
            return
        self.output_box.delete(1.0, tk.END)
        self.output_box.insert(tk.END, f"{action_name} for '{value}' submitted.")

    def show_group_input(self):
        self.clear_form()
        tk.Label(self.form_frame, text="Add User to Group", font=("Arial", 14, "bold")).pack(pady=5)
        tk.Label(self.form_frame, text="Username:").pack(anchor="w")
        self.username_entry = tk.Entry(self.form_frame, width=30)
        self.username_entry.pack()
        tk.Label(self.form_frame, text="Group:").pack(anchor="w", pady=(10,0))
        self.group_entry = tk.Entry(self.form_frame, width=30)
        self.group_entry.pack()
        tk.Button(self.form_frame, text="Submit", command=self.add_user_to_group_submit).pack(pady=10)

    def add_user_to_group_submit(self):
        username = self.username_entry.get().strip()
        group = self.group_entry.get().strip()
        if not username or not group:
            messagebox.showerror("Input Error", "Both username and group are required.")
            return
        self.output_box.delete(1.0, tk.END)
        self.output_box.insert(tk.END, f"Adding user '{username}' to group '{group}'.")

    def list_users(self):
        # Placeholder for actual user listing
        self.output_box.delete(1.0, tk.END)
        self.output_box.insert(tk.END, "Listing all users and their shells...")

if __name__ == "__main__":
    root = tk.Tk()
    app = UserManagerApp(root)
    root.mainloop()

