import tkinter.ttk as ttk
from typing import Tuple
import customtkinter as ctk
from tkinter import *
import baseDeDatos
import clientes
import comprobaciones
import proveedores
import hardware
import datetime


class PedidoNuevo(ctk.CTkToplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title("Nuevo Pedido")
        self.geometry("600x500")
        self.maxsize(width=600, height=500)
        self.minsize(width=600, height=500)    

        fuente_general = ctk.CTkFont(family="Lucida Grande", size=20)
        Fuente_Titulos = ctk.CTkFont(family="Segoe UI", size=36, underline=True)

        ProductosAgregados = []

        def obtener_nuevo_id_pedido():
            ultimos_ids = baseDeDatos.obtener_ultimos_ids()
            nuevo_id = ultimos_ids['ultimo_id_pedidos'] + 1
            return nuevo_id

        def obtener_clientes():
            clientes = baseDeDatos.buscar_todos_clientes() 
            lista_clientes = [f"{cliente[0]} - {cliente[3]}" for cliente in clientes]
            lista_clientes.append("Nuevo Cliente")  
            return lista_clientes

        def obtener_productos():
            productos = baseDeDatos.buscar_todos_hardware()  
            lista_productos = [f"{producto[0]} - {producto[3]}" for producto in productos]
            return lista_productos

        def manejar_seleccion_cliente(event):
            seleccion = combo_clientes.get()
            print(seleccion)
            if seleccion == "Nuevo Cliente":
                controller.show_frame(clientes.Clientes)
                self.destroy()
            else:
                label_nombre_resultado.configure(text=seleccion)

        def agregar_producto(seleccion):
            ProductosAgregados.append(seleccion)
            altura = 290 
            for producto in ProductosAgregados:
                label = ctk.CTkLabel(self, text=producto, font=fuente_general)
            setattr(self, producto, label)
            label.place(x=340, y=altura)
            



        LA_TituloPed = ctk.CTkLabel(self,text="Pedido",font=Fuente_Titulos)
        LA_TituloPed.place(x=250, y=10)

        nuevo_id_pedido = obtener_nuevo_id_pedido()
        label_id_pedido = ctk.CTkLabel(self, text=f"ID Pedido: {nuevo_id_pedido}", font=fuente_general)
        label_id_pedido.place(x=30, y=30)

        # Combobox para seleccionar el cliente
        label_cliente = ctk.CTkLabel(self, text="Cliente:", font=fuente_general)
        label_cliente.place(x=30, y=90)

        lista_clientes = obtener_clientes()
        combo_clientes = ctk.CTkComboBox(self, values=lista_clientes, font=fuente_general,command=manejar_seleccion_cliente)
        combo_clientes.place(x=100,y=90)

        # Campo de texto para el nombre del cliente (rellenado automáticamente al seleccionar un cliente)
        label_nombre_cliente = ctk.CTkLabel(self, text="Nombre del Cliente:", font=fuente_general)
        label_nombre_cliente.place(x=30,y=150)

        label_nombre_resultado = ctk.CTkLabel(self, text="",font=fuente_general)
        label_nombre_resultado.place(x=210,y=150)

        # Mostrar la fecha y hora actual
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        label_fecha_hora = ctk.CTkLabel(self, text=f"Fecha y Hora: {fecha_actual}", font=fuente_general)
        label_fecha_hora.place(x=30, y=210)

        # Combobox para seleccionar el producto
        label_producto = ctk.CTkLabel(self, text="Producto:", font=fuente_general)
        label_producto.place(x=30, y=270)

        lista_productos = obtener_productos()
        combo_productos =ctk.CTkComboBox(self, values=lista_productos, font=fuente_general, width=170,)
        combo_productos.place(x=130, y=270)

        # Botón para agregar más productos
        boton_agregar_producto = ctk.CTkButton(self, text="Agregar Producto", font=fuente_general,
                                               command=lambda: agregar_producto(combo_productos.get()))
        boton_agregar_producto.place(x=400,y=270)



        # Función para agregar el pedido y los detalles
        def agregar_pedido():
            id_cliente_seleccionado = combo_clientes.get().split(" - ")[0]
            productos_seleccionados = combo_productos.get()
            baseDeDatos.crear_pedido(nuevo_id_pedido, id_cliente_seleccionado, fecha_actual, "Registrado")
            baseDeDatos.crear_detalle_pedido(nuevo_id_pedido, productos_seleccionados.split(" - ")[0], productos_seleccionados)
            self.destroy()

        # Botón para agregar el pedido
        boton_agregar = ctk.CTkButton(self, text="Agregar Pedido", font=fuente_general, command=agregar_pedido)
        boton_agregar.place(x=20, y=450)

        # Botón para cancelar y cerrar la ventana
        boton_cancelar = ctk.CTkButton(self, text="Cancelar", font=fuente_general, command=self.destroy,fg_color="#c0392b")
        boton_cancelar.place(x=200, y=450)

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
        self.BTN_Pedido = ctk.CTkButton(self, text="Nuevo Pedido", font=Fuente_General, height=50, width=280, command= lambda: PedidoNuevo(self,controller))
        self.BTN_Pedido.place(x=30, y=100)

        self.BTN_Factura = ctk.CTkButton(self, text="Nueva Factura", font=Fuente_General, height=50, width=280)
        self.BTN_Factura.place(x=30, y=180)

        self.BTN_Factura = ctk.CTkButton(self, text="Nuevo Pedido", font=Fuente_General, height=50, width=280)
        self.BTN_Factura.place(x=30, y=260)

        self.BTN_CancelarPedido = ctk.CTkButton(self, text="Cancelar Pedido", font=Fuente_General, height=50, width=280, fg_color="#c0392b", hover_color="#e74c3c")
        self.BTN_CancelarPedido.place(x=30, y=330)

        self.BTN_Pagar = ctk.CTkButton(self, text="Pagar Factura", font=Fuente_General, height=50, width=280,fg_color="#375ca9", hover_color="#112345")
        self.BTN_Pagar.place(x=30, y=400)

        self.BTN_BuscarPed = ctk.CTkButton(self, text="Buscar Pedido", font=Fuente_General, height=50, width=280, fg_color="#375ca9", hover_color="#112345")
        self.BTN_BuscarPed.place(x=340, y=400)

        self.LA_TituloUltimosPed = ctk.CTkLabel(self, text='Últimos pedidos:', font=Fuente_Caja)
        self.LA_TituloUltimosPed.place(x=340, y=100)

        PedidosLista = []
        PedidosLista = baseDeDatos.buscar_todos_pedidos()
        print(PedidosLista)
        if PedidosLista != None:
            j = 1
            for i in PedidosLista:
                nombrecompleto = 'a' + str(j)
                print(nombrecompleto)
                Ban += 1
                print(Ban)
                altura = 150 + 50 * (j - 1)
                if altura <= 380:
                    label = ctk.CTkLabel(self, text=i, font=Fuente_General)
                    setattr(self, nombrecompleto, label)
                    label.place(x=340, y=altura)  
                    j += 1
                
        

        #------------------------------------Caja------------------------------------
        self.LA_TituloCaja = ctk.CTkLabel(self, text='Caja diaria', font=Fuente_Titulos, text_color='#007090')
        self.LA_TituloCaja.place(x=760, y=100)

        self.LA_Caja = ctk.CTkLabel(self, text='$00000,00', font=Fuente_Caja)
        self.LA_Caja.place(x=760, y=170)

        #----------------------------------Tabla de pedidos-----------------------------------------