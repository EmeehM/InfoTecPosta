import tkinter.ttk
import customtkinter as ctk
import baseDeDatos
import clientes
import comprobaciones
import hardware
import ventas

class Proveedores(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        Fuente_General = ctk.CTkFont(family="Lucida Grande", size=20)
        Fuente_Titulos = ctk.CTkFont(family="Segoe UI", size=36, underline=True)

        # ------------Funciones------------------------------
        # CARGA DE ULTIMOS ID
        def ultimoID():
            ultimosIDvar = baseDeDatos.obtener_ultimos_ids()
            if (ultimosIDvar["ultimo_id_proveedores"] != None):
                UltIdProveedor = ultimosIDvar["ultimo_id_proveedores"] + 1
            else:
                UltIdProveedor = 1000
            return UltIdProveedor

        def cargar_proveedor(CUIT, Nombre, Dir, Tel, Correo, Categoria):
            if comprobaciones.Comprobacion_Proveedores(CUIT, Nombre, Dir, Tel, Correo,Categoria):
                baseDeDatos.agregar_proveedor(ultimoID(), CUIT, Nombre, Dir, Tel, Correo, Categoria)
                self.IdProveedor.configure(text=f"ID-Proveedor: {ultimoID()}")
            Busqueda("", "Id")

        def Busqueda(texto, seleccion):
            for items in self.TV_Busqueda.get_children():
                self.TV_Busqueda.delete(items)
            datos = []
            if (seleccion == "Id"):
                datos = baseDeDatos.buscar_proveedores(id=texto)
            if (seleccion == "Nombre"):
                datos = baseDeDatos.buscar_proveedores(Nombre=texto)
            if (seleccion == "CUIT"):
                datos = baseDeDatos.buscar_proveedores(CUIT=texto)
            for fila in datos:
                self.TV_Busqueda.insert("", "end", values=fila)

        def modificar_seleccionado():
            item_id = self.TV_Busqueda.focus()
            if item_id:
                item_values = self.TV_Busqueda.item(item_id, "values")
                id_proveedores = item_values[0]
                baseDeDatos.modificar_proveedores(
                    id_proveedores,
                    self.IN_CUIT.get(),
                    self.IN_Nombre.get(),
                    self.IN_Direccion.get(),
                    self.IN_Telefono.get(),
                    self.IN_Mail.get(),
                    self.IN_Categoria.get()
                )
                Busqueda("", "Id")

        def eliminar_seleccionado():
            item_id = self.TV_Busqueda.focus()
            if item_id:
                item_values = self.TV_Busqueda.item(item_id, "values")
                id_proveedores = item_values[0]
                baseDeDatos.eliminar_proveedores(id_proveedores)
            Busqueda("", "Id")
            self.IdProveedor.configure(text=f"ID-Proveedor: {ultimoID()}")

        # --------------------------Titulo------------------------------------------
        self.titulo = ctk.CTkLabel(self, text="Proveedores", text_color="#007090", font=Fuente_Titulos)
        self.titulo.grid(row=0, column=0, padx=(5, 360))

        # --------------------Botones arriba a la derecha---------------------------
        self.controller = controller
        self.CambiarFrameClientes = ctk.CTkButton(self, text="Clientes", command=lambda: controller.show_frame(clientes.Clientes),
                                                  font=Fuente_General)
        self.CambiarFrameClientes.grid(row=0, column=1, padx=10)

        self.CambiarFrameHardware = ctk.CTkButton(self, text="Hardware", command=lambda: controller.show_frame(hardware.Hardware),
                                                  font=Fuente_General)
        self.CambiarFrameHardware.grid(row=0, column=2, padx=10)

        self.CambiarFrameVentas = ctk.CTkButton(self, text="Ventas", command=lambda: controller.show_frame(ventas.Ventas),
                                                font=Fuente_General)
        self.CambiarFrameVentas.grid(row=0, column=3, padx=10)

        # -----------------------------------Inputs de datos-----------------------------------------
        self.IdProveedor = ctk.CTkLabel(self, text=f"ID-Proveedor: {ultimoID()} ", font=Fuente_General)
        self.IdProveedor.grid(row=1, column=0, pady=(40, 0), sticky="w", padx=(5, 0))

        self.LA_CUIT = ctk.CTkLabel(self, text="CUIT:", font=Fuente_General)
        self.LA_CUIT.grid(row=2, column=0, sticky="w", pady=(20, 0), padx=(5, 0))
        self.IN_CUIT = ctk.CTkEntry(self, font=Fuente_General, placeholder_text="CUIT")
        self.IN_CUIT.grid(row=2, column=0, sticky="w", padx=(55, 0), pady=(20, 0))

        self.LA_Nombre = ctk.CTkLabel(self, text="Nombre o Razon Social:", font=Fuente_General)
        self.LA_Nombre.grid(row=3, column=0, sticky="w", pady=(20, 0), padx=(5, 0))
        self.IN_Nombre = ctk.CTkEntry(self, placeholder_text="Nombre", font=Fuente_General)
        self.IN_Nombre.grid(row=3, column=0, padx=(220, 0), sticky="w", pady=(20, 0))

        self.LA_Direccion = ctk.CTkLabel(self, text="Dirección:", font=Fuente_General)
        self.LA_Direccion.grid(row=4, column=0, sticky="w", pady=(20, 0), padx=(5, 0))
        self.IN_Direccion = ctk.CTkEntry(self, placeholder_text="Dirección", font=Fuente_General)
        self.IN_Direccion.grid(row=4, column=0, padx=(105, 0), sticky="w", pady=(20, 0))

        self.LA_Telefono = ctk.CTkLabel(self, text="Teléfono:", font=Fuente_General)
        self.LA_Telefono.grid(row=5, column=0, sticky="w", pady=(20, 0), padx=(5, 0))
        self.IN_Telefono = ctk.CTkEntry(self, placeholder_text="Teléfono", font=Fuente_General)
        self.IN_Telefono.grid(row=5, column=0, padx=(100, 0), sticky="w", pady=(20, 0))

        self.LA_Mail = ctk.CTkLabel(self, text="Mail:", font=Fuente_General)
        self.LA_Mail.grid(row=6, column=0, sticky="w", pady=(20, 0), padx=(5, 0))
        self.IN_Mail = ctk.CTkEntry(self, placeholder_text="Mail", font=Fuente_General)
        self.IN_Mail.grid(row=6, column=0, padx=(60, 0), sticky="w", pady=(20, 0))

        self.LA_Categoria = ctk.CTkLabel(self, text="Categoría:", font=Fuente_General)
        self.LA_Categoria.grid(row=7, column=0, sticky="w", pady=(20, 0), padx=(5, 0))
        self.IN_Categoria = ctk.CTkEntry(self, placeholder_text="Categoría", font=Fuente_General)
        self.IN_Categoria.grid(row=7, column=0, padx=(100, 0), sticky="w", pady=(20, 0))

        # ------------------------------GROUPBOX-------------------------------------------------------------------------
        self.CB_Busqueda = ctk.CTkComboBox(self, width=130, height=30, font=Fuente_General,
                                           values=["-", "Id", "Nombre", "CUIT"])
        self.CB_Busqueda.place(x=450, y=100)

        self.IN_Busqueda = ctk.CTkEntry(self, width=260, height=30, font=Fuente_General, placeholder_text="Busqueda")
        self.IN_Busqueda.place(x=600, y=100)

        self.BT_Busqueda = ctk.CTkButton(self, width=100, text="Buscar", font=Fuente_General,
                                         command=lambda: Busqueda(self.IN_Busqueda.get(), self.CB_Busqueda.get()))
        self.BT_Busqueda.place(x=870, y=100)

        columnas = ["ID", "CUIT", "Nombre", "Direccion", "Telefono", "Correo", "Categoría"]
        self.TV_Busqueda = tkinter.ttk.Treeview(self, columns=columnas, height=13, show="headings")
        self.TV_Busqueda.place(x=450, y=150)
        for col in columnas:
            self.TV_Busqueda.heading(col, text=col)
            self.TV_Busqueda.column(col, width=75)

        # ---------------------------------Botones de Abajo-------------------------------------------------------------
        self.BTN_Carga = ctk.CTkButton(self, text="Cargar",
                                       command=lambda: cargar_proveedor(self.IN_CUIT.get(),
                                                                        self.IN_Nombre.get(),
                                                                        self.IN_Direccion.get(),
                                                                        self.IN_Telefono.get(),
                                                                        self.IN_Mail.get(),
                                                                        self.IN_Categoria.get()))
        self.BTN_Carga.grid(row=8, column=0, padx=(10, 170), sticky="we", pady=(10, 0))

        self.BTN_Modificar = ctk.CTkButton(self, text="Modificar", font=Fuente_General,
                                           command=lambda: modificar_seleccionado())
        self.BTN_Modificar.place(x=670,y=460)

        self.BTN_Eliminar = ctk.CTkButton(self, text="Eliminar", font=Fuente_General,fg_color="#c0392b", hover_color="#e74c3c",
                                          command=lambda: eliminar_seleccionado())
        self.BTN_Eliminar.place(x=830,y=460)