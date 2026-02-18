import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

class BackupRestoreWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("MediTrack - Backup & Restore")
        self.geometry("1200x700")
        self.resizable(False, False)
        self.create_ui()

    def create_ui(self):
        top_frame = tk.Frame(self, bg="#FFFFFF", height=60, relief="raised", bd=1)
        top_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(top_frame, text="Backup Status", font=('Inter', 14, 'bold'), bg="#FFFFFF").pack(side="left", padx=20, pady=10)
        tk.Label(top_frame, text="Last Backup: Today 9:00 PM", font=('Inter', 12), bg="#FFFFFF").pack(side="left", padx=20, pady=10)
        canvas = tk.Canvas(top_frame, width=20, height=20, bg="#FFFFFF", highlightthickness=0)
        canvas.pack(side="left", padx=10, pady=10)
        canvas.create_oval(5, 5, 15, 15, fill="#4CAF50", outline="")
        canvas.create_line(7, 10, 10, 13, fill="#FFFFFF", width=2)
        canvas.create_line(10, 13, 13, 7, fill="#FFFFFF", width=2)

        main_frame = tk.Frame(self, bg="#FFFFFF")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        backup_frame = tk.Frame(main_frame, bg="#FFFFFF", relief="raised", bd=1)
        backup_frame.pack(side="left", fill="both", expand=True, padx=5)

        tk.Label(backup_frame, text="Backup", font=('Inter', 16, 'bold'), bg="#FFFFFF").pack(pady=20)

        loc_frame = tk.Frame(backup_frame, bg="#FFFFFF")
        loc_frame.pack(fill="x", padx=20, pady=10)
        tk.Label(loc_frame, text="Backup Location", font=('Inter', 12, 'bold'), bg="#FFFFFF").pack(anchor="w")
        self.location_entry = tk.Entry(loc_frame, font=('Inter', 12), width=40)
        self.location_entry.insert(0, "C:\\MediTrack\\Backups")
        self.location_entry.pack(fill="x", pady=5)
        tk.Button(loc_frame, text="Browse", font=('Inter', 10), bg="#E0E0E0", relief="flat", command=self.browse_location).pack(anchor="e")

        self.include_logs_var = tk.BooleanVar()
        tk.Checkbutton(backup_frame, text="Include Logs", variable=self.include_logs_var, font=('Inter', 12), bg="#FFFFFF").pack(anchor="w", padx=20, pady=10)

        schedule_frame = tk.Frame(backup_frame, bg="#FFFFFF")
        schedule_frame.pack(fill="x", padx=20, pady=10)
        tk.Label(schedule_frame, text="Schedule Backup", font=('Inter', 12, 'bold'), bg="#FFFFFF").pack(anchor="w")
        self.schedule_var = tk.BooleanVar()
        tk.Checkbutton(schedule_frame, text="Enable", variable=self.schedule_var, font=('Inter', 10), bg="#FFFFFF").pack(anchor="w", pady=5)
        time_frame = tk.Frame(schedule_frame, bg="#FFFFFF")
        time_frame.pack(anchor="w")
        tk.Label(time_frame, text="Time:", font=('Inter', 10), bg="#FFFFFF").pack(side="left")
        self.time_entry = tk.Entry(time_frame, font=('Inter', 10), width=10)
        self.time_entry.insert(0, "09:00")
        self.time_entry.pack(side="left", padx=5)

        tk.Button(backup_frame, text="Create Backup Now", font=('Inter', 14, 'bold'), bg="#2196F3", fg="#FFFFFF", relief="flat", padx=20, pady=10, command=self.create_backup).pack(pady=30)

        restore_frame = tk.Frame(main_frame, bg="#FFFFFF", relief="raised", bd=1)
        restore_frame.pack(side="right", fill="both", expand=True, padx=5)

        tk.Label(restore_frame, text="Restore", font=('Inter', 16, 'bold'), bg="#FFFFFF").pack(pady=20)

        columns = ("Date", "Time", "Size")
        self.backup_tree = ttk.Treeview(restore_frame, columns=columns, show="headings", height=10)
        for col in columns:
            self.backup_tree.heading(col, text=col)
            self.backup_tree.column(col, width=120, anchor="center")

        backups = [
            ("2026-02-18", "09:00", "1.2 GB"),
            ("2026-02-17", "21:00", "1.1 GB"),
            ("2026-02-16", "09:00", "1.0 GB")
        ]
        for backup in backups:
            self.backup_tree.insert("", "end", values=backup)

        self.backup_tree.pack(fill="both", expand=True, padx=20, pady=10)

        button_frame = tk.Frame(restore_frame, bg="#FFFFFF")
        button_frame.pack(pady=20)
        tk.Button(button_frame, text="⚠️ Restore Selected", font=('Inter', 12, 'bold'), bg="#FF9800", fg="#FFFFFF", relief="flat", padx=20, command=self.restore_backup).pack()

        self.progress_frame = tk.Frame(self, bg="#FFFFFF", height=50, relief="raised", bd=1)
        self.progress_frame.pack(fill="x", padx=10, pady=10)
        tk.Label(self.progress_frame, text="Progress:", font=('Inter', 12), bg="#FFFFFF").pack(side="left", padx=20, pady=10)
        self.progress_bar = ttk.Progressbar(self.progress_frame, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.pack(side="left", padx=20, pady=10)

    def browse_location(self):
        tk.messagebox.showinfo("Browse", "Browse functionality not implemented.")

    def create_backup(self):
        self.progress_bar["value"] = 0
        for i in range(101):
            self.progress_bar["value"] = i
            self.update_idletasks()
            self.after(50)
        tk.messagebox.showinfo("Backup", "Backup created successfully.")

    def restore_backup(self):
        selected = self.backup_tree.selection()
        if selected:
            self.progress_bar["value"] = 0
            for i in range(101):
                self.progress_bar["value"] = i
                self.update_idletasks()
                self.after(50)
            tk.messagebox.showinfo("Restore", "Backup restored successfully.")
        else:
            tk.messagebox.showerror("Error", "Please select a backup to restore.")
