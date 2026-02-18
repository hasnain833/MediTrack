import tkinter as tk
from tkinter import ttk

class SplashAboutWindow(tk.Toplevel):
    def __init__(self, master, mode='about'):
        super().__init__(master)
        self.mode = mode
        self.title("D. chemist" if mode == 'about' else "")
        self.geometry("600x400")
        self.resizable(False, False)
        self.overrideredirect(True if mode == 'splash' else False)  # No border for splash
        self.create_ui()
        if mode == 'splash':
            self.show_splash()
        else:
            self.show_about()

    def create_ui(self):
        # Canvas for gradient border
        self.canvas = tk.Canvas(self, width=600, height=400, highlightthickness=0)
        self.canvas.pack()

        # Gradient border
        for i in range(10):
            color = self.interpolate_color("#E3F2FD", "#2196F3", i / 9)
            self.canvas.create_rectangle(i, i, 600 - i, 400 - i, outline=color, width=1)

        # White card
        self.canvas.create_rectangle(20, 20, 580, 380, fill="#FFFFFF", outline="")

        # Content
        self.canvas.create_text(300, 80, text="✚", font=('Arial', 60), fill="#1976D2")
        self.canvas.create_text(300, 130, text="D. Chemist", font=('Inter', 48, 'bold'), fill="#1976D2")
        self.canvas.create_text(300, 170, text="Medical Store Management System", font=('Inter', 16), fill="#757575")
        self.canvas.create_text(300, 200, text="Version 2.0.0", font=('Inter', 14), fill="#424242")
        self.canvas.create_text(300, 230, text="© 2026 Your Company Name", font=('Inter', 12), fill="#9E9E9E")
        self.canvas.create_text(300, 260, text="Developed with Python & MySQL", font=('Inter', 12), fill="#9E9E9E")
        self.canvas.create_text(300, 290, text="System Requirements: Windows 10+, Python 3.8+", font=('Inter', 10), fill="#BDBDBD")

        if self.mode == 'splash':
            # Progress bar
            self.progress = ttk.Progressbar(self, orient="horizontal", length=200, mode="determinate")
            self.canvas.create_window(500, 350, window=self.progress, anchor="se")
        else:
            # Close button
            close_btn = tk.Button(self, text="Close", font=('Inter', 12), bg="#F44336", fg="#FFFFFF", relief="flat", command=self.destroy)
            self.canvas.create_window(550, 350, window=close_btn)

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

    def show_splash(self):
        # Simulate loading
        for i in range(101):
            self.progress["value"] = i
            self.update_idletasks()
            self.after(30)
        self.after(500, self.destroy)

    def show_about(self):
        pass  # Static display
