import sys
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QApplication, 
                             QGraphicsDropShadowEffect, QTableWidget, QTableWidgetItem,
                             QHeaderView, QComboBox, QSpacerItem, QSizePolicy)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import (QFont, QColor, QIcon, QPixmap)

class UserCard(QFrame):
    """Horizontal card for user list"""
    def __init__(self, name, role, status, selected=False, parent=None):
        super().__init__(parent)
        self.setFixedSize(160, 100)
        self.selected = selected
        self.status = status
        self.init_ui(name, role)

    def init_ui(self, name, role):
        border_color = "#2C7878" if self.selected else "#E2E8F0"
        self.setStyleSheet(f"""
            QFrame {{
                background: white;
                border: 2px solid {border_color};
                border-radius: 12px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(5)

        # Avatar and Status
        top_h = QHBoxLayout()
        avatar = QLabel("👤")
        avatar.setFont(QFont("Inter", 14))
        avatar.setStyleSheet("border: none; background: #F1F5F9; border-radius: 15px; padding: 5px;")
        top_h.addWidget(avatar)
        top_h.addStretch()
        
        status_dot = QFrame()
        status_dot.setFixedSize(8, 8)
        dot_color = "#22C55E" if self.status == "Active" else "#94A3B8"
        status_dot.setStyleSheet(f"background: {dot_color}; border-radius: 4px; border: none;")
        top_h.addWidget(status_dot)
        layout.addLayout(top_h)

        # Name and Role
        name_lbl = QLabel(name)
        name_lbl.setFont(QFont("Inter", 10, QFont.Bold))
        name_lbl.setStyleSheet("color: #0F172A; border: none;")
        layout.addWidget(name_lbl)

        role_lbl = QLabel(role)
        role_lbl.setFont(QFont("Inter", 8))
        role_lbl.setStyleSheet("color: #64748B; border: none;")
        layout.addWidget(role_lbl)

class PermissionMatrix(QTableWidget):
    """Permission selection grid"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.modules = ["Inventory", "Users", "Medicine", "Customers", "Billing", "Reports"]
        self.actions = ["View", "Add", "Edit", "Delete", "Approve"]
        self.init_ui()

    def init_ui(self):
        self.setRowCount(len(self.modules))
        self.setColumnCount(len(self.actions))
        self.setHorizontalHeaderLabels(self.actions)
        self.setVerticalHeaderLabels(self.modules)
        
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.verticalHeader().setDefaultSectionSize(50)
        
        self.setStyleSheet("""
            QTableWidget {
                background: white;
                border: 1px solid #E2E8F0;
                gridline-color: #F1F5F9;
                border-radius: 12px;
            }
            QHeaderView::section {
                background: #F8FAFC;
                padding: 10px;
                border: none;
                border-bottom: 2px solid #E2E8F0;
                font-weight: bold;
                color: #475569;
            }
        """)

        for r in range(len(self.modules)):
            for c in range(len(self.actions)):
                item = QTableWidgetItem()
                # Default logic: Admin (selected by default in mock) has checks
                allowed = True if r < 4 else False # Mock logic
                icon = "✓" if allowed else "−"
                color = "#2C7878" if allowed else "#94A3B8"
                item.setText(icon)
                item.setTextAlignment(Qt.AlignCenter)
                item.setFont(QFont("Inter", 12, QFont.Bold))
                item.setForeground(QColor(color))
                item.setToolTip(f"{self.actions[c]} {self.modules[r]}")
                self.setItem(r, c, item)

class AuditLog(QFrame):
    """Activity tracking sidebar"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(300)
        self.setStyleSheet("background: #F8FAFC; border-left: 1px solid #E2E8F0;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 25, 20, 20)
        
        title = QLabel("Activity Audit Log")
        title.setFont(QFont("Inter", 12, QFont.Bold))
        title.setStyleSheet("color: #0F172A; margin-bottom: 10px;")
        layout.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")
        
        self.content = QWidget()
        self.vbox = QVBoxLayout(self.content)
        self.vbox.setSpacing(15)
        self.vbox.setAlignment(Qt.AlignTop)
        
        logs = [
            ("12:45 PM", "Admin added 'Panadol'", "192.168.1.1"),
            ("12:10 PM", "Cashier logged in", "192.168.1.14"),
            ("Yesterday", "Permission update: User #12", "192.168.0.5"),
            ("Yesterday", "Inventory CSV Export", "192.168.1.1")
        ]

        for time, action, ip in logs:
            log_item = QFrame()
            log_item.setStyleSheet("background: white; border-radius: 8px; border: 1px solid #E2E8F0;")
            lv = QVBoxLayout(log_item)
            tl = QLabel(time); tl.setFont(QFont("Inter", 7, QFont.Bold)); tl.setStyleSheet("color: #94A3B8;")
            al = QLabel(action); al.setFont(QFont("Inter", 9)); al.setStyleSheet("color: #1E293B;")
            ipl = QLabel(ip); ipl.setFont(QFont("Inter", 7)); ipl.setStyleSheet("color: #64748B;")
            lv.addWidget(tl); lv.addWidget(al); lv.addWidget(ipl)
            self.vbox.addWidget(log_item)

        scroll.setWidget(self.content)
        layout.addWidget(scroll)

class UserManagerWindow(QWidget):
    def __init__(self, master=None):
        super().__init__(None, Qt.Window)
        self.setWindowTitle("User & Permission Console - MediTrack")
        self.resize(1100, 750)
        self.setStyleSheet("background: white;")
        self.init_ui()

    def init_ui(self):
        main_h = QHBoxLayout(self)
        main_h.setContentsMargins(0, 0, 0, 0)
        main_h.setSpacing(0)

        # Left Panel (User Management)
        left_v = QVBoxLayout()
        left_v.setContentsMargins(30, 30, 30, 30)
        left_v.setSpacing(25)

        # Header
        header = QHBoxLayout()
        title_v = QVBoxLayout()
        tl = QLabel("User Management")
        tl.setFont(QFont("Inter", 22, QFont.Bold))
        sl = QLabel("Manage workforce roles and module level accessibility.")
        sl.setStyleSheet("color: #64748B;")
        title_v.addWidget(tl); title_v.addWidget(sl)
        header.addLayout(title_v)
        header.addStretch()
        
        add_btn = QPushButton("+ Add User")
        add_btn.setFixedSize(140, 45)
        add_btn.setStyleSheet("""
            QPushButton { 
                background: #2C7878; color: white; border-radius: 8px; font-weight: bold; 
            }
            QPushButton:hover { background: #1E5050; }
        """)
        header.addWidget(add_btn)
        left_v.addLayout(header)

        # User Cards List
        card_scroll = QScrollArea()
        card_scroll.setWidgetResizable(True)
        card_scroll.setFixedHeight(130)
        card_scroll.setStyleSheet("border: none;")
        
        card_content = QWidget()
        card_h = QHBoxLayout(card_content)
        card_h.setContentsMargins(0, 5, 0, 5)
        card_h.setSpacing(15)
        
        try:
            from database.models import User
            db_users = User.find_all()
        except Exception as e:
            print(f"Error fetching users: {e}")
            db_users = []
        
        for u in db_users:
            # Map role, status to UI requirements
            status = u.get('status', 'Active').capitalize()
            role = u.get('role', 'Staff').capitalize()
            full_name = u.get('full_name') or u.get('username')
            
            card_h.addWidget(UserCard(full_name, role, status, False))
        
        card_h.addStretch()
        
        card_scroll.setWidget(card_content)
        left_v.addWidget(card_scroll)

        # Permission Section
        perm_header = QHBoxLayout()
        ptl = QLabel("Permission Matrix")
        ptl.setFont(QFont("Inter", 14, QFont.Bold))
        perm_header.addWidget(ptl)
        perm_header.addStretch()
        
        role_select = QComboBox()
        role_select.addItems(["Admin Template", "Cashier Template", "Custom..."])
        role_select.setFixedSize(180, 40)
        role_select.setStyleSheet("""
            QComboBox { 
                background: #F1F5F9; border: 1px solid #E2E8F0; border-radius: 8px; padding-left: 10px;
            }
        """)
        perm_header.addWidget(role_select)
        left_v.addLayout(perm_header)

        self.matrix = PermissionMatrix()
        left_v.addWidget(self.matrix)

        main_h.addLayout(left_v, 1)

        # Right Panel (Audit Log)
        self.audit = AuditLog()
        main_h.addWidget(self.audit)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = UserManagerWindow()
    win.show()
    sys.exit(app.exec())
