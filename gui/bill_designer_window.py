import sys
import os
# Add project root to sys.path to support direct execution
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import copy
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QApplication, 
                             QMessageBox, QGridLayout, QSpacerItem, QSizePolicy,
                             QLineEdit, QCheckBox, QColorDialog, QFontDialog,
                             QTabWidget)
from PySide6.QtCore import Qt, QSize, QRect, Signal, QMimeData
from PySide6.QtGui import (QFont, QColor, QPainter, QPen, QBrush, QPixmap, 
                          QPainterPath, QIcon, QDrag)
from datetime import datetime

from services.template_service import TemplateService
from gui.bill_preview_window import InvoicePaper, InvoiceTable

class PropertyField(QFrame):
    def __init__(self, label, value, field_type="text", callback=None, parent=None):
        super().__init__(parent)
        self.callback = callback
        self.field_type = field_type
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 5, 0, 5)
        
        lbl = QLabel(label)
        lbl.setStyleSheet("color: #64748B; font-size: 11px; font-weight: bold;")
        layout.addWidget(lbl)
        
        layout.addStretch()
        
        if field_type == "text":
            self.input = QLineEdit(str(value))
            self.input.setFixedWidth(150)
            self.input.setStyleSheet("border: 1px solid #E2E8F0; border-radius: 4px; padding: 4px;")
            self.input.textChanged.connect(self.on_changed)
            layout.addWidget(self.input)
        elif field_type == "color":
            self.color_btn = QPushButton()
            self.color_btn.setFixedSize(30, 20)
            self.current_color = value
            self.color_btn.setStyleSheet(f"background-color: {value}; border: 1px solid #E2E8F0; border-radius: 4px;")
            self.color_btn.clicked.connect(self.pick_color)
            layout.addWidget(self.color_btn)
        elif field_type == "bool":
            self.check = QCheckBox()
            self.check.setChecked(bool(value))
            self.check.stateChanged.connect(self.on_changed)
            layout.addWidget(self.check)

    def on_changed(self, *args):
        if self.callback:
            if self.field_type == "text":
                self.callback(self.input.text())
            elif self.field_type == "bool":
                self.callback(self.check.isChecked())

    def pick_color(self):
        color = QColorDialog.getColor(QColor(self.current_color), self)
        if color.isValid():
            self.current_color = color.name()
            self.color_btn.setStyleSheet(f"background-color: {self.current_color}; border: 1px solid #E2E8F0; border-radius: 4px;")
            if self.callback:
                self.callback(self.current_color)

class DraggableSection(QFrame):
    def __init__(self, title, key, parent=None):
        super().__init__(parent)
        self.key = key
        self.setAcceptDrops(True)
        self.setFixedHeight(45)
        self.setStyleSheet("""
            QFrame {
                background: #F8FAFC;
                border: 1px solid #E2E8F0;
                border-radius: 6px;
                padding-left: 10px;
            }
            QFrame:hover { border-color: #2C7878; background: white; }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        
        icon = QLabel("≡")
        icon.setStyleSheet("color: #94A3B8; font-size: 16px; font-weight: bold;")
        layout.addWidget(icon)
        
        lbl = QLabel(title)
        lbl.setFont(QFont("Inter", 9, QFont.Bold))
        lbl.setStyleSheet("color: #0F172A;")
        layout.addWidget(lbl)
        
        layout.addStretch()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            mime.setText(self.key)
            drag.setMimeData(mime)
            drag.exec(Qt.MoveAction) # Updated from exec_ to exec for DeprecationWarning

class BillDesignerWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.Window)
        self.setWindowTitle("Bill Template Designer")
        self.resize(1200, 800) # Compact size
        self.setStyleSheet("background-color: #F8FAFC;")
        
        self.current_template = TemplateService.load_template()
        self.zoom_level = 0.75 # Default zoomed out to fit better
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Top Action Bar
        top_bar = QFrame()
        top_bar.setFixedHeight(65)
        top_bar.setStyleSheet("background: white; border-bottom: 1px solid #E2E8F0;")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(25, 0, 25, 0)
        
        title_box = QVBoxLayout()
        title = QLabel("Template Designer")
        title.setFont(QFont("Inter", 14, QFont.Bold))
        title.setStyleSheet("color: #0F172A;")
        title_box.addWidget(title)
        
        subtitle = QLabel("Admin - Live Bill Customization")
        subtitle.setStyleSheet("color: #64748B; font-size: 10px; font-weight: bold; letter-spacing: 0.5px;")
        title_box.addWidget(subtitle)
        top_layout.addLayout(title_box)
        
        top_layout.addStretch()
        
        # Zoom Controls
        zoom_group = QFrame()
        zoom_group.setStyleSheet("background: #F1F5F9; border-radius: 6px; border: 1px solid #E2E8F0;")
        zg_l = QHBoxLayout(zoom_group)
        zg_l.setContentsMargins(5, 5, 5, 5)
        
        btn_zoom_out = QPushButton("−")
        btn_zoom_out.setFixedSize(30, 30)
        btn_zoom_out.setStyleSheet("background: white; border-radius: 4px; font-weight: bold;")
        btn_zoom_out.clicked.connect(self.zoom_out)
        
        self.zoom_lbl = QLabel(f"{int(self.zoom_level * 100)}%")
        self.zoom_lbl.setFixedWidth(40)
        self.zoom_lbl.setAlignment(Qt.AlignCenter)
        self.zoom_lbl.setStyleSheet("font-weight: bold; color: #475569;")
        
        btn_zoom_in = QPushButton("+")
        btn_zoom_in.setFixedSize(30, 30)
        btn_zoom_in.setStyleSheet("background: white; border-radius: 4px; font-weight: bold;")
        btn_zoom_in.clicked.connect(self.zoom_in)
        
        zg_l.addWidget(btn_zoom_out)
        zg_l.addWidget(self.zoom_lbl)
        zg_l.addWidget(btn_zoom_in)
        top_layout.addWidget(zoom_group)
        
        top_layout.addSpacing(20)
        
        btn_style = "padding: 8px 18px; border-radius: 6px; font-weight: bold; font-size: 12px;"
        
        reset_btn = QPushButton("Reset Default")
        reset_btn.setStyleSheet(f"{btn_style} background: #FEF2F2; color: #EF4444;")
        reset_btn.clicked.connect(self.reset_template)
        top_layout.addWidget(reset_btn)
        
        save_btn = QPushButton("Save & Apply")
        save_btn.setStyleSheet(f"{btn_style} background: #2C7878; color: white;")
        save_btn.clicked.connect(self.save_template)
        top_layout.addWidget(save_btn)
        
        main_layout.addWidget(top_bar)

        # 2. Split Workspace (Left: Settings, Right: Preview)
        workspace = QHBoxLayout()
        workspace.setSpacing(0)
        
        # --- LEFT PANEL (Settings) ---
        settings_panel = QFrame()
        settings_panel.setFixedWidth(380)
        settings_panel.setStyleSheet("background: white; border-right: 1px solid #E2E8F0;")
        settings_layout = QVBoxLayout(settings_panel)
        settings_layout.setContentsMargins(15, 15, 15, 15)
        settings_layout.setSpacing(20)
        
        # Sections Organizer
        settings_layout.addWidget(QLabel("Layout Organizer", styleSheet="color: #64748B; font-weight: bold; font-size: 11px; text-transform: uppercase;"))
        sections_v = QVBoxLayout()
        sections_v.setSpacing(8)
        sections_v.addWidget(DraggableSection("Store Header", "header"))
        sections_v.addWidget(DraggableSection("Invoice Details", "meta"))
        sections_v.addWidget(DraggableSection("Items Table", "table"))
        sections_v.addWidget(DraggableSection("Financial Summary", "summary"))
        sections_v.addWidget(DraggableSection("Footer Controls", "footer"))
        settings_layout.addLayout(sections_v)
        
        line = QFrame(); line.setFixedHeight(1); line.setStyleSheet("background: #F1F5F9;"); settings_layout.addWidget(line)
        
        settings_layout.addWidget(QLabel("Customization Properties", styleSheet="color: #64748B; font-weight: bold; font-size: 11px; text-transform: uppercase;"))
        
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #F1F5F9; border-radius: 8px; background: white; }
            QTabBar::tab { padding: 10px 12px; background: #F8FAFC; border: 1px solid #E2E8F0; border-bottom: none; border-top-left-radius: 6px; border-top-right-radius: 6px; font-size: 10px; font-weight: bold; color: #64748B; }
            QTabBar::tab:selected { background: white; color: #2C7878; border-bottom: 2px solid white; }
        """)
        
        # Store Details Tab
        store_tab = QWidget()
        store_l = QVBoxLayout(store_tab)
        store_l.setSpacing(5)
        store_l.addWidget(PropertyField("Title", self.current_template['store']['name'], callback=lambda v: self.update_store('name', v)))
        store_l.addWidget(PropertyField("Tagline", self.current_template['store']['tagline'], callback=lambda v: self.update_store('tagline', v)))
        store_l.addWidget(PropertyField("Title Color", self.current_template['store']['color'], "color", callback=lambda v: self.update_store('color', v)))
        store_l.addWidget(PropertyField("Address Color", self.current_template['store']['address_color'], "color", callback=lambda v: self.update_store('address_color', v)))
        store_l.addStretch()
        tabs.addTab(store_tab, "BRANDING")
        
        # Theme/Typography Tab
        theme_tab = QWidget()
        theme_l = QVBoxLayout(theme_tab)
        theme_l.setSpacing(5)
        theme_l.addWidget(PropertyField("Primary Theme", self.current_template['theme']['primary'], "color", callback=lambda v: self.update_theme('primary', v)))
        theme_l.addWidget(PropertyField("Secondary Color", self.current_template['theme']['accent'], "color", callback=lambda v: self.update_theme('accent', v)))
        theme_l.addWidget(PropertyField("Font Family", self.current_template['theme']['font_family'], callback=lambda v: self.update_theme('font_family', v)))
        theme_l.addStretch()
        tabs.addTab(theme_tab, "THEME")
        
        # Elements Tab
        elem_tab = QWidget()
        elem_l = QVBoxLayout(elem_tab)
        elem_l.setSpacing(5)
        elem_l.addWidget(PropertyField("Show QR Code", self.current_template['footer']['show_qr'], "bool", callback=lambda v: self.update_footer('show_qr', v)))
        elem_l.addWidget(PropertyField("Show Bank Details", self.current_template['footer']['show_bank'], "bool", callback=lambda v: self.update_footer('show_bank', v)))
        elem_l.addWidget(PropertyField("Thanks Note", self.current_template['footer']['thanks_text'], callback=lambda v: self.update_footer('thanks_text', v)))
        elem_l.addStretch()
        tabs.addTab(elem_tab, "ELEMENTS")
        
        settings_layout.addWidget(tabs)
        workspace.addWidget(settings_panel)

        # --- RIGHT PANEL (Preview) ---
        preview_panel = QFrame()
        preview_layout = QVBoxLayout(preview_panel)
        preview_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background: #CBD5E1;") # Darker background for paper contrast
        
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignCenter)
        self.scroll_layout.setContentsMargins(50, 50, 50, 50)
        
        self.paper = InvoicePaper()
        self.paper_layout = QVBoxLayout(self.paper)
        self.paper_layout.setContentsMargins(50, 50, 50, 50)
        self.paper_layout.setSpacing(15)
        
        self.scroll_layout.addWidget(self.paper)
        scroll.setWidget(self.scroll_content)
        preview_layout.addWidget(scroll)
        
        workspace.addWidget(preview_panel, 1)

        main_layout.addLayout(workspace)
        
        # Initial Preview Render
        self.render_preview()
        self.apply_zoom()

    def zoom_in(self):
        if self.zoom_level < 1.5:
            self.zoom_level += 0.1
            self.apply_zoom()

    def zoom_out(self):
        if self.zoom_level > 0.4:
            self.zoom_level -= 0.1
            self.apply_zoom()

    def apply_zoom(self):
        scaled_w = int(794 * self.zoom_level)
        scaled_h = int(1123 * self.zoom_level)
        self.paper.setFixedSize(scaled_w, scaled_h)
        self.zoom_lbl.setText(f"{int(self.zoom_level * 100)}%")
        # Force layout refresh
        self.render_preview()

    def update_store(self, key, val):
        self.current_template['store'][key] = val
        self.render_preview()

    def update_theme(self, key, val):
        self.current_template['theme'][key] = val
        self.render_preview()
    
    def update_footer(self, key, val):
        self.current_template['footer'][key] = val
        self.render_preview()

    def render_preview(self):
        # Clear paper layout
        while self.paper_layout.count():
            item = self.paper_layout.takeAt(0)
            if item.widget(): 
                item.widget().deleteLater()
            elif item.layout():
                # Correctly clean up sub-layouts
                self.clear_layout(item.layout())
        
        t = self.current_template
        fs_factor = self.zoom_level # Scale factor for font sizes
        
        # 1. Header
        header = QHBoxLayout()
        logo_v = QVBoxLayout()
        name = QLabel(t['store']['name'])
        name.setFont(QFont(t['theme']['font_family'], int(22 * fs_factor), QFont.Bold))
        name.setStyleSheet(f"color: {t['store']['color']}; letter-spacing: {int(2 * fs_factor)}px;")
        logo_v.addWidget(name)
        
        tagline = QLabel(t['store']['tagline'])
        tagline.setFont(QFont(t['theme']['font_family'], int(8 * fs_factor), QFont.Bold))
        tagline.setStyleSheet(f"color: {t['store']['tagline_color']}; letter-spacing: {int(1 * fs_factor)}px;")
        logo_v.addWidget(tagline)
        header.addLayout(logo_v)
        header.addStretch()
        
        addr = QLabel(t['store']['address'])
        addr.setFont(QFont(t['theme']['font_family'], int(9 * fs_factor)))
        addr.setAlignment(Qt.AlignRight)
        addr.setStyleSheet(f"color: {t['store']['address_color']}; line-height: 1.4;")
        header.addWidget(addr)
        self.paper_layout.addLayout(header)

        # 2. Title
        title_v = QVBoxLayout()
        title_v.setSpacing(int(5 * fs_factor))
        title = QLabel("TAX INVOICE")
        title.setFont(QFont(t['theme']['font_family'], int(18 * fs_factor), QFont.ExtraLight))
        title.setStyleSheet(f"color: {t['theme']['accent']}; letter-spacing: {int(4 * fs_factor)}px;")
        title_v.addWidget(title)
        underline = QFrame(); underline.setFixedHeight(int(1 * fs_factor)); underline.setFixedWidth(int(60 * fs_factor))
        underline.setStyleSheet(f"background: {t['theme']['primary']};"); title_v.addWidget(underline)
        self.paper_layout.addLayout(title_v)

        # 3. Dummy Table (Scaled)
        dummy_items = [("Sample Medicine A", 10.0, 5, 50.0), ("Sample Medicine B", 45.0, 2, 90.0)]
        table = InvoiceTable(dummy_items, template=t)
        # Note: InvoiceTable doesn't support scaling internally, but we can wrap it if needed.
        # For simplicity, we just add it. If scaling is critical, we'd need to modify InvoiceTable.
        self.paper_layout.addWidget(table)

        # 4. Footer
        self.paper_layout.addStretch()
        footer = QHBoxLayout()
        
        if t['footer']['show_qr']:
            qr = QLabel("[QR]")
            qr.setFixedSize(int(50 * fs_factor), int(50 * fs_factor))
            qr.setStyleSheet(f"background: #F1F5F9; color: #94A3B8; font-size: {int(8 * fs_factor)}px;")
            qr.setAlignment(Qt.AlignCenter)
            footer.addWidget(qr)
        
        footer.addStretch()
        
        thanks = QLabel(t['footer']['thanks_text'])
        thanks.setStyleSheet(f"color: {t['footer']['thanks_color']}; font-family: 'Brush Script MT'; font-size: {int(24 * fs_factor)}px;")
        footer.addWidget(thanks)
        
        self.paper_layout.addLayout(footer)

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout(item.layout())

    def save_template(self):
        if TemplateService.save_template(self.current_template):
            QMessageBox.information(self, "Success", "Bill template saved and applied!")
        else:
            QMessageBox.critical(self, "Error", "Failed to save template.")

    def reset_template(self):
        if QMessageBox.question(self, "Reset", "Restore default professional template?") == QMessageBox.Yes:
            self.current_template = copy.deepcopy(TemplateService.DEFAULT_TEMPLATE)
            TemplateService.save_template(self.current_template)
            self.render_preview()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BillDesignerWindow()
    window.show()
    sys.exit(app.exec())
