import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from gui.login_window import LoginWindow
from database.connection import Database
from utils.helpers import setup_logging

from utils.theme import Theme

def main():
    setup_logging()
    app = QApplication(sys.argv)
    
    # Global Font Selection
    app.setFont(Theme.get_font(14))
    
    try:
        db = Database()
        db.test_connection()
    except Exception as e:
        QMessageBox.critical(None, "Database Error", 
                            f"Cannot connect to database.\nPlease check:\n"
                            f"1. MySQL is running on Localhost\n"
                            f"2. Network connection\n"
                            f"3. Database credentials\n\nError: {e}")
        return

    window = LoginWindow()
    
    # Global Style Override
    app.setStyleSheet(f"""
        QWidget {{ border: none; outline: none; }}
        QLabel {{ background: transparent; border: none; color: {Theme.TEXT_MAIN.name()}; }}
        QMessageBox QLabel {{ min-width: 300px; }}
        QDialog {{ background-color: white; border: none; }}
        QScrollBar:vertical {{
            border: none;
            background: #F8FAFC;
            width: 8px;
            margin: 0;
        }}
        QScrollBar::handle:vertical {{
            background: #CBD5E1;
            min-height: 20px;
            border-radius: 4px;
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
    """)
    
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()