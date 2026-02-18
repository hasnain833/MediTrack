import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

class StockReportWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("MediTrack - Stock Report")
        self.geometry("1200x700")
        self.resizable(False, False)
        self.current_filter = "All Stock"
        self.create_ui()
        self.load_data()

    def create_ui(self):
        # Top tabs
        top_frame = tk.Frame(self, bg="#FFFFFF", height=50, relief="raised", bd=1)
        top_frame.pack(fill="x", padx=10, pady=10)

        filters = ["All Stock", "Low Stock", "Expiring Soon", "Out of Stock"]
        self.filter_buttons = {}
        for i, filt in enumerate(filters):
            btn = tk.Button(top_frame, text=filt, font=('Inter', 12, 'bold'), bg="#E0E0E0" if filt != self.current_filter else "#2196F3",
                            fg="#FFFFFF", relief="flat", padx=20, command=lambda f=filt: self.set_filter(f))
            btn.pack(side="left", padx=10, pady=10)
            self.filter_buttons[filt] = btn

        # Main frame
        main_frame = tk.Frame(self, bg="#FFFFFF")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Table
        table_frame = tk.Frame(main_frame, bg="#FFFFFF", relief="raised", bd=1)
        table_frame.pack(side="left", fill="both", expand=True, padx=10)

        columns = ("Medicine", "Batch", "Expiry", "Current Stock", "Reorder Level", "Action")
        self.stock_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
        for col in columns:
            self.stock_tree.heading(col, text=col)
            self.stock_tree.column(col, width=150, anchor="center")

        # Sample stock data
        self.stock_data = [
            ("Paracetamol", "B001", "2026-05-01", "50", "20", "Edit"),
            ("Ibuprofen", "B002", "2025-12-01", "5", "10", "Edit"),
            ("Expired Med", "B003", "2024-01-01", "20", "15", "Edit"),
            ("Vitamin C", "B004", "2027-03-15", "0", "25", "Edit"),
            ("Aspirin", "B005", "2026-08-20", "15", "10", "Edit"),
            ("Antibiotic", "B006", "2025-11-10", "8", "12", "Edit")
        ]

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.stock_tree.yview)
        self.stock_tree.configure(yscrollcommand=scrollbar.set)
        self.stock_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Right panel
        right_frame = tk.Frame(main_frame, bg="#FFFFFF", width=300, relief="raised", bd=1)
        right_frame.pack(side="right", fill="y", padx=10)
        right_frame.pack_propagate(False)

        tk.Label(right_frame, text="Summary", font=('Inter', 16, 'bold'), bg="#FFFFFF").pack(pady=20)

        self.total_value_label = tk.Label(right_frame, text="Total Value: Rs. 456,780", font=('Inter', 12), bg="#FFFFFF")
        self.total_value_label.pack(pady=10)

        self.low_stock_label = tk.Label(right_frame, text="Low Stock Items: 23", font=('Inter', 12), bg="#FFFFFF")
        self.low_stock_label.pack(pady=10)

        self.expiring_label = tk.Label(right_frame, text="Expiring in 30 days: 45", font=('Inter', 12), bg="#FFFFFF")
        self.expiring_label.pack(pady=10)

        # Bottom export
        bottom_frame = tk.Frame(self, bg="#FFFFFF", height=50, relief="raised", bd=1)
        bottom_frame.pack(fill="x", padx=10, pady=10)
        tk.Button(bottom_frame, text="Export PDF", font=('Inter', 12, 'bold'), bg="#FF5722", fg="#FFFFFF", relief="flat", padx=20, command=self.export_pdf).pack(side="right", padx=10)
        tk.Button(bottom_frame, text="Export Excel", font=('Inter', 12, 'bold'), bg="#4CAF50", fg="#FFFFFF", relief="flat", padx=20, command=self.export_excel).pack(side="right", padx=10)

    def set_filter(self, filt):
        self.current_filter = filt
        for f, btn in self.filter_buttons.items():
            btn.config(bg="#E0E0E0" if f != filt else "#2196F3")
        self.load_data()

    def load_data(self):
        for item in self.stock_tree.get_children():
            self.stock_tree.delete(item)

        filtered_data = []
        today = datetime.now()
        for item in self.stock_data:
            medicine, batch, expiry_str, stock_str, reorder_str, action = item
            stock = int(stock_str)
            reorder = int(reorder_str)
            try:
                expiry = datetime.strptime(expiry_str, "%Y-%m-%d")
                expired = expiry < today
                expiring_soon = (expiry - today).days <= 30 and not expired
            except:
                expired = False
                expiring_soon = False

            if self.current_filter == "All Stock":
                filtered_data.append((medicine, batch, expiry_str, stock_str, reorder_str, action, expired, expiring_soon, stock < reorder))
            elif self.current_filter == "Low Stock" and stock < reorder:
                filtered_data.append((medicine, batch, expiry_str, stock_str, reorder_str, action, expired, expiring_soon, True))
            elif self.current_filter == "Expiring Soon" and expiring_soon:
                filtered_data.append((medicine, batch, expiry_str, stock_str, reorder_str, action, expired, expiring_soon, stock < reorder))
            elif self.current_filter == "Out of Stock" and stock == 0:
                filtered_data.append((medicine, batch, expiry_str, stock_str, reorder_str, action, expired, expiring_soon, stock < reorder))

        for item in filtered_data:
            medicine, batch, expiry_str, stock_str, reorder_str, action, expired, expiring_soon, low_stock = item
            tag = ""
            if expired:
                tag = "expired"
            elif low_stock:
                tag = "low_stock"
            else:
                tag = "normal"
            self.stock_tree.insert("", "end", values=(medicine, batch, expiry_str, stock_str, reorder_str, action), tags=(tag,))

        self.stock_tree.tag_configure("expired", background="#FFEBEE")
        self.stock_tree.tag_configure("low_stock", background="#FFF9C4")
        self.stock_tree.tag_configure("normal", background="#E8F5E8")

        # Update summaries (dummy updates)
        low_stock_count = sum(1 for item in filtered_data if item[8])
        expiring_count = sum(1 for item in filtered_data if item[7])
        self.low_stock_label.config(text=f"Low Stock Items: {low_stock_count}")
        self.expiring_label.config(text=f"Expiring in 30 days: {expiring_count}")

    def export_pdf(self):
        tk.messagebox.showinfo("Export", "Exporting stock report to PDF...")

    def export_excel(self):
        tk.messagebox.showinfo("Export", "Exporting stock report to Excel...")
