import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class CustomerWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("MediTrack - Customer Management")
        self.geometry("1200x700")
        self.resizable(False, False)
        self.create_ui()

    def create_ui(self):
        # Top frame
        top_frame = tk.Frame(self, bg="#FFFFFF", height=60, relief="raised", bd=1)
        top_frame.pack(fill="x", padx=10, pady=10)

        # Search bar
        search_frame = tk.Frame(top_frame, bg="#FFFFFF")
        search_frame.pack(side="left", padx=10)
        tk.Label(search_frame, text="Phone:", font=('Inter', 10), bg="#FFFFFF").pack(side="left")
        self.search_entry = tk.Entry(search_frame, font=('Inter', 10), width=20)
        self.search_entry.pack(side="left", padx=5)
        search_btn = tk.Button(search_frame, text="🔍", font=('Inter', 10), bg="#E0E0E0", relief="flat", command=self.search_customer)
        search_btn.pack(side="left", padx=5)

        # Add Customer button
        add_btn = tk.Button(top_frame, text="Add Customer", font=('Inter', 12, 'bold'), bg="#2196F3", fg="#FFFFFF", relief="flat", padx=20, command=self.add_customer)
        add_btn.pack(side="right", padx=10)

        # Main frame
        main_frame = tk.Frame(self, bg="#FFFFFF")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Customer table
        table_frame = tk.Frame(main_frame, bg="#FFFFFF", relief="raised", bd=1)
        table_frame.pack(side="left", fill="both", expand=True, padx=10)

        columns = ("ID", "Name", "Phone", "Email", "Address", "Total Purchases", "Last Purchase", "Actions")
        self.customer_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
        for col in columns:
            self.customer_tree.heading(col, text=col)
            self.customer_tree.column(col, width=120, anchor="center")

        # Sample customers
        self.customers = [
            ("1", "John Doe", "1234567890", "john@example.com", "123 Main St", "Rs. 5000", "2026-02-15", "📄"),
            ("2", "Jane Smith", "0987654321", "jane@example.com", "456 Elm St", "Rs. 3200", "2026-02-10", "📄"),
            ("3", "Bob Johnson", "1122334455", "bob@example.com", "789 Oak St", "Rs. 1500", "2026-02-05", "📄"),
            ("4", "Alice Brown", "5566778899", "alice@example.com", "321 Pine St", "Rs. 7800", "2026-02-18", "📄")
        ]
        self.load_customers()

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.customer_tree.yview)
        self.customer_tree.configure(yscrollcommand=scrollbar.set)
        self.customer_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Right sidebar
        sidebar_frame = tk.Frame(main_frame, bg="#FFFFFF", width=250, relief="raised", bd=1)
        sidebar_frame.pack(side="right", fill="y", padx=10)
        sidebar_frame.pack_propagate(False)

        tk.Label(sidebar_frame, text="Recent Customers", font=('Inter', 14, 'bold'), bg="#FFFFFF").pack(pady=10)

        recent_customers = [
            ("John Doe", "J"),
            ("Jane Smith", "J"),
            ("Bob Johnson", "B"),
            ("Alice Brown", "A")
        ]
        for name, initial in recent_customers:
            customer_frame = tk.Frame(sidebar_frame, bg="#F5F5F5", relief="raised", bd=1)
            customer_frame.pack(fill="x", padx=10, pady=5)
            # Avatar
            avatar_canvas = tk.Canvas(customer_frame, width=30, height=30, bg="#F5F5F5", highlightthickness=0)
            avatar_canvas.pack(side="left", padx=5)
            avatar_canvas.create_oval(5, 5, 25, 25, fill="#2196F3", outline="")
            avatar_canvas.create_text(15, 15, text=initial, font=('Inter', 12, 'bold'), fill="#FFFFFF")
            # Name
            tk.Label(customer_frame, text=name, font=('Inter', 10), bg="#F5F5F5").pack(side="left", padx=5)

        # Bottom pagination
        bottom_frame = tk.Frame(self, bg="#FFFFFF", height=50, relief="raised", bd=1)
        bottom_frame.pack(fill="x", padx=10, pady=10)
        tk.Button(bottom_frame, text="< Previous", relief="flat").pack(side="left")
        tk.Label(bottom_frame, text="Page 1 of 1", bg="#FFFFFF").pack(side="left", expand=True)
        tk.Button(bottom_frame, text="Next >", relief="flat").pack(side="right")

    def load_customers(self):
        for item in self.customer_tree.get_children():
            self.customer_tree.delete(item)
        for customer in self.customers:
            self.customer_tree.insert("", "end", values=customer)

    def search_customer(self):
        phone = self.search_entry.get()
        if phone:
            filtered = [c for c in self.customers if phone in c[2]]
            self.customer_tree.delete(*self.customer_tree.get_children())
            for customer in filtered:
                self.customer_tree.insert("", "end", values=customer)
        else:
            self.load_customers()

    def add_customer(self):
        # Placeholder
        messagebox.showinfo("Add Customer", "Add Customer functionality not implemented yet.")
