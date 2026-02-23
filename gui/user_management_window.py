from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QDialog, QLineEdit, QComboBox, QMessageBox, QApplication)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor
from utils.theme import Theme
from gui.components import ModernButton

class AddUserDialog(QDialog):
    """Clean dialog for adding new system users"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Register New User")
        self.setFixedWidth(400)
        self.setStyleSheet(f"background: white; border-radius: 12px;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        title = QLabel("Add New User")
        title.setFont(Theme.get_font(18, QFont.Bold))
        layout.addWidget(title)

        # Form Fields
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username (e.g. john_doe)")
        self.style_input(self.username)
        layout.addWidget(self.username)

        self.full_name = QLineEdit()
        self.full_name.setPlaceholderText("Full Name")
        self.style_input(self.full_name)
        layout.addWidget(self.full_name)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Initial Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.style_input(self.password)
        layout.addWidget(self.password)

        self.role = QComboBox()
        self.role.addItems(["admin", "cashier"])
        self.role.setFixedHeight(45)
        self.role.setStyleSheet(f"""
            QComboBox {{ 
                background: {Theme.BG_MAIN.name()}; 
                border: none; 
                border-radius: 8px; 
                padding-left: 10px;
                color: {Theme.TEXT_MAIN.name()};
            }}
        """)
        layout.addWidget(self.role)

        layout.addSpacing(10)

        # Buttons
        btn_h = QHBoxLayout()
        cancel = QPushButton("Cancel")
        cancel.setFixedHeight(45)
        cancel.setStyleSheet("background: transparent; color: #64748B; border: none; font-weight: bold;")
        cancel.clicked.connect(self.reject)
        btn_h.addWidget(cancel)

        save = ModernButton("Register User")
        save.clicked.connect(self.handle_save)
        btn_h.addWidget(save)
        
        layout.addLayout(btn_h)

    def style_input(self, widget):
        widget.setFixedHeight(45)
        widget.setStyleSheet(f"""
            QLineEdit {{
                background: {Theme.BG_MAIN.name()};
                border: none;
                border-radius: 8px;
                padding-left: 12px;
                color: {Theme.TEXT_MAIN.name()};
            }}
        """)

    def handle_save(self):
        u = self.username.text().strip()
        p = self.password.text().strip()
        f = self.full_name.text().strip()
        r = self.role.currentText()

        if not u or not p or not f:
            QMessageBox.warning(self, "Required Fields", "Please fill in all fields.")
            return

        try:
            from database.models import User
            User.create(u, p, f, r)
            QMessageBox.information(self, "Success", f"User '{u}' registered successfully.")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Creation Error", f"Failed to create user: {e}")

class UserManagerWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("User Management")
        self.setStyleSheet("background: white;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Simple Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Full Name", "Username", "Role"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setStyleSheet(f"""
            QTableWidget {{ 
                border: none; 
                background: white; 
                alternate-background-color: {Theme.BG_MAIN.name()};
            }}
            QHeaderView::section {{ 
                background: {Theme.BG_MAIN.name()}; 
                padding: 15px; 
                border: none; 
                font-weight: bold;
                color: {Theme.TEXT_SUB.name()};
            }}
        """)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)
        
        self.load_users()

    def load_users(self):
        try:
            from database.models import User
            users = User.find_all()
            self.table.setRowCount(len(users))
            for i, u in enumerate(users):
                self.table.setItem(i, 0, QTableWidgetItem(str(u['id'])))
                self.table.setItem(i, 1, QTableWidgetItem(u['full_name']))
                self.table.setItem(i, 2, QTableWidgetItem(u['username']))
                
                role_item = QTableWidgetItem(u['role'].upper())
                role_item.setForeground(QColor(Theme.PRIMARY.name() if u['role'] == 'admin' else Theme.TEXT_SUB.name()))
                role_item.setFont(Theme.get_font(9, QFont.Bold))
                self.table.setItem(i, 3, role_item)
        except Exception as e:
            print(f"Error loading users: {e}")

    def add_user(self):
        dialog = AddUserDialog(self)
        if dialog.exec():
            self.load_users()

    def setup_header_actions(self, layout):
        self.add_btn = ModernButton("+ Register User")
        self.add_btn.setFixedWidth(180)
        self.add_btn.clicked.connect(self.add_user)
        layout.addWidget(self.add_btn)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = UserManagerWindow()
    win.show()
    sys.exit(app.exec())
