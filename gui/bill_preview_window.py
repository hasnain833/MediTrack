import tkinter as tk
from tkinter import ttk
from datetime import datetime

class BillPreviewWindow(tk.Toplevel):
    def __init__(self, master, bill_data):
        super().__init__(master)
        self.title("Bill Preview")
        self.geometry("800x1000")   
        self.resizable(False, False)
        self.create_ui(bill_data)

    def create_ui(self, bill_data):
        self.canvas = tk.Canvas(self, bg="#FFFFFF")
        self.canvas.pack(fill="both", expand=True)

        self.canvas.create_text(400, 50, text="D. Chemist Medical Store", font=('Inter', 24, 'bold'), fill="#1976D2")
        self.canvas.create_text(400, 80, text="123 Pharmacy Street, Karachi, Pakistan - 74000", font=('Inter', 12), fill="#424242")
        self.canvas.create_text(400, 100, text="Phone: +92-321-1234567 | NTN: NTN123456789", font=('Inter', 12), fill="#424242")

        self.canvas.create_text(400, 140, text="Tax Invoice", font=('Inter', 18, 'bold'), fill="#1976D2")
        self.canvas.create_text(100, 170, text=f"Bill No: {bill_data.get('bill_no', 'BILL001')}", anchor="w", font=('Inter', 12), fill="#424242")
        self.canvas.create_text(100, 190, text=f"Date: {datetime.now().strftime('%Y-%m-%d')}", anchor="w", font=('Inter', 12), fill="#424242")


        self.canvas.create_text(100, 220, text="Customer Details:", anchor="w", font=('Inter', 14, 'bold'), fill="#1976D2")
        self.canvas.create_text(100, 240, text=f"Name: {bill_data.get('customer_name', 'John Doe')}", anchor="w", font=('Inter', 12), fill="#424242")
        self.canvas.create_text(100, 260, text=f"Phone: {bill_data.get('customer_phone', '1234567890')}", anchor="w", font=('Inter', 12), fill="#424242")
        self.canvas.create_text(100, 280, text=f"Address: {bill_data.get('customer_address', '123 Main St')}", anchor="w", font=('Inter', 12), fill="#424242")

        self.canvas.create_text(100, 320, text="Items:", anchor="w", font=('Inter', 14, 'bold'), fill="#1976D2")

        headers = ["Sl No", "Medicine Name", "Batch", "Qty", "Price", "Amount"]
        y = 340
        for i, header in enumerate(headers):
            x = 100 + i * 100
            self.canvas.create_text(x, y, text=header, font=('Inter', 10, 'bold'), fill="#424242")

        items = bill_data.get('items', [
            ("1", "Paracetamol", "B001", "2", "10.00", "20.00"),
            ("2", "Ibuprofen", "B002", "1", "15.00", "15.00")
        ])
        y_start = 360
        for i, item in enumerate(items):
            y = y_start + i * 20
            for j, cell in enumerate(item):
                x = 100 + j * 100
                self.canvas.create_text(x, y, text=cell, font=('Inter', 10), fill="#424242")

        y_totals = y_start + len(items) * 20 + 20
        subtotal = bill_data.get('subtotal', 35.00)
        discount = bill_data.get('discount', 0.00)
        gst = bill_data.get('gst', 5.60)
        total = bill_data.get('total', 40.60)

        self.canvas.create_text(500, y_totals, text=f"Subtotal: Rs.{subtotal:.2f}", anchor="e", font=('Inter', 12), fill="#424242")
        self.canvas.create_text(500, y_totals + 20, text=f"Discount: Rs.{discount:.2f}", anchor="e", font=('Inter', 12), fill="#424242")
        self.canvas.create_text(500, y_totals + 40, text=f"GST: Rs.{gst:.2f}", anchor="e", font=('Inter', 12), fill="#424242")
        self.canvas.create_text(500, y_totals + 60, text=f"Grand Total: Rs.{total:.2f}", anchor="e", font=('Inter', 14, 'bold'), fill="#1976D2")

        self.canvas.create_text(100, y_totals + 80, text=f"Total in Words: Forty Rupees and Sixty Paise Only", anchor="w", font=('Inter', 12), fill="#424242")

        y_footer = y_totals + 120
        self.canvas.create_text(400, y_footer, text="Thank you, visit again!", font=('Inter', 12), fill="#1976D2")
        self.canvas.create_text(400, y_footer + 20, text="[QR Code for FBR Compliance - Placeholder]", font=('Inter', 10), fill="#9E9E9E")

        print_btn = tk.Button(self, text="Print Bill", font=('Inter', 12, 'bold'), bg="#4CAF50", fg="#FFFFFF", relief="flat", command=self.print_bill)
    def print_bill(self):
        # Placeholder for printing functionality
        tk.messagebox.showinfo("Print", "Printing bill... (Placeholder)")
