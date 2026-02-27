from PySide6.QtWidgets import QPushButton, QFrame, QVBoxLayout, QHBoxLayout, QLabel, QGraphicsDropShadowEffect, QTableWidget, QTableWidgetItem, QHeaderView
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
        bg = "white" if self.isChecked() else "transparent"
        text = Theme.PRIMARY.name() if self.isChecked() else "white"
        weight = "bold" if self.isChecked() else "normal"
        opacity = "1.0" if self.isChecked() else "0.7"
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg};
                color: {text};
                border: none;
                border-radius: 12px;
                text-align: left;
                padding-left: 20px;
                font-size: 14px;
                font-weight: {weight};
                opacity: {opacity};
                margin: 0 10px;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
            }}
            QPushButton:checked {{
                background-color: white;
                color: {Theme.PRIMARY.name()};
            }}
        """)

class EnhancedMetricCard(QFrame):
    def __init__(self, title, value, change, color_bg, parent=None):
        super().__init__(parent)
        self.setFixedHeight(125)
        self.setMinimumWidth(230)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 20px;
                border: 1px solid #F1F5F9;
            }}
        """)
        
        # Soft Premium Glow/Shadow based on accent color
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(color_bg.red(), color_bg.green(), color_bg.blue(), 25))
        shadow.setOffset(0, 8)
        self.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(10)
        
        top_bar = QHBoxLayout()
        self.title_label = QLabel(title)
        self.title_label.setFont(Theme.get_font(11, QFont.Medium))
        self.title_label.setStyleSheet("color: #64748B; background: transparent; border: none;")
        top_bar.addWidget(self.title_label)
        top_bar.addStretch()
        
        # Tiny indicator circle
        dot = QFrame()
        dot.setFixedSize(8, 8)
        dot.setStyleSheet(f"background-color: {color_bg.name()}; border-radius: 4px; border: none;")
        top_bar.addWidget(dot)
        layout.addLayout(top_bar)
        
        bottom_row = QHBoxLayout()
        bottom_row.setAlignment(Qt.AlignBottom)
        
        self.val_label = QLabel(value)
        self.val_label.setFont(Theme.get_font(24, QFont.Bold))
        self.val_label.setStyleSheet("color: #0F172A; background: transparent; border: none;")
        bottom_row.addWidget(self.val_label)
        
        bottom_row.addStretch()
        
        self.change_label = QLabel(change)
        self.change_label.setFont(Theme.get_font(11, QFont.Bold))
        # Logic to determine color based on '+' or '-'
        c_color = "#10B981" if "+" in change else "#EF4444"
        self.change_label.setStyleSheet(f"color: {c_color}; background: transparent; border: none;")
        bottom_row.addWidget(self.change_label)
        
        layout.addLayout(bottom_row)
