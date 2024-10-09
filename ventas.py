import tkinter.ttk

import customtkinter as ctk
from tkinter import *

import baseDeDatos
import clientes
import comprobaciones
import proveedores
import hardware


class Ventas(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        Fuente_General = ctk.CTkFont(family="Lucida Grande", size=20)
        Fuente_Titulos = ctk.CTkFont(family="Segoe UI", size=36, underline=True)

        #------------Funciones------------------------------
        

        #--------------------------Titulo------------------------------------------
        self.titulo = ctk.CTkLabel(self, text="Ventas", text_color="#007090", font=Fuente_Titulos)
        self.titulo.grid(row=0, column=0, padx=(10, 360), pady=(0,20))

        #--------------------Botones arriba a la derecha---------------------------
        self.controller = controller
        self.CambiarFrameCliente = ctk.CTkButton(self, text="Clientes", command=lambda: controller.show_frame(clientes.Clientes),font=Fuente_General)
        self.CambiarFrameCliente.place(x=550, y=20)

        self.CambiarFrameSocios = ctk.CTkButton(self, text="Proveedores", command=lambda: controller.show_frame(proveedores.Proveedores),font=Fuente_General)
        self.CambiarFrameSocios.place(x=700, y=20)

        self.CambiarFrameProveedores = ctk.CTkButton(self, text="Hardware", command=lambda: controller.show_frame(hardware.Hardware),font=Fuente_General)
        self.CambiarFrameProveedores.place(x=850, y=20)

        #-----------------------------------Inputs de datos-----------------------------------------

        self.BTN_Pedido = ctk.CTkButton(self, text="Nuevo Pedido",font=Fuente_General,height=50,width=280)
        self.BTN_Pedido.place(x=30, y=100)

        self.BTN_Factura = ctk.CTkButton(self, text="Nueva Factura",font=Fuente_General,height=50,width=280)
        self.BTN_Factura.place(x=30, y=170)

        self.BTN_Factura = ctk.CTkButton(self, text="Nuevo Pedido",font=Fuente_General,height=50,width=280)
        self.BTN_Factura.place(x=30, y=240)


        #----------------------------------Tabla de pedidos-----------------------------------------
        self.CB_Busqueda = ctk.CTkComboBox(self, width=130, height=30, font=Fuente_General,
                                           values=["-", "Pedidos", "Facturas", "Prespuestos"])
        self.CB_Busqueda.place(x=450, y=100)

        self.IN_Busqueda = ctk.CTkEntry(self, width=260, height=30, font=Fuente_General, placeholder_text="Busqueda")
        self.IN_Busqueda.place(x=600, y=100)

        self.BT_Busqueda = ctk.CTkButton(self, width=100, text="Buscar", font=Fuente_General,)
        self.BT_Busqueda.place(x=870, y=100)

        columnas = ["ID", "DNI", "CUIT", "Nombre", "Direccion", "Telefono", "Correo", "Socio", "Gerente"]
        self.TV_Busqueda = tkinter.ttk.Treeview(self, columns=columnas, height=13, show="headings")
        self.TV_Busqueda.place(x=450, y=150)
        for col in columnas:
            self.TV_Busqueda.heading(col, text=col)
            self.TV_Busqueda.column(col, width=58)




