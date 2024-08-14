import tkinter as ttk
import customtkinter as ctk

#Opciones de apariencia general
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class Hardware(ctk.CTkFrame):
    def __init__(self):
        super().__init__()

        self.titulo = ctk.CTkLabel(self,text="HARDWARE")
        self.titulo.pack(pady=10)

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("InfoTec")
        self.geometry("1200x800")

        #TODO: Revisar este codigo :D

        # Container to hold the frames
        container = ctk.CTkFrame(self)
        container.pack(side="right", fill="both", expand=True)

        self.frames = {}
        for F in (Hardware):
            frame = F(parent=container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Hardware)

    def show_frame(self, page_class):
        frame = self.frames[page_class]
        frame.tkraise()


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()