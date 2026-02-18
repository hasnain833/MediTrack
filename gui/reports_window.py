import tkinter as tk
from tkinter import ttk
from datetime import datetime

class ReportsWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("MediTrack - Reports Dashboard")
        self.geometry("1200x800")
        self.resizable(False, False)
        self.create_ui()

    def create_ui(self):
        # Top date selector
        top_frame = tk.Frame(self, bg="#FFFFFF", height=80, relief="raised", bd=1)
        top_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(top_frame, text="Date Range:", font=('Inter', 12, 'bold'), bg="#FFFFFF").pack(side="left", padx=10)
        tk.Label(top_frame, text="From", font=('Inter', 10), bg="#FFFFFF").pack(side="left", padx=5)
        self.from_entry = tk.Entry(top_frame, font=('Inter', 10), width=15)
        self.from_entry.insert(0, "YYYY-MM-DD")
        self.from_entry.pack(side="left", padx=5)
        tk.Label(top_frame, text="📅", font=('Inter', 10), bg="#FFFFFF").pack(side="left")

        tk.Label(top_frame, text="To", font=('Inter', 10), bg="#FFFFFF").pack(side="left", padx=5)
        self.to_entry = tk.Entry(top_frame, font=('Inter', 10), width=15)
        self.to_entry.insert(0, "YYYY-MM-DD")
        self.to_entry.pack(side="left", padx=5)
        tk.Label(top_frame, text="📅", font=('Inter', 10), bg="#FFFFFF").pack(side="left")

        generate_btn = tk.Button(top_frame, text="Generate Report", font=('Inter', 12, 'bold'), bg="#4CAF50", fg="#FFFFFF", relief="flat", padx=20, command=self.generate_report)
        generate_btn.pack(side="right", padx=10)

        # Report cards grid
        cards_frame = tk.Frame(self, bg="#FFFFFF")
        cards_frame.pack(fill="both", expand=True, padx=10, pady=10)

        reports = [
            {"title": "Daily Sales Report", "icon": "📊", "preview": "Graph"},
            {"title": "Stock Report", "icon": "📦", "preview": "Inventory"},
            {"title": "Expiry Report", "icon": "⚠️", "preview": "Warning"},
            {"title": "GST Report", "icon": "💰", "preview": "Tax"}
        ]

        for i, report in enumerate(reports):
            row = i // 2
            col = i % 2
            self.create_report_card(cards_frame, row, col, report)

        # Bottom chart preview
        chart_frame = tk.Frame(self, bg="#FFFFFF", relief="raised", bd=1)
        chart_frame.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(chart_frame, text="Report Preview - Last Generated Report", font=('Inter', 14, 'bold'), bg="#FFFFFF").pack(pady=10)

        self.chart_canvas = tk.Canvas(chart_frame, bg="#FFFFFF", height=300)
        self.chart_canvas.pack(fill="x", padx=20, pady=10)
        self.draw_sample_chart()

    def create_report_card(self, parent, row, col, report):
        card = tk.Frame(parent, bg="#F5F5F5", relief="raised", bd=2, width=500, height=200)
        card.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")
        card.pack_propagate(False)

        # Icon and title
        tk.Label(card, text=report["icon"], font=('Arial', 40), bg="#F5F5F5").pack(pady=10)
        tk.Label(card, text=report["title"], font=('Inter', 14, 'bold'), bg="#F5F5F5", fg="#1976D2").pack(pady=5)

        # Preview
        tk.Label(card, text=f"Preview: {report['preview']}", font=('Inter', 10), bg="#F5F5F5").pack(pady=5)

        # View button
        view_btn = tk.Button(card, text="View Report", font=('Inter', 10, 'bold'), bg="#2196F3", fg="#FFFFFF", relief="flat", padx=10, command=lambda: self.view_report(report["title"]))
        view_btn.pack(pady=10)

    def draw_sample_chart(self):
        # Sample bar chart
        data = [10, 15, 12, 18, 14, 20, 16]
        max_val = max(data)
        bar_width = 40
        spacing = 20
        start_x = 50

        for i, val in enumerate(data):
            x1 = start_x + i * (bar_width + spacing)
            y1 = 250
            x2 = x1 + bar_width
            y2 = y1 - (val / max_val) * 200
            self.chart_canvas.create_rectangle(x1, y1, x2, y2, fill="#2196F3")
            self.chart_canvas.create_text(x1 + bar_width/2, y1 + 10, text=str(val), font=('Inter', 8))

        # Labels
        self.chart_canvas.create_text(300, 280, text="Sample Sales Data", font=('Inter', 12, 'bold'))

    def generate_report(self):
        from_date = self.from_entry.get()
        to_date = self.to_entry.get()
        tk.messagebox.showinfo("Generate Report", f"Generating report from {from_date} to {to_date}")

    def view_report(self, report_title):
        if report_title == "Daily Sales Report":
            from gui.daily_sales_report_window import DailySalesReportWindow
            DailySalesReportWindow(self)
        elif report_title == "Stock Report":
            from gui.stock_report_window import StockReportWindow
            StockReportWindow(self)
        else:
            tk.messagebox.showinfo("View Report", f"Viewing {report_title}")
