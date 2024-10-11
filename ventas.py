import tkinter.ttk as ttk
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
        Fuente_Caja = ctk.CTkFont(family="Segoe UI", size=36)
        Ban = 0
        UltimosPedList = []

        #------------Funciones------------------------------


        #--------------------------Titulo------------------------------------------
        self.titulo = ctk.CTkLabel(self, text="Ventas", text_color="#007090", font=Fuente_Titulos)
        self.titulo.grid(row=0, column=0, padx=(10, 360), pady=(0, 20))

        #--------------------Botones arriba a la derecha---------------------------
        self.controller = controller
        self.CambiarFrameCliente = ctk.CTkButton(self, text="Clientes", command=lambda: controller.show_frame(clientes.Clientes), font=Fuente_General)
        self.CambiarFrameCliente.place(x=550, y=20)

        self.CambiarFrameSocios = ctk.CTkButton(self, text="Proveedores", command=lambda: controller.show_frame(proveedores.Proveedores), font=Fuente_General)
        self.CambiarFrameSocios.place(x=700, y=20)

        self.CambiarFrameProveedores = ctk.CTkButton(self, text="Hardware", command=lambda: controller.show_frame(hardware.Hardware), font=Fuente_General)
        self.CambiarFrameProveedores.place(x=850, y=20)

        #-----------------------------------Inputs de datos-----------------------------------------
        self.BTN_Pedido = ctk.CTkButton(self, text="Nuevo Pedido", font=Fuente_General, height=50, width=280)
        self.BTN_Pedido.place(x=30, y=100)

        self.BTN_Factura = ctk.CTkButton(self, text="Nueva Factura", font=Fuente_General, height=50, width=280)
        self.BTN_Factura.place(x=30, y=170)

        self.BTN_Factura = ctk.CTkButton(self, text="Nuevo Pedido", font=Fuente_General, height=50, width=280)
        self.BTN_Factura.place(x=30, y=240)

        self.BTN_CancelarPedido = ctk.CTkButton(self, text="Cancelar Pedido", font=Fuente_General, height=50, width=280, fg_color="#c0392b", hover_color="#e74c3c")
        self.BTN_CancelarPedido.place(x=30, y=310)

        self.BTN_Pagar = ctk.CTkButton(self, text="Pagar Factura", font=Fuente_General, height=50, width=280)
        self.BTN_Pagar.place(x=30, y=380)

        self.LA_TituloUltimosPed = ctk.CTkLabel(self, text='Últimos pedidos:', font=Fuente_Caja)
        self.LA_TituloUltimosPed.place(x=380, y=100)

        test = baseDeDatos.obtener_ultimos_ids()  # Get the latest IDs from the database
        j = 1
        for i in test:
            nombrecompleto = 'a' + str(j)
            print(nombrecompleto)
            Ban += 1
            print(Ban)

            label = ctk.CTkLabel(self, text=i, font=Fuente_General)
            setattr(self, nombrecompleto, label)
            label.place(x=380, y=150 + 50 * (j - 1))  # Adjust position dynamically
            j += 1

        #------------------------------------Caja------------------------------------
        self.LA_TituloCaja = ctk.CTkLabel(self, text='Caja diaria', font=Fuente_Titulos, text_color='#007090')
        self.LA_TituloCaja.place(x=760, y=100)

        self.LA_Caja = ctk.CTkLabel(self, text='$00000,00', font=Fuente_Caja)
        self.LA_Caja.place(x=760, y=170)

        #----------------------------------Tabla de pedidos-----------------------------------------