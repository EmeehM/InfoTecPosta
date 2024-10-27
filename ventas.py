import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
from typing import Tuple
import customtkinter as ctk
from tkinter import *
import baseDeDatos
import clientes
import comprobaciones
import proveedores
import hardware
import datetime

class BuscarPedido(ctk.CTkToplevel):
    def __init__(self, parent,controller):
        super().__init__(parent)
        self.controller = controller
        self.title("Nueva Factura")
        self.geometry("600x500")
        self.maxsize(width=600, height=500)
        self.minsize(width=600, height=500)
        self.grab_set()

        fuente_general = ctk.CTkFont(family="Lucida Grande", size=20)
        Fuente_Titulos = ctk.CTkFont(family="Segoe UI", size=36, underline=True)


        def obtener_pedidos():
            clientes = baseDeDatos.buscar_todos_pedidos() 
            lista_clientes = [f"{cliente[0]} - {cliente[2]}" for cliente in clientes]
            lista_clientes.insert(0,"-") 
            return lista_clientes

        def manejar_seleccion_pedidos(event):
            seleccion = combo_pedidos.get().split(" - ")
            datosPedido = baseDeDatos.buscar_pedido(seleccion[0])
            label_nombre_resultado.configure(text=f" {datosPedido[1]} - {datosPedido[2]}")
            ProductosAgregados = baseDeDatos.buscar_detalle_pedido(datosPedido[0])
            label_estado_pedido.configure(text=f"Estado de Pedido : {datosPedido[4]}")
            label_fecha_hora.configure(text=f"Fecha y Hora:{datosPedido[3]} ")
            i=0
            MontoTotal = 0
            print(ProductosAgregados)
            for producto in ProductosAgregados:
                    altura = 330 +(30 * i)
                    label = ctk.CTkLabel(self, text=f"{ProductosAgregados[i][3]}, {ProductosAgregados[i][4]}, {ProductosAgregados[i][6]}, {ProductosAgregados[i][7]}   " , font=fuente_general)
                    setattr(self,"Productos", label)
                    label.place(x=30, y=altura)
                    MontoTotal = MontoTotal + ProductosAgregados[i][7]
                    i = i+1
                    print(i)
            label_monto_total.configure(text=f"Monto Total : {MontoTotal}")
            label_monto_final.configure(text=f"Monto Final : {MontoTotal * 1.21}")

            

        LA_TituloPed = ctk.CTkLabel(self,text="Buscar Pedidos",font=Fuente_Titulos)
        LA_TituloPed.place(x=230, y=10)

        label_estado_pedido = ctk.CTkLabel(self, text=f"Estado de Pedido :", font=fuente_general)
        label_estado_pedido.place(x=30, y=80)

        # Combobox para seleccionar el cliente
        label_pedido = ctk.CTkLabel(self, text="Pedido:", font=fuente_general)
        label_pedido.place(x=30, y=140)

        lista_clientes = obtener_pedidos()
        combo_pedidos = ctk.CTkComboBox(self, values=lista_clientes, font=fuente_general,command=manejar_seleccion_pedidos,width=250)
        combo_pedidos.place(x=100,y=140)

        # Campo de texto para el nombre del cliente (rellenado automáticamente al seleccionar un cliente)
        label_nombre_cliente = ctk.CTkLabel(self, text="Nombre del Cliente:", font=fuente_general)
        label_nombre_cliente.place(x=30,y=200)

        label_nombre_resultado = ctk.CTkLabel(self, text="",font=fuente_general)
        label_nombre_resultado.place(x=210,y=200)

        # Mostrar la fecha y hora actual
        label_fecha_hora = ctk.CTkLabel(self, text=f"Fecha y Hora: ", font=fuente_general)
        label_fecha_hora.place(x=30, y=260)

        label_Detalles = ctk.CTkLabel(self, text="Nombre------- Cantidad ---------PrecioU --------------PrecioTot")
        label_Detalles.place(x=10,y=290)
        # Función para agregar el pedido y los detalles

        label_monto_total = ctk.CTkLabel(self,text="Monto Total : ")
        label_monto_total.place(x=370,y=290)
        label_monto_final = ctk.CTkLabel(self,text="Monto Final : ")
        label_monto_final.place(x=370,y=340)

class CancelarPedido(ctk.CTkToplevel):
    def __init__(self, parent ,controller):
        super().__init__(parent)
        self.controller = controller
        self.title("Detalles de Pedido")
        self.geometry("300x300")
        self.maxsize(width=300, height=300)
        self.minsize(width=300, height=300)
        self.grab_set()

        def obtener_pedidos():
            clientes = baseDeDatos.buscar_todos_pedidos()
            lista_clientes = []
            print(clientes)
            for cliente in clientes:
                print(cliente[4])
                if cliente[4] != "Cancelado":
                    print("true")
                    lista_clientes.append(f"{cliente[0]} - {cliente[2]}")     
            lista_clientes.insert(0,"-") 
            print(lista_clientes)
            return lista_clientes


        def EliminarSel(event):
            seleccion = combo_pedidos.get().split(" - ")
            PedidoSeleccionado = baseDeDatos.buscar_pedido(seleccion[0])
            print(PedidoSeleccionado)
            if messagebox.askyesno(title="Eliminar Pedido", message="Desea Eliminar Este pedido?"):
                baseDeDatos.editar_pedido(id_pedido=PedidoSeleccionado[0],nueva_condicion="Cancelado",nueva_fecha=PedidoSeleccionado[3])
                self.destroy()


        titulo = ctk.CTkLabel(self,text="Eliminar Pedido")
        titulo.place(x=100,y=10)

        listaPed = obtener_pedidos()
        combo_pedidos = ctk.CTkComboBox(self, values=listaPed, command=EliminarSel)
        combo_pedidos.place(x=100,y=150)

class PedidoDetalles(ctk.CTkToplevel):
    def __init__(self, parent,id_pedido, controller):
        super().__init__(parent)
        self.controller = controller
        self.title("Detalles de Pedido")
        self.geometry("600x500")
        self.maxsize(width=600, height=500)
        self.minsize(width=600, height=500)
        self.grab_set()    

        fuente_general = ctk.CTkFont(family="Lucida Grande", size=20)
        Fuente_Titulos = ctk.CTkFont(family="Segoe UI", size=36, underline=True)
        i = 1
        ProductosAgregados = []

        def obtener_productos():
            productos = baseDeDatos.buscar_todos_hardware()
            lista_productos = [f"{producto[0]} - {producto[3]}" for producto in productos]
            lista_productos.insert(0,"-")
            lista_productos.append("Nuevo Hardware")
            return lista_productos

        def agregar_producto():
            print(ProductosAgregados)
            i=int(len(ProductosAgregados))
            print(i)
            Hardware = baseDeDatos.buscar_hardware(id_hard=IDHard.get().split(" - ")[0])
            Componente.configure(text=f"Nombre : {Hardware[0][1]}")
            Stock.configure(text=f"Stock disponible : {Hardware[0][3]}")
            PrecioUnitario.configure(text=f"Precio Unitario : {Hardware[0][2]}")
            PrecioTotal.configure(text=f"Precio Total : {Hardware[0][2] * int(Cantidad.get())}")
            ProductosAgregados.append([IDHard.get().split(" - ")[1],Cantidad.get()])
            print(ProductosAgregados)
            altura = 330 +(30 * i) 
            baseDeDatos.crear_detalle_pedido(id_pedido,IDHard.get().split(" - ")[0],IDHard.get().split(" - ")[1],Cantidad.get(),Stock.cget("text").split(" : ")[1]
                                             ,PrecioUnitario.cget("text").split(" : ")[1],PrecioTotal.cget("text").split(" : ")[1])
            messagebox.showinfo(title="Producto Cargado!",message="Producto cargado con exito!")
            
            label = ctk.CTkLabel(self, text=ProductosAgregados[-1], font=fuente_general)
            setattr(self, str(ProductosAgregados), label)
            label.place(x=30, y=altura)

        def manejar_seleccion_Hard(event):
            seleccion = []
            seleccion = IDHard.get().split(" - ")
            if seleccion == "Nuevo Hardware" : 
                controller.show_frame(hardware.Hardware)
                self.destroy()
            elif seleccion == "-":
                messagebox.showerror(title="ERROR",message="Elija Un cliente")
            elif Cantidad.get()== "" and seleccion != "Nuevo Hardware":
                messagebox.showerror(title="ERROR",message="Agregue una cantidad de productos")
                IDHard.set("-")
            else:
                Hardware = baseDeDatos.buscar_hardware(id_hard=seleccion[0])
                Componente.configure(text=f"Nombre : {Hardware[0][1]}")
                Stock.configure(text=f"Stock disponible : {Hardware[0][3]}")
                PrecioUnitario.configure(text=f"Precio Unitario : {Hardware[0][2]}")
                PrecioTotal.configure(text=f"Precio Total : {Hardware[0][2] * int(Cantidad.get())}")

        def Cerrar():
            if messagebox.askokcancel(title="Cerrar",message="Cerrar todo?") :
                PedidoNuevo.destroy(parent)
                self.destroy()
            

        Titulo = ctk.CTkLabel(self,text=f"Agregar el hardware que requiera al pedido: {id_pedido}",font=fuente_general)
        Titulo.place(x=10, y=10)

        lista_hard=obtener_productos()
        IDHard = ctk.CTkComboBox(self,values=lista_hard,command=manejar_seleccion_Hard)
        IDHard.place(x=10,y=60)

        Componente = ctk.CTkLabel(self,text=f"Nombre: ")
        Componente.place(x=10,y=100)

        Cantidad = ctk.CTkEntry(self,placeholder_text="Cantidad")
        Cantidad.place(x=10,y=140)
        
        Stock = ctk.CTkLabel(self,text="Stock disponible: ")
        Stock.place(x=10,y=180)
        
        PrecioUnitario = ctk.CTkLabel(self,text="Precio Unitario: ")
        PrecioUnitario.place(x=10,y=220)

        PrecioTotal = ctk.CTkLabel(self,text="Precio total: ")
        PrecioTotal.place(x=10,y=260)
        
        label_Detalles = ctk.CTkLabel(self, text="Nombre------- Cantidad")
        label_Detalles.place(x=10,y=320)

        AgregarProd = ctk.CTkButton(self,text="Agregar Producto",command=agregar_producto)
        AgregarProd.place(x=10,y=290)

        CerrarBTN = ctk.CTkButton(self,text="Finalizar",command=Cerrar)
        CerrarBTN.place(x=10,y=450)

class PedidoNuevo(ctk.CTkToplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title("Nuevo Pedido")
        self.geometry("600x500")
        self.maxsize(width=600, height=500)
        self.minsize(width=600, height=500)
        self.grab_set()

        fuente_general = ctk.CTkFont(family="Lucida Grande", size=20)
        Fuente_Titulos = ctk.CTkFont(family="Segoe UI", size=36, underline=True)

        def obtener_nuevo_id_pedido():
            ultimos_ids = baseDeDatos.obtener_ultimos_ids()
            if ultimos_ids['ultimo_id_pedidos'] != None:
                nuevo_id = ultimos_ids['ultimo_id_pedidos'] + 1
            else:
                nuevo_id = 1
            
            return nuevo_id

        def obtener_clientes():
            clientes = baseDeDatos.buscar_todos_clientes() 
            lista_clientes = [f"{cliente[0]} - {cliente[3]}" for cliente in clientes]
            lista_clientes.insert(0,"-")
            lista_clientes.append("Nuevo Cliente")  
            return lista_clientes

        def manejar_seleccion_cliente(event):
            seleccion = combo_clientes.get()
            if seleccion == "Nuevo Cliente":
                controller.show_frame(clientes.Clientes)
                self.destroy()
            else:
                label_nombre_resultado.configure(text=seleccion)
            
        LA_TituloPed = ctk.CTkLabel(self,text="Nuevo Pedido",font=Fuente_Titulos)
        LA_TituloPed.place(x=230, y=10)

        nuevo_id_pedido = obtener_nuevo_id_pedido()
        label_id_pedido = ctk.CTkLabel(self, text=f"ID Pedido: {nuevo_id_pedido}", font=fuente_general)
        label_id_pedido.place(x=30, y=80)

        # Combobox para seleccionar el cliente
        label_cliente = ctk.CTkLabel(self, text="Cliente:", font=fuente_general)
        label_cliente.place(x=30, y=140)

        lista_clientes = obtener_clientes()
        combo_clientes = ctk.CTkComboBox(self, values=lista_clientes, font=fuente_general,command=manejar_seleccion_cliente,width=250)
        combo_clientes.place(x=100,y=140)

        # Campo de texto para el nombre del cliente (rellenado automáticamente al seleccionar un cliente)
        label_nombre_cliente = ctk.CTkLabel(self, text="Nombre del Cliente:", font=fuente_general)
        label_nombre_cliente.place(x=30,y=200)

        label_nombre_resultado = ctk.CTkLabel(self, text="",font=fuente_general)
        label_nombre_resultado.place(x=210,y=200)

        # Mostrar la fecha y hora actual
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        label_fecha_hora = ctk.CTkLabel(self, text=f"Fecha y Hora: {fecha_actual}", font=fuente_general)
        label_fecha_hora.place(x=30, y=260)



        # Función para agregar el pedido y los detalles
        def agregar_pedido():
            if combo_clientes.get() == "-" or combo_clientes.get() == "":
                messagebox.showwarning(title="Error",message="SELECCIONE UN CLIENTE") 
            elif messagebox.askyesno(title="Cambiando de Ventana",message="Esta seguro de que los datos son correctos?") :
                id_cliente_seleccionado = combo_clientes.get().split(" - ")
                baseDeDatos.crear_pedido(id_cliente_seleccionado[0],id_cliente_seleccionado[1] , fecha_actual, "Registrado")
                PedidoDetalles(self, nuevo_id_pedido, controller)           
            else:
                print("Canceled")
            

        # Botón para agregar el pedido
        boton_agregar = ctk.CTkButton(self, text="Agregar Pedido", font=fuente_general, command=agregar_pedido)
        boton_agregar.place(x=20, y=450)

        # Botón para cancelar y cerrar la ventana
        boton_cancelar = ctk.CTkButton(self, text="Cancelar", font=fuente_general, command=self.destroy,fg_color="#c0392b")
        boton_cancelar.place(x=200, y=450)

class FacturaNuevo(ctk.CTkToplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title("Nueva Factura")
        self.geometry("600x500")
        self.maxsize(width=600, height=500)
        self.minsize(width=600, height=500)
        self.grab_set()

        fuente_general = ctk.CTkFont(family="Lucida Grande", size=20)
        Fuente_Titulos = ctk.CTkFont(family="Segoe UI", size=36, underline=True)

        
        def obtener_nuevo_id_factura():
            ultimos_ids = baseDeDatos.obtener_ultimos_ids()
            if ultimos_ids['ultimo_id_factura'] != None:
                nuevo_id = ultimos_ids['ultimo_id_factura'] + 1
            else:
                nuevo_id = 1
            return nuevo_id

        def obtener_pedidos():
            clientes = baseDeDatos.buscar_todos_pedidos() 
            lista_clientes = [f"{cliente[0]} - {cliente[2]}" for cliente in clientes]
            lista_clientes.insert(0,"-") 
            return lista_clientes

        def manejar_seleccion_pedidos(event):
            seleccion = combo_pedidos.get().split(" - ")
            datosPedido = baseDeDatos.buscar_pedido(seleccion[0])
            label_nombre_resultado.configure(text=f" {datosPedido[1]} - {datosPedido[2]}")
            ProductosAgregados = baseDeDatos.buscar_detalle_pedido(datosPedido[0])
            i=0
            MontoTotal = 0
            print(ProductosAgregados)
            for producto in ProductosAgregados:
                    altura = 330 +(30 * i)
                    label = ctk.CTkLabel(self, text=f"{ProductosAgregados[i][3]}, {ProductosAgregados[i][4]}, {ProductosAgregados[i][6]}, {ProductosAgregados[i][7]}   " , font=fuente_general)
                    setattr(self,"Productos", label)
                    label.place(x=30, y=altura)
                    MontoTotal = MontoTotal + ProductosAgregados[i][7]
                    i = i+1
                    print(i)
            label_monto_total.configure(text=f"Monto Total : {MontoTotal}")
            label_monto_final.configure(text=f"Monto Final : {MontoTotal * 1.21}")

            

        LA_TituloPed = ctk.CTkLabel(self,text="Nueva Factura",font=Fuente_Titulos)
        LA_TituloPed.place(x=230, y=10)

        nuevo_id_factura = obtener_nuevo_id_factura()
        label_id_pedido = ctk.CTkLabel(self, text=f"ID Factura: {nuevo_id_factura}", font=fuente_general)
        label_id_pedido.place(x=30, y=80)

        # Combobox para seleccionar el cliente
        label_pedido = ctk.CTkLabel(self, text="Pedido:", font=fuente_general)
        label_pedido.place(x=30, y=140)

        lista_clientes = obtener_pedidos()
        combo_pedidos = ctk.CTkComboBox(self, values=lista_clientes, font=fuente_general,command=manejar_seleccion_pedidos,width=250)
        combo_pedidos.place(x=100,y=140)

        # Campo de texto para el nombre del cliente (rellenado automáticamente al seleccionar un cliente)
        label_nombre_cliente = ctk.CTkLabel(self, text="Nombre del Cliente:", font=fuente_general)
        label_nombre_cliente.place(x=30,y=200)

        label_nombre_resultado = ctk.CTkLabel(self, text="",font=fuente_general)
        label_nombre_resultado.place(x=210,y=200)

        # Mostrar la fecha y hora actual
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        label_fecha_hora = ctk.CTkLabel(self, text=f"Fecha y Hora: {fecha_actual}", font=fuente_general)
        label_fecha_hora.place(x=30, y=260)

        label_Detalles = ctk.CTkLabel(self, text="Nombre------- Cantidad ---------PrecioU --------------PrecioTot")
        label_Detalles.place(x=10,y=290)
        # Función para agregar el pedido y los detalles

        label_monto_total = ctk.CTkLabel(self,text="Monto Total : ")
        label_monto_total.place(x=370,y=290)
        label_monto_final = ctk.CTkLabel(self,text="Monto Final : ")
        label_monto_final.place(x=370,y=340)

        combo_forma_pago = ctk.CTkComboBox(self,values=["Efectivo","Cheque","Credito"])
        combo_forma_pago.place(x=370,y=380)

        def agregar_factura():
            if combo_pedidos.get() == "-" or combo_pedidos.get() == "":
                messagebox.showwarning(title="Error",message="SELECCIONE UN PEDIDO") 
            elif messagebox.askyesno(title="Cambiando de Ventana",message="Esta seguro de que los datos son correctos?") :
                
                baseDeDatos.crear_factura(label_nombre_resultado.cget("text").split(" - ")[0],label_nombre_resultado.cget("text").split(" - ")[1],label_fecha_hora.cget("text")
                                          ,label_monto_final.cget("text").split(" : ")[1],label_monto_total.cget("text").split(" : ")[1],combo_forma_pago.get(),nuevo_id_factura)         
                self.destroy()
            else:
                print("Canceled")
            

        # Botón para agregar el pedido
        boton_agregar = ctk.CTkButton(self, text="Agregar Factura", font=fuente_general, command=agregar_factura)
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

        self.BTN_Factura = ctk.CTkButton(self, text="Nueva Factura", font=Fuente_General, height=50, width=280,command=lambda: FacturaNuevo(self,controller))
        self.BTN_Factura.place(x=30, y=180)

        self.BTN_Factura = ctk.CTkButton(self, text="", font=Fuente_General, height=50, width=280)
        self.BTN_Factura.place(x=30, y=260)

        self.BTN_CancelarPedido = ctk.CTkButton(self, text="Cancelar Pedido", font=Fuente_General, height=50, width=280, fg_color="#c0392b", hover_color="#e74c3c",command=lambda : CancelarPedido(self,controller))
        self.BTN_CancelarPedido.place(x=30, y=330)

        self.BTN_Pagar = ctk.CTkButton(self, text="Pagar Factura", font=Fuente_General, height=50, width=280,fg_color="#375ca9", hover_color="#112345")
        self.BTN_Pagar.place(x=30, y=400)

        self.BTN_BuscarPed = ctk.CTkButton(self, text="Buscar Pedido", font=Fuente_General, height=50, width=280, fg_color="#375ca9", hover_color="#112345", command=lambda : BuscarPedido(self,controller))
        self.BTN_BuscarPed.place(x=340, y=400)

        self.LA_TituloUltimosPed = ctk.CTkLabel(self, text='Últimos pedidos:', font=Fuente_Caja)
        self.LA_TituloUltimosPed.place(x=340, y=100)

        PedidosLista = []
        PedidosLista = baseDeDatos.buscar_todos_pedidos()
        if PedidosLista != None:
            j = 1
            for i in PedidosLista:
                nombrecompleto = 'a' + str(j)
                Ban += 1
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