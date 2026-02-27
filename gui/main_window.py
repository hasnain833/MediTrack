import sys
from PySide6.QtWidgets import (QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, 
                             QFrame, QTableWidget, QTableWidgetItem, QHeaderView, 
                             QMessageBox, QGraphicsDropShadowEffect, QApplication, 
                             QLineEdit, QScrollArea, QStackedWidget)
from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QPoint, QRect, QTimer
from PySide6.QtGui import QFont, QColor, QPalette, QBrush, QPainter, QPen, QLinearGradient, QPainterPath, QPixmap

class Sparkline(QWidget):
    def __init__(self, data, color="#2C7878", parent=None):
        super().__init__(parent)
        self.data = data
        self.color = color
        self.setFixedHeight(30)

    def paintEvent(self, event):
        if not self.data: return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        pen = QPen(QColor(self.color), 2)
        painter.setPen(pen)
        
        max_val = max(self.data) if max(self.data) > 0 else 1
        min_val = min(self.data)
        range_val = max_val - min_val if max_val != min_val else 1
        
        step_x = self.width() / (len(self.data) - 1)
        path = QPainterPath()
        
        for i, val in enumerate(self.data):
            x = i * step_x
            y = self.height() - ((val - min_val) / range_val * (self.height() - 4)) - 2
            if i == 0:
                path.moveTo(x, y)
            else:
                path.lineTo(x, y)
        
        painter.drawPath(path)

class GlassCard(QFrame):
    def __init__(self, title, value, spark_data, color="#2C7878", callback=None, parent=None):
        super().__init__(parent)
        self.callback = callback
        if callback:
            self.setCursor(Qt.PointingHandCursor)
        self.setMinimumWidth(230)
        self.setFixedHeight(120)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: none;
                border-radius: 16px;
            }}
            QFrame:hover {{
                background-color: {Theme.BG_MAIN.name()};
            }}
        """)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 25))
        shadow.setOffset(0, 10)
        self.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        
        top_row = QHBoxLayout()
        title_label = QLabel(title)
        title_label.setFont(Theme.get_font(10))
        title_label.setStyleSheet("color: #64748B; background: transparent; border: none;")
        top_row.addWidget(title_label)
        layout.addLayout(top_row)
        
        val_label = QLabel(value)
        val_label.setFont(Theme.get_font(20, QFont.Bold))
        val_label.setStyleSheet(f"color: #1E293B; background: transparent; border: none;")
        layout.addWidget(val_label)
        
        self.spark = Sparkline(spark_data, color, self)
        layout.addWidget(self.spark)

    def mousePressEvent(self, event):
        if self.callback:
            self.callback()
        super().mousePressEvent(event)

class SectionHeader(QWidget):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setFixedHeight(50)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(5)
        
        self.label = QLabel(title)
        self.label.setFont(QFont("Inter", 16, QFont.Bold))
        self.label.setStyleSheet("color: #0F172A; border: none; background: transparent;")
        self.layout.addWidget(self.label)
        
        self.underline = QFrame()
        self.underline.setFixedHeight(2)
        self.underline.setFixedWidth(30)
        self.underline.setStyleSheet("background-color: #2C7878; border-radius: 1px;")
        self.layout.addWidget(self.underline)
        
        self.anim = QPropertyAnimation(self.underline, b"minimumWidth")
        self.setMouseTracking(True)

    def enterEvent(self, event):
        self.anim.stop()
        self.anim.setDuration(300)
        self.anim.setStartValue(self.underline.width())
        self.anim.setEndValue(100)
        self.anim.setEasingCurve(QEasingCurve.OutQuint)
        self.anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.anim.stop()
        self.anim.setDuration(300)
        self.anim.setStartValue(self.underline.width())
        self.anim.setEndValue(30)
        self.anim.setEasingCurve(QEasingCurve.OutQuint)
        self.anim.start()
        super().leaveEvent(event)

class AreaChart(QWidget):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data 
        self.setMouseTracking(True)
        self.hover_index = -1

    def paintEvent(self, event):
        if not self.data: return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        w, h = self.width(), self.height()
        padding = 40
        chart_w, chart_h = w - padding * 2, h - padding * 2
        
        max_val = max(self.data) * 1.2
        step_x = chart_w / (len(self.data) - 1)
        
        path = QPainterPath()
        gradient = QLinearGradient(0, padding, 0, h - padding)
        gradient.setColorAt(0, QColor(Theme.PRIMARY_TEAL.red(), Theme.PRIMARY_TEAL.green(), Theme.PRIMARY_TEAL.blue(), 150))
        gradient.setColorAt(1, QColor(Theme.PRIMARY_TEAL.red(), Theme.PRIMARY_TEAL.green(), Theme.PRIMARY_TEAL.blue(), 0))
        
        points = []
        for i, val in enumerate(self.data):
            x = padding + i * step_x
            y = h - padding - (val / max_val * chart_h)
            points.append(QPoint(x, y))
            if i == 0:
                path.moveTo(x, y)
            else:
                path.lineTo(x, y)
        
        # Close path for fill
        fill_path = QPainterPath(path)
        fill_path.lineTo(padding + chart_w, h - padding)
        fill_path.lineTo(padding, h - padding)
        fill_path.closeSubpath()
        
        painter.fillPath(fill_path, gradient)
        
        painter.setPen(QPen(Theme.PRIMARY_TEAL, 3))
        painter.drawPath(path)
        
        if self.hover_index != -1:
            p = points[self.hover_index]
            painter.setBrush(QColor("white"))
            painter.drawEllipse(p, 6, 6)
            painter.setPen(QPen(Theme.PRIMARY_TEAL, 2))
            painter.drawEllipse(p, 6, 6)
            
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor("#1E293B"))
            tooltip_rect = QRect(p.x() - 40, p.y() - 40, 80, 30)
            painter.drawRoundedRect(tooltip_rect, 6, 6)
            painter.setPen(QColor("white"))
            painter.setFont(QFont("Inter", 9, QFont.Bold))
            painter.drawText(tooltip_rect, Qt.AlignCenter, f"Rs.{self.data[self.hover_index]}")

    def mouseMoveEvent(self, event):
        padding = 40
        chart_w = self.width() - padding * 2
        step_x = chart_w / (len(self.data) - 1)
        
        idx = round((event.x() - padding) / step_x)
        if 0 <= idx < len(self.data):
            if idx != self.hover_index:
                self.hover_index = idx
                self.update()
        else:
            self.hover_index = -1
            self.update()

class DonutChart(QWidget):
    def __init__(self, segments, parent=None):
        super().__init__(parent)
        self.segments = segments 

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        rect = self.rect().adjusted(10, 10, -10, -10)
        size = min(rect.width(), rect.height())
        center_rect = QRect(rect.center().x() - size/2, rect.center().y() - size/2, size, size)
        
        start_angle = 90 * 16
        for label, percent, color in self.segments:
            span_angle = - (percent / 100) * 360 * 16
            painter.setBrush(QColor(color))
            painter.setPen(Qt.NoPen)
            painter.drawPie(center_rect, start_angle, span_angle)
            start_angle += span_angle
            
        painter.setBrush(QColor("white"))
        inner_size = size * 0.7
        inner_rect = QRect(rect.center().x() - inner_size/2, rect.center().y() - inner_size/2, inner_size, inner_size)
        painter.drawEllipse(inner_rect)
        
        painter.setPen(QColor("#1E293B"))
        painter.setFont(QFont("Inter", 12, QFont.Bold))
        painter.drawText(inner_rect, Qt.AlignCenter, "Inventory\nStatus")

from utils.theme import Theme
from gui.components import ModernButton, GlassCard as GlobalGlassCard, SidebarButton

class MainWindow(QWidget):
    def __init__(self, current_user="admin", user_role="admin"):
        super().__init__()
        self.setWindowTitle("D. Chemist - Dashboard")
        self.setMinimumSize(1024, 720) # Allows resizing but sets a sane floor
        self.resize(1100, 750) # Standard initial size
        self.current_user = current_user
        self.user_role = user_role
        self.setStyleSheet(f"background-color: {Theme.BG_MAIN.name()};")
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- Sidebar Navigation ---
        class GradientSidebar(QFrame):
            def paintEvent(self, event):
                painter = QPainter(self)
                painter.setRenderHint(QPainter.Antialiasing)
                grad = QLinearGradient(0, 0, 0, self.height())
                grad.setColorAt(0, Theme.DEEP_NAVY)
                grad.setColorAt(1, Theme.ROYAL_BLUE)
                painter.setBrush(grad)
                painter.setPen(Qt.NoPen)
                painter.drawRect(self.rect())

        self.sidebar = GradientSidebar()
        self.sidebar.setFixedWidth(280)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(20, 40, 20, 40)
        sidebar_layout.setSpacing(10)

        # Sidebar Logo
        logo_container = QHBoxLayout()
        logo_container.setContentsMargins(20, 0, 20, 0)
        logo_icon = QLabel()
        logo_icon.setFixedSize(45, 45)
        logo_pix = QPixmap("images/logo.png")
        if not logo_pix.isNull():
            logo_icon.setPixmap(logo_pix.scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_icon.setAlignment(Qt.AlignCenter)
        logo_icon.setStyleSheet("background: transparent; border: none;")
        logo_container.addWidget(logo_icon)
        
        logo_text = QLabel("D. Chemist")
        logo_text.setFont(QFont(["Alex Brush", "Brush Script MT", "Gabriola", "Script MT Bold"], 26))
        logo_text.setStyleSheet("color: white; background: transparent; border: none;")
        logo_container.addWidget(logo_text)
        logo_container.addStretch()
        sidebar_layout.addLayout(logo_container)
        
        sidebar_layout.addSpacing(40)
        
        # Navigation Buttons
        self.nav_group = []
        nav_items = [
            ("Dashboard", self.show_dashboard),
            ("Inventory", self.open_inventory),
            ("Billing", self.open_billing),
        ]
        
        # Admin-only modules
        if self.user_role == "admin":
            nav_items.extend([
                ("Financials", self.open_financials),
                ("Users", self.open_user_mgmt)
            ])
        
        for text, callback in nav_items:
            btn = SidebarButton(text)
            btn.clicked.connect(callback)
            sidebar_layout.addWidget(btn)
            self.nav_group.append(btn)
        
        self.nav_group[0].setChecked(True) # Default
        
        sidebar_layout.addStretch()
        
        # Bottom Navigation
        settings_btn = SidebarButton("Settings")
        sidebar_layout.addWidget(settings_btn)
        
        logout_btn = SidebarButton("Log out")
        logout_btn.clicked.connect(self.logout)
        sidebar_layout.addWidget(logout_btn)

        main_layout.addWidget(self.sidebar)

        # --- Main Content Area ---
        self.content_stack = QFrame()
        self.content_stack_layout = QVBoxLayout(self.content_stack)
        self.content_stack_layout.setContentsMargins(0, 0, 0, 0)
        
        # Header (Now dynamic titles and actions)
        self.header = QFrame()
        self.header.setFixedHeight(80)
        self.header.setStyleSheet("background-color: white; border-bottom: 1px solid #F1F5F9;")
        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(40, 0, 40, 0)
        
        # Search Bar
        search_container = QFrame()
        search_container.setFixedWidth(350)
        search_container.setStyleSheet(f"background-color: white; border-radius: 20px; border: 1px solid {Theme.BORDER.name()};")
        s_layout = QHBoxLayout(search_container)
        s_layout.setContentsMargins(15, 0, 15, 0)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search items, transactions...")
        self.search_input.setStyleSheet("border: none; background: transparent; height: 35px;")
        self.search_input.setFont(Theme.get_font(12))
        s_layout.addWidget(self.search_input)
        header_layout.addWidget(search_container)
        
        header_layout.addStretch()
        
        # Profile Section
        profile_header = QWidget()
        ph_layout = QHBoxLayout(profile_header)
        ph_layout.setSpacing(15)
        
        u_text = QVBoxLayout()
        u_text.setSpacing(0)
        u_name_h = QLabel(self.current_user)
        u_name_h.setFont(Theme.get_font(13, QFont.Bold))
        u_name_h.setStyleSheet(f"color: {Theme.TEXT_MAIN.name()};")
        u_role_h = QLabel("Welcome Back")
        u_role_h.setFont(Theme.get_font(10))
        u_role_h.setStyleSheet(f"color: {Theme.TEXT_SUB.name()};")
        u_text.addWidget(u_name_h)
        u_text.addWidget(u_role_h)
        ph_layout.addLayout(u_text)
        
        avatar_h = QLabel(self.current_user[0].upper())
        avatar_h.setFixedSize(40, 40)
        avatar_h.setAlignment(Qt.AlignCenter)
        avatar_h.setStyleSheet(f"background-color: #E2E8F0; color: #1E293B; border-radius: 20px; font-weight: bold;")
        ph_layout.addWidget(avatar_h)
        
        header_layout.addWidget(profile_header)
        
        self.content_stack_layout.addWidget(self.header)

        # Scrollable Body
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("border: none; background: transparent;")
        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("background-color: #F8FAFC;") # Softer premium background
        self.body_layout = QVBoxLayout(self.scroll_content)
        self.body_layout.setContentsMargins(40, 30, 40, 40)
        self.body_layout.setSpacing(35)
        
        self.scroll.setWidget(self.scroll_content)
        
        # View Container (Stacked Widget)
        self.view_stack = QStackedWidget()
        self.view_stack.addWidget(self.scroll) # Index 0: Dashboard
        self.content_stack_layout.addWidget(self.view_stack)
        
        main_layout.addWidget(self.content_stack)
        
        self.show_dashboard_content()

    def populate_table(self):
        # ... existing populate_table code ...
        pass

    def _switch_view(self, index, view_attr, view_class):
        print(f"DEBUG: Switching to view index {index}")
        if not hasattr(self, view_attr):
            if view_attr == 'dashboard_view':
                view = self.scroll
            else:
                view = view_class(self)
                self.view_stack.addWidget(view)
            setattr(self, view_attr, view)
        
        for i, btn in enumerate(self.nav_group):
            btn.setChecked(i == index)
        
        self.view_stack.setCurrentWidget(getattr(self, view_attr))
        self.update_header(index)

    def update_header(self, index):
        # We can still update the "Welcome Back" or profile title if needed
        # but for now let's just ensure we don't crash and maybe update the search placeholder
        placeholders = ["Search items...", "Search medicines...", "Search bills...", "Search financials...", "Search users..."]
        if hasattr(self, 'search_input') and index < len(placeholders):
            self.search_input.setPlaceholderText(placeholders[index])

    def show_dashboard(self):
        self._switch_view(0, 'dashboard_view', None)

    def open_inventory(self):
        from gui.inventory_window import InventoryWindow
        self._switch_view(1, 'inventory_view', InventoryWindow)

    def open_billing(self):
        from gui.billing_window import BillingWindow
        self._switch_view(2, 'billing_view', BillingWindow)

    def open_financials(self):
        from gui.financial_window import FinancialOverviewWindow
        self._switch_view(3, 'financial_view', FinancialOverviewWindow)

    def open_designer(self):
        from gui.bill_designer_window import BillDesignerWindow
        self._switch_view(4, 'designer_view', BillDesignerWindow)

    def open_user_mgmt(self):
        from gui.user_management_window import UserManagerWindow
        self._switch_view(5, 'user_mgmt_view', UserManagerWindow)

    def show_dashboard_content(self):
        # Clear layout first
        while self.body_layout.count():
            item = self.body_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()
            
        from gui.components import EnhancedMetricCard
        
        # Metrics Row
        metrics_layout = QHBoxLayout()
        metrics_layout.setSpacing(25)
        
        metrics = [
            ("Total Profit", "Rs. 1250.00", "+12.5%/Month", Theme.ROYAL_BLUE),
            ("Total Sale", "Rs. 1250.00", "+18%/Month", Theme.PRIMARY_TEAL),
            ("Low Stock", "752", "-5.2%", Theme.ERROR),
            ("System Users", "355", "+12", Theme.INFO)
        ]
        
        for title, val, change, color in metrics:
            card = EnhancedMetricCard(title, val, change, color)
            metrics_layout.addWidget(card)
        self.body_layout.addLayout(metrics_layout)
        
        # Charts Row
        charts_row = QHBoxLayout()
        charts_row.setSpacing(25)
        
        # Big Sales Chart
        sales_container = self.create_container_card("Total Sale", 400)
        sales_container.layout().setContentsMargins(0, 0, 0, 0)
        area = AreaChart([4500, 5200, 4800, 6100, 5900, 7200, 6800, 8100, 7500, 9200])
        sales_container.layout().addWidget(area)
        charts_row.addWidget(sales_container, 2)
        
        # Profit Chart (or Bar chart)
        profit_container = self.create_container_card("Total Profit", 400)
        # For now reusing AreaChart but could be a BarChart
        area2 = AreaChart([3000, 4000, 3500, 5000, 4500, 6000])
        profit_container.layout().addWidget(area2)
        charts_row.addWidget(profit_container, 1)
        
        self.body_layout.addLayout(charts_row)
        
        # Transactions and Legend Row
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(25)
        
        # Transaction Table
        trans_card = self.create_container_card("Transaction", 350)
        table = QTableWidget(3, 5)
        table.setHorizontalHeaderLabels(["Order ID", "Date", "Medicine Name", "Quantity", "Price"])
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.verticalHeader().setVisible(False)
        table.setShowGrid(False)
        table.setStyleSheet("""
            QTableWidget {
                border: none;
                background: transparent;
            }
            QHeaderView::section {
                background-color: transparent;
                border: none;
                color: #6B7280;
                font-weight: bold;
                padding: 10px;
            }
        """)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Dummy data
        data = [
            ("025636", "12-08-26", "Doxiva 200mg", "2", "Rs. 25"),
            ("025637", "12-08-26", "Monus 10mg", "1", "Rs. 17"),
            ("052366", "12-08-26", "Revortil 2mg", "1", "Rs. 15")
        ]
        for r, row in enumerate(data):
            for c, val in enumerate(row):
                table.setItem(r, c, QTableWidgetItem(val))
        
        trans_card.layout().addWidget(table)
        bottom_row.addWidget(trans_card, 2)
        
        # Demanded Drugs
        drugs_card = self.create_container_card("Demanded Drugs", 350)
        donut = DonutChart([("Doxiva", 40, "#F43F5E"), ("Exium", 20, "#6366F1"), ("Paracetomol", 20, "#EAB308"), ("Sef", 20, "#2563EB")])
        drugs_card.layout().addWidget(donut)
        bottom_row.addWidget(drugs_card, 1)
        
        self.body_layout.addLayout(bottom_row)


    def handle_logout(self):
        reply = QMessageBox.question(self, 'Logout', 'Are you sure you want to logout?',
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            print("DEBUG: Logging out...")
            try:
                from gui.login_window import LoginWindow
                self.login_win = LoginWindow()
                self.login_win.show()
                self.close()
            except Exception as e:
                import traceback
                traceback.print_exc()
                QMessageBox.critical(self, "Logout Error", f"Could not return to login screen.\n\nError: {e}")

    def create_container_card(self, title, fixed_h):
        card = QFrame()
        if fixed_h > 0: card.setFixedHeight(fixed_h)
        card.setStyleSheet("background: white; border-radius: 20px; border: none;")
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 15))
        shadow.setOffset(0, 8)
        card.setGraphicsEffect(shadow)
        
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setSpacing(0)
        
        header_widget = QWidget()
        header_widget.setFixedHeight(55)
        h_layout = QVBoxLayout(header_widget)
        h_layout.setContentsMargins(20, 15, 20, 0)
        h_layout.setSpacing(4)
        
        t_label = QLabel(title)
        t_label.setFont(Theme.get_font(12, QFont.Bold))
        t_label.setStyleSheet("color: #1E293B; border: none; background: transparent;")
        h_layout.addWidget(t_label)
        
        indicator = QFrame()
        indicator.setFixedHeight(2)
        indicator.setFixedWidth(35)
        indicator.setStyleSheet(f"background-color: {Theme.PRIMARY.name()}; border-radius: 1px;")
        h_layout.addWidget(indicator)
        
        card_layout.addWidget(header_widget)
        return card

    def keyPressEvent(self, event):
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_K:
            self.search_input.setFocus()
        super().keyPressEvent(event)

    def logout(self):
        from gui.login_window import LoginWindow
        self.login_win = LoginWindow()
        self.login_win.show()
        self.close()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
