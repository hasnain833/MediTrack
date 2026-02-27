import sys
import os
# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QApplication, 
                             QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QColor, QPainter, QPixmap
from datetime import datetime
from services.template_service import TemplateService

class ReportPreviewWindow(QWidget):
    def __init__(self, title, columns, data, parent=None):
        super().__init__(parent, Qt.Window)
        self.setWindowTitle(f"{title} - D. Chemist Reports")
        self.resize(900, 800)
        self.setStyleSheet("background-color: #F1F5F9;")
        
        self.report_title = title
        self.columns = columns
        self.data = data
        self.template = TemplateService.load_template()
        
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Action Bar
        top_bar = QFrame()
        top_bar.setFixedHeight(70)
        top_bar.setStyleSheet("background: white; border-bottom: 1px solid #E2E8F0;")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(30, 0, 30, 0)
        
        lbl_title = QLabel(self.report_title)
        lbl_title.setFont(QFont("Inter", 16, QFont.Bold))
        lbl_title.setStyleSheet("color: #0F172A;")
        top_layout.addWidget(lbl_title)
        
        top_layout.addStretch()
        
        btn_print = QPushButton("Print PDF")
        btn_print.setFixedSize(120, 40)
        btn_print.setStyleSheet(f"background: {self.template['theme']['primary']}; color: white; border-radius: 6px; font-weight: bold;")
        btn_print.clicked.connect(lambda: QMessageBox.information(self, "Print", "Report sent to PDF printer..."))
        top_layout.addWidget(btn_print)
        
        main_layout.addWidget(top_bar)

        # 2. Report Content (Paper Style)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background: #CBD5E1;")
        
        paper_container = QWidget()
        paper_layout = QVBoxLayout(paper_container)
        paper_layout.setContentsMargins(40, 40, 40, 40)
        paper_layout.setAlignment(Qt.AlignCenter)
        
        paper = QFrame()
        paper.setFixedWidth(800)
        paper.setMinimumHeight(1000)
        paper.setStyleSheet("background: white; border-radius: 4px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);")
        p_layout = QVBoxLayout(paper)
        p_layout.setContentsMargins(50, 50, 50, 50)
        p_layout.setSpacing(20)
        
        # Report Header
        header = QHBoxLayout()
        info_l = QVBoxLayout()
        name = QLabel(self.template['store']['name'])
        name.setFont(QFont("Inter", 18, QFont.Bold))
        name.setStyleSheet(f"color: {self.template['theme']['primary']};")
        info_l.addWidget(name)
        
        tagline = QLabel(self.template['store']['tagline'])
        tagline.setStyleSheet("color: #64748B; font-size: 10px; font-weight: bold;")
        info_l.addWidget(tagline)
        header.addLayout(info_l)
        
        header.addStretch()
        
        meta_r = QVBoxLayout()
        date_lbl = QLabel(f"Generated: {datetime.now().strftime('%d %b %Y, %H:%M')}")
        date_lbl.setAlignment(Qt.AlignRight)
        date_lbl.setStyleSheet("color: #64748B; font-size: 10px;")
        meta_r.addWidget(date_lbl)
        header.addLayout(meta_r)
        p_layout.addLayout(header)
        
        line = QFrame(); line.setFixedHeight(2); line.setStyleSheet(f"background: {self.template['theme']['primary']};"); p_layout.addWidget(line)
        
        subtitle = QLabel(f"Total Items: {len(self.data)}")
        subtitle.setFont(QFont("Inter", 10, QFont.Bold))
        subtitle.setStyleSheet("color: #475569;")
        p_layout.addWidget(subtitle)

        # Data Table
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.columns))
        self.table.setHorizontalHeaderLabels(self.columns)
        self.table.setRowCount(len(self.data))
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.NoSelection)
        self.table.setShowGrid(False)
        
        # Styling Table
        self.table.setStyleSheet(f"""
            QTableWidget {{ border: none; background: white; }}
            QHeaderView::section {{
                background: {self.template['table']['header_bg']};
                color: {self.template['table']['header_text']};
                padding: 10px;
                border: none;
                font-weight: bold;
                font-size: 11px;
            }}
        """)
        
        h_header = self.table.horizontalHeader()
        for i in range(len(self.columns)):
            h_header.setSectionResizeMode(i, QHeaderView.Stretch)

        for r, row_data in enumerate(self.data):
            for c, (key, label) in enumerate(zip(self.columns, self.columns)):
                val = str(row_data.get(label.lower().replace(" ", "_"), ""))
                item = QTableWidgetItem(val)
                item.setFont(QFont("Inter", 10))
                
                # Highlight stock if low
                if label.lower() == "stock" and int(val) <= row_data.get('reorder_level', 10):
                    item.setForeground(QColor("#EF4444"))
                    item.setFont(QFont("Inter", 10, QFont.Bold))
                
                self.table.setItem(r, c, item)
                
        # Fix table height to its content to avoid inner scroll
        table_height = self.table.rowCount() * 35 + 40
        self.table.setFixedHeight(table_height)
        p_layout.addWidget(self.table)
        
        p_layout.addStretch()
        
        p_footer = QLabel("Confidential System Report - D. Chemist Enterprise")
        p_footer.setAlignment(Qt.AlignCenter)
        p_footer.setStyleSheet("color: #94A3B8; font-size: 9px; border-top: 1px solid #F1F5F9; padding-top: 10px;")
        p_layout.addWidget(p_footer)
        
        paper_layout.addWidget(paper)
        scroll.setWidget(paper_container)
        main_layout.addWidget(scroll)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo_data = [
        {"name": "Paracetamol", "stock": 5, "category": "Pain", "reorder_level": 10},
        {"name": "Panadol", "stock": 2, "category": "Pain", "reorder_level": 5}
    ]
    win = ReportPreviewWindow("Low Stock Report", ["Name", "Stock", "Category", "Reorder Level"], demo_data)
    win.show()
    sys.exit(app.exec())