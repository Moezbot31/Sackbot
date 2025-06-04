import sys
import tkinter as tk
from tkinter import ttk
from auth import AuthManager
from video_engine import VideoEngine

class SackbotApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sackbot - Video Maker")
        self.geometry("1200x800")
        self.configure(bg="#181818")
        self.set_dark_theme()
        self.init_ui()

    def set_dark_theme(self):
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('.',
                        background='#181818',
                        foreground='#ffffff',
                        fieldbackground='#1e1e1e',
                        bordercolor='#242424',
                        highlightthickness=0)
        style.configure('TLabel', background='#181818', foreground='#ffffff')
        style.configure('TButton', background='#1e1e1e', foreground='#ffffff', borderwidth=1)
        style.map('TButton', background=[('active', '#242424')])

    def init_ui(self):
        label = ttk.Label(self, text="Welcome to Sackbot - Modern Video Creation Tool", font=("Segoe UI", 20))
        label.pack(pady=40)

if __name__ == "__main__":
    # Example usage of AuthManager and VideoEngine in headless mode
    auth = AuthManager()
    video = VideoEngine()
    print("[Auth] Registering user: ", auth.register('testuser', 'password123'))
    print("[Auth] Logging in: ", auth.login('testuser', 'password123'))
    print("[Auth] Is authenticated? ", auth.is_authenticated())
    print("[Video] Export stub: ", video.export_video('input.mp4', 'output.mp4'))
    # Uncomment below to run GUI if in a graphical environment
    # app = SackbotApp()
    # app.mainloop()
