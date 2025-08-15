#!/usr/bin/env python3

import ttkbootstrap as tb
from ui.main_window import UserManagerApp

if __name__ == "__main__":
#    root = tb.Window(themename="morph")
    app = UserManagerApp()
    app.mainloop()

