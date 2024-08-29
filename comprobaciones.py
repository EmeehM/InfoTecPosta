import tkinter as ttk
import tkinter.messagebox


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

def Comprobacion_Clientes():
    return