import tkinter as ttk
import customtkinter as ctk
from hardware import Hardware
from clientes import Clientes

#Opciones de apariencia general
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("InfoTec")
        self.maxsize(width=1000, height=500)
        self.minsize(width=1000, height=500)
        #Dibujado de la pantalla en el centro mas o menos
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_x = round((screen_width / 2) - (1000 / 2))
        position_y = round((screen_height / 2) - (500 / 2))
        self.geometry(f"1200x800+{position_x}+{position_y}")

        # Container que tiene a los frames dentro
        container = ctk.CTkFrame(self)
        container.pack(side="right", fill="both", expand=True)

        self.frames = {}
        for F in (Hardware, Clientes):
            frame = F(parent=container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Clientes)

    def show_frame(self, page_class):
        frame = self.frames[page_class]
        frame.tkraise()

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
