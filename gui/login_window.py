import sys
import bcrypt
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QCheckBox,
                             QVBoxLayout, QHBoxLayout, QMessageBox, QFrame, QGraphicsDropShadowEffect)
from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QPoint, QEasingCurve, QRect, QEvent
from PySide6.QtGui import QFont, QColor, QLinearGradient, QPalette, QBrush, QPainter, QPen, QPixmap
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
        self.setWindowTitle("D. Chemist - Enterprise Login")
        self.setMinimumSize(1000, 650)
        self.db = Database()
        self.init_ui()
        from PySide6.QtCore import QTimer
        QTimer.singleShot(100, self.start_entrance_animation)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Create the smooth blue/teal gradient background
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, Theme.DEEP_NAVY)
        gradient.setColorAt(0.5, Theme.ROYAL_BLUE)
        gradient.setColorAt(1, Theme.PRIMARY_TEAL)
        
        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        
        # Frosted Glass Card
        self.login_card = QFrame()
        self.login_card.setObjectName("login_card")
        self.login_card.setFixedWidth(460)
        self.login_card.setStyleSheet(f"""
            QFrame#login_card {{
                background-color: rgba(255, 255, 255, 0.15);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 30px;
            }}
        """)
        
        # Apply shadow for depth
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(50)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 15)
        self.login_card.setGraphicsEffect(shadow)
        
        card_layout = QVBoxLayout(self.login_card)
        card_layout.setContentsMargins(50, 60, 50, 60)
        card_layout.setSpacing(25)
        
        # Logo Icon Container
        logo_container = QHBoxLayout()
        logo_icon = QLabel()
        logo_icon.setFixedSize(70, 70)
        logo_pixmap = QPixmap("images/logo.png")
        if not logo_pixmap.isNull():
            logo_icon.setPixmap(logo_pixmap.scaled(45, 45, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_icon.setAlignment(Qt.AlignCenter)
        logo_icon.setStyleSheet("background: transparent; border: none;")
        logo_container.addWidget(logo_icon)
        card_layout.addLayout(logo_container)
        
        card_layout.addSpacing(10)
        
        welcome = QLabel("D. Chemist")
        welcome.setAlignment(Qt.AlignCenter)
        # Use Alex Brush with elegant script fallbacks
        welcome.setFont(QFont(["Alex Brush", "Brush Script MT", "Gabriola", "Script MT Bold"], 42))
        welcome.setStyleSheet("color: white; background: transparent; border: none;")
        card_layout.addWidget(welcome)
        
        subtext = QLabel("Enter your credentials to continue")
        subtext.setAlignment(Qt.AlignCenter)
        subtext.setFont(Theme.get_font(13))
        subtext.setStyleSheet("color: rgba(255, 255, 255, 0.7); background: transparent; border: none;")
        card_layout.addWidget(subtext)
        
        card_layout.addSpacing(20)
        
        # Inputs with modern glass styling
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Username")
        self.user_input.setFixedHeight(50)
        self.user_input.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 0 15px;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                background-color: rgba(255, 255, 255, 0.15);
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
        """)
        card_layout.addWidget(self.user_input)
        
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Password")
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setFixedHeight(50)
        self.pass_input.setStyleSheet(self.user_input.styleSheet())
        card_layout.addWidget(self.pass_input)
        
        card_layout.addSpacing(10)
        
        self.signin_btn = ModernButton("Sign In")
        self.signin_btn.setFixedHeight(50)
        self.signin_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Theme.PRIMARY_TEAL.name()};
                color: {Theme.DEEP_NAVY.name()};
                border-radius: 12px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: white;
            }}
        """)
        self.signin_btn.clicked.connect(self.login)
        card_layout.addWidget(self.signin_btn)
        
        forgot_btn = QPushButton("Having trouble signing in?")
        forgot_btn.setFont(Theme.get_font(12))
        forgot_btn.setStyleSheet("color: rgba(255, 255, 255, 0.5); border: none; background: transparent;")
        forgot_btn.setCursor(Qt.PointingHandCursor)
        card_layout.addWidget(forgot_btn, 0, Qt.AlignCenter)
        
        main_layout.addWidget(self.login_card)

    def start_entrance_animation(self):
        stable_pos = self.login_card.pos()
        self.anim = QPropertyAnimation(self.login_card, b"pos")
        self.anim.setDuration(1000)
        self.anim.setStartValue(QPoint(stable_pos.x(), stable_pos.y() + 100))
        self.anim.setEndValue(stable_pos)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        
        self.fade = QPropertyAnimation(self.login_card, b"windowOpacity")
        self.fade.setDuration(1000)
        self.fade.setStartValue(0)
        self.fade.setEndValue(1)
        
        self.anim.start()

    def login(self):
        username = self.user_input.text().strip()
        password = self.pass_input.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Login Error", "Please enter both username and password.")
            return
            
        try:
            from database.models import User
            user = User.find_by_username(username)
            
            if user:
                stored_hash = user['password_hash']
                role = user['role']
                
                if isinstance(stored_hash, str):
                    stored_hash = stored_hash.encode('utf-8')
                
                if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                    self.accept_login(username, role)
                else:
                    QMessageBox.critical(self, "Login Failed", "Invalid username or password.")
            else:
                QMessageBox.critical(self, "Login Failed", "Invalid username or password.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An internal error occurred: {e}")

    def accept_login(self, username, role):
        try:
            if hasattr(role, 'decode'):
                role = role.decode('utf-8')
            
            if role == "cashier":
                from gui.billing_window import BillingWindow
                self.bill_win = BillingWindow()
                self.bill_win.show()
            else:
                self.main_window = MainWindow(username, role)
                self.main_window.show()
            
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Redirection Error", f"Could not open application window.\n\n{e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
