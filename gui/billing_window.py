import tkinter as tk
from tkinter import ttk
from datetime import datetime

class BillingWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("MediTrack - Point of Sale")
        self.geometry("1100x600")
        self.resizable(False, False)
        self.cart = []
        self.current_bill_no = f"BILL{datetime.now().strftime('%Y%m%d')}001"
        self.create_ui()

    def create_ui(self):
        left_frame = tk.Frame(self, bg="#F5F5F5", width=480)
        left_frame.pack(side="left", fill="y", padx=10, pady=10)

        right_frame = tk.Frame(self, bg="#FFFFFF", width=720)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.create_left_panel(left_frame)

        self.create_right_panel(right_frame)

    def create_left_panel(self, parent):
        customer_frame = tk.Frame(parent, bg="#FFFFFF", relief="raised", bd=1)
        customer_frame.pack(fill="x", pady=10, padx=10)

        tk.Label(customer_frame, text="Customer Details", font=('Inter', 14, 'bold'), bg="#FFFFFF").pack(pady=10)

        tk.Label(customer_frame, text="Mobile Number", font=('Inter', 10), bg="#FFFFFF").pack(anchor="w", padx=10)
        self.mobile_entry = tk.Entry(customer_frame, font=('Inter', 10))
        self.mobile_entry.pack(fill="x", padx=10, pady=5)

        tk.Label(customer_frame, text="Name", font=('Inter', 10), bg="#FFFFFF").pack(anchor="w", padx=10)
        self.name_entry = tk.Entry(customer_frame, font=('Inter', 10))
        self.name_entry.pack(fill="x", padx=10, pady=5)

        tk.Label(customer_frame, text="Address", font=('Inter', 10), bg="#FFFFFF").pack(anchor="w", padx=10)
        self.address_entry = tk.Entry(customer_frame, font=('Inter', 10))
        self.address_entry.pack(fill="x", padx=10, pady=5)

        search_frame = tk.Frame(parent, bg="#FFFFFF", relief="raised", bd=1)
        search_frame.pack(fill="both", expand=True, pady=10, padx=10)

        tk.Label(search_frame, text="Product Search", font=('Inter', 14, 'bold'), bg="#FFFFFF").pack(pady=10)

        self.search_entry = tk.Entry(search_frame, font=('Inter', 10))
        self.search_entry.pack(fill="x", padx=10, pady=5)
        self.search_entry.bind("<KeyRelease>", self.search_products)

        columns = ("Name", "Price", "Stock")
        self.product_tree = ttk.Treeview(search_frame, columns=columns, show="headings", height=15)
        for col in columns:
            self.product_tree.heading(col, text=col)
            self.product_tree.column(col, width=120, anchor="center")

        self.products = [
            ("Paracetamol", "10.00", "50"),
            ("Ibuprofen", "15.00", "30"),
            ("Vitamin C", "20.00", "100"),
            ("Aspirin", "5.00", "25")
        ]
        for prod in self.products:
            self.product_tree.insert("", "end", values=prod)

        self.product_tree.pack(fill="both", expand=True, padx=10, pady=5)
        self.product_tree.bind("<Double-1>", self.add_to_cart)

    def create_right_panel(self, parent):
        header_frame = tk.Frame(parent, bg="#FFFFFF")
        header_frame.pack(fill="x", pady=10)

        tk.Label(header_frame, text=f"Bill No: {self.current_bill_no}", font=('Inter', 12, 'bold'), bg="#FFFFFF").pack(side="left", padx=10)
        tk.Label(header_frame, text=f"Date: {datetime.now().strftime('%Y-%m-%d')}", font=('Inter', 12), bg="#FFFFFF").pack(side="right", padx=10)

        cart_frame = tk.Frame(parent, bg="#FFFFFF", relief="raised", bd=1)
        cart_frame.pack(fill="both", expand=True, pady=10)

        tk.Label(cart_frame, text="Shopping Cart", font=('Inter', 14, 'bold'), bg="#FFFFFF").pack(pady=10)

        columns = ("Item", "Medicine", "Price", "Qty", "Total")
        self.cart_tree = ttk.Treeview(cart_frame, columns=columns, show="headings", height=10)
        for col in columns:
            self.cart_tree.heading(col, text=col)
            self.cart_tree.column(col, width=120, anchor="center")

        self.cart_tree.pack(fill="both", expand=True, padx=10, pady=5)

        totals_frame = tk.Frame(cart_frame, bg="#FFFFFF")
        totals_frame.pack(fill="x", padx=10, pady=10)

        self.subtotal_label = tk.Label(totals_frame, text="Subtotal: Rs. 0.00", font=('Inter', 12), bg="#FFFFFF")
        self.subtotal_label.pack(anchor="w")

        tk.Label(totals_frame, text="Discount (%)", font=('Inter', 10), bg="#FFFFFF").pack(anchor="w", pady=5)
        self.discount_entry = tk.Entry(totals_frame, font=('Inter', 10), width=10)
        self.discount_entry.pack(anchor="w", pady=5)
        self.discount_entry.bind("<KeyRelease>", self.update_totals)

        self.gst_label = tk.Label(totals_frame, text="GST: Rs. 0.00", font=('Inter', 12), bg="#FFFFFF")
        self.gst_label.pack(anchor="w")

        self.total_label = tk.Label(totals_frame, text="Grand Total: Rs. 0.00", font=('Inter', 16, 'bold'), fg="#1976D2", bg="#FFFFFF")
        self.total_label.pack(anchor="w", pady=10)

        payment_frame = tk.Frame(parent, bg="#FFFFFF")
        payment_frame.pack(fill="x", pady=10)

        tk.Label(payment_frame, text="Payment Method", font=('Inter', 12), bg="#FFFFFF").pack(side="left", padx=10)
        self.payment_var = tk.StringVar(value="Cash")
        tk.OptionMenu(payment_frame, self.payment_var, "Cash", "Card", "UPI").pack(side="left", padx=10)

        tk.Button(payment_frame, text="Generate Bill", font=('Inter', 14, 'bold'), bg="#4CAF50", fg="#FFFFFF", padx=20, command=self.generate_bill).pack(side="right", padx=10)

    def search_products(self, event):
        query = self.search_entry.get().lower()
        self.product_tree.delete(*self.product_tree.get_children())
        for prod in self.products:
            if query in prod[0].lower():
                self.product_tree.insert("", "end", values=prod)

    def add_to_cart(self, event):
        selected = self.product_tree.selection()
        if selected:
            item = self.product_tree.item(selected[0], "values")
            name, price, stock = item
            qty = 1  # Default qty
            total = float(price) * qty
            self.cart.append((name, price, str(qty), f"{total:.2f}"))
            self.update_cart()

    def update_cart(self):
        self.cart_tree.delete(*self.cart_tree.get_children())
        subtotal = 0
        for i, item in enumerate(self.cart, 1):
            self.cart_tree.insert("", "end", values=(i, *item))
            subtotal += float(item[3])
        discount = float(self.discount_entry.get() or 0) / 100
        discounted = subtotal * (1 - discount)
        gst = discounted * 0.12
        total = discounted + gst
        self.subtotal_label.config(text=f"Subtotal: Rs.{subtotal:.2f}")
        self.gst_label.config(text=f"GST: Rs.{gst:.2f}")
        self.total_label.config(text=f"Grand Total: Rs.{total:.2f}")

    def generate_bill(self):
        bill_data = {
            'bill_no': self.current_bill_no,
            'customer_name': self.name_entry.get(),
            'customer_phone': self.mobile_entry.get(),
            'customer_address': self.address_entry.get(),
            'items': [self.cart[i] for i in range(len(self.cart))],
            'subtotal': self.extract_value(self.subtotal_label.cget("text")),
            'discount': float(self.discount_entry.get() or 0),
            'gst': self.extract_value(self.gst_label.cget("text")),
            'total': self.extract_value(self.total_label.cget("text"))
        }

        from gui.bill_preview_window import BillPreviewWindow
        BillPreviewWindow(self, bill_data)

    def extract_value(self, text):
        if "Rs." in text:
            return float(text.split("Rs.")[1].strip())
        else:
            return float(text.strip())

    def update_totals(self, event):
        self.update_cart()
