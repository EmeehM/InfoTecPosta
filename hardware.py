import tkinter.messagebox
import tkinter.ttk

import customtkinter as ctk
from tkinter import *

import baseDeDatos
import clientes
import comprobaciones
import proveedores
import ventas


class Hardware(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        Fuente_General = ctk.CTkFont(family="Lucida Grande", size=20)
        Fuente_Titulos = ctk.CTkFont(family="Segoe UI", size=36, underline=True)

        #------------Funciones------------------------------
        #CARGA DE ULTIMOS ID
        def ultimosID():
            ultimosIDvar = baseDeDatos.obtener_ultimos_ids()
            if (ultimosIDvar["ultimo_id_hardware"] != None):
                UltIdHard = ultimosIDvar["ultimo_id_hardware"] + 1
            else:
                UltIdHard = 1000

            if (ultimosIDvar["ultimo_id_tipohard"] != None):
                UltIdTipo = ultimosIDvar["ultimo_id_tipohard"] + 1
            else:
                UltIdTipo = 2000

            if (ultimosIDvar["ultimo_id_marca"] != None):
                UltIdMarca = ultimosIDvar["ultimo_id_marca"] + 1
            else:
                UltIdMarca = 3000

            return{
                "idTipo" : UltIdTipo,
                "idMarca" : UltIdMarca,
                "idHard" : UltIdHard
            }


        #CARGA MARCAS DE HARDWARE
        MarcasDeHard = baseDeDatos.obtener_marca()
        MarcasDeHard.insert(0, "-")
        MarcasDeHard.append("Agregar")

        #CARGA TIPOS DE HARDWARE
        TiposDeHard = baseDeDatos.obtener_tipos()
        TiposDeHard.insert(0, "-")
        TiposDeHard.append("Agregar")

        def AgregarHard():
            if(comprobaciones.Comprobacion_Hardware(self.IN_Nombre.get(),self.IN_Precio.get(),self.IN_Unidades.get())):
                baseDeDatos.agregar_hardware(ultimosID().get("idHard"),self.IN_Nombre.get(), self.IN_Precio.get(),
                                             self.IN_Unidades.get(), self.CB_TipoHard.get(),
                                             self.CB_MarcaHard.get())
                self.IdHardware.configure(text=f"ID-Hardware: {ultimosID().get("idHard")} ")


        def SeleccionTipo(seleccion):
            if(seleccion == "Agregar"):
                self.Dialog = ctk.CTkInputDialog(text="Agregar Nuevo tipo:", title="Tipo de Hardware",)
                Auxiliar=str(self.Dialog.get_input())
                if(Auxiliar != None and Auxiliar.strip() != "" and Auxiliar != "None"):
                    baseDeDatos.agregar_tipo(ultimosID().get("UltIdTipo"),Auxiliar)
                else:
                    tkinter.messagebox.showerror(title="Error",message="ERROR, el input no puede estar vacio!")
                TiposDeHard = baseDeDatos.obtener_tipos()
                TiposDeHard.insert(0, "-")
                TiposDeHard.append("Agregar")
                self.CB_TipoHard.configure(values=TiposDeHard)

        def SeleccionMarca(seleccion):
            if(seleccion == "Agregar"):
                self.Dialog = ctk.CTkInputDialog(text="Agregar Nueva Marca:", title="Marcas")
                Auxiliar=str(self.Dialog.get_input())
                if(Auxiliar != None and Auxiliar.strip() != "" and Auxiliar != "None"):
                    baseDeDatos.agregar_marca(ultimosID().get("UltIdMarca"),Auxiliar)
                else:
                    tkinter.messagebox.showerror(title="Error",message="ERROR, el input no puede estar vacio!")
                MarcasDeHard = baseDeDatos.obtener_marca()
                MarcasDeHard.insert(0, "-")
                MarcasDeHard.append("Agregar")
                self.CB_MarcaHard.configure(values=MarcasDeHard)

        def Busqueda(texto,seleccion):
            for items in self.TV_Busqueda.get_children():
                self.TV_Busqueda.delete(items)
            datos = []
            if(seleccion == "Id"):
                datos = baseDeDatos.buscar_hardware(id_hard=texto)
            if(seleccion == "Nombre"):
                datos = baseDeDatos.buscar_hardware(caracteristicas=texto)
            if(seleccion == "Tipo"):
                datos = baseDeDatos.buscar_hardware(tipo=texto)
            for fila in datos:
                self.TV_Busqueda.insert("", "end", values=fila)

        def modificar_seleccionado():
            # Obtener el ID del elemento seleccionado
            item_id = self.TV_Busqueda.focus()

            if item_id:  # Asegurarse de que hay un elemento seleccionado
                # Obtener los valores del elemento seleccionado
                item_values = self.TV_Busqueda.item(item_id, "values")

                # Aquí item_values debería contener los valores de la fila seleccionada
                id_hard = item_values[0]

                # Ahora llama a la función para modificar la base de datos
                baseDeDatos.modificar_hardware(
                    id_hard,
                    self.IN_Nombre.get(),
                    self.IN_Precio.get(),
                    self.IN_Unidades.get()
                )
                Busqueda("","Id")
        def eliminar_seleccionado():
            # Obtener el ID del elemento seleccionado
            item_id = self.TV_Busqueda.focus()

            if item_id:  # Asegurarse de que hay un elemento seleccionado
                # Obtener los valores del elemento seleccionado
                item_values = self.TV_Busqueda.item(item_id, "values")

                # Aquí item_values debería contener los valores de la fila seleccionada
                id_hard = item_values[0]

                # Ahora llama a la función para eliminar el registro
                baseDeDatos.eliminar_hardware(id_hard)
            Busqueda("", "Id")
            ultimosID = baseDeDatos.obtener_ultimos_ids()
            if (ultimosID["ultimo_id_hardware"] != None):
                UltIdHard = ultimosID["ultimo_id_hardware"] + 1
            else:
                UltIdHard = 1000
            self.IdHardware.configure(text=f"ID-Hardware: {UltIdHard} ")

        def eliminar_marca(marca):
            baseDeDatos.eliminar_marca(marca)
            MarcasDeHard = baseDeDatos.obtener_marca()
            MarcasDeHard.insert(0, "-")
            MarcasDeHard.append("Agregar")
            self.CB_MarcaHard.configure(values=MarcasDeHard)
            self.CB_MarcaHard.set(MarcasDeHard[0])
            ultimosID = baseDeDatos.obtener_ultimos_ids()

        def eliminar_tipo(tipo):
            baseDeDatos.eliminar_tipo(tipo)
            TiposDeHard = baseDeDatos.obtener_tipos()
            TiposDeHard.insert(0, "-")
            TiposDeHard.append("Agregar")
            self.CB_TipoHard.configure(values=TiposDeHard)
            self.CB_TipoHard.set(TiposDeHard[0])

        #--------------------------Titulo------------------------------------------
        self.titulo = ctk.CTkLabel(self, text="Hardware", text_color="#007090", font=Fuente_Titulos)
        self.titulo.grid(row=0, column=0, padx=(10, 360), pady=(0,20))

        #--------------------Botones arriba a la derecha---------------------------
        self.controller = controller
        self.CambiarFrameCliente = ctk.CTkButton(self, text="Clientes", command=lambda: controller.show_frame(clientes.Clientes),font=Fuente_General)
        self.CambiarFrameCliente.grid(row=0, column=1, padx=10)

        self.CambiarFrameSocios = ctk.CTkButton(self, text="Proveedores", command=lambda: controller.show_frame(proveedores.Proveedores),font=Fuente_General)
        self.CambiarFrameSocios.grid(row=0, column=2, padx=10)

        self.CambiarFrameProveedores = ctk.CTkButton(self, text="Ventas", command=lambda: controller.show_frame(ventas.Ventas),font=Fuente_General)
        self.CambiarFrameProveedores.grid(row=0, column=3, padx=10)

        #-----------------------------------Inputs de datos-----------------------------------------
        self.IdHardware= ctk.CTkLabel(self,text=f"ID-Hardware: {ultimosID().get("idHard")} ",font=Fuente_General)
        self.IdHardware.grid(row=1, column=0,pady=(40,0),sticky="w",padx=(5,0))

        self.LA_TipoHard = ctk.CTkLabel(self, text="Tipo de Hardware:", font=Fuente_General)
        self.LA_TipoHard.grid(row=2, column=0, sticky="w",pady=(20,0),padx=(5,0))
        self.CB_TipoHard = ctk.CTkComboBox(self, values=TiposDeHard,font=Fuente_General, command=SeleccionTipo)
        self.CB_TipoHard.grid(row=2, column=0,sticky="w",padx=(180,0),pady=(20,0))
        self.BTN_EliminarTipo = ctk.CTkButton(self,text="Eliminar", width=5, command=lambda : eliminar_tipo(self.CB_TipoHard.get()))
        self.BTN_EliminarTipo.grid(row=2,padx=(200,0),pady=(20,0))

        self.LA_MarcaHard = ctk.CTkLabel(self, text="Marca de Hardware:", font=Fuente_General)
        self.LA_MarcaHard.grid(row=3, column=0, sticky="w", pady=(20, 0),padx=(5,0))
        self.CB_MarcaHard = ctk.CTkComboBox(self, values=MarcasDeHard, font=Fuente_General, command=SeleccionMarca)
        self.CB_MarcaHard.grid(row=3, column=0, sticky="w", padx=(190, 0), pady=(20, 0))
        self.BTN_EliminarMarca = ctk.CTkButton(self, text="Eliminar", width=5,command=lambda : eliminar_marca(self.CB_MarcaHard.get()))
        self.BTN_EliminarMarca.grid(row=3, padx=(210, 0), pady=(20, 0))

        self.LA_Nombre= ctk.CTkLabel(self,text="Nombre del Componente:",font=Fuente_General)
        self.LA_Nombre.grid(row=4,column=0,sticky="w",pady=(20,0),padx=(5,0))
        self.IN_Nombre = ctk.CTkEntry(self,placeholder_text="Nombre",font=Fuente_General)
        self.IN_Nombre.grid(row=4,column=0,padx=(245,0),sticky="w",pady=(20,0))

        self.LA_Precio = ctk.CTkLabel(self, text="Precio del Componente:", font=Fuente_General)
        self.LA_Precio.grid(row=5, column=0, sticky="w", pady=(20, 0),padx=(5,0))
        self.IN_Precio = ctk.CTkEntry(self, placeholder_text="Precio", font=Fuente_General)
        self.IN_Precio.grid(row=5, column=0, padx=(230, 0), sticky="w", pady=(20, 0))

        self.LA_Unidades = ctk.CTkLabel(self, text="Cantidad de Unidades:", font=Fuente_General)
        self.LA_Unidades.grid(row=6, column=0, sticky="w", pady=(20, 0),padx=(5,0))
        self.IN_Unidades = ctk.CTkEntry(self, placeholder_text="Unidades", font=Fuente_General)
        self.IN_Unidades.grid(row=6, column=0, padx=(218, 0), sticky="w", pady=(20, 0))
        #------------------------------GROUPBOX-------------------------------------------------------------------------
        self.CB_Busqueda = ctk.CTkComboBox(self, width=130, height=30,font=Fuente_General,values=["-","Id","Nombre","Tipo"])
        self.CB_Busqueda.place(x=450, y=100)

        self.IN_Busqueda = ctk.CTkEntry(self, width=260, height=30,font=Fuente_General,placeholder_text="Busqueda")
        self.IN_Busqueda.place(x=600, y=100)

        self.BT_Busqueda = ctk.CTkButton(self, width=100, text="Buscar", font=Fuente_General, command=lambda: Busqueda(self.IN_Busqueda.get(),self.CB_Busqueda.get()))
        self.BT_Busqueda.place(x=870, y=100)

        columnas = ["ID", "Caracteristicas", "Precio Unitario", "Unidades Disponibles", "Tipo", "Marca"]
        self.TV_Busqueda = tkinter.ttk.Treeview(self,columns=columnas, height=13, show="headings")
        self.TV_Busqueda.place(x=450, y=150)
        for col in columnas:
            self.TV_Busqueda.heading(col, text=col)
            self.TV_Busqueda.column(col, width=90)


        #---------------------------------Botones de Abajo-------------------------------------------------------------
        self.BTN_Carga = ctk.CTkButton(self, text="Cargar", command=lambda: AgregarHard())
        self.BTN_Carga.grid(row=7, column=0,padx=(10,170), sticky="we")

        self.BTN_Modificar = ctk.CTkButton(self, text="Modificar",font=Fuente_General, command=lambda: modificar_seleccionado())
        self.BTN_Modificar.grid(row=7, column=2,pady=(80,10))

        self.BTN_Eliminar = ctk.CTkButton(self,text="Eliminar",fg_color="#c0392b",hover_color="#e74c3c",font= Fuente_General,command=lambda: eliminar_seleccionado())
        self.BTN_Eliminar.grid(row=7,column=3, pady=(80,10))



