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
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()