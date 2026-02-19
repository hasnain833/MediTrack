import sys
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QApplication, 
                             QGraphicsDropShadowEffect, QProgressBar)
from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QTimer, QRect, Property
from PySide6.QtGui import (QFont, QColor, QPainter, QBrush)

class LowStockCard(QFrame):
    """Horizontal card for a single low-stock medicine"""
    def __init__(self, item_data, parent=None):
        super().__init__(parent)
        self.setFixedSize(180, 220)
        self.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Medicine Name
        name = QLabel(item_data['name'])
        name.setFont(QFont("Inter", 10, QFont.Bold))
        name.setStyleSheet("color: #0F172A; border: none;")
        name.setWordWrap(True)
        layout.addWidget(name)

        # Quantity Info
        qty_v = QVBoxLayout()
        qty_v.setSpacing(4)
        count_lbl = QLabel(f"{item_data['qty']} remaining")
        count_lbl.setFont(QFont("Inter", 8))
        count_lbl.setStyleSheet("color: #EA580C; font-weight: bold; border: none;")
        qty_v.addWidget(count_lbl)

        pbar = QProgressBar()
        pbar.setFixedHeight(6)
        pbar.setRange(0, item_data['reorder'])
        pbar.setValue(item_data['qty'])
        pbar.setTextVisible(False)
        pbar.setStyleSheet("""
            QProgressBar { background: #FFEDD5; border-radius: 3px; border: none; }
            QProgressBar::chunk { background: #F97316; border-radius: 3px; }
        """)
        qty_v.addWidget(pbar)
        layout.addLayout(qty_v)

        # Details
        details = QLabel(f"Min: {item_data['reorder']}\nSupp: {item_data['supplier']}")
        details.setFont(QFont("Inter", 8))
        details.setStyleSheet("color: #64748B; border: none;")
        layout.addWidget(details)

        layout.addStretch()

        # Reorder Button
        reorder_btn = QPushButton("Reorder")
        reorder_btn.setFixedHeight(32)
        reorder_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: 1px solid #2C7878;
                border-radius: 6px;
                color: #2C7878;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(44, 120, 120, 0.05);
            }
        """)
        layout.addWidget(reorder_btn)

class LowStockModal(QWidget):
    def __init__(self, parent=None, items=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.showFullScreen()
        
        self.items = items or []
        self._scale = 0.8 # For animation
        self.init_ui()

    def get_scale(self): return self._scale
    def set_scale(self, s):
        self._scale = s
        self.card.setFixedSize(500 * s, 450 * s)
        self.update_position()
    
    scale = Property(float, get_scale, set_scale)

    def init_ui(self):
        # 1. Overlay
        self.overlay = QFrame(self)
        self.overlay.setGeometry(self.rect())
        self.overlay.setStyleSheet("background: rgba(15, 23, 42, 0.5);") # Backdrop dim
        
        # 2. Main Card
        self.card = QFrame(self)
        self.card.setFixedSize(500, 450)
        self.card.setStyleSheet("background: rgba(255, 255, 255, 0.95); border-radius: 20px;")
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(50)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 20)
        self.card.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self.card)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header Area
        header = QFrame()
        header_l = QVBoxLayout(header)
        header_l.setContentsMargins(0, 30, 0, 10)
        header_l.setSpacing(12)

        icon_circle = QFrame()
        icon_circle.setFixedSize(50, 50)
        icon_circle.setStyleSheet("background: #FFF7ED; border-radius: 25px;")
        ic_l = QVBoxLayout(icon_circle)
        icon = QLabel("⚠️")
        icon.setFont(QFont("Inter", 20))
        icon.setAlignment(Qt.AlignCenter)
        ic_l.addWidget(icon)
        
        header_l.addWidget(icon_circle, 0, Qt.AlignCenter)

        title = QLabel("Low Stock Alert")
        title.setFont(QFont("Inter", 18, QFont.DemiBold))
        title.setStyleSheet("color: #0F172A;")
        header_l.addWidget(title, 0, Qt.AlignCenter)
        
        layout.addWidget(header)

        # Scrollable Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("background: transparent; border: none;")
        
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        h_layout = QHBoxLayout(scroll_content)
        h_layout.setContentsMargins(30, 10, 30, 20)
        h_layout.setSpacing(15)

        for item in self.items:
            h_layout.addWidget(LowStockCard(item))
        
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        # Action Buttons
        actions = QFrame()
        actions.setFixedHeight(95)
        actions.setStyleSheet("background: #F8FAFC; border-bottom-left-radius: 20px; border-bottom-right-radius: 20px;")
        act_l = QHBoxLayout(actions)
        act_l.setContentsMargins(30, 0, 30, 0)
        act_l.setSpacing(15)

        dismiss_btn = QPushButton("Dismiss All")
        dismiss_btn.setFixedHeight(48)
        dismiss_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #64748B;
                font-weight: bold;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
            }
            QPushButton:hover { background: #F1F5F9; }
        """)
        dismiss_btn.clicked.connect(self.close)
        
        review_btn = QPushButton("Review All Items")
        review_btn.setFixedHeight(48)
        review_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2C7878, stop:1 #1E5050);
                color: white;
                font-weight: bold;
                border: none;
                border-radius: 12px;
            }
            QPushButton:hover { background: #1E5050; }
        """)
        
        act_l.addWidget(dismiss_btn, 1)
        act_l.addWidget(review_btn, 1)
        layout.addWidget(actions)

        self.update_position()
        self.animate_entrance()

    def update_position(self):
        screen = QApplication.primaryScreen().geometry()
        cw, ch = self.card.width(), self.card.height()
        self.card.move((screen.width() - cw) // 2, (screen.height() - ch) // 2)

    def animate_entrance(self):
        self.ani = QPropertyAnimation(self, b"scale")
        self.ani.setDuration(500)
        self.ani.setStartValue(0.5)
        self.ani.setEndValue(1.0)
        self.ani.setEasingCurve(QEasingCurve.OutBack) # Spring effect
        self.ani.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    mock_items = [
        {"name": "Panadol CF 500mg", "qty": 12, "reorder": 50, "supplier": "GSK Healthcare"},
        {"name": "Augmentin 625mg", "qty": 5, "reorder": 20, "supplier": "Pfizer Ltd"},
        {"name": "Gaviscon Syrup", "qty": 8, "reorder": 15, "supplier": "Reckitt Benckiser"},
        {"name": "Brufen 400mg", "qty": 18, "reorder": 40, "supplier": "Abbott Labs"}
    ]
    
    modal = LowStockModal(items=mock_items)
    modal.show()
    sys.exit(app.exec())
