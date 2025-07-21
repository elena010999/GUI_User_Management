# main.py

import tkinter as tk
from ui.main_window import UserManagerApp

if __name__ == "__main__":
    root = tk.Tk()
    app = UserManagerApp(root)
    root.mainloop()

