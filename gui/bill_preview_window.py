import sys
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QApplication, 
                             QMessageBox, QGridLayout, QSpacerItem, QSizePolicy)
from PySide6.QtCore import Qt, QSize, QRect
from PySide6.QtGui import QFont, QColor, QPainter, QPen, QBrush, QPixmap, QPainterPath
from datetime import datetime
from services.template_service import TemplateService

class InvoicePaper(QFrame):
    """Refined paper widget with subtle medical cross watermark"""
    def __init__(self, template=None, parent=None):
        super().__init__(parent)
        self.template = template or TemplateService.load_template()
        self.setFixedSize(794, 1123)
        self.setStyleSheet("background-color: white;")

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Center of paper
        w, h = self.width(), self.height()
        cx, cy = w // 2, h // 2
        
        # Draw Medical Cross Watermark (5% Opacity)
        painter.setPen(Qt.NoPen)
        primary = QColor(self.template['theme']['primary'])
        color = QColor(primary.red(), primary.green(), primary.blue(), 12) 
        painter.setBrush(color)
        
        size = 200
        thickness = 60
        
        painter.drawRect(cx - thickness // 2, cy - size // 2, thickness, size)
        painter.drawRect(cx - size // 2, cy - thickness // 2, size, thickness)

class InvoiceTable(QFrame):
    """Spreadsheet-style table for invoice items"""
    def __init__(self, items, template=None, parent=None):
        super().__init__(parent)
        t = template or TemplateService.load_template()
        self.setStyleSheet(f"background: white; border-top: 2px solid {t['theme']['primary']};")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header Row
        header = QFrame()
        header.setFixedHeight(35)
        header.setStyleSheet(f"background: {t['table']['header_bg']}; border-bottom: 1px solid {t['table']['row_border']};")
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(10, 0, 10, 0)
        
        cols = [
            ("ITEM", 1), ("BATCH", 0.7), 
            ("EXPIRY", 0.7), ("QTY", 0.4), ("RATE", 0.6), 
            ("GST%", 0.4), ("AMOUNT", 0.8)
        ]
        
        for text, stretch in cols:
            lbl = QLabel(text)
            f = QFont()
            f.setFamily(t['theme']['font_family'])
            f.setPointSize(8)
            f.setBold(True)
            lbl.setFont(f)
            lbl.setStyleSheet(f"color: {t['table']['header_text']}; border: none;")
            h_layout.addWidget(lbl, stretch * 10)
            
        layout.addWidget(header)

        # Item Rows
        for i, item in enumerate(items):
            row = QFrame()
            row.setFixedHeight(30)
            row.setStyleSheet(f"border-bottom: 1px solid {t['table']['row_border']};")
            r_layout = QHBoxLayout(row)
            r_layout.setContentsMargins(10, 0, 10, 0)
            
            vals = [
                (item[0], 1), ("BT-12", 0.7), 
                ("12/26", 0.7), (str(item[2]), 0.4), (f"{item[1]:.2f}", 0.6), 
                ("12%", 0.4), (f"{item[3]:.2f}", 0.8)
            ]
            
            for val, stretch in vals:
                lbl = QLabel(val)
                f_row = QFont()
                f_row.setFamily(t['theme']['font_family'])
                f_row.setPointSize(9)
                lbl.setFont(f_row)
                if stretch == 0.8: # Amount col
                    f_m = QFont()
                    f_m.setFamily("JetBrains Mono")
                    f_m.setPointSize(9)
                    f_m.setBold(True)
                    lbl.setFont(f_m)
                    lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                r_layout.addWidget(lbl, stretch * 10)
            layout.addWidget(row)

class BillPreviewWindow(QWidget):
    def __init__(self, master, bill_data):
        super().__init__(None, Qt.Window)
        self.setWindowTitle("Professional Invoice - D. Chemist")
        self.resize(850, 950)
        self.setStyleSheet(f"background-color: {Theme.BG_MAIN.name()};")
        self.bill_data = bill_data
        self.template = TemplateService.load_template()
        self.init_ui()

    def init_ui(self):
        t = self.template
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")
        
        self.paper = InvoicePaper()
        paper_layout = QVBoxLayout(self.paper)
        paper_layout.setContentsMargins(50, 50, 50, 50)
        paper_layout.setSpacing(15)

        # 1. Header Section
        header = QHBoxLayout()
        logo_v = QVBoxLayout()
        name = QLabel(t['store']['name'])
        f22b = QFont()
        f22b.setFamily(t['theme']['font_family'])
        f22b.setPointSize(22)
        f22b.setBold(True)
        name.setFont(f22b)
        name.setStyleSheet(f"color: {t['store']['color']}; letter-spacing: 2px;")
        logo_v.addWidget(name)
        
        tagline = QLabel(t['store']['tagline'])
        f8b = QFont()
        f8b.setFamily(t['theme']['font_family'])
        f8b.setPointSize(8)
        f8b.setBold(True)
        tagline.setFont(f8b)
        tagline.setStyleSheet(f"color: {t['store']['tagline_color']}; letter-spacing: 1px;")
        logo_v.addWidget(tagline)
        header.addLayout(logo_v)
        
        header.addStretch()
        
        addr = QLabel(t['store']['address'])
        f9 = QFont()
        f9.setFamily(t['theme']['font_family'])
        f9.setPointSize(9)
        addr.setFont(f9)
        addr.setAlignment(Qt.AlignRight)
        addr.setStyleSheet(f"color: {t['store']['address_color']}; line-height: 1.4;")
        header.addWidget(addr)
        paper_layout.addLayout(header)

        # 2. Tax Invoice Title
        title_v = QVBoxLayout()
        title_v.setSpacing(5)
        title = QLabel("TAX INVOICE")
        f18l = QFont()
        f18l.setFamily(t['theme']['font_family'])
        f18l.setPointSize(18)
        f18l.setWeight(QFont.Light)
        title.setFont(f18l)
        title.setStyleSheet(f"color: {t['theme']['accent']}; letter-spacing: 4px; text-transform: uppercase;")
        title_v.addWidget(title)
        
        underline = QFrame(); underline.setFixedHeight(1); underline.setFixedWidth(60)
        underline.setStyleSheet(f"background: {t['theme']['primary']};"); title_v.addWidget(underline)
        paper_layout.addLayout(title_v)

        # 3. Metadata Boxes
        meta_row = QHBoxLayout()
        meta_row.setSpacing(30)
        
        # Left: Bill To
        cust_box = QFrame()
        cust_layout = QVBoxLayout(cust_box)
        lbl = QLabel("BILL TO")
        f8ba = QFont(); f8ba.setFamily(t['theme']['font_family']); f8ba.setPointSize(8); f8ba.setBold(True)
        lbl.setFont(f8ba); lbl.setStyleSheet("color: #94A3B8;")
        cust_layout.addWidget(lbl)
        cust_name = QLabel(self.bill_data.get('customer_name', 'Walk-in Customer'))
        f11b = QFont(); f11b.setFamily(t['theme']['font_family']); f11b.setPointSize(11); f11b.setBold(True)
        cust_name.setFont(f11b)
        cust_layout.addWidget(cust_name)
        cust_layout.addWidget(QLabel(f"PH: {self.bill_data.get('customer_phone', '--')}", styleSheet="color: #64748B;"))
        meta_row.addWidget(cust_box, 1)
        
        # Right: Invoice Details
        inv_card = QFrame()
        inv_card.setStyleSheet(f"background: {t['theme'].get('bg_card', '#F8FAFC')}; border-radius: 8px; border: none;")
        inv_l = QGridLayout(inv_card)
        inv_l.setSpacing(10)
        
        def add_meta_field(row, l, v):
            kl = QLabel(l); f_k = QFont(); f_k.setFamily(t['theme']['font_family']); f_k.setPointSize(8); f_k.setBold(True); kl.setFont(f_k); kl.setStyleSheet("color: #64748B;")
            vl = QLabel(v); f_v = QFont(); f_v.setFamily(t['theme']['font_family']); f_v.setPointSize(9); f_v.setBold(True); vl.setFont(f_v)
            inv_l.addWidget(kl, row, 0); inv_l.addWidget(vl, row, 1)

        add_meta_field(0, "INVOICE NO", self.bill_data.get('bill_no', 'POS-0001'))
        add_meta_field(1, "DATE", self.bill_data.get('date', '2026-02-19'))
        add_meta_field(2, "DUE DATE", datetime.now().strftime("%Y-%m-%d"))
        meta_row.addWidget(inv_card, 1)
        
        paper_layout.addLayout(meta_row)
        paper_layout.addSpacing(10)

        # 4. Main Table
        self.table = InvoiceTable(self.bill_data.get('items', []), t)
        paper_layout.addWidget(self.table)

        # 5. Financial Summary (Flex Layout)
        paper_layout.addSpacing(20)
        flex_row = QHBoxLayout()
        flex_row.setSpacing(50)
        
        # Left: Amount in Words
        words_v = QVBoxLayout()
        words_v.addStretch()
        w_lbl = QLabel("TOTAL AMOUNT IN WORDS")
        f8bw = QFont(); f8bw.setFamily(t['theme']['font_family']); f8bw.setPointSize(8); f8bw.setBold(True); w_lbl.setFont(f8bw); w_lbl.setStyleSheet("color: #94A3B8;")
        words_v.addWidget(w_lbl)
        
        total_words = QLabel("Seventy-Two Rupees and Eighty Paise Only")
        f10i = QFont(); f10i.setFamily(t['theme']['font_family']); f10i.setPointSize(10); f10i.setItalic(True)
        total_words.setFont(f10i)
        total_words.setStyleSheet("color: #0F172A; border-bottom: 2px dotted #E2E8F0; padding-bottom: 10px;")
        words_v.addWidget(total_words)
        
        if t['footer'].get('show_bank', True):
            bank = QLabel("BANK DETAILS\nStandard Chartered Bank | A/C: 1234567890\nIBAN: PK12 SCBL 0000 0001 2345 6789")
            f7 = QFont(); f7.setFamily(t['theme']['font_family']); f7.setPointSize(7)
            bank.setFont(f7); bank.setStyleSheet("color: #94A3B8; margin-top: 15px;")
            words_v.addWidget(bank)
        flex_row.addLayout(words_v, 1)
        
        # Right: Totals Card
        total_v = QVBoxLayout()
        summary = QFrame()
        summary.setFixedWidth(280)
        summary.setStyleSheet(f"background: white; border: none; border-radius: 12px;")
        sum_layout = QVBoxLayout(summary)
        sum_layout.setSpacing(10)
        
        def sum_row(l, v, b=False, s=False):
            row = QHBoxLayout()
            kl = QLabel(l)
            fk = QFont(); fk.setFamily(t['theme']['font_family']); fk.setPointSize(9); fk.setBold(b); kl.setFont(fk)
            vl = QLabel(f"Rs. {float(v):.2f}")
            fv = QFont(); fv.setFamily("JetBrains Mono"); fv.setPointSize(10 if not s else 14); fv.setBold(True)
            vl.setFont(fv)
            vl.setAlignment(Qt.AlignRight)
            if s: vl.setStyleSheet("color: white;")
            row.addWidget(kl); row.addStretch(); row.addWidget(vl)
            return row

        sum_layout.addLayout(sum_row("Subtotal", self.bill_data.get('subtotal', 0)))
        
        discount = self.bill_data.get('discount', 0)
        if discount > 0:
            row_d = sum_row("Discount", discount)
            row_d.itemAt(2).widget().setStyleSheet("color: #EF4444; font-weight: bold;")
            sum_layout.addLayout(row_d)

        sum_layout.addLayout(sum_row("Taxable Value", self.bill_data.get('subtotal', 0) - discount))
        
        gst_split = QHBoxLayout()
        cg = QVBoxLayout()
        cg.addWidget(QLabel("CGST (6%)", styleSheet="color: #64748B; font-size: 8px; font-weight: bold;"))
        vl_cg = QLabel(f"Rs. {self.bill_data.get('gst', 0)/2:.2f}")
        fcg = QFont(); fcg.setFamily(t['theme']['font_family']); fcg.setPointSize(9); fcg.setBold(True); vl_cg.setFont(fcg)
        cg.addWidget(vl_cg)
        
        sg = QVBoxLayout()
        sg.addWidget(QLabel("SGST (6%)", styleSheet="color: #64748B; font-size: 8px; font-weight: bold;"))
        vl_sg = QLabel(f"Rs. {self.bill_data.get('gst', 0)/2:.2f}")
        fsg = QFont(); fsg.setFamily(t['theme']['font_family']); fsg.setPointSize(9); fsg.setBold(True); vl_sg.setFont(fsg)
        sg.addWidget(vl_sg)
        
        gst_split.addLayout(cg); gst_split.addLayout(sg)
        sum_layout.addLayout(gst_split)
        
        grand_box = QFrame()
        grand_box.setFixedHeight(60)
        grand_box.setStyleSheet(f"background: {t['theme']['primary']}; border-radius: 8px;")
        gb_layout = QVBoxLayout(grand_box)
        gb_layout.addLayout(sum_row("GRAND TOTAL", self.bill_data.get('total', 0), True, True))
        sum_layout.addWidget(grand_box)
        
        total_v.addWidget(summary)
        flex_row.addLayout(total_v)
        paper_layout.addLayout(flex_row)

        # 6. Footer
        paper_layout.addStretch()
        footer = QHBoxLayout()
        
        if t['footer'].get('show_qr', True):
            qr_place = QLabel("[QR CODE]")
            qr_place.setFixedSize(60, 60)
            qr_place.setStyleSheet("background: #F1F5F9; border-radius: 4px; color: #94A3B8; font-size: 8px;")
            qr_place.setAlignment(Qt.AlignCenter)
            footer.addWidget(qr_place)
        
        footer.addStretch()
        
        thanks = QLabel(t['footer']['thanks_text'])
        thanks.setStyleSheet(f"color: {t['footer']['thanks_color']}; font-family: 'Brush Script MT', 'Italianno', cursive; font-size: 24px; font-style: italic;")
        footer.addWidget(thanks)
        
        paper_layout.addLayout(footer)

        scroll_content = QWidget()
        scroll_content.setStyleSheet(f"background-color: {Theme.BG_MAIN.name()};")
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setAlignment(Qt.AlignCenter)
        scroll_layout.addWidget(self.paper)
        scroll.setWidget(scroll_content)
        
        main_layout.addWidget(scroll)

        float_footer = QFrame()
        float_footer.setFixedHeight(80)
        float_footer.setStyleSheet(f"background: white; border: none; border-top: 2px solid {Theme.BORDER.name()};")
        ff_layout = QHBoxLayout(float_footer)
        ff_layout.setContentsMargins(40, 0, 40, 0)
        
        p_btn = QPushButton("Print Receipt")
        p_btn.setFixedSize(160, 45)
        p_btn.setStyleSheet(f"background: {t['theme']['primary']}; color: white; border-radius: 8px; font-weight: bold;")
        p_btn.clicked.connect(lambda: QMessageBox.information(self, "Print", "Dispatching to thermal printer..."))
        ff_layout.addStretch()
        ff_layout.addWidget(p_btn)
        
        main_layout.addWidget(float_footer)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    data = {
        "bill_no": "INV/2026/0892",
        "date": "2026-02-19",
        "customer_name": "HASNAIN ALI",
        "customer_phone": "+92 321 4567890",
        "items": [
            ("Paracetamol 500mg USP", 10.0, 5, 50.0),
            ("Amoxicillin Trihydrate", 45.0, 2, 90.0),
            ("Gaviscon Liquid 150ml", 350.0, 1, 350.0),
            ("Vitamin D3 Drops", 120.0, 3, 360.0)
        ],
        "subtotal": 850.0,
        "gst": 102.0,
        "total": 952.0
    }
    try:
        window = BillPreviewWindow(None, data)
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"CRASH: {e}")
