import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from gui.login_window import LoginWindow
from database.connection import Database
from utils.helpers import setup_logging

def main():
    setup_logging()
    app = QApplication(sys.argv)
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
    
    # Global Style Override for Dialogs and Visibility
    app.setStyleSheet("""
        QWidget { color: #1E293B; }
        QLabel { color: #1E293B; }
        QMessageBox QLabel { color: #1E293B; min-width: 300px; }
        QPushButton { color: #1E293B; }
        QDialog { background-color: white; }
    """)
    
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()