import sys
from PySide6.QtWidgets import (QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, 
                             QFrame, QTableWidget, QTableWidgetItem, QHeaderView, 
                             QMessageBox, QGraphicsDropShadowEffect, QApplication, 
                             QLineEdit, QScrollArea)
from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QPoint, QRect, QTimer
from PySide6.QtGui import QFont, QColor, QPalette, QBrush, QPainter, QPen, QLinearGradient, QPainterPath

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
    def __init__(self, title, value, trend, trend_val, spark_data, color="#2C7878", callback=None, parent=None):
        super().__init__(parent)
        self.callback = callback
        if callback:
            self.setCursor(Qt.PointingHandCursor)
        self.setFixedWidth(230)
        self.setFixedHeight(110)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px solid #F1F5F9;
                border-radius: 16px;
            }}
            QFrame:hover {{
                border-color: {color};
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
        title_label.setFont(QFont("Inter", 10))
        title_label.setStyleSheet("color: #64748B; background: transparent; border: none;")
        top_row.addWidget(title_label)
        
        trend_label = QLabel(f"{trend} {trend_val}")
        trend_label.setFont(QFont("Inter", 9, QFont.Bold))
        trend_color = "#10B981" if "+" in trend else "#EF4444"
        trend_label.setStyleSheet(f"color: {trend_color}; background: transparent; border: none;")
        top_row.addWidget(trend_label, 0, Qt.AlignRight)
        layout.addLayout(top_row)
        
        val_label = QLabel(value)
        val_label.setFont(QFont("Inter", 20, QFont.Bold))
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
        gradient.setColorAt(0, QColor(44, 120, 120, 150))
        gradient.setColorAt(1, QColor(44, 120, 120, 0))
        
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
        
        painter.setPen(QPen(QColor("#2C7878"), 3))
        painter.drawPath(path)
        
        if self.hover_index != -1:
            p = points[self.hover_index]
            painter.setBrush(QColor("white"))
            painter.drawEllipse(p, 6, 6)
            painter.setPen(QPen(QColor("#2C7878"), 2))
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

class MainWindow(QWidget):
    def __init__(self, current_user="admin", user_role="admin"):
        super().__init__()
        self.setWindowTitle("MediTrack - Executive Dashboard")
        self.setFixedSize(1100, 700)
        self.current_user = current_user
        self.user_role = user_role
        self.bg_color = "#F8FAFC"
        self.accent = "#2C7878"
        self.primary = "#0F172A"
        
        self.setStyleSheet(f"background-color: {self.bg_color};")
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Premium Sticky Header
        self.header = QFrame()
        self.header.setFixedHeight(75)
        self.header.setStyleSheet("""
            QFrame {
                background-color: white;
                border-bottom: 2px solid #F1F5F9;
            }
        """)
        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(30, 0, 30, 0)
        header_layout.setSpacing(20)
        
        # Logo Section
        logo_area = QVBoxLayout()
        logo_area.setSpacing(0)
        logo = QLabel("MediTrack")
        logo.setFont(QFont("Inter", 20, QFont.Bold))
        logo.setStyleSheet(f"color: {self.primary}; border: none; background: transparent;")
        
        tagline = QLabel("PHARMACY OS")
        tagline.setFont(QFont("Inter", 8, QFont.Bold))
        tagline.setStyleSheet("color: #94A3B8; letter-spacing: 1px; background: transparent; border: none;")
        
        logo_area.addWidget(logo)
        logo_area.addWidget(tagline)
        header_layout.addLayout(logo_area)
        
        header_layout.addStretch()
        
        # Refined Search Bar
        self.search_container = QFrame()
        self.search_container.setFixedWidth(380)
        self.search_container.setFixedHeight(42)
        self.search_container.setStyleSheet("""
            QFrame {
                background: #F8FAFC;
                border-radius: 8px;
                border: 1px solid #E2E8F0;
            }
        """)
        search_layout = QHBoxLayout(self.search_container)
        search_layout.setContentsMargins(15, 0, 15, 0)
        
        search_icon = QLabel("🔍")
        search_icon.setStyleSheet("border: none; background: transparent; font-size: 11px;")
        search_layout.addWidget(search_icon)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Quick search... (Ctrl+K)")
        self.search_input.setStyleSheet("border: none; background: transparent; color: #1E293B; font-size: 13px;")
        search_layout.addWidget(self.search_input)
        
        shortcut_hint = QLabel("🔍")
        shortcut_hint.setStyleSheet("""
            QLabel {
                color: #64748B;
                font-size: 10px;
                font-weight: bold;
                border: 1px solid #E2E8F0;
                padding: 2px 6px;
                border-radius: 4px;
                background: white;
            }
        """)
        search_layout.addWidget(shortcut_hint)
        header_layout.addWidget(self.search_container)
        
        header_layout.addStretch()
        
        # Notification & Profile Section
        profile_section = QHBoxLayout()
        profile_section.setSpacing(15)
        
        notif_btn = QPushButton("🔔")
        notif_btn.setFixedSize(38, 38)
        notif_btn.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                border: 1px solid #F1F5F9;
                border-radius: 19px;
                background: #F8FAFC;
                color: #F59E0B;
            }
            QPushButton:hover {
                background: white;
                border-color: #E2E8F0;
            }
        """)
        profile_section.addWidget(notif_btn)
        
        user_info = QVBoxLayout()
        user_info.setSpacing(0)
        u_name = QLabel(self.current_user.capitalize())
        u_name.setFont(QFont("Inter", 13, QFont.Bold))
        u_name.setStyleSheet("color: #1E293B; background: transparent; border: none;")
        
        u_role = QLabel(self.user_role.capitalize() if self.user_role else "User")
        u_role.setFont(QFont("Inter", 9))
        u_role.setStyleSheet("color: #64748B; background: transparent; border: none;")
        
        user_info.addWidget(u_name)
        user_info.addWidget(u_role)
        profile_section.addLayout(user_info)
        
        avatar = QLabel(self.current_user[0].upper())
        avatar.setFixedSize(42, 42)
        avatar.setAlignment(Qt.AlignCenter)
        avatar.setFont(QFont("Inter", 15, QFont.Bold))
        avatar.setStyleSheet(f"background-color: {self.accent}; color: white; border-radius: 21px;")
        profile_section.addWidget(avatar)
        
        header_layout.addLayout(profile_section)

        logout_btn = QPushButton("🚪")
        logout_btn.setFixedSize(38, 38)
        logout_btn.setToolTip("Logout")
        logout_btn.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                border: 1px solid #F1F5F9;
                border-radius: 19px;
                background: #F8FAFC;
                color: #EF4444;
            }
            QPushButton:hover {
                background: #FEF2F2;
                border-color: #FEE2E2;
            }
        """)
        logout_btn.clicked.connect(self.handle_logout)
        header_layout.addWidget(logout_btn)

        main_layout.addWidget(self.header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background: transparent;")
        scroll_content = QWidget()
        scroll_content.setStyleSheet(f"background-color: {self.bg_color};")
        self.content_layout = QVBoxLayout(scroll_content)
        self.content_layout.setContentsMargins(30, 20, 30, 30)
        self.content_layout.setSpacing(25)
        
        self.content_layout.addWidget(SectionHeader("Executive Dashboard"))
        
        # 1. Welcome Row
        welcome_row = QHBoxLayout()
        welcome_box = QVBoxLayout()
        subtitle = QLabel("Welcome back, here's what's happening today.")
        subtitle.setStyleSheet("color: #64748B;")
        welcome_box.addWidget(subtitle)
        welcome_row.addLayout(welcome_box)
        welcome_row.addStretch()
        
        self.content_layout.addLayout(welcome_row)
        
        export_btn = QPushButton("Export Data ↓")
        export_btn.setStyleSheet(f"background: white; border: 1px solid #E2E8F0; padding: 10px 20px; border-radius: 8px; font-weight: bold; color: {self.primary};")
        welcome_row.addWidget(export_btn)

        # 2. Operations Hub (Quick Actions) - MOVED TO TOP
        self.content_layout.addWidget(SectionHeader("Operations Hub"))
        
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(15)
        
        quick_actions = [
            ("💳 Billing", "#0EA5E9", "Generate invoices and settle payments", self.open_billing),
            ("📦 Inventory", "#6366F1", "Manage stock levels and medicines", self.open_inventory),
            ("🎨 Designer", "#EC4899", "Customize bill print template", self.open_designer),
            ("💰 Financials", "#10B981", "Detailed sales overview and reports", self.open_financials),
            ("📊 Reports", "#F59E0B", "View low stock and inventory reports", self.open_low_stock_report)
        ]
        
        for text, color, desc, callback in quick_actions:
            btn_card = QFrame()
            btn_card.setFixedHeight(80)
            btn_card.setCursor(Qt.PointingHandCursor)
            btn_card.setStyleSheet(f"""
                QFrame {{
                    background: white;
                    border: 1px solid #E2E8F0;
                    border-radius: 12px;
                }}
                QFrame:hover {{
                    border-color: {color};
                    background: #F8FAFC;
                }}
            """)
            
            # Click event for the card
            btn_card.mousePressEvent = lambda e, cb=callback: cb()
            
            btn_layout = QHBoxLayout(btn_card)
            btn_layout.setContentsMargins(15, 10, 15, 10)
            
            icon_box = QVBoxLayout()
            label = QLabel(text)
            label.setFont(QFont("Inter", 12, QFont.Bold))
            label.setStyleSheet(f"color: {self.primary}; border: none; background: transparent;")
            
            sub = QLabel(desc)
            sub.setFont(QFont("Inter", 8))
            sub.setStyleSheet("color: #64748B; border: none; background: transparent;")
            
            icon_box.addWidget(label)
            icon_box.addWidget(sub)
            btn_layout.addLayout(icon_box)
            btn_layout.addStretch()
            
            arrow = QLabel("→")
            arrow.setStyleSheet(f"color: {color}; font-size: 16px; font-weight: bold; border: none;")
            btn_layout.addWidget(arrow)
            
            actions_layout.addWidget(btn_card)
            
        self.content_layout.addLayout(actions_layout)

        # 3. Metric Cards Row
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)
        
        try:
            from database.models import Sale, Medicine
            stats = Sale.get_todays_stats()
            low_stock = Medicine.get_low_stock_count()
        except Exception as e:
            print(f"Error fetching metrics: {e}")
            stats = {'revenue': 0, 'orders': 0}
            low_stock = 0

        metrics = [
            ("Today's Revenue", f"Rs.{stats['revenue']:,.0f}", "↑", "0%", [0, stats['revenue']], "#10B981", self.open_financials),
            ("Orders Processed", str(stats['orders']), "↑", "0%", [0, stats['orders']], "#6366F1", self.open_financials),
            ("Low Stock Items", str(low_stock), "!", "Alert", [0, low_stock], "#F59E0B", self.open_low_stock_report),
            ("Registered Staff", "2", "→", "Stable", [1, 2, 2, 2], "#8B5CF6", None)
        ]
        
        for title, value, sign, p_val, chart_data, color, callback in metrics:
            card = GlassCard(title, value, sign, p_val, chart_data, color, callback)
            cards_layout.addWidget(card)
        self.content_layout.addLayout(cards_layout)
        
        charts_row = QHBoxLayout()
        charts_row.setSpacing(25)
        
        # Analytics Area Chart (60%)
        analytics_card = self.create_container_card("Sales Analytics", 280)
        self.area_chart = AreaChart([4500, 5200, 4800, 6100, 5900, 7200, 6800, 8100, 7500, 9200])
        analytics_card.layout().addWidget(self.area_chart)
        analytics_card.layout().setContentsMargins(15, 0, 15, 15)
        charts_row.addWidget(analytics_card, 60)
        
        # Inventory Donut Chart (40%)
        inventory_card = self.create_container_card("Inventory Health", 280)
        self.donut_chart = DonutChart([
            ("In Stock", 65, "#2C7878"),
            ("Low Stock", 20, "#F59E0B"),
            ("Out of Stock", 15, "#EF4444")
        ])
        inventory_card.layout().addWidget(self.donut_chart)
        inventory_card.layout().setContentsMargins(15, 0, 15, 15)
        charts_row.addWidget(inventory_card, 40)
        
        self.content_layout.addLayout(charts_row)

        # 5. Recent Transactions
        self.content_layout.addWidget(SectionHeader("Recent Transactions"))
        
        trans_card = QFrame()
        trans_card.setStyleSheet("background: white; border-radius: 20px; border: 1px solid rgba(226, 232, 240, 0.8);")
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setColor(QColor(0, 0, 0, 15))
        shadow.setOffset(0, 10)
        trans_card.setGraphicsEffect(shadow)
        
        self.content_layout.addWidget(trans_card)
        
        trans_layout = QVBoxLayout(trans_card)
        trans_layout.setContentsMargins(0, 20, 0, 0)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Customer", "Date", "Amount", "Status"])
        self.table.setStyleSheet("""
            QTableWidget { border: none; background: white; gridline-color: #F1F5F9; border-radius: 20px; }
            QHeaderView::section { background-color: #F8FAFC; padding: 15px; border: none; font-weight: bold; color: #64748B; }
            QTableWidget::item { padding: 15px; border-bottom: 1px solid #F1F5F9; }
            QTableWidget::item:hover { background-color: #F8FAFC; }
        """)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.populate_table()
        trans_layout.addWidget(self.table)
        
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)

    # Navigation Methods
    def open_billing(self):
        print("DEBUG: Opening Billing Terminal...")
        try:
            from gui.billing_window import BillingWindow
            self.bill_win = BillingWindow(self)
            self.bill_win.show()
        except Exception as e:
            QMessageBox.critical(self, "Navigation Error", f"Could not launch Billing module.\n\nError: {e}")

    def open_inventory(self):
        print("DEBUG: Opening Inventory Manager...")
        try:
            from gui.inventory_window import InventoryWindow
            self.inv_win = InventoryWindow(self)
            self.inv_win.show()
        except Exception as e:
            QMessageBox.critical(self, "Navigation Error", f"Could not launch Inventory module.\n\nError: {e}")

    def open_designer(self):
        print("DEBUG: Opening Bill Template Designer...")
        try:
            from gui.bill_designer_window import BillDesignerWindow
            self.designer_win = BillDesignerWindow(self)
            self.designer_win.show()
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Navigation Error", f"Could not launch Designer module.\n\nError: {e}")

    def open_financials(self):
        print("DEBUG: Opening Financial Overview...")
        try:
            from gui.financial_window import FinancialOverviewWindow
            self.fin_win = FinancialOverviewWindow(self)
            self.fin_win.show()
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Navigation Error", f"Could not launch Financials module.\n\nError: {e}")

    def open_low_stock_report(self):
        print("DEBUG: Opening Low Stock Report...")
        try:
            from database.models import Medicine
            from gui.report_preview_window import ReportPreviewWindow
            
            data = Medicine.get_low_stock_items()
            if not data:
                QMessageBox.information(self, "Report", "All stock levels are currently healthy!")
                return
                
            self.report_win = ReportPreviewWindow(
                "Low Stock Medicine Report", 
                ["Medicine Name", "Category", "Batch No", "Stock Qty", "Reorder Level"],
                data,
                self
            )
            self.report_win.show()
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Report Error", f"Could not generate report.\n\nError: {e}")

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

    def open_reports(self):
        self.open_low_stock_report()

    def create_container_card(self, title, fixed_h):
        card = QFrame()
        if fixed_h > 0: card.setFixedHeight(fixed_h)
        card.setStyleSheet("background: white; border-radius: 16px; border: 1px solid #E2E8F0;")
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 15))
        shadow.setOffset(0, 8)
        card.setGraphicsEffect(shadow)
        
        # Use a proper layout for the card to ensure header space
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setSpacing(0)
        
        # Header area
        header_widget = QWidget()
        header_widget.setFixedHeight(55)
        h_layout = QVBoxLayout(header_widget)
        h_layout.setContentsMargins(20, 15, 20, 0)
        h_layout.setSpacing(4)
        
        t_label = QLabel(title)
        t_label.setFont(QFont("Inter", 12, QFont.Bold))
        t_label.setStyleSheet("color: #1E293B; border: none; background: transparent;")
        h_layout.addWidget(t_label)
        
        indicator = QFrame()
        indicator.setFixedHeight(2)
        indicator.setFixedWidth(35)
        indicator.setStyleSheet(f"background-color: {self.accent}; border-radius: 1px;")
        h_layout.addWidget(indicator)
        
        card_layout.addWidget(header_widget)
        
        # This will be the content area where charts are added
        return card

    def populate_table(self):
        data = [
            ["#TX1285", "John Alexander", "Feb 19, 10:24 AM", "Rs.1,250", "Completed"],
            ["#TX1286", "Sarah Miller", "Feb 19, 09:15 AM", "Rs.850", "Pending"],
            ["#TX1287", "Robert King", "Feb 18, 05:30 PM", "Rs.14,200", "Refunded"],
            ["#TX1288", "Emma Watson", "Feb 18, 04:12 PM", "Rs.520", "Completed"],
            ["#TX1289", "Michael Chen", "Feb 18, 02:45 PM", "Rs.3,100", "Completed"]
        ]
        self.table.setRowCount(len(data))
        for row, r_data in enumerate(data):
            for col, val in enumerate(r_data):
                if col == 4:
                    # Status Badge with dot
                    badge = QWidget()
                    b_layout = QHBoxLayout(badge)
                    b_layout.setContentsMargins(10, 5, 10, 5)
                    
                    dot = QLabel("●")
                    color = "#10B981" if val == "Completed" else "#F59E0B" if val == "Pending" else "#EF4444"
                    dot.setStyleSheet(f"color: {color}; font-size: 10px; border: none;")
                    b_layout.addWidget(dot)
                    
                    text = QLabel(val)
                    text.setFont(QFont("Inter", 9, QFont.Medium))
                    text.setStyleSheet(f"color: {color}; border: none;")
                    b_layout.addWidget(text)
                    b_layout.addStretch()
                    self.table.setCellWidget(row, col, badge)
                else:
                    item = QTableWidgetItem(val)
                    item.setFlags(Qt.ItemIsEnabled)
                    self.table.setItem(row, col, item)

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
