import tkinter as tk
from tkinter import ttk
from datetime import datetime

class InventoryWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("MediTrack - Inventory Management")
        self.geometry("1200x800")
        self.resizable(False, False)
        self.create_ui()

    def create_ui(self):
        # Top frame for search and add button
        top_frame = tk.Frame(self, bg="#FFFFFF", height=60, relief="raised", bd=1)
        top_frame.pack(fill="x", padx=10, pady=10)

        # Search bar
        search_frame = tk.Frame(top_frame, bg="#FFFFFF")
        search_frame.pack(side="left", padx=10)
        self.search_entry = tk.Entry(search_frame, font=('Inter', 12), width=30)
        self.search_entry.pack(side="left")
        search_btn = tk.Button(search_frame, text="🔍", font=('Inter', 12), bg="#E0E0E0", relief="flat", command=self.search)
        search_btn.pack(side="left", padx=5)

        # Add Medicine button
        add_btn = tk.Button(top_frame, text="Add Medicine", font=('Inter', 12, 'bold'), bg="#2196F3", fg="#FFFFFF", relief="flat", padx=20, command=self.add_medicine)
        add_btn.pack(side="right", padx=10)

        # Main frame for table and filters
        main_frame = tk.Frame(self, bg="#FFFFFF")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Table
        table_frame = tk.Frame(main_frame, bg="#FFFFFF", relief="raised", bd=1)
        table_frame.pack(side="left", fill="both", expand=True)

        columns = ("ID", "Medicine Name", "Category", "Company", "Batch No", "Expiry Date", "Quantity", "Price", "Actions")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")

        # Sample data
        self.sample_data = [
            ("1", "Paracetamol", "Painkiller", "ABC Pharma", "B001", "2026-05-01", "50", "10.00", "Edit | Delete"),
            ("2", "Ibuprofen", "Painkiller", "XYZ Corp", "B002", "2025-12-01", "5", "15.00", "Edit | Delete"),
            ("3", "Expired Med", "Expired", "Old Co", "B003", "2024-01-01", "20", "5.00", "Edit | Delete"),
            ("4", "Vitamin C", "Vitamin", "Health Inc", "B004", "2027-03-15", "100", "20.00", "Edit | Delete"),
        ]
        self.load_data()

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Filter panel
        filter_frame = tk.Frame(main_frame, bg="#FFFFFF", width=250, relief="raised", bd=1)
        filter_frame.pack(side="right", fill="y", padx=10)
        filter_frame.pack_propagate(False)

        tk.Label(filter_frame, text="Filters", font=('Inter', 14, 'bold'), bg="#FFFFFF").pack(pady=10)

        tk.Label(filter_frame, text="Categories", font=('Inter', 12), bg="#FFFFFF").pack(anchor="w", padx=10)
        self.category_vars = {}
        categories = ["Painkiller", "Antibiotic", "Vitamin"]
        for cat in categories:
            var = tk.BooleanVar()
            self.category_vars[cat] = var
            tk.Checkbutton(filter_frame, text=cat, variable=var, bg="#FFFFFF", command=self.filter_data).pack(anchor="w", padx=20)

        tk.Label(filter_frame, text="Expiry Filter", font=('Inter', 12), bg="#FFFFFF").pack(anchor="w", padx=10, pady=10)
        self.expiry_var = tk.StringVar(value="All")
        tk.OptionMenu(filter_frame, self.expiry_var, "All", "Expiring Soon", "Expired", command=self.filter_data).pack(padx=10)

        # Bottom pagination
        bottom_frame = tk.Frame(self, bg="#FFFFFF", height=50, relief="raised", bd=1)
        bottom_frame.pack(fill="x", padx=10, pady=10)
        tk.Button(bottom_frame, text="< Previous", relief="flat", command=self.prev_page).pack(side="left")
        self.page_label = tk.Label(bottom_frame, text="Page 1 of 1", bg="#FFFFFF")
        self.page_label.pack(side="left", expand=True)
        tk.Button(bottom_frame, text="Next >", relief="flat", command=self.next_page).pack(side="right")

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for i, item in enumerate(self.sample_data):
            tag = ""
            quantity = int(item[6])
            expiry = item[5]
            try:
                exp_date = datetime.strptime(expiry, "%Y-%m-%d")
                if exp_date < datetime.now():
                    tag = "expired"
                elif quantity < 10:
                    tag = "low_stock"
            except:
                pass
            self.tree.insert("", "end", values=item, tags=(tag,))
        # Alternating colors
        for i, item_id in enumerate(self.tree.get_children()):
            if i % 2 == 0:
                self.tree.item(item_id, tags=("even",))
            else:
                self.tree.item(item_id, tags=("odd",))
        self.tree.tag_configure("expired", background="#FFEBEE")
        self.tree.tag_configure("low_stock", background="#FFF9C4")
        self.tree.tag_configure("even", background="#F5F5F5")
        self.tree.tag_configure("odd", background="#FFFFFF")

    def filter_data(self, *args):
        # Simple filter implementation
        filtered = []
        selected_categories = [cat for cat, var in self.category_vars.items() if var.get()]
        expiry_filter = self.expiry_var.get()
        for item in self.sample_data:
            category = item[2]
            expiry = item[5]
            quantity = int(item[6])
            include = True
            if selected_categories and category not in selected_categories:
                include = False
            if expiry_filter == "Expiring Soon" and not (10 < quantity < 20):  # Placeholder logic
                include = False
            elif expiry_filter == "Expired":
                try:
                    exp_date = datetime.strptime(expiry, "%Y-%m-%d")
                    if exp_date >= datetime.now():
                        include = False
                except:
                    include = False
            if include:
                filtered.append(item)
        self.sample_data = filtered
        self.load_data()

    def search(self):
        query = self.search_entry.get().lower()
        filtered = [item for item in self.sample_data if query in item[1].lower() or query in item[2].lower()]
        self.sample_data = filtered
        self.load_data()

    def add_medicine(self):
        from gui.add_medicine_window import AddMedicineWindow
        AddMedicineWindow(self)

    def prev_page(self):
        # Placeholder
        pass

    def next_page(self):
        # Placeholder
        pass
