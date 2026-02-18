import tkinter as tk
from tkinter import ttk
from datetime import datetime
import math

class DailySalesReportWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("MediTrack - Daily Sales Report")
        self.geometry("1400x900")
        self.resizable(False, False)
        self.create_ui()

    def create_ui(self):
        # Top frame
        top_frame = tk.Frame(self, bg="#FFFFFF", height=100, relief="raised", bd=1)
        top_frame.pack(fill="x", padx=10, pady=10)

        # Date
        tk.Label(top_frame, text="Date: February 18, 2026", font=('Inter', 16, 'bold'), bg="#FFFFFF").pack(side="left", padx=20, pady=20)

        # Export buttons
        export_frame = tk.Frame(top_frame, bg="#FFFFFF")
        export_frame.pack(side="right", padx=20, pady=20)
        tk.Button(export_frame, text="Export PDF", font=('Inter', 10, 'bold'), bg="#FF5722", fg="#FFFFFF", relief="flat", padx=10, command=self.export_pdf).pack(side="left", padx=5)
        tk.Button(export_frame, text="Export Excel", font=('Inter', 10, 'bold'), bg="#4CAF50", fg="#FFFFFF", relief="flat", padx=10, command=self.export_excel).pack(side="left", padx=5)

        # Summary cards
        summary_frame = tk.Frame(self, bg="#FFFFFF")
        summary_frame.pack(fill="x", padx=10, pady=10)

        summaries = [
            {"label": "Total Bills", "value": "45"},
            {"label": "Total Sales", "value": "Rs. 28,450"},
            {"label": "Average Bill Value", "value": "Rs. 632"},
            {"label": "Top Payment Method", "value": "UPI"}
        ]

        for i, summary in enumerate(summaries):
            self.create_summary_card(summary_frame, i, summary)

        # Charts frame
        charts_frame = tk.Frame(self, bg="#FFFFFF")
        charts_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Bar chart
        bar_frame = tk.Frame(charts_frame, bg="#FFFFFF", relief="raised", bd=1)
        bar_frame.pack(side="left", fill="both", expand=True, padx=5)
        tk.Label(bar_frame, text="Hourly Sales", font=('Inter', 14, 'bold'), bg="#FFFFFF").pack(pady=10)
        self.bar_canvas = tk.Canvas(bar_frame, bg="#FFFFFF", height=300)
        self.bar_canvas.pack(fill="both", expand=True, padx=20, pady=10)
        self.draw_bar_chart()

        # Pie chart
        pie_frame = tk.Frame(charts_frame, bg="#FFFFFF", relief="raised", bd=1)
        pie_frame.pack(side="right", fill="both", expand=True, padx=5)
        tk.Label(pie_frame, text="Payment Method Split", font=('Inter', 14, 'bold'), bg="#FFFFFF").pack(pady=10)
        self.pie_canvas = tk.Canvas(pie_frame, bg="#FFFFFF", height=300)
        self.pie_canvas.pack(fill="both", expand=True, padx=20, pady=10)
        self.draw_pie_chart()

        # Sales table
        table_frame = tk.Frame(self, bg="#FFFFFF", relief="raised", bd=1)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(table_frame, text="Detailed Sales", font=('Inter', 14, 'bold'), bg="#FFFFFF").pack(pady=10)

        columns = ("Bill No", "Time", "Customer", "Items", "Amount", "Payment")
        self.sales_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        for col in columns:
            self.sales_tree.heading(col, text=col)
            self.sales_tree.column(col, width=150, anchor="center")

        # Sample sales data
        sales_data = [
            ("001", "09:00", "John Doe", "Paracetamol", "Rs. 100", "Cash"),
            ("002", "10:30", "Jane Smith", "Ibuprofen", "Rs. 150", "UPI"),
            ("003", "11:15", "Bob Johnson", "Vitamin C", "Rs. 200", "Card"),
            ("004", "12:00", "Alice Brown", "Aspirin", "Rs. 50", "Cash"),
            ("005", "13:45", "Charlie White", "Antibiotic", "Rs. 300", "UPI")
        ]
        for item in sales_data:
            self.sales_tree.insert("", "end", values=item)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.sales_tree.yview)
        self.sales_tree.configure(yscrollcommand=scrollbar.set)
        self.sales_tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")

    def create_summary_card(self, parent, col, summary):
        card = tk.Frame(parent, bg="#F5F5F5", relief="raised", bd=2, width=300, height=80)
        card.grid(row=0, column=col, padx=20, pady=10, sticky="ew")
        card.pack_propagate(False)

        tk.Label(card, text=summary["value"], font=('Inter', 18, 'bold'), bg="#F5F5F5", fg="#1976D2").pack(pady=5)
        tk.Label(card, text=summary["label"], font=('Inter', 10), bg="#F5F5F5").pack()

    def draw_bar_chart(self):
        # Sample hourly sales data
        hours = ["9AM", "10AM", "11AM", "12PM", "1PM", "2PM", "3PM", "4PM", "5PM", "6PM", "7PM", "8PM", "9PM"]
        sales = [500, 700, 600, 800, 900, 750, 650, 850, 950, 1000, 900, 800, 600]
        max_sale = max(sales)
        bar_width = 30
        spacing = 10
        start_x = 50

        for i, (hour, sale) in enumerate(zip(hours, sales)):
            x1 = start_x + i * (bar_width + spacing)
            y1 = 250
            x2 = x1 + bar_width
            y2 = y1 - (sale / max_sale) * 200
            self.bar_canvas.create_rectangle(x1, y1, x2, y2, fill="#2196F3")
            self.bar_canvas.create_text(x1 + bar_width/2, y1 + 15, text=hour, font=('Inter', 8))
            self.bar_canvas.create_text(x1 + bar_width/2, y2 - 10, text=str(sale), font=('Inter', 8))

    def draw_pie_chart(self):
        # Payment method data
        data = {"Cash": 40, "Card": 25, "UPI": 35}
        colors = ["#4CAF50", "#FF9800", "#2196F3"]
        total = sum(data.values())
        start_angle = 0
        center_x, center_y = 150, 150
        radius = 80

        for i, (method, value) in enumerate(data.items()):
            angle = (value / total) * 360
            extent = angle
            self.pie_canvas.create_arc(center_x - radius, center_y - radius, center_x + radius, center_y + radius,
                                       start=start_angle, extent=extent, fill=colors[i], outline="")
            # Label
            mid_angle = start_angle + extent / 2
            label_x = center_x + (radius + 20) * math.cos(math.radians(mid_angle - 90))
            label_y = center_y + (radius + 20) * math.sin(math.radians(mid_angle - 90))
            self.pie_canvas.create_text(label_x, label_y, text=f"{method}: {value}%", font=('Inter', 10))
            start_angle += extent

    def export_pdf(self):
        tk.messagebox.showinfo("Export", "Exporting to PDF...")

    def export_excel(self):
        tk.messagebox.showinfo("Export", "Exporting to Excel...")
