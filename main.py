import tkinter as ttk
import customtkinter as ctk

#Opciones de apariencia general
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("InfoTec")
        self.geometry("1200x800")


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()