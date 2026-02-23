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

from utils.theme import Theme
from gui.components import ModernButton, GlassCard

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MediTrack - Enterprise Login")
        self.setMinimumSize(900, 600)
        self.resize(1000, 650)
        self.setStyleSheet(f"background-color: {Theme.BG_MAIN.name()};")
        self.db = Database()
        self.init_ui()
        from PySide6.QtCore import QTimer
        QTimer.singleShot(100, self.start_entrance_animation)

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Left Sidebar (Visual Branding)
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(400)
        self.sidebar.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1E293B, stop:1 #334155);
            }
        """)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(50, 80, 50, 50)
        
        logo_label = QLabel("M")
        logo_label.setFixedSize(60, 60)
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet(f"background-color: {Theme.PRIMARY.name()}; color: white; border-radius: 12px; font-size: 32px; font-weight: bold;")
        sidebar_layout.addWidget(logo_label)
        
        sidebar_layout.addSpacing(30)
        
        self.app_name = QLabel("MediTrack")
        self.app_name.setFont(Theme.get_font(42, QFont.ExtraLight))
        self.app_name.setStyleSheet("color: white;")
        sidebar_layout.addWidget(self.app_name)
        
        self.tagline = QLabel("The Future of Pharmacy\nManagement Systems")
        self.tagline.setFont(Theme.get_font(18, QFont.Light))
        self.tagline.setStyleSheet("color: #94A3B8;")
        sidebar_layout.addWidget(self.tagline)
        
        sidebar_layout.addStretch()
        
        main_layout.addWidget(self.sidebar)

        # Right Container (Login Form)
        self.right_container = QWidget()
        right_layout = QVBoxLayout(self.right_container)
        right_layout.setAlignment(Qt.AlignCenter)
        
        self.login_card = GlassCard()
        self.login_card.setFixedWidth(440)
        
        card_layout = QVBoxLayout(self.login_card)
        card_layout.setContentsMargins(45, 50, 45, 50)
        card_layout.setSpacing(20)
        
        welcome = QLabel("Welcome Back")
        welcome.setFont(Theme.get_font(28, QFont.Bold))
        welcome.setStyleSheet(f"color: {Theme.TEXT_MAIN.name()};")
        card_layout.addWidget(welcome)
        
        subtext = QLabel("Login to manage your pharmacy inventory")
        subtext.setFont(Theme.get_font(14))
        subtext.setStyleSheet(f"color: {Theme.TEXT_SUB.name()};")
        card_layout.addWidget(subtext)
        
        card_layout.addSpacing(10)
        
        self.user_input = MaterialInput("Username")
        card_layout.addWidget(self.user_input)
        
        self.pass_input = MaterialInput("Password", is_password=True)
        card_layout.addWidget(self.pass_input)
        
        card_layout.addSpacing(10)
        
        self.signin_btn = ModernButton("Sign In")
        self.signin_btn.clicked.connect(self.login)
        card_layout.addWidget(self.signin_btn)
        
        forgot_btn = QPushButton("Forgot your password?")
        forgot_btn.setFont(Theme.get_font(13))
        forgot_btn.setStyleSheet(f"color: {Theme.PRIMARY.name()}; border: none; background: transparent;")
        forgot_btn.setCursor(Qt.PointingHandCursor)
        card_layout.addWidget(forgot_btn, 0, Qt.AlignCenter)
        
        right_layout.addWidget(self.login_card)
        main_layout.addWidget(self.right_container)

    def start_entrance_animation(self):
        # Capture current stable position after layout activation
        # This prevents the jump from (0,0)
        stable_pos = self.login_card.pos()
        self.anim = QPropertyAnimation(self.login_card, b"pos")
        self.anim.setDuration(800)
        self.anim.setStartValue(QPoint(stable_pos.x(), stable_pos.y() + 80))
        self.anim.setEndValue(stable_pos)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.anim.start()


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
