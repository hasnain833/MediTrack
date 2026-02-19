import sys
import bcrypt
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QCheckBox,
                             QVBoxLayout, QHBoxLayout, QMessageBox, QFrame, QGraphicsDropShadowEffect)
from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QPoint, QEasingCurve, QRect, QEvent
from PySide6.QtGui import QFont, QColor, QLinearGradient, QPalette, QBrush, QPainter, QPen
from database.connection import Database
from gui.main_window import MainWindow

class MaterialInput(QWidget):
    def __init__(self, label_text, is_password=False, parent=None):
        super().__init__(parent)
        self.setFixedHeight(60)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 15, 0, 0)
        self.layout.setSpacing(0)

        self.label = QLabel(label_text, self)
        self.label.setStyleSheet("color: #64748B; background: transparent;")
        self.label.setFont(QFont("Inter", 11))
        self.label.move(0, 25)
        self.entry = QLineEdit(self)
        self.entry.setStyleSheet("""
            QLineEdit {
                border: none;
                border-bottom: 1px solid #E2E8F0;
                background: transparent;
                color: #1E293B;
                padding-bottom: 5px;
                font-size: 14px;
            }
        """)
        if is_password:
            self.entry.setEchoMode(QLineEdit.Password)
        
        self.layout.addWidget(self.entry)

        self.focus_bar = QFrame(self)
        self.focus_bar.setFixedHeight(2)
        self.focus_bar.setStyleSheet("background-color: #2C7878;")
        self.focus_bar.setFixedWidth(0)
        self.focus_bar.move(0, 58)

        self.label_anim = QPropertyAnimation(self.label, b"pos")
        self.bar_anim = QPropertyAnimation(self.focus_bar, b"size")

        self.entry.focused = False
        self.entry.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self.entry:
            if event.type() == QEvent.FocusIn:
                self.on_focus_in()
            elif event.type() == QEvent.FocusOut:
                self.on_focus_out()
        return super().eventFilter(obj, event)

    def on_focus_in(self):
        self.animate_label(True)
        self.animate_bar(True)
        self.entry.setStyleSheet("border: none; border-bottom: 1px solid #CBD5E1; background: transparent; color: #1E293B; padding-bottom: 5px; font-size: 14px;")

    def on_focus_out(self):
        if not self.entry.text():
            self.animate_label(False)
        self.animate_bar(False)
        self.entry.setStyleSheet("border: none; border-bottom: 1px solid #E2E8F0; background: transparent; color: #1E293B; padding-bottom: 5px; font-size: 14px;")

    def animate_label(self, up):
        start = self.label.pos()
        end = QPoint(0, 0) if up else QPoint(0, 25)
        self.label_anim.setDuration(200)
        self.label_anim.setStartValue(start)
        self.label_anim.setEndValue(end)
        self.label_anim.setEasingCurve(QEasingCurve.InOutQuad)
        self.label_anim.start()
        
        self.label.setStyleSheet(f"color: {'#2C7878' if up else '#64748B'}; font-size: {'10px' if up else '14px'}; font-weight: {'bold' if up else 'normal'};")

    def animate_bar(self, expand):
        self.bar_anim.setDuration(250)
        self.bar_anim.setStartValue(QSize(0, 2))
        self.bar_anim.setEndValue(QSize(self.width(), 2) if expand else QSize(0, 2))
        self.bar_anim.start()

class ToggleSwitch(QCheckBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(45, 22)
        self.setCursor(Qt.PointingHandCursor)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        painter.setPen(Qt.NoPen)
        if self.isChecked():
            painter.setBrush(QBrush(QColor("#2C7878")))
        else:
            painter.setBrush(QBrush(QColor("#CBD5E1")))
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 11, 11)
        
        painter.setBrush(QBrush(QColor("white")))
        x = 25 if self.isChecked() else 3
        painter.drawEllipse(x, 3, 16, 16)

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MediTrack - Enterprise Login")
        self.setFixedSize(1000, 600)
        self.setStyleSheet("background-color: white;")
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(440)
        self.sidebar.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0A2647, stop:1 #1B4D6E);
            }
        """)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(50, 100, 50, 50)
        
        self.app_name = QLabel("MediTrack")
        self.app_name.setFont(QFont("Inter", 48, QFont.ExtraLight))
        self.app_name.setStyleSheet("color: white;")
        sidebar_layout.addWidget(self.app_name)
        
        self.tagline = QLabel("Enterprise Pharmacy Management")
        self.tagline.setFont(QFont("Inter", 16, QFont.Light))
        self.tagline.setStyleSheet("color: #CBD5E1;")
        sidebar_layout.addWidget(self.tagline)
        
        sidebar_layout.addStretch()
        
        deco = QLabel("✚")
        deco.setFont(QFont("Arial", 120))
        deco.setStyleSheet("color: rgba(255, 255, 255, 0.05);")
        sidebar_layout.addWidget(deco, 0, Qt.AlignCenter)
        
        main_layout.addWidget(self.sidebar)

        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        right_layout.setAlignment(Qt.AlignCenter)
        
        card = QFrame()
        card.setFixedWidth(440)
        card.setStyleSheet("background-color: white; border-radius: 12px;")
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setXOffset(0)
        shadow.setYOffset(10)
        shadow.setColor(QColor(0, 0, 0, 40))
        card.setGraphicsEffect(shadow)
        
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 50, 40, 50)
        card_layout.setSpacing(25)
        
        welcome = QLabel("Welcome back")
        welcome.setFont(QFont("Inter", 24, QFont.Bold))
        welcome.setStyleSheet("color: #1E293B;")
        card_layout.addWidget(welcome)
        
        subtext = QLabel("Please enter your account details.")
        subtext.setFont(QFont("Inter", 11))
        subtext.setStyleSheet("color: #64748B;")
        card_layout.addWidget(subtext)
        
        self.user_input = MaterialInput("Username")
        card_layout.addWidget(self.user_input)
        
        self.pass_input = MaterialInput("Password", is_password=True)
        card_layout.addWidget(self.pass_input)
        
        remember_layout = QHBoxLayout()
        self.remember_toggle = ToggleSwitch()
        remember_layout.addWidget(self.remember_toggle)
        remember_layout.addWidget(QLabel("Remember me", styleSheet="color: #64748B; font-size: 13px;"))
        remember_layout.addStretch()
        
        forgot_btn = QPushButton("Forgot password?")
        forgot_btn.setStyleSheet("color: #2C7878; font-weight: bold; border: none; background: transparent;")
        remember_layout.addWidget(forgot_btn)
        card_layout.addLayout(remember_layout)
        
        self.signin_btn = QPushButton("Sign In")
        self.signin_btn.setFixedHeight(48)
        self.signin_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2C7878, stop:1 #1E5F5F);
                color: white;
                border-radius: 6px;
                font-weight: bold;
                font-size: 15px;
            }
            QPushButton:hover {
                background: #1B4D4D;
            }
        """)
        self.signin_btn.clicked.connect(self.login)
        card_layout.addWidget(self.signin_btn)
        
        help_layout = QHBoxLayout()
        help_layout.addWidget(QLabel("Need help?", styleSheet="color: #64748B;"))
        
        support_btn = QPushButton("Contact support")
        support_btn.setStyleSheet("""
            QPushButton {
                color: #64748B;
                border: 1px solid #E2E8F0;
                padding: 5px 15px;
                border-radius: 4px;
                background: transparent;
            }
            QPushButton:hover {
                background: #F8FAFC;
            }
        """)
        help_layout.addWidget(support_btn)
        card_layout.addLayout(help_layout)
        
        right_layout.addWidget(card)
        main_layout.addWidget(right_container)

    def login(self):
        username = self.user_input.entry.text().strip()
        password = self.pass_input.entry.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Login Error", "Please enter both username and password.")
            return
            
        try:
            from database.models import User
            print(f"DEBUG: Login attempt for '{username}' (Password length: {len(password)})")
            user = User.find_by_username(username)
            
            if user:
                stored_hash = user['password_hash']
                role = user['role']
                print(f"DEBUG: Found user. Role: {role}")
                
                if isinstance(stored_hash, str):
                    stored_hash = stored_hash.encode('utf-8')
                
                if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                    print("DEBUG: Authentication successful.")
                    self.accept_login(username, role)
                else:
                    print(f"DEBUG: Auth failed for '{username}'. Password did not match.")
                    QMessageBox.critical(self, "Login Failed", "Invalid username or password.")
            else:
                print(f"DEBUG: User '{username}' not found.")
                QMessageBox.critical(self, "Login Failed", "Invalid username or password.")
        except Exception as e:
            import traceback
            print(f"CRITICAL: Login crash:\n{traceback.format_exc()}")
            QMessageBox.critical(self, "Error", f"An internal error occurred: {e}")

    def accept_login(self, username, role):
        try:
            print(f"DEBUG: accept_login called with role: {role}")
            # Ensure role is string for comparison
            if hasattr(role, 'decode'):
                role = role.decode('utf-8')
            
            if role == "cashier":
                print("DEBUG: Redirecting to Billing Terminal...")
                from gui.billing_window import BillingWindow
                self.bill_win = BillingWindow()
                self.bill_win.show()
            else:
                print("DEBUG: Redirecting to MainWindow...")
                self.main_window = MainWindow(username, role)
                self.main_window.show()
            
            print("DEBUG: Closing Login Window...")
            self.close()
        except Exception as e:
            import traceback
            error_msg = traceback.format_exc()
            print(f"DEBUG: Redirection Crash:\n{error_msg}")
            QMessageBox.critical(self, "Redirection Error", f"Could not open application window.\n\n{e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
