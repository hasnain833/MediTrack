import sys
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QFrame, QGraphicsDropShadowEffect, QScrollArea,
                             QCheckBox, QComboBox, QSpacerItem, QSizePolicy)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QColor, QIcon
from datetime import datetime

from utils.theme import Theme
from gui.components import ModernButton

class InventoryWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("MediTrack - Inventory")
        self.setMinimumSize(1000, 700)
        self.resize(1100, 750)
        self.setStyleSheet(f"background-color: {Theme.BG_MAIN.name()};")
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # 2. Main content area (Split Sidebar/Table)
        content_row = QHBoxLayout()
        content_row.setSpacing(30)

        # Sidebar Filters
        sidebar = QFrame()
        sidebar.setFixedWidth(280)
        sidebar.setStyleSheet(f"background: white; border-radius: 16px; border: none;")
        side_layout = QVBoxLayout(sidebar)
        side_layout.setContentsMargins(25, 30, 25, 30)
        side_layout.setSpacing(25)

        # Search
        search_box = QVBoxLayout()
        search_lbl = QLabel("QUICK SEARCH")
        search_lbl.setFont(Theme.get_font(10, QFont.Bold))
        search_lbl.setStyleSheet(f"color: {Theme.TEXT_SUB.name()}; letter-spacing: 1px;")
        search_box.addWidget(search_lbl)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search medicines...")
        self.search_input.setFixedHeight(45)
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                border: none;
                border-radius: 8px;
                padding: 0 12px;
                background: {Theme.BG_MAIN.name()};
            }}
            QLineEdit:focus {{
                background: white;
                border: 1px solid {Theme.PRIMARY.name()};
            }}
        """)
        self.search_input.textChanged.connect(self.search)
        search_box.addWidget(self.search_input)
        side_layout.addLayout(search_box)

        # Category Filters
        cat_box = QVBoxLayout()
        cat_lbl = QLabel("CATEGORIES")
        cat_lbl.setFont(Theme.get_font(10, QFont.Bold))
        cat_lbl.setStyleSheet(f"color: {Theme.TEXT_SUB.name()}; letter-spacing: 1px;")
        cat_box.addWidget(cat_lbl)

        self.cat_checks = {}
        for cat in ["Painkiller", "Antibiotic", "Vitamin", "Expired"]:
            cb = QCheckBox(cat)
            cb.setStyleSheet(f"color: {Theme.TEXT_MAIN.name()}; font-size: 13px; padding: 5px;")
            cb.stateChanged.connect(self.filter_data)
            self.cat_checks[cat] = cb
            cat_box.addWidget(cb)
        side_layout.addLayout(cat_box)

        side_layout.addStretch()
        
        # Stats summary
        stats_box = QFrame()
        stats_box.setStyleSheet(f"background: {Theme.BG_MAIN.name()}; border-radius: 12px; border: none;")
        stats_layout = QVBoxLayout(stats_box)
        
        self.stats_lbl = QLabel("Total Items: 0")
        self.stats_lbl.setFont(Theme.get_font(13, QFont.Bold))
        self.stats_lbl.setStyleSheet(f"color: {Theme.TEXT_MAIN.name()};")
        stats_layout.addWidget(self.stats_lbl)
        side_layout.addWidget(stats_box)
        
        # Table Area
        table_card = QFrame()
        table_card.setStyleSheet("background: white; border-radius: 16px; border: none;")
        tl = QVBoxLayout(table_card)
        tl.setContentsMargins(20, 20, 20, 20)
        
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["ID", "Medicine Name", "Category", "Company", "Batch", "Expiry", "Stock", "Price"])
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background: white;
                border: none;
                gridline-color: {Theme.BG_MAIN.name()};
            }}
            QHeaderView::section {{
                background: {Theme.BG_MAIN.name()};
                padding: 12px;
                border: none;
                border-bottom: 2px solid {Theme.BORDER.name()};
                font-weight: bold;
                color: {Theme.TEXT_SUB.name()};
            }}
        """)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        tl.addWidget(self.table)
        
        content_row.addWidget(sidebar, 0) # Sidebar keeps fixed width
        content_row.addWidget(table_card, 1) # Table expands

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

    def setup_header_actions(self, layout):
        self.add_btn = ModernButton("+ Register Medicine")
        self.add_btn.setFixedWidth(200)
        self.add_btn.clicked.connect(self.add_medicine)
        layout.addWidget(self.add_btn)

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = InventoryWindow()
    window.show()
    sys.exit(app.exec())
