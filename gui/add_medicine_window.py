import sys
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QFrame, QGraphicsDropShadowEffect, 
                             QScrollArea, QComboBox, QSlider, QGridLayout, 
                             QCompleter, QDateEdit, QStyle, QApplication)
from PySide6.QtCore import Qt, QSize, QDate, QRect, QPoint
from PySide6.QtGui import (QFont, QColor, QPainter, QPen, QBrush, QLinearGradient, 
                           QIcon, QPainterPath)

class StyledLabel(QLabel):
    """Figma-style label: 12pt uppercase semibold teal"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFont(QFont("Inter", 10, QFont.DemiBold))
        self.setStyleSheet("color: #2C7878; text-transform: uppercase; letter-spacing: 0.5px;")

class ModernInput(QLineEdit):
    """Modern input with hover/focus states and subtle glow"""
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setFixedHeight(45)
        self.setStyleSheet("""
            QLineEdit {
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                padding: 0 12px;
                background: white;
                font-size: 14px;
                color: #1E293B;
            }
            QLineEdit:hover {
                border-color: #CBD5E1;
            }
            QLineEdit:focus {
                border: 2px solid #2C7878;
            }
        """)

class QuantityStepper(QWidget):
    """Styled quantity stepper with rounded buttons"""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        btn_style = """
            QPushButton {
                background: #F1F5F9;
                border: 1px solid #E2E8F0;
                border-radius: 6px;
                font-weight: bold;
                font-size: 16px;
                color: #475569;
            }
            QPushButton:hover { background: #E2E8F0; }
        """
        
        self.minus_btn = QPushButton("-")
        self.minus_btn.setFixedSize(32, 32)
        self.minus_btn.setStyleSheet(btn_style)
        
        self.value_input = QLineEdit("0")
        self.value_input.setFixedWidth(60)
        self.value_input.setFixedHeight(32)
        self.value_input.setAlignment(Qt.AlignCenter)
        self.value_input.setStyleSheet("border: 1px solid #E2E8F0; border-radius: 6px; background: white;")
        
        self.plus_btn = QPushButton("+")
        self.plus_btn.setFixedSize(32, 32)
        self.plus_btn.setStyleSheet(btn_style)
        
        layout.addWidget(self.minus_btn)
        layout.addWidget(self.value_input)
        layout.addWidget(self.plus_btn)
        
        self.minus_btn.clicked.connect(lambda: self.update_val(-1))
        self.plus_btn.clicked.connect(lambda: self.update_val(1))

    def update_val(self, delta):
        val = int(self.value_input.text() or 0)
        self.value_input.setText(str(max(0, val + delta)))

class ProgressIndicator(QWidget):
    """Top progress bar showing current step"""
    def __init__(self, steps, current=0, parent=None):
        super().__init__(parent)
        self.steps = steps
        self.current = current
        self.setFixedHeight(60)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        w = self.width()
        h = self.height()
        padding = 50
        track_y = h // 2 - 2
        
        # Draw track
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#F1F5F9"))
        painter.drawRoundedRect(padding, track_y, w - 2*padding, 4, 2, 2)
        
        # Draw active track
        step_w = (w - 2*padding) / (len(self.steps) - 1)
        active_w = self.current * step_w
        painter.setBrush(QColor("#2C7878"))
        painter.drawRoundedRect(padding, track_y, active_w, 4, 2, 2)
        
        # Draw nodes
        for i, step in enumerate(self.steps):
            x = padding + (i * step_w)
            is_active = i <= self.current
            
            painter.setBrush(QColor("white"))
            painter.setPen(QPen(QColor("#2C7878") if is_active else QColor("#CBD5E1"), 2))
            painter.drawEllipse(QPoint(x, track_y + 2), 6, 6)
            
            if is_active:
                painter.setBrush(QColor("#2C7878"))
                painter.drawEllipse(QPoint(x, track_y + 2), 3, 3)
            
            # Label
            painter.setPen(QPen(QColor("#2C7878") if i == self.current else QColor("#64748B")))
            painter.setFont(QFont("Inter", 8, QFont.Bold if i == self.current else QFont.Normal))
            rect = QRect(x - 50, track_y + 15, 100, 20)
            painter.drawText(rect, Qt.AlignCenter, step)

class AddMedicineWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.Window)
        self.setWindowTitle("MediTrack - Add New Medicine")
        self.setFixedSize(900, 680)
        self.setStyleSheet("background-color: white;")
        self.primary = "#0F172A"
        self.accent = "#2C7878"
        self.border = "#E2E8F0"
        self.init_ui()

    def paintEvent(self, event):
        """Draw subtle dot pattern background"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor(226, 232, 240, 100), 1))
        
        spacing = 20
        for x in range(0, self.width(), spacing):
            for y in range(0, self.height(), spacing):
                painter.drawPoint(x, y)

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Top Progress Indicator
        self.progress = ProgressIndicator(["Basic Info", "Inventory", "Pricing"], 0)
        main_layout.addWidget(self.progress)

        # 2. Scrollable Form Content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background: transparent;")
        
        content = QWidget()
        content.setStyleSheet("background: transparent;")
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(40, 10, 40, 80)
        content_layout.setSpacing(40)

        # LEFT COLUMN (Main Form)
        left_col = QVBoxLayout()
        left_col.setSpacing(20)

        # Medicine Name
        left_col.addWidget(StyledLabel("Medicine Name"))
        self.name_input = ModernInput("e.g. Paracetamol 500mg")
        completer = QCompleter(["Paracetamol", "Ibuprofen", "Amoxicillin", "Cefixime"])
        self.name_input.setCompleter(completer)
        left_col.addWidget(self.name_input)

        row1 = QHBoxLayout()
        # Category
        cat_v = QVBoxLayout()
        cat_v.addWidget(StyledLabel("Category"))
        self.cat_combo = QComboBox()
        self.cat_combo.addItems(["Painkiller", "Antibiotic", "Vitamin", "Surgical"])
        self.cat_combo.setFixedHeight(45)
        self.cat_combo.setStyleSheet(f"""
            QComboBox {{ 
                border: 1px solid #E2E8F0; 
                border-radius: 8px; 
                padding-left: 10px; 
                background: white;
                color: #1E293B;
            }}
            QComboBox:focus {{ border: 2px solid #2C7878; }}
            QComboBox::drop-down {{ border: none; width: 30px; }}
            QComboBox::down-arrow {{ image: none; border-left: 5px solid transparent; border-right: 5px solid transparent; border-top: 5px solid #64748B; margin-right: 10px; }}
            QAbstractItemView {{
                background-color: white;
                border: 1px solid #E2E8F0;
                selection-background-color: #F8FAFC;
                selection-color: #2C7878;
                outline: none;
                padding: 4px;
            }}
        """)
        self.cat_combo.view().setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        cat_v.addWidget(self.cat_combo)
        row1.addLayout(cat_v)

        # Batch Number
        batch_v = QVBoxLayout()
        batch_v.addWidget(StyledLabel("Batch Number"))
        self.batch_input = ModernInput("BT-00123")
        batch_v.addWidget(self.batch_input)
        row1.addLayout(batch_v)
        left_col.addLayout(row1)

        row2 = QHBoxLayout()
        # Expiry Date
        exp_v = QVBoxLayout()
        exp_v.addWidget(StyledLabel("Expiry Date"))
        self.expiry_input = QDateEdit(QDate.currentDate().addYears(1))
        self.expiry_input.setFixedHeight(45)
        self.expiry_input.setCalendarPopup(True)
        
        # Style the calendar widget
        calendar = self.expiry_input.calendarWidget()
        calendar.setStyleSheet(f"""
            QCalendarWidget QWidget {{ background-color: white; }}
            QCalendarWidget QToolButton {{
                color: #1E293B;
                background-color: white;
                border: none;
                font-weight: bold;
            }}
            QCalendarWidget QMenu {{ background-color: white; }}
            QCalendarWidget QSpinBox {{ background-color: white; color: #1E293B; }}
            QCalendarWidget QAbstractItemView:enabled {{
                color: #1E293B;
                selection-background-color: #2C7878;
                selection-color: white;
                outline: none;
            }}
            QCalendarWidget #qt_calendar_navigationbar {{ background-color: white; border-bottom: 1px solid #E2E8F0; }}
        """)
        
        self.expiry_input.setStyleSheet("""
            QDateEdit { 
                border: 1px solid #E2E8F0; 
                border-radius: 8px; 
                padding-left: 10px; 
                background: white;
                color: #1E293B;
            }
            QDateEdit:focus { border: 2px solid #2C7878; }
            QDateEdit::drop-down { border: none; width: 30px; }
            QDateEdit::down-arrow { image: none; border-left: 5px solid transparent; border-right: 5px solid transparent; border-top: 5px solid #64748B; margin-right: 10px; }
        """)
        exp_v.addWidget(self.expiry_input)
        row2.addLayout(exp_v)

        # Quantity
        qty_v = QVBoxLayout()
        qty_v.addWidget(StyledLabel("Initial Quantity"))
        self.qty_stepper = QuantityStepper()
        qty_v.addWidget(self.qty_stepper)
        row2.addLayout(qty_v)
        left_col.addLayout(row2)

        # Pricing Section
        left_col.addSpacing(10)
        left_col.addWidget(StyledLabel("Pricing Details"))
        
        price_grid = QGridLayout()
        price_grid.setSpacing(15)
        
        for i, label_txt in enumerate(["Unit Cost ($)", "Selling Price ($)", "MRP ($)"]):
            lbl = StyledLabel(label_txt)
            price_grid.addWidget(lbl, 0, i)
            inp = ModernInput("0.00")
            inp.setAlignment(Qt.AlignRight)
            price_grid.addWidget(inp, 1, i)
        
        left_col.addLayout(price_grid)
        left_col.addStretch()
        
        content_layout.addLayout(left_col, 2)

        # RIGHT COLUMN (Quick Actions)
        right_col = QVBoxLayout()
        right_col.setSpacing(20)

        actions_card = QFrame()
        actions_card.setFixedWidth(280)
        actions_card.setStyleSheet("background: #F8FAFC; border-radius: 16px; border: 1px solid #E2E8F0;")
        act_layout = QVBoxLayout(actions_card)
        act_layout.setContentsMargins(20, 20, 20, 20)
        act_layout.setSpacing(15)
        
        act_layout.addWidget(StyledLabel("Quick Actions"))
        
        scan_btn = QPushButton("📷  Scan Barcode")
        scan_btn.setFixedHeight(45)
        scan_btn.setStyleSheet("""
            QPushButton { background: white; border: 1px solid #E2E8F0; border-radius: 8px; font-weight: bold; color: #1E293B;}
            QPushButton:hover { background: #F1F5F9; border-color: #CBD5E1; }
        """)
        act_layout.addWidget(scan_btn)

        dup_btn = QPushButton("🔍  Duplicate from Existing")
        dup_btn.setFixedHeight(45)
        dup_btn.setStyleSheet(scan_btn.styleSheet())
        act_layout.addWidget(dup_btn)
        
        act_layout.addSpacing(10)
        act_layout.addWidget(StyledLabel("Reorder Level"))
        self.reorder_slider = QSlider(Qt.Horizontal)
        self.reorder_slider.setRange(0, 100)
        self.reorder_slider.setValue(20)
        act_layout.addWidget(self.reorder_slider)
        
        reorder_hint = QLabel("Notify when stock below 20")
        reorder_hint.setStyleSheet("color: #64748B; font-size: 11px;")
        act_layout.addWidget(reorder_hint)
        self.reorder_slider.valueChanged.connect(lambda v: reorder_hint.setText(f"Notify when stock below {v}"))

        act_layout.addStretch()
        right_col.addWidget(actions_card)
        right_col.addStretch()

        content_layout.addLayout(right_col, 1)
        scroll.setWidget(content)
        main_layout.addWidget(scroll)

        # 3. Sticky Footer
        footer = QFrame()
        footer.setFixedHeight(85)
        footer.setStyleSheet("""
            QFrame { background: white; border-top: 1px solid #E2E8F0; }
        """)
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(40, 0, 40, 0)
        footer_layout.setSpacing(15)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("color: #64748B; font-weight: bold; border: none; background: transparent;")
        cancel_btn.clicked.connect(self.close)
        footer_layout.addWidget(cancel_btn)
        
        footer_layout.addStretch()

        save_add_btn = QPushButton("Save & Add Another")
        save_add_btn.setFixedSize(180, 45)
        save_add_btn.setStyleSheet(f"""
            QPushButton {{
                border: 2px solid #E2E8F0;
                border-radius: 12px;
                color: {self.primary};
                font-weight: bold;
            }}
            QPushButton:hover {{ background: #F8FAFC; }}
        """)
        footer_layout.addWidget(save_add_btn)

        save_btn = QPushButton("Save Medicine")
        save_btn.setFixedSize(160, 45)
        save_btn.clicked.connect(self.save_medicine)
        save_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #2C7878, stop:1 #1E5050);
                color: white;
                border-radius: 12px;
                font-weight: bold;
            }
            QPushButton:hover { background: #1E5050; }
        """)
        footer_layout.addWidget(save_btn)

        main_layout.addWidget(footer)

    def save_medicine(self):
        try:
            from database.models import Medicine
            from PySide6.QtWidgets import QMessageBox
            
            # 1. Collect Data
            name = self.name_input.text().strip()
            category = self.cat_combo.currentText()
            batch = self.batch_input.text().strip()
            expiry = self.expiry_input.date().toPython()
            qty = int(self.qty_stepper.value_input.text() or 0)
            reorder = self.reorder_slider.value()
            
            # Since pricing fields were added dynamically in a grid, we need to find them
            # or track them. In the original code, they were just local 'inp' vars.
            # I'll modify the loop to store them or just find them by index.
            # Grid: row 0 is labels, row 1 is inputs.
            cost = self.find_input_at(1, 0)
            selling = self.find_input_at(1, 1)
            
            if not name:
                QMessageBox.warning(self, "Validation Error", "Medicine name is required.")
                return

            data = {
                'medicine_name': name,
                'category': category,
                'company': 'Generic', # Placeholder as company field was missing in specific form
                'batch_no': batch,
                'expiry_date': expiry,
                'stock_qty': qty,
                'price': float(selling.text() or 0),
                'reorder_level': reorder
            }
            
            # 2. Save
            Medicine.create(data)
            
            # 3. Success
            QMessageBox.information(self, "Success", f"'{name}' has been added to inventory.")
            
            # 4. Refresh Parent if InventoryWindow
            if hasattr(self.parent(), 'refresh_data'):
                self.parent().refresh_data()
            
            self.close()
            
        except Exception as e:
            print(f"Error saving medicine: {e}")
            QMessageBox.critical(self, "Save Error", f"Could not save medicine.\n\n{e}")

    def find_input_at(self, row, col):
        # Helper to find input in the price_grid
        # This is a bit hacky because the grid wasn't stored
        # I'll use findChildren as a safer way or just fix the init_ui to store them
        # Let's check how many ModernInputs we have.
        inputs = self.findChildren(ModernInput)
        # name_input is 0, batch_input is 1, then the 3 price inputs 2,3,4
        if row == 1:
            if col == 0: return inputs[2] # Unit Cost
            if col == 1: return inputs[3] # Selling
            if col == 2: return inputs[4] # MRP
        return None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AddMedicineWindow()
    window.show()
    sys.exit(app.exec())
