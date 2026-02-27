import sys
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QFrame, QGraphicsDropShadowEffect, 
                             QScrollArea, QComboBox, QSlider, QGridLayout, 
                             QCompleter, QDateEdit, QStyle, QApplication,
                             QCheckBox, QTextEdit)
from PySide6.QtCore import Qt, QSize, QDate, QRect, QPoint
from PySide6.QtGui import (QFont, QColor, QPainter, QPen, QBrush, QLinearGradient, 
                           QIcon, QPainterPath)

from utils.theme import Theme
from gui.components import ModernButton, GlassCard as GlobalGlassCard

class StyledLabel(QLabel):
    """Figma-style label: 12pt uppercase semibold teal"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFont(Theme.get_font(10, QFont.DemiBold))
        self.setStyleSheet(f"color: {Theme.PRIMARY.name()}; text-transform: uppercase; letter-spacing: 0.5px; border: none; background: transparent;")

class ModernInput(QLineEdit):
    """Modern input with hover/focus states and subtle glow"""
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setFixedHeight(45)
        self.setStyleSheet(f"""
            QLineEdit {{
                border: 1px solid {Theme.BORDER.name()};
                border-radius: 8px;
                padding: 0 12px;
                background: white;
                font-size: 14px;
                color: {Theme.TEXT_MAIN.name()};
            }}
            QLineEdit:hover {{
                border-color: {Theme.BORDER_DARK.name()};
            }}
            QLineEdit:focus {{
                border: 2px solid {Theme.PRIMARY.name()};
            }}
        """)

class QuantityStepper(QWidget):
    """Styled quantity stepper with rounded buttons"""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        btn_style = f"""
            QPushButton {{
                background: {Theme.BG_MAIN.name()};
                border: 1px solid {Theme.BORDER.name()};
                border-radius: 6px;
                font-weight: bold;
                font-size: 16px;
                color: {Theme.TEXT_SUB.name()};
            }}
            QPushButton:hover {{ background: {Theme.BORDER.name()}; }}
        """
        
        self.minus_btn = QPushButton("-")
        self.minus_btn.setFixedSize(36, 36)
        self.minus_btn.setStyleSheet(btn_style)
        self.minus_btn.setCursor(Qt.PointingHandCursor)
        
        self.value_input = QLineEdit("0")
        self.value_input.setFixedWidth(70)
        self.value_input.setFixedHeight(36)
        self.value_input.setAlignment(Qt.AlignCenter)
        self.value_input.setFont(Theme.get_font(12, QFont.Bold))
        self.value_input.setStyleSheet(f"border: 1px solid {Theme.BORDER.name()}; border-radius: 6px; background: white; color: {Theme.TEXT_MAIN.name()};")
        
        self.plus_btn = QPushButton("+")
        self.plus_btn.setFixedSize(36, 36)
        self.plus_btn.setStyleSheet(btn_style)
        self.plus_btn.setCursor(Qt.PointingHandCursor)
        
        layout.addWidget(self.minus_btn)
        layout.addWidget(self.value_input)
        layout.addWidget(self.plus_btn)
        
        self.minus_btn.clicked.connect(lambda: self.update_val(-1))
        self.plus_btn.clicked.connect(lambda: self.update_val(1))

    def update_val(self, delta):
        try:
            val = int(self.value_input.text() or 0)
            self.value_input.setText(str(max(0, val + delta)))
        except: self.value_input.setText("0")

class ProgressIndicator(QWidget):
    """Top progress bar showing current step"""
    def __init__(self, steps, current=0, parent=None):
        super().__init__(parent)
        self.steps = steps
        self.current = current
        self.setFixedHeight(70)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        w = self.width()
        h = self.height()
        padding = 60
        track_y = h // 2 - 5
        
        # Draw track
        painter.setPen(Qt.NoPen)
        painter.setBrush(Theme.BG_MAIN)
        painter.drawRoundedRect(padding, track_y, w - 2*padding, 6, 3, 3)
        
        # Draw active track
        step_w = (w - 2*padding) / (len(self.steps) - 1)
        active_w = self.current * step_w
        painter.setBrush(Theme.PRIMARY)
        painter.drawRoundedRect(padding, track_y, active_w, 6, 3, 3)
        
        # Draw nodes
        for i, step in enumerate(self.steps):
            x = padding + (i * step_w)
            is_active = i <= self.current
            
            painter.setBrush(QColor("white"))
            painter.setPen(QPen(Theme.PRIMARY if is_active else Theme.BORDER_DARK, 2))
            painter.drawEllipse(QPoint(x, track_y + 3), 8, 8)
            
            if is_active:
                painter.setBrush(Theme.PRIMARY)
                painter.drawEllipse(QPoint(x, track_y + 3), 4, 4)
            
            # Label
            painter.setPen(QPen(Theme.PRIMARY if i == self.current else Theme.TEXT_SUB))
            painter.setFont(Theme.get_font(9, QFont.Bold if i == self.current else QFont.Normal))
            rect = QRect(x - 60, track_y + 20, 120, 25)
            painter.drawText(rect, Qt.AlignCenter, step)

class AddMedicineWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.Window)
        self.setWindowTitle("D. Chemist Pro - Register Medicine")
        self.setMinimumSize(850, 650)
        self.resize(950, 720)
        self.setStyleSheet(f"background-color: {Theme.BG_MAIN.name()};")
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
        self.progress = ProgressIndicator(["Basic Info", "Inventory", "Pricing", "Medical"], 0)
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

        # Row 1: Medicine Name & Barcode
        row_name = QHBoxLayout()
        name_v = QVBoxLayout()
        name_v.addWidget(StyledLabel("Medicine Name"))
        self.name_input = ModernInput("e.g. Panadol, Arinac")
        completer = QCompleter(["Panadol", "Arinac", "Paracetamol", "Amoxicillin"])
        self.name_input.setCompleter(completer)
        name_v.addWidget(self.name_input)
        row_name.addLayout(name_v, 2)

        barcode_v = QVBoxLayout()
        barcode_v.addWidget(StyledLabel("Barcode / SKU"))
        self.barcode_input = ModernInput("Scan or type barcode")
        barcode_v.addWidget(self.barcode_input)
        row_name.addLayout(barcode_v, 1)
        left_col.addLayout(row_name)

        # Row 2: Strength & Form
        row2 = QHBoxLayout()
        strength_v = QVBoxLayout()
        strength_v.addWidget(StyledLabel("Strength"))
        self.strength_input = ModernInput("e.g. 500mg, 10mg/5ml")
        strength_v.addWidget(self.strength_input)
        row2.addLayout(strength_v)

        form_v = QVBoxLayout()
        form_v.addWidget(StyledLabel("Form"))
        self.form_input = ModernInput("e.g. Tablet, Syrup, Injection")
        form_v.addWidget(self.form_input)
        row2.addLayout(form_v)
        left_col.addLayout(row2)

        # Row 3: Category & Company
        row3 = QHBoxLayout()
        cat_v = QVBoxLayout()
        cat_v.addWidget(StyledLabel("Category"))
        self.cat_combo = QComboBox()
        self.cat_combo.addItems(["Painkiller", "Antibiotic", "Vitamin", "Antipyretic", "Supplement", "Others"])
        self.cat_combo.setFixedHeight(45)
        self.cat_combo.setStyleSheet(self.get_combo_style())
        cat_v.addWidget(self.cat_combo)
        row3.addLayout(cat_v)

        comp_v = QVBoxLayout()
        comp_v.addWidget(StyledLabel("Company / Manufacturer"))
        self.company_input = ModernInput("e.g. GSK, Abbott, Getz")
        comp_v.addWidget(self.company_input)
        row3.addLayout(comp_v)
        left_col.addLayout(row3)

        # Inventory Row: Batch & Expiry
        left_col.addSpacing(10)
        left_col.addWidget(StyledLabel("Inventory & Expiry"))
        row_inv = QHBoxLayout()
        
        batch_v = QVBoxLayout()
        batch_v.addWidget(StyledLabel("Batch Number"))
        self.batch_input = ModernInput("BT-00123")
        batch_v.addWidget(self.batch_input)
        row_inv.addLayout(batch_v)

        exp_v = QVBoxLayout()
        exp_v.addWidget(StyledLabel("Expiry Date"))
        self.expiry_input = QDateEdit(QDate.currentDate().addYears(1))
        self.expiry_input.setFixedHeight(45)
        self.expiry_input.setCalendarPopup(True)
        self.expiry_input.setStyleSheet(self.get_date_style())
        exp_v.addWidget(self.expiry_input)
        row_inv.addLayout(exp_v)
        left_col.addLayout(row_inv)

        # Quantity Row: Stock & Reorder
        row_qty = QHBoxLayout()
        qty_v = QVBoxLayout()
        qty_v.addWidget(StyledLabel("Initial Stock Quantity"))
        self.qty_stepper = QuantityStepper()
        qty_v.addWidget(self.qty_stepper)
        row_qty.addLayout(qty_v)

        reorder_v = QVBoxLayout()
        reorder_v.addWidget(StyledLabel("Reorder Level"))
        self.reorder_input = ModernInput("50")
        self.reorder_input.setFixedWidth(100)
        reorder_v.addWidget(self.reorder_input)
        row_qty.addLayout(reorder_v)
        row_qty.addStretch()
        left_col.addLayout(row_qty)

        # Medical Info Section
        left_col.addSpacing(10)
        left_col.addWidget(StyledLabel("Medical Information & Compliance"))
        
        # Indication
        left_col.addWidget(StyledLabel("Indication (Usage)"))
        self.indication_input = ModernInput("e.g. Fever, Headache, Infection")
        left_col.addWidget(self.indication_input)

        # Side Effects
        left_col.addWidget(StyledLabel("Potential Side Effects"))
        self.side_effects_input = ModernInput("e.g. Drowsiness, Nausea")
        left_col.addWidget(self.side_effects_input)

        row_med = QHBoxLayout()
        age_v = QVBoxLayout()
        age_v.addWidget(StyledLabel("Age Restriction"))
        self.age_input = ModernInput("e.g. None, 12+, Adults only")
        age_v.addWidget(self.age_input)
        row_med.addLayout(age_v)

        presc_v = QVBoxLayout()
        presc_v.addSpacing(25) # align with input center
        self.presc_chk = QCheckBox("Prescription Required")
        self.presc_chk.setStyleSheet(f"color: {Theme.TEXT_MAIN.name()}; font-weight: bold; font-size: 13px;")
        presc_v.addWidget(self.presc_chk)
        row_med.addLayout(presc_v)
        left_col.addLayout(row_med)

        # Pricing Section
        left_col.addSpacing(10)
        left_col.addWidget(StyledLabel("Pricing Details"))
        
        price_grid = QGridLayout()
        price_grid.setSpacing(15)
        
        self.cost_input = ModernInput("0.00")
        self.cost_input.setAlignment(Qt.AlignRight)
        price_grid.addWidget(StyledLabel("Unit Cost"), 0, 0)
        price_grid.addWidget(self.cost_input, 1, 0)

        self.price_input = ModernInput("0.00")
        self.price_input.setAlignment(Qt.AlignRight)
        price_grid.addWidget(StyledLabel("Selling Price"), 0, 1)
        price_grid.addWidget(self.price_input, 1, 1)

        self.mrp_input = ModernInput("0.00")
        self.mrp_input.setAlignment(Qt.AlignRight)
        price_grid.addWidget(StyledLabel("MRP"), 0, 2)
        price_grid.addWidget(self.mrp_input, 1, 2)
        
        left_col.addLayout(price_grid)
        left_col.addStretch()
        
        content_layout.addLayout(left_col, 2)

        # RIGHT COLUMN (Quick Actions)
        right_col = QVBoxLayout()
        right_col.setSpacing(20)

        actions_card = QFrame()
        actions_card.setFixedWidth(300)
        actions_card.setStyleSheet(f"background: white; border-radius: 16px; border: none;")
        act_layout = QVBoxLayout(actions_card)
        act_layout.setContentsMargins(25, 25, 25, 25)
        act_layout.setSpacing(20)
        
        act_layout.addWidget(StyledLabel("Quick Actions"))
        
        self.scan_btn = ModernButton("📷  Scan Barcode", primary=False)
        act_layout.addWidget(self.scan_btn)

        self.dup_btn = ModernButton("🔍  Duplicate Selected", primary=False)
        act_layout.addWidget(self.dup_btn)
        
        act_layout.addSpacing(15)
        act_layout.addWidget(StyledLabel("Reorder Level"))
        self.reorder_slider = QSlider(Qt.Horizontal)
        self.reorder_slider.setRange(0, 500)
        self.reorder_slider.setValue(50)
        self.reorder_slider.setStyleSheet(f"""
            QSlider::groove:horizontal {{ background: {Theme.BG_MAIN.name()}; height: 6px; border-radius: 3px; }}
            QSlider::handle:horizontal {{ background: {Theme.PRIMARY.name()}; width: 18px; margin: -6px 0; border-radius: 9px; }}
        """)
        act_layout.addWidget(self.reorder_slider)
        
        reorder_hint = QLabel("Notify when stock below 50")
        reorder_hint.setStyleSheet(f"color: {Theme.TEXT_SUB.name()}; font-size: 11px;")
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
        footer.setStyleSheet(f"""
            QFrame {{ background: white; border-top: 2px solid {Theme.BORDER.name()}; }}
        """)
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(40, 0, 40, 0)
        footer_layout.setSpacing(15)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.setStyleSheet(f"color: {Theme.TEXT_SUB.name()}; font-weight: bold; border: none; background: transparent;")
        cancel_btn.clicked.connect(self.close)
        footer_layout.addWidget(cancel_btn)
        
        footer_layout.addStretch()

        self.save_add_btn = ModernButton("Save & Add Another", primary=False)
        self.save_add_btn.setFixedWidth(200)
        footer_layout.addWidget(self.save_add_btn)

        self.save_btn = ModernButton("Register Product")
        self.save_btn.setFixedWidth(180)
        self.save_btn.clicked.connect(self.save_medicine)
        footer_layout.addWidget(self.save_btn)

        main_layout.addWidget(footer)

    def save_medicine(self):
        try:
            from database.models import Medicine
            from PySide6.QtWidgets import QMessageBox
            
            # 1. Collect Data
            name = self.name_input.text().strip()
            barcode = self.barcode_input.text().strip()
            strength = self.strength_input.text().strip()
            form = self.form_input.text().strip()
            category = self.cat_combo.currentText()
            company = self.company_input.text().strip()
            
            batch = self.batch_input.text().strip()
            expiry = self.expiry_input.date().toPython()
            qty = int(self.qty_stepper.value_input.text() or 0)
            reorder = int(self.reorder_input.text() or 50)
            
            indication = self.indication_input.text().strip()
            side_effects = self.side_effects_input.text().strip()
            age_limit = self.age_input.text().strip()
            presc_req = self.presc_chk.isChecked()
            
            price = float(self.price_input.text() or 0)
            
            if not name:
                QMessageBox.warning(self, "Validation Error", "Medicine name is required.")
                return

            data = {
                'medicine_name': name,
                'category': category,
                'company': company or 'Generic',
                'barcode': barcode,
                'strength': strength,
                'form': form,
                'batch_no': batch,
                'expiry_date': expiry,
                'stock_qty': qty,
                'price': price,
                'reorder_level': reorder,
                'indication': indication,
                'side_effects': side_effects,
                'age_restriction': age_limit,
                'prescription_required': presc_req
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

    def get_combo_style(self):
        return f"""
            QComboBox {{ 
                border: none; 
                border-radius: 8px; 
                padding-left: 12px; 
                background: {Theme.BG_MAIN.name()};
                color: {Theme.TEXT_MAIN.name()};
            }}
            QComboBox:focus {{ border: 1px solid {Theme.PRIMARY.name()}; background: white; }}
            QComboBox::drop-down {{ border: none; width: 30px; }}
            QComboBox::down-arrow {{ image: none; border-left: 5px solid transparent; border-right: 5px solid transparent; border-top: 5px solid {Theme.TEXT_SUB.name()}; margin-right: 10px; }}
            QAbstractItemView {{
                background-color: white;
                border: 1px solid {Theme.BORDER.name()};
                selection-background-color: {Theme.BG_MAIN.name()};
                selection-color: {Theme.PRIMARY.name()};
                outline: none;
                padding: 6px;
                color: {Theme.TEXT_MAIN.name()};
            }}
        """

    def get_date_style(self):
        return f"""
            QDateEdit {{ 
                border: none; 
                border-radius: 8px; 
                padding-left: 12px; 
                background: {Theme.BG_MAIN.name()};
                color: {Theme.TEXT_MAIN.name()};
            }}
            QDateEdit:focus {{ border: 1px solid {Theme.PRIMARY.name()}; background: white; }}
            QDateEdit::drop-down {{ border: none; width: 30px; }}
            QDateEdit::down-arrow {{ image: none; border-left: 5px solid transparent; border-right: 5px solid transparent; border-top: 5px solid {Theme.TEXT_SUB.name()}; margin-right: 10px; }}
        """

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AddMedicineWindow()
    window.show()
    sys.exit(app.exec())
