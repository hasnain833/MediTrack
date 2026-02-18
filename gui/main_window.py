import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import math

class MainWindow:
    def __init__(self, current_user="admin"):
        self.root = tk.Tk()
        self.root.title("MediTrack - Medical Store Management")
        self.root.geometry("1100x600")
        self.root.resizable(False, False)
        self.current_user = current_user

        try:
            self.title_font = ('Inter', 18, 'bold')
            self.header_font = ('Inter', 12)
            self.stat_font = ('Inter', 24, 'bold')
            self.label_font = ('Inter', 10)
            self.button_font = ('Inter', 12, 'bold')
        except:
            self.title_font = ('Helvetica', 18, 'bold')
            self.header_font = ('Helvetica', 12)
            self.stat_font = ('Helvetica', 24, 'bold')
            self.label_font = ('Helvetica', 10)
            self.button_font = ('Helvetica', 12, 'bold')

        self.create_ui()

        self.check_low_stock_alert()

    def check_low_stock_alert(self):
        low_stock = [
            {'name': 'Ibuprofen', 'qty': 5, 'reorder': 10},
            {'name': 'Expired Med', 'qty': 2, 'reorder': 15}
        ]

        # Check for low stock alerts
        if low_stock:
            from gui.low_stock_alert_window import LowStockAlertWindow
            LowStockAlertWindow(self.root, low_stock)

    def create_ui(self):
        self.root.config(bg="#E3F2FD")

        # Canvas for UI elements
        self.canvas = tk.Canvas(self.root, bg="#E3F2FD", width=1100, height=600, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Top header bar
        self.create_header()

        # Stats cards
        self.create_stats_cards()

        # Quick actions and recent bills
        self.create_quick_actions()
        self.create_recent_bills()

        # Bottom status bar
        self.create_status_bar()

    def create_header(self):
        # Header background
        self.canvas.create_rectangle(0, 0, 1100, 60, fill="#FFFFFF", outline="#E0E0E0", width=1)

        # Store name
        self.canvas.create_text(20, 30, text="D. Chemist", anchor="w", font=self.title_font, fill="#1976D2")

        # User profile section
        self.canvas.create_text(1050, 20, text="Admin", anchor="e", font=self.header_font, fill="#424242")
        self.canvas.create_oval(1070, 10, 1090, 30, fill="#1976D2", outline="")
        self.canvas.create_text(1080, 20, text="A", font=self.header_font, fill="#FFFFFF")
        logout_btn = tk.Button(self.root, text="Logout", font=self.header_font, bg="#F44336", fg="#FFFFFF",
                               relief="flat", bd=0, command=self.logout)
        self.canvas.create_window(1100, 20, window=logout_btn, width=60, height=25, anchor="w")

    def create_stats_cards(self):
        stats = [
            {"label": "Today's Sale", "value": "Rs.12,450"},
            {"label": "Total Medicines", "value": "1,234"},
            {"label": "Low Stock Items", "value": "23"},
            {"label": "Expiring Soon", "value": "45"}
        ]
        start_x = 20
        y = 80
        for i, stat in enumerate(stats):
            x = start_x + i * 270
            self.create_stat_card(x, y, stat)

    def create_stat_card(self, x, y, stat):
        width, height = 250, 100
        self.canvas.create_rectangle(x+3, y+3, x+width+3, y+height+3, fill="#D0D0D0", outline="")
        self.canvas.create_rectangle(x, y, x+width, y+height, fill="#FFFFFF", outline="#E0E0E0", width=1)
        self.canvas.create_text(x + 125, y + 25, text=stat["value"], font=self.stat_font, fill="#1976D2", anchor="center")
        self.canvas.create_text(x + 125, y + 50, text=stat["label"], font=self.label_font, fill="#424242", anchor="center")

    def create_quick_actions(self):
        self.canvas.create_text(50, 220, text="Quick Actions", anchor="w", font=self.title_font, fill="#1976D2")
        actions = [
            {"text": "New Bill", "color": "#4CAF50"},
            {"text": "Add Medicine", "color": "#2196F3"},
            {"text": "Add Customer", "color": "#FF9800"},
            {"text": "Stock Report", "color": "#9C27B0"}
        ]
        y_start = 250
        for i, action in enumerate(actions):
            y = y_start + i * 80
            self.create_action_button(50, y, action)

    def create_action_button(self, x, y, action):
        width, height = 250, 60
        self.canvas.create_rectangle(x+3, y+3, x+width+3, y+height+3, fill="#D0D0D0", outline="")
        self.canvas.create_rectangle(x, y, x+width, y+height, fill=action["color"], outline="")
        self.canvas.create_text(x + width/2, y + height/2, text=action["text"], font=self.button_font, fill="#FFFFFF")
        self.canvas.tag_bind(self.canvas.create_rectangle(x, y, x+width, y+height, fill="", outline=""), "<Button-1>",
                             lambda e, t=action["text"]: self.perform_action(t))

    def create_recent_bills(self):
        self.canvas.create_text(450, 220, text="Recent Bills", anchor="w", font=self.title_font, fill="#1976D2")
        headers = ["Bill No", "Date", "Customer", "Amount"]
        x_start = 450
        y = 250
        col_width = 150
        for i, header in enumerate(headers):
            x = x_start + i * col_width
            self.canvas.create_text(x + col_width/2, y, text=header, font=self.header_font, fill="#424242")
        bills = [
            ["001", "2026-02-18", "John Doe", "Rs. 500"],
            ["002", "2026-02-18", "Jane Smith", "Rs. 750"],
            ["003", "2026-02-17", "Bob Johnson", "Rs. 300"]
        ]
        for i, bill in enumerate(bills):
            row_y = y + 30 + i * 25
            for j, cell in enumerate(bill):
                x = x_start + j * col_width
                self.canvas.create_text(x + col_width/2, row_y, text=cell, font=self.label_font, fill="#424242")

    def perform_action(self, action):
        if action == "New Bill":
            from gui.billing_window import BillingWindow
            BillingWindow(self.root)
        elif action == "Add Medicine":
            from gui.inventory_window import InventoryWindow
            InventoryWindow(self.root)
        elif action == "Add Customer":
            from gui.customer_window import CustomerWindow
            CustomerWindow(self.root)
        elif action == "Stock Report":
            from gui.reports_window import ReportsWindow
            ReportsWindow(self.root)
        elif action == "Settings":
            from gui.settings_window import SettingsWindow
            SettingsWindow(self.root)
        elif action == "Inventory":
            from gui.inventory_window import InventoryWindow
            InventoryWindow(self.root)
        else:
            messagebox.showinfo("Action", f"Performing {action}")

    def logout(self):
        self.root.destroy()
        from gui.login_window import LoginWindow
        LoginWindow().run()

    def run(self):
        self.root.mainloop()
