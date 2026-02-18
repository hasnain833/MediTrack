import tkinter as tk
from tkinter import messagebox
import bcrypt
from database.connection import Database
from gui.main_window import MainWindow
from PIL import Image, ImageTk

class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MediTrack - Login")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Set font
        try:
            self.title_font = ('Inter', 24, 'bold')
            self.label_font = ('Inter', 12)
            self.button_font = ('Inter', 14, 'bold')
            self.version_font = ('Inter', 10)
        except:
            self.title_font = ('Helvetica', 24, 'bold')
            self.label_font = ('Helvetica', 12)
            self.button_font = ('Helvetica', 14, 'bold')
            self.version_font = ('Helvetica', 10)

        self.db = Database()
        self.draw_ui(800, 600)
        self.root.bind('<Configure>', self.on_resize)

    def draw_ui(self, width, height):
        # Canvas for gradient background
        self.canvas = tk.Canvas(self.root, width=width, height=height, highlightthickness=0, takefocus=0)
        self.canvas.place(x=0, y=0, width=width, height=height)

        # Create vertical gradient
        for y in range(height):
            factor = y / max(1, height - 1)
            color = self.interpolate_color("#E3F2FD", "#FFFFFF", factor)
            self.canvas.create_line(0, y, width, y, fill=color, width=1)

        # Centered white card with shadow (400x400)
        card_w, card_h = 400, 400
        card_x = (width - card_w) // 2
        card_y = (height - card_h) // 2

        # Shadow on canvas
        shadow_offset = 5
        self.canvas.create_rectangle(card_x + shadow_offset, card_y + shadow_offset,
                                     card_x + card_w + shadow_offset, card_y + card_h + shadow_offset,
                                     fill="#D0D0D0", outline="")

        # Card frame on root
        card_frame = tk.Frame(self.root, bg="#FFFFFF", bd=1, relief="solid")
        card_frame.place(x=card_x, y=card_y, width=card_w, height=card_h)

        # Logo and title
        logo_label = tk.Label(card_frame, text="D.C", font=self.title_font, bg="#FFFFFF", fg="#1976D2")
        logo_label.pack(pady=20)

        # Username label
        username_label = tk.Label(card_frame, text="Username", font=self.label_font, bg="#FFFFFF", fg="#424242")
        username_label.pack(pady=5)

        # Username entry
        self.username_entry = tk.Entry(card_frame, font=('Inter', 12), bd=1, relief="sunken", bg="#FFFFFF",
                                       insertbackground="#424242")
        self.username_entry.pack(pady=5, padx=50, fill="x")
        self.username_entry.focus_force()

        # Password label
        password_label = tk.Label(card_frame, text="Password", font=self.label_font, bg="#FFFFFF", fg="#424242")
        password_label.pack(pady=5)

        # Password entry
        self.password_entry = tk.Entry(card_frame, font=('Inter', 12), bd=1, relief="sunken", bg="#FFFFFF",
                                       insertbackground="#424242", show="*")
        self.password_entry.pack(pady=5, padx=50, fill="x")

        # Login button
        self.login_btn = tk.Button(card_frame, text="Login", font=self.button_font, bg="#2196F3", fg="#FFFFFF",
                                   relief="raised", bd=2, command=self.login)
        self.login_btn.pack(pady=20, padx=50, fill="x")

    def on_resize(self, event):
        if event.widget == self.root:
            # Store current input values
            current_username = self.username_entry.get() if hasattr(self, 'username_entry') and self.username_entry.winfo_exists() else ""
            current_password = self.password_entry.get() if hasattr(self, 'password_entry') and self.password_entry.winfo_exists() else ""
            self.draw_ui(event.width, event.height)
            # Restore input values
            self.username_entry.delete(0, tk.END)
            self.username_entry.insert(0, current_username)
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, current_password)

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

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        print(f"Username: '{username}', Password: '{password}'")

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        try:
            user = self.db.fetch_one("SELECT password_hash FROM users WHERE username = %s", (username,))
            if user and bcrypt.checkpw(password.encode('utf-8'), user[0].encode('utf-8')):
                self.root.destroy()
                MainWindow(username).run()
            else:
                messagebox.showerror("Error", "Invalid username or password.")
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")

    def run(self):
        self.root.mainloop()