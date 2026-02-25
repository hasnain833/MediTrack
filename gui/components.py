from PySide6.QtWidgets import QPushButton, QFrame, QVBoxLayout, QGraphicsDropShadowEffect
from PySide6.QtGui import QColor, QPainter, QBrush, QPen, QFont
from PySide6.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve
from utils.theme import Theme

class ModernButton(QPushButton):
    def __init__(self, text, primary=True, parent=None):
        super().__init__(text, parent)
        self.primary = primary
        self.setFixedHeight(45)
        self.setMinimumWidth(130)  # Prevents text from being cut off
        self.setCursor(Qt.PointingHandCursor)
        self.setFont(Theme.get_font(13, QFont.Bold))
        
        # Default Styles
        self.update_style()

    def update_style(self, hover=False):
        if self.primary:
            bg = Theme.PRIMARY_DARK.name() if hover else Theme.PRIMARY.name()
            fg = "white"
            border = "none"
        else:
            bg = "#F1F5F9" if hover else "white"
            fg = Theme.TEXT_MAIN.name()
            border = f"1px solid {Theme.BORDER.name()}"

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg};
                color: {fg};
                border: {border};
                border-radius: 8px;
                padding: 0 18px;
            }}
        """)

    def enterEvent(self, event):
        self.update_style(hover=True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.update_style(hover=False)
        super().leaveEvent(event)

class GlassCard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 16px;
                border: none;
            }
        """)
        
        # Premium Shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(8)
        shadow.setColor(QColor(0, 0, 0, 30))
        self.setGraphicsEffect(shadow)

class SidebarButton(QPushButton):
    def __init__(self, text, icon_text="", parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(50)
        self.setCursor(Qt.PointingHandCursor)
        self.setFont(Theme.get_font(13, QFont.Medium))
        self.setCheckable(True)
        self.update_style()

    def update_style(self):
        self.setStyleSheet(f"""
            QPushButton {{
                text-align: left;
                padding-left: 20px;
                border: none;
                border-radius: 8px;
                color: {Theme.TEXT_MAIN.name()};
                background: transparent;
            }}
            QPushButton:hover {{
                background-color: #F1F5F9;
                color: {Theme.PRIMARY.name()};
            }}
            QPushButton:checked {{
                background-color: #E6F4F4;
                color: {Theme.PRIMARY.name()};
                font-weight: bold;
            }}
        """)
