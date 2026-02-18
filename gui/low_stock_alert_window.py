import tkinter as tk
from tkinter import ttk

class LowStockAlertWindow(tk.Toplevel):
    def __init__(self, master, low_stock_items):
        super().__init__(master)
        self.title("")
        self.geometry("400x300")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.overrideredirect(True)
        self.create_overlay()
        self.create_dialog(low_stock_items)

    def create_overlay(self):
        self.overlay = tk.Frame(self, bg="#000000")
        self.overlay.place(x=0, y=0, relwidth=1, relheight=1)
        self.overlay.config(bg="#000000")

    def create_dialog(self, low_stock_items):
        dialog = tk.Frame(self, bg="#FFFFFF", relief="raised", bd=2)
        dialog.place(relx=0.5, rely=0.5, anchor="center", width=400, height=300)

        warning_canvas = tk.Canvas(dialog, width=50, height=50, bg="#FFFFFF", highlightthickness=0)
        warning_canvas.pack(pady=10)
        warning_canvas.create_polygon(25, 5, 45, 35, 5, 35, fill="#FFEB3B", outline="#F57C00")
        warning_canvas.create_text(25, 20, text="!", font=('Arial', 20, 'bold'), fill="#F57C00")

        tk.Label(dialog, text="Low Stock Alert", font=('Inter', 16, 'bold'), fg="#F44336", bg="#FFFFFF").pack(pady=5)

        list_frame = tk.Frame(dialog, bg="#FFFFFF")
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        for item in low_stock_items:
            item_frame = tk.Frame(list_frame, bg="#F5F5F5", relief="ridge", bd=1)
            item_frame.pack(fill="x", pady=2)

            tk.Label(item_frame, text=item['name'], font=('Inter', 10, 'bold'), bg="#F5F5F5").pack(side="left", padx=5)
            tk.Label(item_frame, text=f"Qty: {item['qty']}", font=('Inter', 10), fg="#F44336", bg="#F5F5F5").pack(side="left", padx=5)
            tk.Label(item_frame, text=f"Reorder: {item['reorder']}", font=('Inter', 10), bg="#F5F5F5").pack(side="left", padx=5)
            tk.Button(item_frame, text="Reorder", font=('Inter', 8), bg="#4CAF50", fg="#FFFFFF", relief="flat", command=lambda i=item: self.reorder(i)).pack(side="right", padx=5)

        button_frame = tk.Frame(dialog, bg="#FFFFFF")
        button_frame.pack(fill="x", pady=10)
        tk.Button(button_frame, text="View All", font=('Inter', 10, 'bold'), bg="#2196F3", fg="#FFFFFF", relief="flat", command=self.view_all).pack(side="left", padx=20)
        tk.Button(button_frame, text="Dismiss", font=('Inter', 10, 'bold'), bg="#9E9E9E", fg="#FFFFFF", relief="flat", command=self.destroy).pack(side="right", padx=20)

    def reorder(self, item):
        tk.messagebox.showinfo("Reorder", f"Initiating reorder for {item['name']}")

    def view_all(self):
        self.destroy()
        from gui.inventory_window import InventoryWindow
        InventoryWindow(self.master)
