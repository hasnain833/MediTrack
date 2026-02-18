import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import tkinter as tk
from gui.splash_about_window import SplashAboutWindow
from gui.login_window import LoginWindow
from database.connection import Database
from utils.helpers import setup_logging

def main():
    setup_logging()
    root = tk.Tk()
    root.withdraw()
    splash = SplashAboutWindow(root, 'splash')
    splash.wait_window()

    try:
        db = Database()
        db.test_connection()
    except Exception as e:
        root.deiconify()
        tk.messagebox.showerror(
            "Database Error",
            f"Cannot connect to database.\nPlease check:\n"
            f"1. MySQL is running on System 1\n"
            f"2. Network connection\n"
            f"3. Database credentials\n\nError: {e}"
        )
        return
    
    app = LoginWindow()
    app.run()

if __name__ == "__main__":
    main()