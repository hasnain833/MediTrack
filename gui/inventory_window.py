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
        self.setWindowTitle("D. Chemist - Inventory")
        self.setMinimumSize(1000, 700)
        self.resize(1100, 750)
        self.setStyleSheet(f"background-color: {Theme.BG_MAIN.name()};")
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 20, 40, 40)
        main_layout.setSpacing(20)

        # Table Area
        table_card = QFrame()
        table_card.setStyleSheet("background: white; border-radius: 20px; border: none;")
        
        # Shadow for the card
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 15))
        shadow.setOffset(0, 8)
        table_card.setGraphicsEffect(shadow)
        
        tl = QVBoxLayout(table_card)
        tl.setContentsMargins(35, 35, 35, 35)
        tl.setSpacing(25)

        # Header section for search and stats
        header_row = QHBoxLayout()
        
        # Search Container
        search_container = QFrame()
        search_container.setFixedWidth(400)
        search_container.setFixedHeight(50)
        search_container.setStyleSheet(f"background-color: {Theme.BG_MAIN.name()}; border-radius: 25px; border: 1px solid {Theme.BORDER.name()};")
        s_layout = QHBoxLayout(search_container)
        s_layout.setContentsMargins(20, 0, 20, 0)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search medicines, categories, companies...")
        self.search_input.setStyleSheet("border: none; background: transparent;")
        self.search_input.setFont(Theme.get_font(12))
        self.search_input.textChanged.connect(self.search)
        s_layout.addWidget(self.search_input)
        header_row.addWidget(search_container)
        
        header_row.addStretch()
        
        # Stats summary
        self.stats_lbl = QLabel("Total Items: 0")
        self.stats_lbl.setFont(Theme.get_font(13, QFont.Bold))
        self.stats_lbl.setStyleSheet(f"color: {Theme.TEXT_MAIN.name()};")
        header_row.addWidget(self.stats_lbl)
        
        tl.addLayout(header_row)
        
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(["Medicine Name", "Strength", "Form", "Category", "Company", "Batch", "Expiry", "Stock", "Price"])
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background: white;
                border: none;
                gridline-color: transparent;
                color: {Theme.TEXT_MAIN.name()};
                font-size: 13px;
                outline: none;
            }}
            QTableWidget::item {{
                padding: 15px;
                border-bottom: 1px solid {Theme.BG_MAIN.name()};
            }}
            QTableWidget::item:selected {{
                background-color: {Theme.PRIMARY.name()};
                color: white;
                border: none;
            }}
            QHeaderView::section {{
                background: #F9FAFB;
                padding: 12px;
                border: none;
                border-bottom: 2px solid {Theme.BORDER.name()};
                font-weight: bold;
                color: #6B7280;
                font-size: 12px;
                text-transform: uppercase;
            }}
        """)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        # Configure column resizing
        header = self.table.horizontalHeader()
        header.setMinimumSectionSize(80)
        header.setSectionResizeMode(QHeaderView.Interactive)
        header.setSectionResizeMode(0, QHeaderView.Stretch)          # Name
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents) # Strength
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents) # Form
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents) # Category
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents) # Company
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents) # Stock
        header.setSectionResizeMode(8, QHeaderView.ResizeToContents) # Price
        
        self.table.setColumnWidth(0, 200)
        tl.addWidget(self.table)
        
        main_layout.addWidget(table_card)
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
            # ["Medicine Name", "Strength", "Form", "Category", "Company", "Batch", "Expiry", "Stock", "Price"]
            fields = [
                r_data.get('medicine_name', ''),
                r_data.get('strength', ''),
                r_data.get('form', ''),
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
                if col == 7: # Stock
                    try:
                        stock_val = int(float(val))
                        if stock_val < 10:
                            item.setForeground(QColor("#EF4444")) # Urgent
                            item.setFont(QFont("Inter", 10, QFont.Bold))
                    except: pass
                elif col == 6: # Expiry
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
        
        if not hasattr(self, 'current_data') or not self.current_data:
            return

        if not selected_cats:
            self.load_data(self.current_data)
            return
            
        filtered = [item for item in self.current_data if item.get('category') in selected_cats]
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
        self.add_btn.setMinimumWidth(220)
        self.add_btn.clicked.connect(self.add_medicine)
        layout.addWidget(self.add_btn)

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = InventoryWindow()
    window.show()
    sys.exit(app.exec())
