import tkinter .ttk

import customtkinter as ctk

import baseDeDatos
import comprobaciones
import hardware
import proveedores


class Clientes(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        Fuente_General = ctk.CTkFont(family="Lucida Grande", size=20)
        Fuente_Titulos = ctk.CTkFont(family="Segoe UI", size=36, underline=True)

        # ------------Funciones------------------------------
        # CARGA DE ULTIMOS ID
        def ultimoID():
            ultimosIDvar = baseDeDatos.obtener_ultimos_ids()
            if (ultimosIDvar["ultimo_id_clientes"] != None):
                UltIdCliente = ultimosIDvar["ultimo_id_clientes"] + 1
            else:
                UltIdCliente = 1000
            return UltIdCliente

        def cargar_cliente(DNI,CUIT,Nombre,Dir,Tel,Correo,Socio,Gerente):
            if comprobaciones.Comprobacion_Clientes(DNI, CUIT, Nombre, Dir, Tel, Correo):
                baseDeDatos.agregar_cliente(ultimoID(), DNI, CUIT, Nombre, Dir, Tel, Correo,
                                                Socio, Gerente)
                self.IdCliente.configure(text=f"ID-Cliente:{ultimoID()}")
            Busqueda("", "Id")

        def Busqueda(texto, seleccion):
            for items in self.TV_Busqueda.get_children():
                self.TV_Busqueda.delete(items)
            datos = []
            if (seleccion == "Id"):
                datos = baseDeDatos.buscar_clientes(id=texto)
            if (seleccion == "Nombre"):
                datos = baseDeDatos.buscar_clientes(Nombre=texto)
            if (seleccion == "DNI"):
                datos = baseDeDatos.buscar_clientes(DNI=texto)
            if (seleccion == "Socios"):
                datos = baseDeDatos.buscar_clientes(id=texto, Socio="1")
            for fila in datos:
                self.TV_Busqueda.insert("", "end", values=fila)

        def modificar_seleccionado():
            # Obtener el ID del elemento seleccionado
            item_id = self.TV_Busqueda.focus()

            if item_id:  # Asegurarse de que hay un elemento seleccionado
                # Obtener los valores del elemento seleccionado
                item_values = self.TV_Busqueda.item(item_id, "values")

                # Aquí item_values debería contener los valores de la fila seleccionada
                id_clientes = item_values[0]

                # Ahora llama a la función para modificar la base de datos
                baseDeDatos.modificar_clientes(
                    id_clientes,
                    self.IN_DNI.get(),
                    self.IN_CUIT.get(),
                    self.IN_Nombre.get(),
                    self.IN_Direccion.get(),
                    self.IN_Telefono.get(),
                    self.IN_Mail.get(),
                    self.CHK_Socio.get(),
                    self.CHK_SocioGerente.get()
                )
                Busqueda("", "Id")

        def eliminar_seleccionado():
            # Obtener el ID del elemento seleccionado
            item_id = self.TV_Busqueda.focus()

            if item_id:  # Asegurarse de que hay un elemento seleccionado
                # Obtener los valores del elemento seleccionado
                item_values = self.TV_Busqueda.item(item_id, "values")

                # Aquí item_values debería contener los valores de la fila seleccionada
                id_clientes = item_values[0]

                # Ahora llama a la función para eliminar el registro
                baseDeDatos.eliminar_clientes(id_clientes)
            Busqueda("", "Id")
            self.IdCliente.configure(text=f"ID-Cliente: {ultimoID()}")

        # --------------------------Titulo------------------------------------------
        self.titulo = ctk.CTkLabel(self, text="Clientes", text_color="#007090", font=Fuente_Titulos)
        self.titulo.grid(row=0, column=0, padx=(5, 360))

        # --------------------Botones arriba a la derecha---------------------------
        self.controller = controller
        self.CambiarFrameHardWare = ctk.CTkButton(self, text="Hardware",
                                                 command=lambda: controller.show_frame(hardware.Hardware),
                                                 font=Fuente_General)
        self.CambiarFrameHardWare.grid(row=0, column=1, padx=10)

        self.CambiarFrameSocios = ctk.CTkButton(self, text="Proveedores", command=lambda: controller.show_frame(proveedores.Proveedores),
                                                font=Fuente_General)
        self.CambiarFrameSocios.grid(row=0, column=2, padx=10)

        self.CambiarFrameProveedores = ctk.CTkButton(self, text="Ventas", command=lambda: controller.show_frame(),
                                                     font=Fuente_General)
        self.CambiarFrameProveedores.grid(row=0, column=3, padx=10)

        # -----------------------------------Inputs de datos-----------------------------------------
        self.IdCliente = ctk.CTkLabel(self, text=f"ID-Cliente: {ultimoID()} ", font=Fuente_General)
        self.IdCliente.grid(row=1, column=0, pady=(40, 0), sticky="w",padx=(5,0))

        self.LA_DNI = ctk.CTkLabel(self, text="DNI:", font=Fuente_General)
        self.LA_DNI.grid(row=2, column=0, sticky="w", pady=(20, 0),padx=(5,0))
        self.IN_DNI = ctk.CTkEntry(self, font=Fuente_General,placeholder_text="DNI")
        self.IN_DNI.grid(row=2, column=0, sticky="w", padx=(55, 0), pady=(20, 0))

        self.LA_CUIT = ctk.CTkLabel(self, text="CUIT:", font=Fuente_General)
        self.LA_CUIT.grid(row=3, column=0, sticky="w", pady=(20, 0),padx=(5,0))
        self.IN_CUIT = ctk.CTkEntry(self, font=Fuente_General,placeholder_text="CUIT")
        self.IN_CUIT.grid(row=3, column=0, sticky="w", padx=(70, 0), pady=(20, 0))

        self.LA_Nombre = ctk.CTkLabel(self, text="Nombre o Razon Social:", font=Fuente_General)
        self.LA_Nombre.grid(row=4, column=0, sticky="w", pady=(20, 0),padx=(5,0))
        self.IN_Nombre = ctk.CTkEntry(self, placeholder_text="Nombre", font=Fuente_General)
        self.IN_Nombre.grid(row=4, column=0, padx=(235, 0), sticky="w", pady=(20, 0))

        self.LA_Direccion = ctk.CTkLabel(self, text="Dirección:", font=Fuente_General)
        self.LA_Direccion.grid(row=5, column=0, sticky="w", pady=(20, 0),padx=(5,0))
        self.IN_Direccion = ctk.CTkEntry(self, placeholder_text="Dirección", font=Fuente_General)
        self.IN_Direccion.grid(row=5, column=0, padx=(105, 0), sticky="w", pady=(20, 0))

        self.LA_Telefono = ctk.CTkLabel(self, text="Teléfono:", font=Fuente_General)
        self.LA_Telefono.grid(row=6, column=0, sticky="w", pady=(20, 0),padx=(5,0))
        self.IN_Telefono = ctk.CTkEntry(self, placeholder_text="Teléfono", font=Fuente_General)
        self.IN_Telefono.grid(row=6, column=0, padx=(100, 0), sticky="w", pady=(20, 0))

        self.LA_Mail = ctk.CTkLabel(self, text="Mail:", font=Fuente_General)
        self.LA_Mail.grid(row=7, column=0, sticky="w", pady=(20, 0),padx=(5,0))
        self.IN_Mail = ctk.CTkEntry(self, placeholder_text="Mail", font=Fuente_General)
        self.IN_Mail.grid(row=7, column=0, padx=(60, 0), sticky="w", pady=(20, 0))

        self.CHK_Socio = ctk.CTkCheckBox(self, text="Socio")
        self.CHK_Socio.grid(row = 8, column=0, sticky="w",padx=(10,0),pady=(15,0))
        self.CHK_SocioGerente = ctk.CTkCheckBox(self, text="Socio Gerente")
        self.CHK_SocioGerente.grid(row=8, column=0, padx=(10,0),pady=(15,0))


        # ------------------------------GROUPBOX-------------------------------------------------------------------------
        self.CB_Busqueda = ctk.CTkComboBox(self, width=130, height=30, font=Fuente_General,
                                           values=["-", "Id", "Nombre", "DNI","Socios"])
        self.CB_Busqueda.place(x=450, y=100)

        self.IN_Busqueda = ctk.CTkEntry(self, width=260, height=30, font=Fuente_General, placeholder_text="Busqueda")
        self.IN_Busqueda.place(x=600, y=100)

        self.BT_Busqueda = ctk.CTkButton(self, width=100, text="Buscar", font=Fuente_General,
                                         command=lambda: Busqueda(self.IN_Busqueda.get(), self.CB_Busqueda.get()))
        self.BT_Busqueda.place(x=870, y=100)

        columnas = ["ID", "DNI", "CUIT", "Nombre", "Direccion", "Telefono", "Correo", "Socio", "Gerente"]
        self.TV_Busqueda = tkinter.ttk.Treeview(self, columns=columnas, height=13, show="headings")
        self.TV_Busqueda.place(x=450, y=150)
        for col in columnas:
            self.TV_Busqueda.heading(col, text=col)
            self.TV_Busqueda.column(col, width=58)

        # ---------------------------------Botones de Abajo-------------------------------------------------------------
        self.BTN_Carga = ctk.CTkButton(self, text="Cargar",
                                       command=lambda: cargar_cliente(self.IN_DNI.get(),
                                                                        self.IN_CUIT.get(),
                                                                        self.IN_Nombre.get(),
                                                                        self.IN_Direccion.get(),
                                                                        self.IN_Telefono.get(),
                                                                        self.IN_Mail.get(),
                                                                        self.CHK_Socio.get(),
                                                                        self.CHK_SocioGerente.get()))
        self.BTN_Carga.grid(row=9, column=0, padx=(10, 170), sticky="we", pady=(10,0))

        self.BTN_Modificar = ctk.CTkButton(self, text="Modificar", font=Fuente_General,
                                           command=lambda: modificar_seleccionado())
        self.BTN_Modificar.place(x=670,y=460)

        self.BTN_Eliminar = ctk.CTkButton(self, text="Eliminar", fg_color="#c0392b", hover_color="#e74c3c",
                                          font=Fuente_General, command=lambda: eliminar_seleccionado())
        self.BTN_Eliminar.place(x=830,y=460)