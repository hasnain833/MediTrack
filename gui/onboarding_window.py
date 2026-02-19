import sys
import random
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QStackedWidget, QLineEdit,
                             QApplication, QGraphicsDropShadowEffect, QGraphicsBlurEffect,
                             QSpacerItem, QSizePolicy, QProgressBar)
from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QPoint, QTimer, QRect
from PySide6.QtGui import (QFont, QColor, QPainter, QPen, QBrush, QPixmap, QPainterPath)

class StepIndicator(QWidget):
    """Modern step indicator with connected circles"""
    def __init__(self, count, parent=None):
        super().__init__(parent)
        self.count = count
        self.current = 0
        self.setFixedHeight(40)
        self.teal = QColor("#2C7878")
        self.gray = QColor("#E2E8F0")

    def set_step(self, step):
        self.current = step
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        w = self.width()
        spacing = 60
        total_w = (self.count - 1) * spacing
        start_x = (w - total_w) // 2
        
        # Draw connections
        pen = QPen(self.gray, 2)
        painter.setPen(pen)
        painter.drawLine(start_x, 20, start_x + total_w, 20)
        
        # Highlight active connection
        if self.current > 0:
            pen.setColor(self.teal)
            painter.setPen(pen)
            painter.drawLine(start_x, 20, start_x + (self.current * spacing), 20)

        # Draw circles
        for i in range(self.count):
            x = start_x + (i * spacing)
            is_active = i <= self.current
            
            painter.setPen(Qt.NoPen)
            painter.setBrush(self.teal if is_active else self.gray)
            painter.drawEllipse(x - 10, 20 - 10, 20, 20)
            
            if i == self.current:
                painter.setBrush(Qt.white)
                painter.drawEllipse(x - 4, 20 - 4, 8, 8)

class OnboardingStep(QWidget):
    """Base class for onboarding steps"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(40, 40, 40, 40)
        self.layout.setSpacing(20)

class WelcomeStep(OnboardingStep):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Illustration placeholder
        illu = QLabel("💊")
        illu.setFont(QFont("Inter", 64))
        illu.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(illu)
        
        text_v = QVBoxLayout()
        title = QLabel("Welcome to RxDesk")
        title.setFont(QFont("Inter", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #0F172A;")
        
        subtitle = QLabel("The most sophisticated pharmacy management system for modern retailers.")
        subtitle.setFont(QFont("Inter", 11))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #64748B;")
        
        text_v.addWidget(title)
        text_v.addWidget(subtitle)
        self.layout.addLayout(text_v)
        
        # Feature Highlights
        feat_h = QHBoxLayout()
        feat_h.setSpacing(15)
        
        features = [
            ("⚡", "Express Billing", "High-speed POS interface"),
            ("📦", "Smart Inventory", "Live stock tracking"),
            ("📊", "Deep Analytics", "Revenue insight reports")
        ]
        
        for icon, name, desc in features:
            card = QFrame()
            card.setStyleSheet("background: #F8FAFC; border-radius: 12px; border: 1px solid #E2E8F0;")
            cv = QVBoxLayout(card)
            il = QLabel(icon); il.setFont(QFont("Inter", 20)); il.setAlignment(Qt.AlignCenter)
            nl = QLabel(name); nl.setFont(QFont("Inter", 10, QFont.Bold)); nl.setAlignment(Qt.AlignCenter)
            dl = QLabel(desc); dl.setFont(QFont("Inter", 8)); dl.setAlignment(Qt.AlignCenter); dl.setWordWrap(True)
            dl.setStyleSheet("color: #64748B;")
            cv.addWidget(il); cv.addWidget(nl); cv.addWidget(dl)
            feat_h.addWidget(card)
            
        self.layout.addLayout(feat_h)

class DBStep(OnboardingStep):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        title = QLabel("Setting up your workspace")
        title.setFont(QFont("Inter", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title)
        
        self.layout.addStretch()
        
        # Animated Progress
        self.status_lbl = QLabel("Connecting to secure database...")
        self.status_lbl.setAlignment(Qt.AlignCenter)
        self.status_lbl.setStyleSheet("color: #64748B;")
        self.layout.addWidget(self.status_lbl)
        
        self.pbar = QProgressBar()
        self.pbar.setFixedHeight(8)
        self.pbar.setStyleSheet("""
            QProgressBar { background: #F1F5F9; border-radius: 4px; text-align: center; }
            QProgressBar::chunk { background: #2C7878; border-radius: 4px; }
        """)
        self.pbar.setRange(0, 0) # Indeterminate
        self.layout.addWidget(self.pbar)
        
        self.layout.addStretch()
        
        # Success Icon (hidden initially)
        self.success_icon = QLabel("✅")
        self.success_icon.setFont(QFont("Inter", 48))
        self.success_icon.setAlignment(Qt.AlignCenter)
        self.success_icon.setVisible(False)
        self.layout.addWidget(self.success_icon)

    def start_test(self):
        QTimer.singleShot(2000, self.finish_test)
        
    def finish_test(self):
        self.pbar.setRange(0, 100)
        self.pbar.setValue(100)
        self.status_lbl.setText("Database connected successfully!")
        self.status_lbl.setStyleSheet("color: #2C7878; font-weight: bold;")
        self.success_icon.setVisible(True)

class ProfileStep(OnboardingStep):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        title = QLabel("Configure your pharmacy")
        title.setFont(QFont("Inter", 20, QFont.Bold))
        self.layout.addWidget(title)
        
        form = QVBoxLayout()
        form.setSpacing(15)
        
        for lbl in ["Pharmacy Name", "License Number", "Contact Email"]:
            v = QVBoxLayout()
            l = QLabel(lbl.upper()); l.setFont(QFont("Inter", 8, QFont.Bold)); l.setStyleSheet("color: #64748B;")
            e = QLineEdit()
            e.setFixedHeight(45)
            e.setStyleSheet("border: 1px solid #E2E8F0; border-radius: 8px; padding-left: 10px;")
            v.addWidget(l); v.addWidget(e)
            form.addLayout(v)
            
        self.layout.addLayout(form)
        self.layout.addStretch()

class CompleteStep(OnboardingStep):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Confetti placeholder
        self.icon = QLabel("🎉")
        self.icon.setFont(QFont("Inter", 72))
        self.icon.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.icon)
        
        title = QLabel("You're all set!")
        title.setFont(QFont("Inter", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title)
        
        desc = QLabel("Welcome to the future of pharmacy management.\nYour dashboard is ready for you.")
        desc.setFont(QFont("Inter", 11))
        desc.setAlignment(Qt.AlignCenter)
        desc.setStyleSheet("color: #64748B;")
        self.layout.addWidget(desc)
        
        self.layout.addStretch()

class OnboardingWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.showFullScreen()
        
        self.init_ui()

    def init_ui(self):
        # 1. Background Overlay (Semi-transparent with blur simulation)
        bg = QFrame(self)
        bg.setGeometry(self.rect())
        bg.setStyleSheet("background: rgba(15, 23, 42, 0.7);")
        
        # 2. Centered Card
        self.card = QFrame(self)
        self.card.setFixedSize(800, 550)
        self.card.setStyleSheet("background: white; border-radius: 24px;")
        
        card_shadow = QGraphicsDropShadowEffect()
        card_shadow.setBlurRadius(40)
        card_shadow.setColor(QColor(0, 0, 0, 50))
        card_shadow.setOffset(0, 10)
        self.card.setGraphicsEffect(card_shadow)
        
        # Center card in window
        screen = QApplication.primaryScreen().geometry()
        self.card.move((screen.width() - 800) // 2, (screen.height() - 550) // 2)
        
        layout = QVBoxLayout(self.card)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Top Indicator
        self.indicator = StepIndicator(4)
        layout.addWidget(self.indicator)
        
        # Content Stack
        self.stack = QStackedWidget()
        self.step1 = WelcomeStep()
        self.step2 = DBStep()
        self.step3 = ProfileStep()
        self.step4 = CompleteStep()
        
        self.stack.addWidget(self.step1)
        self.stack.addWidget(self.step2)
        self.stack.addWidget(self.step3)
        self.stack.addWidget(self.step4)
        layout.addWidget(self.stack)
        
        # Footer Navigation
        footer = QFrame()
        footer.setFixedHeight(80)
        footer.setStyleSheet("border-top: 1px solid #F1F5F9;")
        f_layout = QHBoxLayout(footer)
        f_layout.setContentsMargins(40, 0, 40, 0)
        
        self.skip_btn = QPushButton("Skip tour")
        self.skip_btn.setStyleSheet("color: #64748B; border: none; font-weight: bold;")
        self.skip_btn.clicked.connect(self.close)
        f_layout.addWidget(self.skip_btn)
        
        f_layout.addStretch()
        
        self.next_btn = QPushButton("Next")
        self.next_btn.setFixedSize(120, 45)
        self.next_btn.setStyleSheet("""
            QPushButton { background: #2C7878; color: white; border-radius: 8px; font-weight: bold; }
            QPushButton:hover { background: #1E5050; }
        """)
        self.next_btn.clicked.connect(self.next_step)
        f_layout.addWidget(self.next_btn)
        
        layout.addWidget(footer)

    def next_step(self):
        current = self.stack.currentIndex()
        if current < 3:
            self.stack.setCurrentIndex(current + 1)
            self.indicator.set_step(current + 1)
            
            # Step specific logic
            if current + 1 == 1:
                self.step2.start_test()
            elif current + 1 == 3:
                self.next_btn.setText("Go to Dashboard")
                self.skip_btn.setVisible(False)
        else:
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OnboardingWindow()
    window.show()
    sys.exit(app.exec())
