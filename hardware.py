import customtkinter as ctk

import clientes


class Hardware(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        Fuente_General = ctk.CTkFont(family="Lucida Grande", size=20)
        Fuente_Titulos = ctk.CTkFont(family="Segoe UI", size=36, underline=True)

        #------------Funciones------------------------------
        placeholder = 0o001
        TiposDeHard = ["-","Agregar"]
        MarcasDeHard = ["-","Agregar"]
        def SeleccionTipo(seleccion):
            if(seleccion == "Agregar"):
                TiposDeHard.append("a")
                self.CB_TipoHard.configure(values=TiposDeHard)

        def SeleccionMarca(seleccion):
            if(seleccion == "Agregar"):
                MarcasDeHard.append("a")
                self.CB_MarcaHard.configure(values=MarcasDeHard)


        #--------------------------Titulo------------------------------------------
        self.titulo = ctk.CTkLabel(self, text="Hardware", text_color="#007090", font=Fuente_Titulos)
        self.titulo.grid(row=0, column=0, padx=(5, 550))

        #--------------------Botones arriba a la derecha---------------------------
        self.controller = controller
        self.CambiarFrameCliente = ctk.CTkButton(self, text="Clientes", command=lambda: controller.show_frame(clientes.Clientes),font=Fuente_General)
        self.CambiarFrameCliente.grid(row=0, column=1, padx=10)
        self.CambiarFrameSocios = ctk.CTkButton(self, text="Socios", command=lambda: controller.show_frame(),font=Fuente_General)
        self.CambiarFrameSocios.grid(row=0, column=2, padx=10)
        self.CambiarFrameProveedores = ctk.CTkButton(self, text="Proveedores", command=lambda: controller.show_frame(),font=Fuente_General)
        self.CambiarFrameProveedores.grid(row=0, column=3, padx=10)

        #-----------------------------------Inputs de datos-----------------------------------------
        self.IdCliente= ctk.CTkLabel(self,text=f"ID-Hardware: {placeholder} ",font=Fuente_General)
        self.IdCliente.grid(row=1, column=0,pady=(40,0),sticky="w")

        self.LA_TipoHard = ctk.CTkLabel(self, text="Tipo de Hardware:", font=Fuente_General)
        self.LA_TipoHard.grid(row=2, column=0, sticky="w",pady=(20,0))
        self.CB_TipoHard = ctk.CTkComboBox(self, values=TiposDeHard,font=Fuente_General, command=SeleccionTipo)
        self.CB_TipoHard.grid(row=2, column=0,sticky="w",padx=(180,0),pady=(20,0))

        self.LA_MarcaHard = ctk.CTkLabel(self, text="Tipo de Hardware:", font=Fuente_General)
        self.LA_MarcaHard.grid(row=3, column=0, sticky="w", pady=(20, 0))
        self.CB_MarcaHard = ctk.CTkComboBox(self, values=MarcasDeHard, font=Fuente_General, command=SeleccionMarca)
        self.CB_MarcaHard.grid(row=3, column=0, sticky="w", padx=(180, 0), pady=(20, 0))

        self.LA_Nombre= ctk.CTkLabel(self,text="Nombre del Componente:",font=Fuente_General)
        self.LA_Nombre.grid(row=4,column=0,sticky="w",pady=(20,0))
        self.IN_Nombre = ctk.CTkEntry(self,placeholder_text="Nombre",font=Fuente_General)
        self.IN_Nombre.grid(row=4,column=0,padx=(245,0),sticky="w",pady=(20,0))