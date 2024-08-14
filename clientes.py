import customtkinter as ctk

import hardware


class Clientes(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        Fuente_General = ctk.CTkFont(family="Lucida Grande", size=20)
        Fuente_Titulos = ctk.CTkFont(family="Segoe UI", size=36, underline=True)

        self.titulo = ctk.CTkLabel(self, text="CLIENTES")
        #self.titulo.pack(pady=10)

        self.controller = controller
        self.CambiarFrameCliente = ctk.CTkButton(self, text="Hardware", command=lambda: controller.show_frame(hardware.Hardware),font=Fuente_General)
        self.CambiarFrameCliente.grid(row=0, column=1, padx=10)
        self.CambiarFrameSocios = ctk.CTkButton(self, text="Socios", command=lambda: controller.show_frame(),
                                                font=Fuente_General)
        self.CambiarFrameSocios.grid(row=0, column=2, padx=10)
        self.CambiarFrameProveedores = ctk.CTkButton(self, text="Proveedores", command=lambda: controller.show_frame(),
                                                     font=Fuente_General)
        self.CambiarFrameProveedores.grid(row=0, column=3, padx=10)