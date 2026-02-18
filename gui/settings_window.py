import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class SettingsWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("MediTrack - Settings")
        self.geometry("1000x600")
        self.resizable(False, False)
        self.current_tab = "General"
        self.create_ui()
        self.show_tab("General")

    def create_ui(self):
        # Left tabs
        left_frame = tk.Frame(self, bg="#F5F5F5", width=200, relief="raised", bd=1)
        left_frame.pack(side="left", fill="y", padx=10, pady=10)
        left_frame.pack_propagate(False)

        tk.Label(left_frame, text="Settings", font=('Inter', 16, 'bold'), bg="#F5F5F5").pack(pady=20)

        tabs = ["General", "Users", "Backup", "Database", "Printing", "Tax Settings"]
        self.tab_buttons = {}
        for tab in tabs:
            btn = tk.Button(left_frame, text=tab, font=('Inter', 12), bg="#E0E0E0", relief="flat", pady=10,
                            command=lambda t=tab: self.show_tab(t))
            btn.pack(fill="x", padx=10, pady=5)
            self.tab_buttons[tab] = btn

        # Right content
        self.content_frame = tk.Frame(self, bg="#FFFFFF", relief="raised", bd=1)
        self.content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    def show_tab(self, tab):
        self.current_tab = tab
        for t, btn in self.tab_buttons.items():
            btn.config(bg="#E0E0E0" if t != tab else "#2196F3", fg="#000000" if t != tab else "#FFFFFF")

        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if tab == "General":
            self.show_general()
        elif tab == "Users":
            self.show_users()
        elif tab == "Backup":
            self.show_backup()
        else:
            tk.Label(self.content_frame, text=f"{tab} settings coming soon.", font=('Inter', 14), bg="#FFFFFF").pack(pady=50)

    def show_general(self):
        tk.Label(self.content_frame, text="General Settings", font=('Inter', 18, 'bold'), bg="#FFFFFF").pack(pady=20)

        form_frame = tk.Frame(self.content_frame, bg="#FFFFFF")
        form_frame.pack(pady=20, padx=50, fill="both", expand=True)

        # Store Name
        tk.Label(form_frame, text="Store Name", font=('Inter', 12, 'bold'), bg="#FFFFFF").grid(row=0, column=0, sticky="w", pady=10)
        store_name_entry = tk.Entry(form_frame, font=('Inter', 12), width=30)
        store_name_entry.insert(0, "D. Chemist")
        store_name_entry.grid(row=0, column=1, pady=10, padx=20)

        # Address
        tk.Label(form_frame, text="Address", font=('Inter', 12, 'bold'), bg="#FFFFFF").grid(row=1, column=0, sticky="w", pady=10)
        address_entry = tk.Entry(form_frame, font=('Inter', 12), width=30)
        address_entry.insert(0, "123 Main St, City")
        address_entry.grid(row=1, column=1, pady=10, padx=20)

        # Phone
        tk.Label(form_frame, text="Phone", font=('Inter', 12, 'bold'), bg="#FFFFFF").grid(row=2, column=0, sticky="w", pady=10)
        phone_entry = tk.Entry(form_frame, font=('Inter', 12), width=30)
        phone_entry.insert(0, "1234567890")
        phone_entry.grid(row=2, column=1, pady=10, padx=20)

        # GST Number
        tk.Label(form_frame, text="GST Number", font=('Inter', 12, 'bold'), bg="#FFFFFF").grid(row=3, column=0, sticky="w", pady=10)
        gst_entry = tk.Entry(form_frame, font=('Inter', 12), width=30)
        gst_entry.insert(0, "GST123456789")
        gst_entry.grid(row=3, column=1, pady=10, padx=20)

        # Save button
        tk.Button(form_frame, text="Save", font=('Inter', 12, 'bold'), bg="#4CAF50", fg="#FFFFFF", relief="flat", padx=20, command=self.save_general).grid(row=4, column=1, pady=20, sticky="e")

    def show_users(self):
        tk.Label(self.content_frame, text="User Management", font=('Inter', 18, 'bold'), bg="#FFFFFF").pack(pady=10)

        # Top add button
        top_frame = tk.Frame(self.content_frame, bg="#FFFFFF")
        top_frame.pack(fill="x", pady=10)
        tk.Button(top_frame, text="Add New User", font=('Inter', 12, 'bold'), bg="#2196F3", fg="#FFFFFF", relief="flat", padx=20, command=self.add_user).pack(side="right")

        # Main content
        main_frame = tk.Frame(self.content_frame, bg="#FFFFFF")
        main_frame.pack(fill="both", expand=True)

        # Left user table
        table_frame = tk.Frame(main_frame, bg="#FFFFFF", relief="raised", bd=1)
        table_frame.pack(side="left", fill="both", expand=True, padx=10)

        columns = ("Username", "Full Name", "Role", "Phone", "Last Login", "Status", "Actions")
        self.user_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        for col in columns:
            self.user_tree.heading(col, text=col)
            self.user_tree.column(col, width=120, anchor="center")

        # Sample users with more details
        users = [
            ("admin", "Administrator", "Admin", "1234567890", "2026-02-18 10:00", "Active", "✏️ 🗑️"),
            ("pharmacist", "John Pharmacist", "Pharmacist", "0987654321", "2026-02-17 15:30", "Active", "✏️ 🗑️"),
            ("cashier", "Jane Cashier", "Cashier", "1122334455", "2026-02-16 12:00", "Inactive", "✏️ 🗑️")
        ]
        for user in users:
            self.user_tree.insert("", "end", values=user)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.user_tree.yview)
        self.user_tree.configure(yscrollcommand=scrollbar.set)
        self.user_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Right permissions sidebar
        perm_frame = tk.Frame(main_frame, bg="#FFFFFF", width=300, relief="raised", bd=1)
        perm_frame.pack(side="right", fill="y", padx=10)
        perm_frame.pack_propagate(False)

        tk.Label(perm_frame, text="Role Permissions", font=('Inter', 14, 'bold'), bg="#FFFFFF").pack(pady=20)

        modules = ["Inventory", "Billing", "Reports", "Customers", "Settings"]
        permissions = ["Full", "View", "None"]

        perm_vars = {}
        for module in modules:
            tk.Label(perm_frame, text=module, font=('Inter', 12, 'bold'), bg="#FFFFFF").pack(anchor="w", padx=10, pady=5)
            for perm in permissions:
                var = tk.BooleanVar()
                perm_vars[f"{module}_{perm}"] = var
                tk.Checkbutton(perm_frame, text=perm, variable=var, bg="#FFFFFF").pack(anchor="w", padx=20)

        # Save permissions button
        tk.Button(perm_frame, text="Save Permissions", font=('Inter', 12, 'bold'), bg="#4CAF50", fg="#FFFFFF", relief="flat", padx=10, command=self.save_permissions).pack(pady=20)

    def show_backup(self):
        tk.Label(self.content_frame, text="Backup Settings", font=('Inter', 18, 'bold'), bg="#FFFFFF").pack(pady=20)

        backup_frame = tk.Frame(self.content_frame, bg="#FFFFFF")
        backup_frame.pack(pady=20, padx=50, fill="both", expand=True)

        # Backup Location
        tk.Label(backup_frame, text="Backup Location", font=('Inter', 12, 'bold'), bg="#FFFFFF").grid(row=0, column=0, sticky="w", pady=10)
        location_entry = tk.Entry(backup_frame, font=('Inter', 12), width=40)
        location_entry.insert(0, "C:\\MediTrack\\Backups")
        location_entry.grid(row=0, column=1, pady=10, padx=20)

        # Backup Now
        tk.Button(backup_frame, text="Backup Now", font=('Inter', 12, 'bold'), bg="#4CAF50", fg="#FFFFFF", relief="flat", padx=20, command=self.open_backup_restore).grid(row=1, column=1, pady=20, sticky="e")

        # Schedule
        tk.Label(backup_frame, text="Schedule", font=('Inter', 12, 'bold'), bg="#FFFFFF").grid(row=2, column=0, sticky="w", pady=10)
        schedule_var = tk.StringVar(value="Daily")
        tk.OptionMenu(backup_frame, schedule_var, "Daily", "Weekly", "Monthly").grid(row=2, column=1, pady=10, sticky="w")

    def save_general(self):
        tk.messagebox.showinfo("Save", "General settings saved.")

    def add_user(self):
        tk.messagebox.showinfo("Add User", "Add user form not implemented yet.")

    def edit_user(self):
        tk.messagebox.showinfo("Edit User", "Edit user functionality not implemented yet.")

    def delete_user(self):
        tk.messagebox.showinfo("Delete User", "Delete user functionality not implemented yet.")

    def save_permissions(self):
        tk.messagebox.showinfo("Save Permissions", "Permissions saved successfully.")

    def backup_now(self):
        tk.messagebox.showinfo("Backup", "Backup initiated.")

    def open_backup_restore(self):
        from gui.backup_restore_window import BackupRestoreWindow
        BackupRestoreWindow(self)
