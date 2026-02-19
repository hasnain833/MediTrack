import sys
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QFrame, QGraphicsDropShadowEffect, 
                             QScrollArea, QListWidget, QListWidgetItem,
                             QApplication, QSpacerItem, QSizePolicy, QMessageBox)
from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtGui import (QFont, QColor, QPainter, QPen, QBrush, QLinearGradient)
from datetime import datetime

class ProductRow(QFrame):
    """List row for products in the POS"""
    def __init__(self, name, price, stock, callback, parent=None):
        super().__init__(parent)
        self.setFixedHeight(65)
        self.setCursor(Qt.PointingHandCursor)
        self.name = name
        self.price = float(price)
        self.stock = int(stock)
        self.callback = callback
        
        self.setStyleSheet("""
            QFrame {
                background: white;
                border-bottom: 1px solid #F1F5F9;
                border-radius: 0px;
            }
            QFrame:hover {
                background: #F8FAFC;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        
        name_info = QVBoxLayout()
        name_info.setSpacing(2)
        self.lbl_name = QLabel(name)
        self.lbl_name.setFont(QFont("Inter", 11, QFont.Bold))
        self.lbl_name.setStyleSheet("color: #0F172A; border: none;")
        
        self.lbl_stock = QLabel(f"In Stock: {stock}")
        self.lbl_stock.setStyleSheet(f"color: {'#2C7878' if self.stock > 10 else '#EF4444'}; font-size: 10px; border: none;")
        name_info.addWidget(self.lbl_name)
        name_info.addWidget(self.lbl_stock)
        layout.addLayout(name_info)
        
        layout.addStretch()
        
        self.lbl_price = QLabel(f"Rs. {self.price:.2f}")
        self.lbl_price.setFont(QFont("Inter", 11, QFont.Bold))
        self.lbl_price.setStyleSheet("color: #2C7878; border: none;")
        layout.addWidget(self.lbl_price)
        
        self.add_btn = QPushButton("+")
        self.add_btn.setFixedSize(30,30)
        self.add_btn.setStyleSheet("""
            QPushButton { background: #F1F5F9; border-radius: 15px; font-weight: bold; border: none; color: #64748B; }
            QPushButton:hover { background: #2C7878; color: white; }
        """)
        self.add_btn.clicked.connect(lambda: self.callback(self.name, self.price))
        layout.addWidget(self.add_btn)

    def mousePressEvent(self, event):
        self.callback(self.name, self.price)

class CartItem(QFrame):
    """Stacked card for cart items"""
    def __init__(self, name, price, qty, on_change, parent=None):
        super().__init__(parent)
        self.setFixedHeight(80)
        self.name = name
        self.price = price
        self.qty = qty
        self.on_change = on_change
        
        self.setStyleSheet("background: white; border-bottom: 1px solid #F1F5F9;")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 5, 15, 5)
        
        info = QVBoxLayout()
        name_lbl = QLabel(name)
        name_lbl.setFont(QFont("Inter", 11, QFont.Bold))
        name_lbl.setStyleSheet("color: #0F172A;")
        
        price_lbl = QLabel(f"Rs. {price:.2f} / unit")
        price_lbl.setStyleSheet("color: #64748B; font-size: 11px;")
        info.addWidget(name_lbl)
        info.addWidget(price_lbl)
        layout.addLayout(info)
        
        layout.addStretch()
        
        # Stepper
        stepper = QHBoxLayout()
        btn_style = "background: #F1F5F9; border: none; border-radius: 12px; font-weight: bold; color: #475569;"
        
        minus = QPushButton("-")
        minus.setFixedSize(28, 28)
        minus.setStyleSheet(btn_style)
        minus.clicked.connect(lambda: self.update_qty(-1))
        
        self.qty_lbl = QLabel(str(qty))
        self.qty_lbl.setFixedWidth(30)
        self.qty_lbl.setAlignment(Qt.AlignCenter)
        self.qty_lbl.setFont(QFont("Inter", 11, QFont.Bold))
        
        plus = QPushButton("+")
        plus.setFixedSize(28, 28)
        plus.setStyleSheet(btn_style)
        plus.clicked.connect(lambda: self.update_qty(1))
        
        stepper.addWidget(minus)
        stepper.addWidget(self.qty_lbl)
        stepper.addWidget(plus)
        layout.addLayout(stepper)
        
        self.total_lbl = QLabel(f"Rs. {price*qty:.2f}")
        self.total_lbl.setFixedWidth(100)
        self.total_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.total_lbl.setFont(QFont("Inter", 12, QFont.Bold))
        self.total_lbl.setStyleSheet("color: #0F172A;")
        layout.addWidget(self.total_lbl)

    def update_qty(self, delta):
        new_qty = self.qty + delta
        if new_qty > 0:
            self.qty = new_qty
            self.qty_lbl.setText(str(self.qty))
            self.total_lbl.setText(f"Rs. {self.price * self.qty:.2f}")
            self.on_change()
        elif new_qty == 0:
            self.on_change(remove=self.name)

class BillingWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.Window)
        self.setWindowTitle("MediTrack POS - Express Checkout")
        self.resize(1100, 700) # Reduced height
        self.setStyleSheet("background: #F8FAFC;")
        
        self.primary = "#0F172A"
        self.accent = "#2C7878"
        self.cart_data = {} # {name: [price, qty]}
        
        # Debounce timer for search
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.execute_search)

        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Left Panel (Inventory Row List) - 40%
        left_panel = QFrame()
        left_panel.setStyleSheet("background: white; border-color: white; border-right: 1px solid #E2E8F0;")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(25, 25, 25, 25)
        left_layout.setSpacing(20)

        title = QLabel("Pharmacy Inventory")
        title.setFont(QFont("Inter", 14, QFont.Bold))
        title.setStyleSheet(f"color: {self.primary};")
        left_layout.addWidget(title)

        # Search Bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search name/brand...")
        self.search_input.setFixedHeight(45)
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                background: white;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                color: #0F172A;
                padding-left: 15px;
                font-size: 14px;
            }}
            QLineEdit:focus {{ border-color: {self.accent}; }}
        """)
        self.search_input.textChanged.connect(self.handle_search_input)
        left_layout.addWidget(self.search_input)

        # Product List Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")
        list_container = QWidget()
        self.list_v = QVBoxLayout(list_container)
        self.list_v.setContentsMargins(0, 0, 0, 0)
        self.list_v.setSpacing(0)
        

        self.products = []
        
        self.list_v.addStretch()
        scroll.setWidget(list_container)
        left_layout.addWidget(scroll)

        main_layout.addWidget(left_panel, 40)

        # 2. Right Panel (Cart & Checkout) - 60%
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        # Header
        header = QFrame()
        header.setFixedHeight(70)
        header.setStyleSheet("border-bottom: 1px solid #F1F5F9; background: white;")
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(30, 0, 30, 0)
        
        cart_title = QLabel("Billing Cart")
        cart_title.setFont(QFont("Inter", 16, QFont.Bold))
        h_layout.addWidget(cart_title)
        
        h_layout.addStretch()
        
        self.bill_no_lbl = QLabel(f"POS-{datetime.now().strftime('%H%M%S')}")
        self.bill_no_lbl.setStyleSheet("color: #64748B; font-weight: bold; margin-right: 10px;")
        h_layout.addWidget(self.bill_no_lbl)

        self.logout_btn = QPushButton("🚪 Logout")
        self.logout_btn.setFixedSize(100, 35)
        self.logout_btn.setStyleSheet("""
            QPushButton {
                background: #FEF2F2;
                color: #EF4444;
                border: 1px solid #FEE2E2;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #FEE2E2;
            }
        """)
        self.logout_btn.clicked.connect(self.handle_logout)
        h_layout.addWidget(self.logout_btn)
        
        right_layout.addWidget(header)

        # Cart Items List
        self.cart_scroll = QScrollArea()
        self.cart_scroll.setWidgetResizable(True)
        self.cart_scroll.setStyleSheet("border: none; background: white;")
        self.cart_container = QWidget()
        self.cart_container.setStyleSheet("background: white;")
        self.cart_v = QVBoxLayout(self.cart_container)
        self.cart_v.setSpacing(0)
        self.cart_v.setContentsMargins(0, 0, 0, 0)
        self.cart_v.addStretch()
        self.cart_scroll.setWidget(self.cart_container)
        right_layout.addWidget(self.cart_scroll)

        # Summary & Checkout
        footer = QFrame()
        footer.setStyleSheet("background: #F8FAFC; border-top: 1px solid #E2E8F0;")
        footer_layout = QVBoxLayout(footer)
        footer_layout.setContentsMargins(30, 20, 30, 20)
        footer_layout.setSpacing(15)

        summary_card = QFrame()
        summary_card.setStyleSheet("background: white; border-radius: 12px; border: 1px solid #E2E8F0;")
        sum_l = QVBoxLayout(summary_card)
        sum_l.setSpacing(8)
        
        lbl_style = "color: #1E293B; font-weight: 500;"
        val_style = "color: #1E293B; font-weight: bold;"

        sum1 = QHBoxLayout()
        ls1 = QLabel("Subtotal"); ls1.setStyleSheet(lbl_style); sum1.addWidget(ls1)
        self.sub_lbl = QLabel("Rs. 0.00"); self.sub_lbl.setAlignment(Qt.AlignRight); self.sub_lbl.setStyleSheet(val_style); sum1.addStretch(); sum1.addWidget(self.sub_lbl)
        
        sum2 = QHBoxLayout()
        ls2 = QLabel("GST (12%)"); ls2.setStyleSheet(lbl_style); sum2.addWidget(ls2)
        self.tax_lbl = QLabel("Rs. 0.00"); self.tax_lbl.setAlignment(Qt.AlignRight); self.tax_lbl.setStyleSheet(val_style); sum2.addStretch(); sum2.addWidget(self.tax_lbl)
        
        # Discount Row
        sum3 = QHBoxLayout()
        ls3 = QLabel("Discount"); ls3.setStyleSheet(lbl_style); sum3.addWidget(ls3)
        self.discount_input_percent = QLineEdit()
        self.discount_input_percent.setPlaceholderText("%")
        self.discount_input_percent.setFixedWidth(50)
        self.discount_input_percent.setStyleSheet("border: 1px solid #E2E8F0; border-radius: 4px; padding: 2px; color: #1E293B;")
        self.discount_input_percent.textChanged.connect(self.update_cart_ui)
        
        self.discount_input_fixed = QLineEdit()
        self.discount_input_fixed.setPlaceholderText("Fixed Rs.")
        self.discount_input_fixed.setFixedWidth(80)
        self.discount_input_fixed.setStyleSheet("border: 1px solid #E2E8F0; border-radius: 4px; padding: 2px; color: #1E293B;")
        self.discount_input_fixed.textChanged.connect(self.update_cart_ui)
        
        self.discount_lbl = QLabel("Rs. 0.00")
        self.discount_lbl.setAlignment(Qt.AlignRight)
        self.discount_lbl.setStyleSheet("color: #EF4444; font-weight: bold;")
        
        sum3.addWidget(self.discount_input_percent)
        sum3.addWidget(self.discount_input_fixed)
        sum3.addStretch()
        sum3.addWidget(self.discount_lbl)
        
        total_row = QHBoxLayout()
        total_lbl = QLabel("Grand Total")
        total_lbl.setFont(QFont("Inter", 14, QFont.Bold))
        total_lbl.setStyleSheet("color: #1E293B;")
        self.total_lbl = QLabel("Rs. 0.00")
        self.total_lbl.setFont(QFont("Inter", 24, QFont.Bold))
        self.total_lbl.setStyleSheet(f"color: {self.accent};")
        total_row.addWidget(total_lbl); total_row.addStretch(); total_row.addWidget(self.total_lbl)
        
        sum_l.addLayout(sum1)
        sum_l.addLayout(sum2)
        sum_l.addLayout(sum3)
        line = QFrame(); line.setFixedHeight(1); line.setStyleSheet("background: #F1F5F9;"); sum_l.addWidget(line)
        sum_l.addLayout(total_row)
        footer_layout.addWidget(summary_card)

        self.complete_btn = QPushButton("COMPLETE SALE →")
        self.complete_btn.setFixedHeight(60)
        self.complete_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 {self.accent}, stop:1 #1E5050);
                color: white;
                border-radius: 8px;
                font-weight: bold;
                font-size: 16px;
            }}
            QPushButton:hover {{ background: #1E5050; }}
            QPushButton:disabled {{ background: #CBD5E1; color: #94A3B8; }}
        """)
        self.complete_btn.setEnabled(False)
        self.complete_btn.clicked.connect(self.complete_sale)
        footer_layout.addWidget(self.complete_btn)

        right_layout.addWidget(footer)
        main_layout.addWidget(right_panel, 60)

    def handle_search_input(self):
        """Called on every keystroke, starts/restarts the debounce timer"""
        term = self.search_input.text().strip()
        if not term:
            self.search_timer.stop()
            self.update_inventory_list([])
            return
            
        # If it's a long number, it's likely a barcode scan - handle immediately
        if term.isdigit() and len(term) >= 8:
            self.search_timer.stop()
            self.execute_search()
        else:
            # Debounce for typing names
            self.search_timer.start(150) # 150ms delay

    def execute_search(self):
        term = self.search_input.text().strip()
        if not term: return

        from database.models import Medicine
        
        # Barcode match (Full match)
        if term.isdigit() and len(term) >= 8:
            med = Medicine.find_by_barcode(term)
            if med:
                self.add_to_cart(med['medicine_name'], med['price'])
                self.search_input.clear()
                return

        # Real-time Filter (DB Search)
        results = Medicine.search(term)
        self.update_inventory_list(results)

    def refresh_inventory_list(self):
        from database.models import Medicine
        self.update_inventory_list(Medicine.get_all())

    def update_inventory_list(self, products):
        # Clear layout
        while self.list_v.count() > 1:
            item = self.list_v.takeAt(0)
            if item.widget(): item.widget().deleteLater()
            
        for prod in products:
            row = ProductRow(prod['medicine_name'], prod['price'], prod['stock_qty'], self.add_to_cart)
            row.inventory_id = prod['id']
            self.list_v.insertWidget(self.list_v.count()-1, row)

    def add_to_cart(self, name, price):
        if name in self.cart_data:
            self.cart_data[name][1] += 1
        else:
            self.cart_data[name] = [price, 1]
        self.update_cart_ui()

    def update_cart_ui(self, remove=None):
        if remove:
            if remove in self.cart_data: del self.cart_data[remove]
            
        # Clear layout
        while self.cart_v.count() > 1:
            item = self.cart_v.takeAt(0)
            if item.widget(): item.widget().deleteLater()
            
        subtotal = 0
        for name, (price, qty) in self.cart_data.items():
            item_widget = CartItem(name, price, qty, self.update_cart_ui)
            self.cart_v.insertWidget(self.cart_v.count()-1, item_widget)
            subtotal += price * qty
            
        tax = subtotal * 0.12 # GST as configured (12%)
        
        # Discount Logic
        discount = 0
        try:
            p_val = self.discount_input_percent.text()
            if p_val:
                discount += (subtotal * float(p_val) / 100)
            
            f_val = self.discount_input_fixed.text()
            if f_val:
                discount += float(f_val)
        except: pass
        
        total = subtotal + tax - discount
        if total < 0: total = 0
        
        self.sub_lbl.setText(f"Rs. {subtotal:.2f}")
        self.tax_lbl.setText(f"Rs. {tax:.2f}")
        self.discount_lbl.setText(f"- Rs. {discount:.2f}")
        self.total_lbl.setText(f"Rs. {total:.2f}")
        self.complete_btn.setEnabled(len(self.cart_data) > 0)

    def complete_sale(self):
        try:
            from database.models import Sale, Customer, AuditLog
            
            subtotal = sum(p[0]*p[1] for p in self.cart_data.values())
            tax = subtotal * 0.12
            
            discount = 0
            try:
                p_val = self.discount_input_percent.text()
                if p_val: discount += (subtotal * float(p_val) / 100)
                f_val = self.discount_input_fixed.text()
                if f_val: discount += float(f_val)
            except: pass
            
            total = subtotal + tax - discount
            if total < 0: total = 0
            
            # 1. Handle Customer
            cust = Customer.find_or_create("Walk-in Customer")
            
            # 2. Prepare items for model (inventory_id, quantity, unit_price, subtotal)
            sale_items = []
            from database.models import Medicine
            all_meds = {m['medicine_name']: m['id'] for m in Medicine.get_all()}
            
            for name, (price, qty) in self.cart_data.items():
                med_id = all_meds.get(name)
                if med_id:
                    sale_items.append((med_id, qty, price, price * qty))

            # 3. Create Sale in DB
            bill_no = self.bill_no_lbl.text()
            user_id = 1 
            
            sale_id = Sale.create_transaction(
                bill_no, 
                user_id, 
                cust['id'], 
                sale_items, 
                (subtotal, tax, total),
                discount=discount
            )
            
            # 4. Log Action
            AuditLog.log(user_id, "SALE_COMPLETE", "BILLING", f"Processed Bill {bill_no}")

            # 5. Show Preview
            bill_data = {
                "bill_no": bill_no,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "customer_name": cust['name'],
                "items": [(n, p[0], p[1], p[0]*p[1]) for n, p in self.cart_data.items()],
                "subtotal": subtotal,
                "discount": discount,
                "gst": tax,
                "total": total
            }
            from gui.bill_preview_window import BillPreviewWindow
            self.preview = BillPreviewWindow(self, bill_data)
            self.preview.show()
            
            # Clear cart on success
            self.cart_data = {}
            self.update_cart_ui()
            
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            QMessageBox.critical(self, "Error", f"Failed to record sale: {e}")

    def handle_logout(self):
        reply = QMessageBox.question(self, 'Logout', 'Are you sure you want to logout?',
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            print("DEBUG: Cashier Logging out...")
            try:
                from gui.login_window import LoginWindow
                self.login_win = LoginWindow()
                self.login_win.show()
                self.close()
            except Exception as e:
                import traceback
                traceback.print_exc()
                QMessageBox.critical(self, "Logout Error", f"Could not return to login screen.\n\nError: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BillingWindow()
    window.show()
    sys.exit(app.exec())
