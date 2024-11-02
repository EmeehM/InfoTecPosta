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
        self.iconbitmap("Infotech_icon.ico")
        self.maxsize(width=600, height=500)
        self.minsize(width=600, height=500)
        self.grab_set()
        datos = []

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
            #-----------------TABLA--------------------------------------
            for items in self.TV_Busqueda.get_children():
                self.TV_Busqueda.delete(items)
            for items in ProductosAgregados:
                datos.append((ProductosAgregados[i][3],ProductosAgregados[i][4],ProductosAgregados[i][6],ProductosAgregados[i][7]))
                i = i+1
            for fila in datos:
                self.TV_Busqueda.insert("", "end", values=fila) 
            
            datos.clear()
            #----------------------------------------------------------
            MontoTotal = 0
            i=0
            for producto in ProductosAgregados: 
                    MontoTotal = MontoTotal + ProductosAgregados[i][7]
            label_monto_total.configure(text=f"Monto Total : {MontoTotal}")
            label_monto_final.configure(text=f"Monto Final : {MontoTotal * 1.21}")

            

        LA_TituloPed = ctk.CTkLabel(self,text="Buscar Pedidos",font=Fuente_Titulos,text_color="#007090")
        LA_TituloPed.place(x=210, y=10)

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

        columnas = ["Nombre", "Cantidad", "Precio U", "Precio Total"]
        self.TV_Busqueda = ttk.Treeview(self, columns=columnas, height=8, show="headings")
        self.TV_Busqueda.place(x=10, y=290)
        for col in columnas:
            self.TV_Busqueda.heading(col, text=col)
            self.TV_Busqueda.column(col, width=80)

        label_monto_total = ctk.CTkLabel(self,text="Monto Total : ",font=fuente_general)
        label_monto_total.place(x=370,y=290)
        label_monto_final = ctk.CTkLabel(self,text="Monto Final : ",font=fuente_general)
        label_monto_final.place(x=370,y=340)

class CancelarPedido(ctk.CTkToplevel):
    def __init__(self, parent ,controller):
        super().__init__(parent)
        self.controller = controller
        self.title("Detalles de Pedido")
        self.geometry("300x300")
        self.iconbitmap("Infotech_icon.ico")
        self.maxsize(width=300, height=300)
        self.minsize(width=300, height=300)
        self.grab_set()

        def obtener_pedidos():
            clientes = baseDeDatos.buscar_todos_pedidos()
            lista_clientes = []
            for cliente in clientes:
                if cliente[4] != "Cancelado":
                    lista_clientes.append(f"{cliente[0]} - {cliente[2]}")     
            lista_clientes.insert(0,"-") 
            return lista_clientes


        def EliminarSel(event):
            seleccion = combo_pedidos.get().split(" - ")
            PedidoSeleccionado = baseDeDatos.buscar_pedido(seleccion[0])
            if messagebox.askyesno(title="Eliminar Pedido", message="Desea Eliminar Este pedido?"):
                baseDeDatos.editar_pedido(id_pedido=PedidoSeleccionado[0],nueva_condicion="Cancelado",nueva_fecha=PedidoSeleccionado[3])
                self.destroy()


        titulo = ctk.CTkLabel(self,text="Eliminar Pedido")
        titulo.place(x=100,y=10)

        listaPed = obtener_pedidos()
        combo_pedidos = ctk.CTkComboBox(self, values=listaPed, command=EliminarSel)
        combo_pedidos.place(x=100,y=150)

class PedidoDetalles(ctk.CTkToplevel):
    def __init__(self, parent,id_pedido, controller,id_cliente_seleccionado,fecha_actual):
        super().__init__(parent)
        self.controller = controller
        self.title("Detalles de Pedido")
        self.geometry("600x500")
        self.iconbitmap("Infotech_icon.ico")
        self.maxsize(width=600, height=500)
        self.minsize(width=600, height=500)
        self.grab_set()    

        fuente_general = ctk.CTkFont(family="Lucida Grande", size=20)
        Fuente_Titulos = ctk.CTkFont(family="Segoe UI", size=36, underline=True)
        i = 1
        Ban = 0
        ProductosAgregados = []
        datos = []

        #-------------------PRIMERA CARGA--------------------------------
        if baseDeDatos.buscar_pedido(id_pedido=id_pedido) != None:
            ProductosAgregados = baseDeDatos.buscar_detalle_pedido(id_pedido=id_pedido)
            #for items in productos meter en datos
            for items in self.TV_Busqueda.get_children():
                self.TV_Busqueda.delete(items)
            for fila in datos:
                self.TV_Busqueda.insert("", "end", values=fila)
            print("a")

        #---------------------------------------------------------------
        def obtener_productos():
            productos = baseDeDatos.buscar_todos_hardware()
            lista_productos = [f"{producto[0]} - {producto[3]}" for producto in productos]
            lista_productos.insert(0,"-")
            lista_productos.append("Nuevo Hardware")
            return lista_productos

        def agregar_producto():
            i=int(len(ProductosAgregados))
            Hardware = baseDeDatos.buscar_hardware(id_hard=IDHard.get().split(" - ")[0])
            if int(Hardware[0][3]) >= int(Cantidad.get()):
                Stock.configure(text=f"Stock disponible : {Hardware[0][3]}")
                PrecioUnitario.configure(text=f"Precio Unitario : {Hardware[0][2]}")
                PrecioTotal.configure(text=f"Precio Total : {Hardware[0][2] * int(Cantidad.get())}")
                ProductosAgregados.append([id_pedido,IDHard.get().split(" - ")[0],IDHard.get().split(" - ")[1],Cantidad.get(),Stock.cget("text").split(" : ")[1]
                                                ,PrecioUnitario.cget("text").split(" : ")[1],PrecioTotal.cget("text").split(" : ")[1]])
                
                messagebox.showinfo(title="Producto Cargado!",message="Producto cargado con exito!")

                datos.append((Hardware[0][0],Hardware[0][1],Hardware[0][3],Cantidad.get()))
                for items in self.TV_Busqueda.get_children():
                    self.TV_Busqueda.delete(items)
                for fila in datos:
                    self.TV_Busqueda.insert("", "end", values=fila)
            else:
                messagebox.showerror(title="Stock Insuficiente",message="No tiene suficiente stock de este producto!")
                
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
                if datos != None and datos != [] and datos != "None":
                    if baseDeDatos.buscar_pedido(id_pedido=id_pedido) == None and ProductosAgregados[0]<6:
                        baseDeDatos.crear_pedido(id_cliente_seleccionado[0],id_cliente_seleccionado[1] , fecha_actual, "Registrado")
                        i=0
                        for items in ProductosAgregados:
                            baseDeDatos.crear_detalle_pedido(ProductosAgregados[i][0],ProductosAgregados[i][1],ProductosAgregados[i][2],ProductosAgregados[i][3],
                                                            ProductosAgregados[i ][4],ProductosAgregados[i][5],ProductosAgregados[i][6])
                            i = i + 1
                        PedidoNuevo.destroy(parent)
                    else:
                        for items in ProductosAgregados:
                            baseDeDatos.eliminar_detalle_pedido(ProductosAgregados[0])
                    self.destroy()
                #else:
                    #messagebox.showerror(title="Agregar Productos",message="Añada por lo menos 1 producto al pedido!")
                
        
        def Editar():
            item_id = self.TV_Busqueda.focus()
            if item_id:
                item_values = self.TV_Busqueda.item(item_id, "values")
                i = 0
                #TODO:Cambiar Tambien los precios xd
                print(len(ProductosAgregados[0]))
                if len(ProductosAgregados[0]) == 7:
                    print("entro 1a")
                    for items in ProductosAgregados:
                        print("entro 1b")
                        print(datos[i])
                        if int(ProductosAgregados[i][1]) == int(item_values[0]) and int(datos[i][0]) == int(item_values[0]):
                            print("entro 1c")
                            if ProductosAgregados[i][4]>int(Cantidad.get):
                                print("entro 1d")
                                ProductosAgregados[i][4] = int(Cantidad.get)
                                datos[i][3] = int(Cantidad.get)
                                messagebox.showinfo(title="Edicion Realizada", message="Edicion Realizada Con exito!")
                    i=i+1
                elif len(ProductosAgregados[0]) == 8:
                    for items in ProductosAgregados:
                        if ProductosAgregados[i][2] == item_values[0] and datos[i][0] == item_values[0]:
                            if ProductosAgregados[i][5]>int(Cantidad.get):
                                ProductosAgregados[i][5] = int(Cantidad.get)
                                datos[i][3] = int(Cantidad.get)
                                messagebox.showinfo(title="Edicion Realizada", message="Edicion Realizada Con exito!")
                    i=i+1
                print(ProductosAgregados)
                for items in self.TV_Busqueda.get_children():
                    self.TV_Busqueda.delete(items)
                for fila in datos:
                    self.TV_Busqueda.insert("", "end", values=fila)
                   

            

        Titulo = ctk.CTkLabel(self,text=f"Hardware al pedido: {id_pedido}",font=Fuente_Titulos)
        Titulo.place(x=10, y=8)

        LBL_Cantidad = ctk.CTkLabel(self,text="Cantidad:",font=fuente_general)
        LBL_Cantidad.place(x=10,y=60)
        Cantidad = ctk.CTkEntry(self,placeholder_text="Cantidad",font=fuente_general)
        Cantidad.place(x=100,y=60)

        Componente = ctk.CTkLabel(self,text=f"Nombre: ",font=fuente_general)
        Componente.place(x=250,y=60)
        lista_hard=obtener_productos()
        IDHard = ctk.CTkComboBox(self,values=lista_hard,command=manejar_seleccion_Hard)
        IDHard.place(x=330,y=60)

        PrecioUnitario = ctk.CTkLabel(self,text="Precio Unitario: ",font=fuente_general)
        PrecioUnitario.place(x=10,y=100)

        PrecioTotal = ctk.CTkLabel(self,text="Precio total: ",font=fuente_general)
        PrecioTotal.place(x=10,y=140)
        
        Stock = ctk.CTkLabel(self,text="Stock disponible: ",font=fuente_general)
        Stock.place(x=250,y=100)
        
        AgregarProd = ctk.CTkButton(self,text="Agregar Producto",command=agregar_producto,font=fuente_general)
        AgregarProd.place(x=10,y=180)

        columnas = ["ID","Nombre","Stock Disponible","Cantidad Pedida"]
        self.TV_Busqueda = ttk.Treeview(self, columns=columnas, height=8, show="headings")
        self.TV_Busqueda.place(x=10, y=240)
        for col in columnas:
            self.TV_Busqueda.heading(col, text=col)
            self.TV_Busqueda.column(col, width=75)

        EditarBTN = ctk.CTkButton(self,text="Editar", command=Editar,font=fuente_general)
        EditarBTN.place(x=10,y=450)
        EliminarBTN = ctk.CTkButton(self,text="Eliminar",font=fuente_general)
        CerrarBTN = ctk.CTkButton(self,text="Finalizar",command=Cerrar,font=fuente_general,fg_color="#c0392b", hover_color="#e74c3c")
        CerrarBTN.place(x=400,y=450)

class PedidoNuevo(ctk.CTkToplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title("Nuevo Pedido")
        self.iconbitmap("Infotech_icon.ico")
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
                PedidoDetalles(self, nuevo_id_pedido, controller, id_cliente_seleccionado, fecha_actual)       
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
        self.iconbitmap("Infotech_icon.ico")
        self.maxsize(width=600, height=500)
        self.minsize(width=600, height=500)
        self.grab_set()

        datos = []
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
            #-----------------TABLA--------------------------------------
            for items in self.TV_Busqueda.get_children():
                self.TV_Busqueda.delete(items)
            for items in ProductosAgregados:
                datos.append((ProductosAgregados[i][3],ProductosAgregados[i][4],ProductosAgregados[i][5],ProductosAgregados[i][6],ProductosAgregados[i][7]))
                i = i+1
            for fila in datos:
                self.TV_Busqueda.insert("", "end", values=fila) 
            
            datos.clear()
            #---------------------------------------------------------
            i=0
            for producto in ProductosAgregados:
                    MontoTotal = MontoTotal + ProductosAgregados[i][7]
                    i = i+1
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

        columnas = ["Nombre", "Cantidad", "Stock","Precio U", "Precio Total"]
        self.TV_Busqueda = ttk.Treeview(self, columns=columnas, height=6, show="headings")
        self.TV_Busqueda.place(x=10, y=290)
        for col in columnas:
            self.TV_Busqueda.heading(col, text=col)
            self.TV_Busqueda.column(col, width=80)

        label_monto_total = ctk.CTkLabel(self,text="Monto Total : ", font=fuente_general)
        label_monto_total.place(x=415,y=290)
        label_monto_final = ctk.CTkLabel(self,text="Monto Final : ", font=fuente_general)
        label_monto_final.place(x=415,y=340)

        combo_forma_pago = ctk.CTkComboBox(self,values=["Efectivo","Cheque","Credito"], font=fuente_general)
        combo_forma_pago.place(x=415,y=380)

        def agregar_factura():
            if combo_pedidos.get() == "-" or combo_pedidos.get() == "":
                messagebox.showwarning(title="Error",message="SELECCIONE UN PEDIDO") 
            elif messagebox.askyesno(title="Cambiando de Ventana",message="Esta seguro de que los datos son correctos?") :
                #TODO: ANTES DE AGREGAR UNA FACTURA INTENTAR RESTAR STOCK - CANTIDAD SI DA NEGATIVO MOSTRAR LA VENTANA DE HARDWARE PARA CAMBIARLO Y AGREGAR FUNCION DE ELIMINAR/EDITAR PA LOS QUE YA ESTAN ASDASDASDASFADSGMNSFKDL
                baseDeDatos.crear_factura(label_nombre_resultado.cget("text").split(" - ")[0],label_nombre_resultado.cget("text").split(" - ")[1],label_fecha_hora.cget("text")
                                          ,label_monto_final.cget("text").split(" : ")[1],label_monto_total.cget("text").split(" : ")[1],combo_forma_pago.get(),combo_pedidos.get().split(" - ")[0])
                baseDeDatos.editar_pedido(id_pedido=combo_pedidos.get().split(" - ")[0],nueva_condicion="Facturado")
                self.destroy()
            else:
                print("Canceled")

        def agregar_presupuesto():
            if combo_pedidos.get() == "-" or combo_pedidos.get() == "":
                messagebox.showwarning(title="Error",message="SELECCIONE UN PEDIDO") 
            elif messagebox.askyesno(title="Cambiando de Ventana",message="Esta seguro de que los datos son correctos?") :
                #TODO: MOSTRAR ESTO EN ALGUN LADO? NI IDEA PARA QUE ES XD, CAPAZ UN PDF O ALGO ASI???
                baseDeDatos.crear_presupuesto(fecha_actual,label_monto_final.cget("text").split(" : ")[1],label_monto_total.cget("text").split(" : ")[1],combo_forma_pago.get(),combo_pedidos.get().split(" - ")[0])
                baseDeDatos.editar_pedido(id_pedido=combo_pedidos.get().split(" - ")[0],nueva_condicion="Presupuestado")
                self.destroy()
            else:
                print("Canceled")
            

        # Botón para agregar el pedido
        boton_agregar = ctk.CTkButton(self, text="Agregar Factura", font=fuente_general, command=agregar_factura)
        boton_agregar.place(x=20, y=450)

        # Botón para cancelar y cerrar la ventana
        boton_cancelar = ctk.CTkButton(self, text="Cancelar", font=fuente_general, command=self.destroy,fg_color="#c0392b")
        boton_cancelar.place(x=200, y=450)

        boton_agregar = ctk.CTkButton(self, text="Presupuestar", font=fuente_general, command=agregar_presupuesto)
        boton_agregar.place(x=380, y=450)

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
        #TODO: ESTE BOTON DEBERIA SER PARA LA PARTE 3 DE MOSTRAR LOS PAGOS O NSQ CREO, HAY ALGO MAS QUE FALTA CREO
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
                