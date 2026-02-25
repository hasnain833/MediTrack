from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QDateEdit, QMessageBox, QComboBox)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont, QColor
from utils.theme import Theme
from gui.components import ModernButton, GlassCard as GlobalGlassCard

class FinancialSummaryCard(QFrame):
    def __init__(self, title, value, color=None, parent=None):
        super().__init__(parent)
        if color is None: color = Theme.PRIMARY.name()
        self.setMinimumWidth(180)
        self.setFixedHeight(110)
        self.setStyleSheet(f"""
            QFrame {{
                background: white;
                border-radius: 16px;
                border: none;
            }}
        """)
        
        from PySide6.QtWidgets import QGraphicsDropShadowEffect
        from PySide6.QtGui import QColor as QC
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(6)
        shadow.setColor(QC(0, 0, 0, 20))
        self.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        
        t_lbl = QLabel(title)
        t_lbl.setFont(Theme.get_font(13, QFont.Medium))
        t_lbl.setStyleSheet(f"color: {Theme.TEXT_SUB.name()}; background: transparent; border: none;")
        layout.addWidget(t_lbl)
        
        self.v_lbl = QLabel(value)
        self.v_lbl.setFont(Theme.get_font(22, QFont.Bold))
        self.v_lbl.setStyleSheet(f"color: {color}; background: transparent; border: none;")
        layout.addWidget(self.v_lbl)

class FinancialOverviewWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Financial Management - Sales Overview")
        self.setMinimumSize(1000, 750)
        self.resize(1150, 800)
        self.setStyleSheet(f"background: {Theme.BG_MAIN.name()};")
        
        self.init_ui()
        self.apply_filter("today")

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # 2. Filter Bar — segmented pill control + date range
        filter_bar = QHBoxLayout()
        filter_bar.setSpacing(12)

        # --- Segmented Pill Container ---
        pill_frame = QFrame()
        pill_frame.setFixedHeight(44)
        pill_frame.setStyleSheet(f"""
            QFrame {{
                background: white;
                border: 1px solid {Theme.BORDER.name()};
                border-radius: 10px;
            }}
        """)
        pill_layout = QHBoxLayout(pill_frame)
        pill_layout.setContentsMargins(4, 4, 4, 4)
        pill_layout.setSpacing(2)

        seg_active = f"""
            QPushButton {{
                background: {Theme.PRIMARY.name()};
                color: white;
                border: none;
                border-radius: 7px;
                padding: 6px 18px;
                font-weight: 700;
                font-size: 13px;
            }}
        """
        seg_inactive = f"""
            QPushButton {{
                background: transparent;
                color: {Theme.TEXT_MAIN.name()};
                border: none;
                border-radius: 7px;
                padding: 6px 18px;
                font-weight: 600;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background: {Theme.BG_MAIN.name()};
                color: {Theme.PRIMARY.name()};
            }}
            QPushButton:checked {{
                background: {Theme.PRIMARY.name()};
                color: white;
            }}
        """

        self.btn_today    = QPushButton("Today")
        self.btn_yesterday = QPushButton("Yesterday")
        self.btn_week     = QPushButton("This Week")
        self.btn_month    = QPushButton("This Month")

        for b in [self.btn_today, self.btn_yesterday, self.btn_week, self.btn_month]:
            b.setCheckable(True)
            b.setStyleSheet(seg_inactive)
            b.setCursor(Qt.PointingHandCursor)
            pill_layout.addWidget(b)

        self.btn_today.clicked.connect(lambda: self.apply_filter("today"))
        self.btn_yesterday.clicked.connect(lambda: self.apply_filter("yesterday"))
        self.btn_week.clicked.connect(lambda: self.apply_filter("week"))
        self.btn_month.clicked.connect(lambda: self.apply_filter("month"))

        filter_bar.addWidget(pill_frame)
        filter_bar.addStretch()

        # --- Date Range Section ---
        range_lbl = QLabel("Range:")
        range_lbl.setStyleSheet(f"color: {Theme.TEXT_SUB.name()}; font-weight: 600; font-size: 13px;")
        filter_bar.addWidget(range_lbl)

        self.start_date = QDateEdit(QDate.currentDate())
        self.start_date.setCalendarPopup(True)
        self.start_date.setFixedHeight(40)
        self.start_date.setFixedWidth(130)
        self.start_date.setStyleSheet(f"padding: 5px 8px; border: 1px solid {Theme.BORDER.name()}; border-radius: 8px; background: white; color: {Theme.TEXT_MAIN.name()}; font-size: 13px;")

        sep_lbl = QLabel("–")
        sep_lbl.setStyleSheet(f"color: {Theme.TEXT_SUB.name()}; font-size: 15px;")

        self.end_date = QDateEdit(QDate.currentDate())
        self.end_date.setCalendarPopup(True)
        self.end_date.setFixedHeight(40)
        self.end_date.setFixedWidth(130)
        self.end_date.setStyleSheet(f"padding: 5px 8px; border: 1px solid {Theme.BORDER.name()}; border-radius: 8px; background: white; color: {Theme.TEXT_MAIN.name()}; font-size: 13px;")

        self.go_btn = ModernButton("Apply Filters")
        self.go_btn.setMinimumWidth(150)
        self.go_btn.setFixedHeight(40)
        self.go_btn.clicked.connect(lambda: self.apply_filter("custom"))

        filter_bar.addWidget(self.start_date)
        filter_bar.addWidget(sep_lbl)
        filter_bar.addWidget(self.end_date)
        filter_bar.addWidget(self.go_btn)
        
        main_layout.addLayout(filter_bar)

        # 3. Summary Stats
        stats_layout = QHBoxLayout()
        self.card_revenue = FinancialSummaryCard("Total Revenue", "Rs. 0.00", Theme.PRIMARY.name())
        self.card_tax = FinancialSummaryCard("Total Tax (GST)", "Rs. 0.00", Theme.TEXT_SUB.name())
        self.card_discount = FinancialSummaryCard("Total Discounts", "Rs. 0.00", "#EF4444")
        self.card_orders = FinancialSummaryCard("Order Count", "0", Theme.TEXT_MAIN.name())
        
        stats_layout.addWidget(self.card_revenue)
        stats_layout.addWidget(self.card_tax)
        stats_layout.addWidget(self.card_discount)
        stats_layout.addWidget(self.card_orders)
        main_layout.addLayout(stats_layout)

        # 4. Sales Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["Bill No", "Date", "Customer", "Cashier", "Subtotal", "Tax", "Grand Total"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setShowGrid(False)
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background: white;
                border: none;
                border-radius: 16px;
                gridline-color: transparent;
                alternate-background-color: {Theme.BG_MAIN.name()};
            }}
            QHeaderView::section {{
                background: {Theme.BG_MAIN.name()};
                padding: 12px;
                border: none;
                border-bottom: 2px solid {Theme.BORDER.name()};
                font-weight: bold;
                color: {Theme.TEXT_MAIN.name()};
                font-size: 13px;
            }}
            QTableWidget::item {{
                padding: 12px;
                border-bottom: 1px solid {Theme.BG_MAIN.name()};
                color: {Theme.TEXT_MAIN.name()};
            }}
        """)
        self.table.setAlternatingRowColors(True)
        main_layout.addWidget(self.table)

    def apply_filter(self, filter_type):
        # Update buttons
        self.btn_today.setChecked(filter_type == "today")
        self.btn_yesterday.setChecked(filter_type == "yesterday")
        self.btn_week.setChecked(filter_type == "week")
        self.btn_month.setChecked(filter_type == "month")

        today = QDate.currentDate()
        start = today
        end = today

        if filter_type == "today":
            start = today
        elif filter_type == "yesterday":
            start = today.addDays(-1)
            end = start
        elif filter_type == "week":
            start = today.addDays(-(today.dayOfWeek() - 1))
        elif filter_type == "month":
            start = QDate(today.year(), today.month(), 1)
        elif filter_type == "custom":
            start = self.start_date.date()
            end = self.end_date.date()

        # Update date inputs visually
        self.start_date.setDate(start)
        self.end_date.setDate(end)
        
        self.load_data(start.toString("yyyy-MM-dd"), end.toString("yyyy-MM-dd"))

    def load_data(self, start_str, end_str):
        try:
            from database.models import Sale
            
            # 1. Load Stats
            stats = Sale.get_summary_stats(start_str, end_str)
            self.card_revenue.v_lbl.setText(f"Rs. {stats['revenue']:.2f}")
            self.card_tax.v_lbl.setText(f"Rs. {stats['tax']:.2f}")
            self.card_discount.v_lbl.setText(f"Rs. {stats['discount']:.2f}")
            self.card_orders.v_lbl.setText(str(stats['count']))
            
            # 2. Load Table
            data = Sale.get_report(start_str, end_str)
            self.table.setRowCount(0)
            for row_data in data:
                row = self.table.rowCount()
                self.table.insertRow(row)
                
                items = [
                    row_data['bill_no'],
                    row_data['created_at'].strftime("%Y-%m-%d %H:%M"),
                    row_data['customer_name'] or "Walk-in",
                    row_data['cashier_name'],
                    f"Rs. {row_data['total_amount']:.2f}",
                    f"Rs. {row_data['tax_amount']:.2f}",
                    f"Rs. {row_data['grand_total']:.2f}"
                ]
                
                for col, text in enumerate(items):
                    item = QTableWidgetItem(str(text))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table.setItem(row, col, item)
                    
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Load Error", f"Could not load sales data.\n\nError: {e}")

    def export_report(self):
        try:
            from gui.report_preview_window import ReportPreviewWindow
            
            headers = ["Bill No", "Date", "Customer", "Cashier", "Revenue"]
            table_data = []
            for r in range(self.table.rowCount()):
                table_data.append([
                    self.table.item(r, 0).text(),
                    self.table.item(r, 1).text(),
                    self.table.item(r, 2).text(),
                    self.table.item(r, 3).text(),
                    self.table.item(r, 6).text()
                ])
            
            if not table_data:
                QMessageBox.information(self, "Export", "No data available to export.")
                return
                
            range_text = f"{self.start_date.date().toString('dd MMM')} - {self.end_date.date().toString('dd MMM yyyy')}"
            self.report_win = ReportPreviewWindow(
                f"Sales Report ({range_text})",
                headers,
                table_data,
                self
            )
            self.report_win.show()
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Could not generate export.\n\nError: {e}")

    def setup_header_actions(self, layout):
        self.export_btn = ModernButton("🖨️ Export Report", primary=False)
        self.export_btn.setFixedWidth(180)
        self.export_btn.clicked.connect(self.export_report)
        layout.addWidget(self.export_btn)

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    win = FinancialOverviewWindow()
    win.show()
    sys.exit(app.exec())
