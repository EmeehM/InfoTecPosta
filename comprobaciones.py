import tkinter as ttk
import tkinter.messagebox
import re


def Comprobacion_Hardware(Nombre,Precio,Unidades):
    if(Precio.isdigit() and Unidades.isdigit()):
        if (Nombre != None and len(Nombre) <= 100):
            if (int(Precio) < 100000 and int(Precio) > 0):
                if (int(Unidades) > 99):
                    return True
                else:
                    tkinter.messagebox.showerror(title="Error en el ingreso de datos",
                                                 message="LA CANTIDAD DE UNIDADES DEBE SER DE MAS DE 3 CIFRAS")
                    return False
            else:
                tkinter.messagebox.showerror(title="Error en el ingreso de datos",
                                             message="EL PRECIO NO PUEDE SER MENOR A 0 NI MAYOR QUE 5 CIFRAS")
                return False
        else:
            tkinter.messagebox.showerror(title="Error en el ingreso de datos",
                                         message="EL NOMBRE NO PUEDE ESTAR VACIO NI SER MAYOR A 100")
            return False
    else:
        tkinter.messagebox.showerror(title="Error en el ingreso de datos",
                                     message="EN LOS CAMPOS PRECIO Y UNIDADES SOLO PUEDEN ESCRIBIRSE NUMEROS")
        return False

def Comprobacion_Clientes(DNI,CUIT,Nombre,Dir,Tel,Correo):
    if(DNI.isdigit() and CUIT.isdigit() and Tel.isdigit()):
        DNI = int(DNI)
        CUIT = int(CUIT)
        Tel = int(Tel)
        print(Correo)
        patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if(DNI>10000000 and DNI<99999999):
            if(CUIT>10000000000 and CUIT<99999999999):
                if(len(Nombre)<40 and Nombre !=None):
                    if(len(Dir)<50 and Dir != None):
                        if(Tel>1000000000 and Tel<9999999999):
                            if re.match(patron,str(Correo)):
                                return True
                            else:
                                tkinter.messagebox.showerror(title="Error en el ingreso de datos",
                                                             message="EL CORREO ESTA MAL INGRESADO")
                                return False
                        else:
                            tkinter.messagebox.showerror(title="Error en el ingreso de datos",
                                                         message="EL TELEFONO DEBE SER DE 20 CARACTERES")
                            return False
                    else:
                        tkinter.messagebox.showerror(title="Error en el ingreso de datos",
                                                     message="LA DIRECCION NO PUEDE SER NULO NI MUY LARGO")
                        return False
                else:
                    tkinter.messagebox.showerror(title="Error en el ingreso de datos",
                                                 message="EL NOMBRE NO PUEDE SER NULO NI MUY LARGO")
                    return False
            else:
                tkinter.messagebox.showerror(title="Error en el ingreso de datos",
                                             message="EL CUIT ES DISTINTO DE 11 DIGITOS")
                return False
        else:
            tkinter.messagebox.showerror(title="Error en el ingreso de datos",
                                         message="EL DNI ES DISTINTO DE 8 DIGITOS")
            return False
    else:
        tkinter.messagebox.showerror(title="Error en el ingreso de datos",
                                     message="EN LOS CAMPOS DNI, CUIT Y TELEFONO SOLO PUEDEN ESCRIBIRSE NUMEROS")
        return False

    return