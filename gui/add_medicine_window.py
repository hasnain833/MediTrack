import tkinter as tk
from tkinter import messagebox

class AddMedicineWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("MediTrack - Add New Medicine")
        self.geometry("700x600")
        self.resizable(False, False)
        self.create_ui()

    def create_ui(self):
        self.canvas = tk.Canvas(self, width=700, height=600, highlightthickness=0, takefocus=0)
        self.canvas.place(x=0, y=0, width=700, height=600)

        for y in range(600):
            factor = y / 599
            color = self.interpolate_color("#E3F2FD", "#FFFFFF", factor)
            self.canvas.create_line(0, y, 700, y, fill=color, width=1)

        card_frame = tk.Frame(self, bg="#FFFFFF", bd=1, relief="solid")
        card_frame.place(x=50, y=50, width=600, height=500)

        tk.Label(card_frame, text="Add New Medicine", font=('Inter', 18, 'bold'), bg="#FFFFFF", fg="#1976D2").pack(pady=20)

        form_frame = tk.Frame(card_frame, bg="#FFFFFF")
        form_frame.pack(pady=10, padx=50, fill="both", expand=True)

        left_frame = tk.Frame(form_frame, bg="#FFFFFF")
        left_frame.grid(row=0, column=0, padx=20, pady=10, sticky="n")

        tk.Label(left_frame, text="Medicine Name", font=('Inter', 12, 'bold'), bg="#FFFFFF", fg="#424242").grid(row=0, column=0, sticky="w", pady=5)
        self.name_entry = tk.Entry(left_frame, font=('Inter', 12), bd=1, relief="solid", width=25)
        self.name_entry.grid(row=1, column=0, pady=5)

        tk.Label(left_frame, text="Category", font=('Inter', 12, 'bold'), bg="#FFFFFF", fg="#424242").grid(row=2, column=0, sticky="w", pady=5)
        self.category_var = tk.StringVar(value="Painkiller")
        tk.OptionMenu(left_frame, self.category_var, "Painkiller", "Antibiotic", "Vitamin", "Other").grid(row=3, column=0, pady=5, sticky="w")

        tk.Label(left_frame, text="Company", font=('Inter', 12, 'bold'), bg="#FFFFFF", fg="#424242").grid(row=4, column=0, sticky="w", pady=5)
        self.company_entry = tk.Entry(left_frame, font=('Inter', 12), bd=1, relief="solid", width=25)
        self.company_entry.grid(row=5, column=0, pady=5)

        tk.Label(left_frame, text="Batch Number", font=('Inter', 12, 'bold'), bg="#FFFFFF", fg="#424242").grid(row=6, column=0, sticky="w", pady=5)
        self.batch_entry = tk.Entry(left_frame, font=('Inter', 12), bd=1, relief="solid", width=25)
        self.batch_entry.grid(row=7, column=0, pady=5)

        right_frame = tk.Frame(form_frame, bg="#FFFFFF")
        right_frame.grid(row=0, column=1, padx=20, pady=10, sticky="n")

        tk.Label(right_frame, text="Expiry Date", font=('Inter', 12, 'bold'), bg="#FFFFFF", fg="#424242").grid(row=0, column=0, sticky="w", pady=5)
        self.expiry_entry = tk.Entry(right_frame, font=('Inter', 12), bd=1, relief="solid", width=25)
        self.expiry_entry.insert(0, "YYYY-MM-DD")
        self.expiry_entry.grid(row=1, column=0, pady=5)

        tk.Label(right_frame, text="Quantity", font=('Inter', 12, 'bold'), bg="#FFFFFF", fg="#424242").grid(row=2, column=0, sticky="w", pady=5)
        self.quantity_entry = tk.Entry(right_frame, font=('Inter', 12), bd=1, relief="solid", width=25)
        self.quantity_entry.grid(row=3, column=0, pady=5)

        tk.Label(right_frame, text="Purchase Price", font=('Inter', 12, 'bold'), bg="#FFFFFF", fg="#424242").grid(row=4, column=0, sticky="w", pady=5)
        self.purchase_entry = tk.Entry(right_frame, font=('Inter', 12), bd=1, relief="solid", width=25)
        self.purchase_entry.grid(row=5, column=0, pady=5)

        tk.Label(right_frame, text="Selling Price", font=('Inter', 12, 'bold'), bg="#FFFFFF", fg="#424242").grid(row=6, column=0, sticky="w", pady=5)
        self.selling_entry = tk.Entry(right_frame, font=('Inter', 12), bd=1, relief="solid", width=25)
        self.selling_entry.grid(row=7, column=0, pady=5)

        tk.Label(right_frame, text="MRP", font=('Inter', 12, 'bold'), bg="#FFFFFF", fg="#424242").grid(row=8, column=0, sticky="w", pady=5)
        self.mrp_entry = tk.Entry(right_frame, font=('Inter', 12), bd=1, relief="solid", width=25)
        self.mrp_entry.grid(row=9, column=0, pady=5)

        tk.Label(right_frame, text="GST (%)", font=('Inter', 12, 'bold'), bg="#FFFFFF", fg="#424242").grid(row=10, column=0, sticky="w", pady=5)
        self.gst_entry = tk.Entry(right_frame, font=('Inter', 12), bd=1, relief="solid", width=25)
        self.gst_entry.grid(row=11, column=0, pady=5)

        tk.Label(right_frame, text="Rack Number", font=('Inter', 12, 'bold'), bg="#FFFFFF", fg="#424242").grid(row=12, column=0, sticky="w", pady=5)
        self.rack_entry = tk.Entry(right_frame, font=('Inter', 12), bd=1, relief="solid", width=25)
        self.rack_entry.grid(row=13, column=0, pady=5)

        button_frame = tk.Frame(card_frame, bg="#FFFFFF")
        button_frame.pack(pady=20)
        tk.Button(button_frame, text="Save", font=('Inter', 12, 'bold'), bg="#2196F3", fg="#FFFFFF", relief="flat", padx=20, command=self.save).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Cancel", font=('Inter', 12, 'bold'), bg="#9E9E9E", fg="#FFFFFF", relief="flat", padx=20, command=self.cancel).grid(row=0, column=1, padx=10)

    def interpolate_color(self, color1, color2, factor):
        r1 = int(color1[1:3], 16)
        g1 = int(color1[3:5], 16)
        b1 = int(color1[5:7], 16)
        r2 = int(color2[1:3], 16)
        g2 = int(color2[3:5], 16)
        b2 = int(color2[5:7], 16)
        r = int(r1 + (r2 - r1) * factor)
        g = int(g1 + (g2 - g1) * factor)
        b = int(b1 + (b2 - b1) * factor)
        return f"#{r:02x}{g:02x}{b:02x}"

    def save(self):
        data = {
            "name": self.name_entry.get(),
            "category": self.category_var.get(),
            "company": self.company_entry.get(),
            "batch": self.batch_entry.get(),
            "expiry": self.expiry_entry.get(),
            "quantity": self.quantity_entry.get(),
            "purchase": self.purchase_entry.get(),
            "selling": self.selling_entry.get(),
            "mrp": self.mrp_entry.get(),
            "gst": self.gst_entry.get(),
            "rack": self.rack_entry.get()
        }
        if not data["name"] or not data["company"]:
            messagebox.showerror("Error", "Medicine Name and Company are required.")
            return
        messagebox.showinfo("Success", "Medicine added successfully!")
        self.destroy()

    def cancel(self):
        self.destroy()
