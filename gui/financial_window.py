import sys
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QDateEdit, QMessageBox)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont, QColor
from datetime import datetime, timedelta

class FinancialSummaryCard(QFrame):
    def __init__(self, title, value, color="#2C7878", parent=None):
        super().__init__(parent)
        self.setFixedWidth(240)
        self.setFixedHeight(100)
        self.setStyleSheet(f"""
            QFrame {{
                background: white;
                border-radius: 12px;
                border: 1px solid #E2E8F0;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        
        t_lbl = QLabel(title)
        t_lbl.setStyleSheet("color: #64748B; font-size: 13px; font-weight: 500;")
        layout.addWidget(t_lbl)
        
        self.v_lbl = QLabel(value)
        self.v_lbl.setStyleSheet(f"color: {color}; font-size: 22px; font-weight: bold;")
        layout.addWidget(self.v_lbl)

class FinancialOverviewWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.Window)
        self.setWindowTitle("Financial Management - Sales Overview")
        self.resize(1100, 800)
        self.setStyleSheet("background: #F8FAFC;")
        
        self.primary = "#0F172A"
        self.accent = "#2C7878"
        
        self.init_ui()
        self.apply_filter("today")

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(25)

        # 1. Header & Quick Filters
        header_row = QHBoxLayout()
        title = QLabel("Sales Overview")
        title.setFont(QFont("Inter", 24, QFont.Bold))
        title.setStyleSheet(f"color: {self.primary};")
        header_row.addWidget(title)
        header_row.addStretch()
        
        export_btn = QPushButton("🖨️ Export Report")
        export_btn.setFixedSize(150, 40)
        export_btn.setStyleSheet(f"""
            QPushButton {{
                background: white; border: 1px solid #E2E8F0; border-radius: 8px; font-weight: bold; color: {self.primary};
            }}
            QPushButton:hover {{ background: #F8FAFC; }}
        """)
        export_btn.clicked.connect(self.export_report)
        header_row.addWidget(export_btn)
        main_layout.addLayout(header_row)

        # 2. Filter Bar
        filter_bar = QHBoxLayout()
        filter_bar.setSpacing(10)
        
        btn_style = """
            QPushButton {
                background: white; border: 1px solid #E2E8F0; padding: 8px 15px; border-radius: 6px; font-weight: 500; color: #475569;
            }
            QPushButton:hover { background: #F8FAFC; border-color: #CBD5E1; }
            QPushButton:checked { background: #2C7878; color: white; border-color: #2C7878; }
        """
        
        self.btn_today = QPushButton("Today")
        self.btn_yesterday = QPushButton("Yesterday")
        self.btn_week = QPushButton("This Week")
        self.btn_month = QPushButton("This Month")
        
        for b in [self.btn_today, self.btn_yesterday, self.btn_week, self.btn_month]:
            b.setCheckable(True)
            b.setStyleSheet(btn_style)
            filter_bar.addWidget(b)
            
        self.btn_today.clicked.connect(lambda: self.apply_filter("today"))
        self.btn_yesterday.clicked.connect(lambda: self.apply_filter("yesterday"))
        self.btn_week.clicked.connect(lambda: self.apply_filter("week"))
        self.btn_month.clicked.connect(lambda: self.apply_filter("month"))

        filter_bar.addSpacing(20)
        filter_bar.addWidget(QLabel("Custom Range:", styleSheet="color: #64748B; font-weight: bold;"))
        
        self.start_date = QDateEdit(QDate.currentDate())
        self.start_date.setCalendarPopup(True)
        self.start_date.setFixedWidth(120)
        self.start_date.setStyleSheet("padding: 5px; border: 1px solid #E2E8F0; border-radius: 4px;")
        
        self.end_date = QDateEdit(QDate.currentDate())
        self.end_date.setCalendarPopup(True)
        self.end_date.setFixedWidth(120)
        self.end_date.setStyleSheet("padding: 5px; border: 1px solid #E2E8F0; border-radius: 4px;")
        
        self.go_btn = QPushButton("Apply")
        self.go_btn.setStyleSheet(f"background: {self.primary}; color: white; padding: 6px 15px; border-radius: 4px; font-weight: bold;")
        self.go_btn.clicked.connect(lambda: self.apply_filter("custom"))
        
        filter_bar.addWidget(self.start_date)
        filter_bar.addWidget(QLabel("-"))
        filter_bar.addWidget(self.end_date)
        filter_bar.addWidget(self.go_btn)
        filter_bar.addStretch()
        
        main_layout.addLayout(filter_bar)

        # 3. Summary Stats
        stats_layout = QHBoxLayout()
        self.card_revenue = FinancialSummaryCard("Total Revenue", "Rs. 0.00", "#1E5F5F")
        self.card_tax = FinancialSummaryCard("Total Tax (GST)", "Rs. 0.00", "#64748B")
        self.card_discount = FinancialSummaryCard("Total Discounts", "Rs. 0.00", "#EF4444")
        self.card_orders = FinancialSummaryCard("Order Count", "0", "#0F172A")
        
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
        self.table.setStyleSheet("""
            QTableWidget {
                background: white;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
                gridline-color: transparent;
                alternate-background-color: #F8FAFC;
            }
            QHeaderView::section {
                background: #F8FAFC;
                padding: 12px;
                border: none;
                border-bottom: 2px solid #E2E8F0;
                font-weight: bold;
                color: #475569;
            }
            QTableWidget::item {
                padding: 12px;
                border-bottom: 1px solid #F1F5F9;
                color: #1E293B;
            }
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

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    win = FinancialOverviewWindow()
    win.show()
    sys.exit(app.exec())
