import sys
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QFrame, QGraphicsDropShadowEffect, QScrollArea,
                             QCheckBox, QComboBox, QSpacerItem, QSizePolicy)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QColor, QIcon
from datetime import datetime

class InventoryWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.Window) # Open as a separate window
        self.setWindowTitle("MediTrack - Inventory Management")
        self.resize(1000, 650)
        self.setStyleSheet("background-color: #F8FAFC;")
        
        self.primary = "#0F172A"
        self.accent = "#2C7878"
        self.border = "#E2E8F0"
        
        self.sample_data = [
            ("1", "Paracetamol", "Painkiller", "ABC Pharma", "B001", "2026-05-01", "50", "10.00"),
            ("2", "Ibuprofen", "Painkiller", "XYZ Corp", "B002", "2025-12-01", "5", "15.00"),
            ("3", "Expired Med", "Expired", "Old Co", "B003", "2024-01-01", "20", "5.00"),
            ("4", "Vitamin C", "Vitamin", "Health Inc", "B004", "2027-03-15", "100", "20.00"),
        ]
        
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(25)

        # 1. Header Area
        header_row = QHBoxLayout()
        
        title_box = QVBoxLayout()
        title = QLabel("Inventory Management")
        title.setFont(QFont("Inter", 20, QFont.Bold))
        title.setStyleSheet(f"color: {self.primary};")
        
        subtitle = QLabel("Track, manage and optimize your pharmacy stock levels.")
        subtitle.setStyleSheet("color: #64748B;")
        title_box.addWidget(title)
        title_box.addWidget(subtitle)
        header_row.addLayout(title_box)
        
        header_row.addStretch()
        
        add_btn = QPushButton("+ Add New Medicine")
        add_btn.setFixedSize(200, 45)
        add_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.accent};
                color: white;
                border-radius: 8px;
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: #1E5050;
            }}
        """)
        add_btn.clicked.connect(self.add_medicine)
        header_row.addWidget(add_btn)
        
        main_layout.addLayout(header_row)

        # 2. Main content area (Split Sidebar/Table)
        content_row = QHBoxLayout()
        content_row.setSpacing(25)

        # Sidebar Filters
        sidebar = QFrame()
        sidebar.setFixedWidth(260)
        sidebar.setStyleSheet(f"background: white; border-radius: 16px; border: 1px solid {self.border};")
        side_layout = QVBoxLayout(sidebar)
        side_layout.setContentsMargins(20, 25, 20, 25)
        side_layout.setSpacing(20)

        # Search inside sidebar
        search_lbl = QLabel("QUICK SEARCH")
        search_lbl.setFont(QFont("Inter", 8, QFont.Bold))
        search_lbl.setStyleSheet("color: #94A3B8; letter-spacing: 1px;")
        side_layout.addWidget(search_lbl)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search medicines...")
        self.search_input.setFixedHeight(40)
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                border: 1px solid {self.border};
                border-radius: 8px;
                padding: 0 10px;
                background: #F8FAFC;
            }}
            QLineEdit:focus {{
                border-color: {self.accent};
            }}
        """)
        self.search_input.textChanged.connect(self.search)
        side_layout.addWidget(self.search_input)

        # Category Filters
        cat_lbl = QLabel("CATEGORIES")
        cat_lbl.setFont(QFont("Inter", 8, QFont.Bold))
        cat_lbl.setStyleSheet("color: #94A3B8; letter-spacing: 1px;")
        side_layout.addWidget(cat_lbl)

        self.cat_checks = {}
        for cat in ["Painkiller", "Antibiotic", "Vitamin", "Expired"]:
            cb = QCheckBox(cat)
            cb.setStyleSheet("color: #475569; font-size: 13px;")
            cb.stateChanged.connect(self.filter_data)
            self.cat_checks[cat] = cb
            side_layout.addWidget(cb)

        side_layout.addStretch()
        
        # Stats summary in sidebar
        stats_box = QFrame()
        stats_box.setStyleSheet(f"background: #F1F5F9; border-radius: 12px; border: none;")
        stats_layout = QVBoxLayout(stats_box)
        
        self.stats_lbl = QLabel("Total Items: 4")
        self.stats_lbl.setFont(QFont("Inter", 11, QFont.Bold))
        self.stats_lbl.setStyleSheet("color: #1E293B;")
        stats_layout.addWidget(self.stats_lbl)
        
        side_layout.addWidget(stats_box)
        
        content_row.addWidget(sidebar)

        # Table Card
        table_card = QFrame()
        table_card.setStyleSheet(f"background: white; border-radius: 16px; border: 1px solid {self.border};")
        table_layout = QVBoxLayout(table_card)
        table_layout.setContentsMargins(2, 2, 2, 2)
        
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["ID", "Medicine Name", "Category", "Company", "Batch", "Expiry", "Stock", "Price"])
        self.table.setStyleSheet("""
            QTableWidget { border: none; background: white; border-radius: 16px; }
            QHeaderView::section { background-color: #F8FAFC; padding: 12px; border: none; font-weight: bold; color: #64748B; font-size: 11px; }
            QTableWidget::item { padding: 12px; border-bottom: 1px solid #F1F5F9; color: #1E293B; }
            QTableWidget::item:hover { background-color: #F8FAFC; }
        """)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setShowGrid(False)
        
        table_layout.addWidget(self.table)
        content_row.addWidget(table_card)

        main_layout.addLayout(content_row)
        
        self.refresh_data()

    def refresh_data(self):
        try:
            from database.models import Medicine
            self.current_data = Medicine.get_all()
            self.load_data(self.current_data)
        except Exception as e:
            print(f"Error refreshing inventory: {e}")

    def load_data(self, data):
        self.table.setRowCount(len(data))
        for row, r_data in enumerate(data):
            # Map dictionary fields to table columns
            # ["ID", "Medicine Name", "Category", "Company", "Batch", "Expiry", "Stock", "Price"]
            fields = [
                str(r_data.get('id', '')),
                r_data.get('medicine_name', ''),
                r_data.get('category', ''),
                r_data.get('company', ''),
                r_data.get('batch_no', ''),
                str(r_data.get('expiry_date', '')),
                str(r_data.get('stock_qty', '0')),
                f"{float(r_data.get('price', 0)):.2f}"
            ]
            
            for col, val in enumerate(fields):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignCenter)
                
                # Style critical values
                if col == 6: # Stock
                    if int(val) < 10:
                        item.setForeground(QColor("#EF4444")) # Urgent
                        item.setFont(QFont("Inter", 10, QFont.Bold))
                elif col == 5: # Expiry
                    try:
                        from datetime import date
                        exp_date = r_data.get('expiry_date')
                        if isinstance(exp_date, str):
                            exp_date = datetime.strptime(exp_date, "%Y-%m-%d").date()
                        
                        if exp_date and exp_date < date.today():
                            item.setForeground(QColor("#EF4444"))
                    except Exception as ex: 
                        print(f"Exp styling error: {ex}")
                
                self.table.setItem(row, col, item)
        
        self.stats_lbl.setText(f"Total Items: {len(data)}")

    def search(self):
        query = self.search_input.text().lower().strip()
        if not query:
            self.refresh_data()
            return
            
        try:
            from database.models import Medicine
            filtered = Medicine.search(query)
            self.load_data(filtered)
        except Exception as e:
            print(f"Search error: {e}")

    def filter_data(self):
        selected_cats = [cat for cat, cb in self.cat_checks.items() if cb.isChecked()]
        if not selected_cats:
            self.load_data(self.sample_data)
            return
            
        filtered = [item for item in self.sample_data if item[2] in selected_cats]
        self.load_data(filtered)

    def add_medicine(self):
        # Open the new PySide6 AddMedicineWindow
        try:
            from gui.add_medicine_window import AddMedicineWindow
            self.add_win = AddMedicineWindow(self)
            self.add_win.show()
        except Exception as e:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Integration Error", f"Could not launch Add Medicine module.\n\nError: {e}")

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = InventoryWindow()
    window.show()
    sys.exit(app.exec())
