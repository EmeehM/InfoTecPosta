import sqlite3
import tkinter

import comprobaciones

# Conectar a la base de datos
conn = sqlite3.connect('HardwareDB.db')
cursor = conn.cursor()

#-------------------------------------------BUSQUEDA--------------------------------------------------------------------
# Función para buscar registros
def buscar_hardware(caracteristicas=None, tipo=None, id_hard=None):
    query = "SELECT * FROM HardwareView WHERE 1=1"
    params = []

    if caracteristicas:
        query += " AND Caracteristicas LIKE ?"
        params.append(f"%{caracteristicas}%")

    if tipo:
        query += " AND Tipo_Hardware LIKE ?"
        params.append(f"%{tipo}%")

    if id_hard:
        query += " AND ID_Hard = ?"
        params.append(id_hard)

    cursor.execute(query, params)
    resultados = cursor.fetchall()

    return resultados
# Función para modificar un registro
def modificar_hardware(id_hard, nuevas_caracteristicas=None, nuevo_precio=None, nuevas_unidades=None):
    ban = False
    cursor.execute("SELECT * FROM Hardware WHERE ID_Hard = ?", (id_hard,))
    hardwareAux = cursor.fetchall()
    query = "UPDATE Hardware SET"
    params = []

    if nuevas_caracteristicas:
        if comprobaciones.Comprobacion_Hardware(nuevas_caracteristicas,hardwareAux[0][4],hardwareAux[0][5]):
            query += " Caracteristicas = ?,"
            params.append(nuevas_caracteristicas)
            ban = True


    if nuevo_precio:
        if comprobaciones.Comprobacion_Hardware(hardwareAux[0][3], nuevo_precio, hardwareAux[0][5]):
            query += " Precio_Unitario = ?,"
            params.append(nuevo_precio)
            ban = True


    if nuevas_unidades:
        if comprobaciones.Comprobacion_Hardware(hardwareAux[0][3], hardwareAux[0][4], nuevas_unidades):
            print(nuevas_unidades)
            query += " Unidades_Disponibles = ?,"
            params.append(nuevas_unidades)
            ban = True

    if ban:
        # Eliminar la última coma
        query = query.rstrip(',')

        query += " WHERE ID_Hard = ?"
        params.append(id_hard)

        cursor.execute(query, params)
        conn.commit()

def buscar_clientes(id = None, Nombre = None,DNI = None , Socio = None):
    if Socio:
        cursor.execute("SELECT * FROM ClientesSocios")
        resultados = cursor.fetchall()
    else:
        query = "SELECT * FROM Clientes WHERE 1=1"
        params = []

        if id:
            query += " AND ID_Clientes LIKE ?"
            params.append(f"%{id}%")

        if Nombre:
            query += " AND Nombre LIKE ?"
            params.append(f"%{Nombre}%")

        if DNI:
            query += " AND DNI LIKE ?"
            params.append(f"%{DNI}%")

        cursor.execute(query, params)
        resultados = cursor.fetchall()


    return resultados

def modificar_clientes(id,DNI=None,CUIT=None,Nombre=None,Dir=None,Tel=None,Correo=None, Socio=None,Gerente=None):
    ban = False
    cursor.execute("SELECT * FROM Clientes WHERE ID_Clientes = ?", (id,))
    Clientexd=cursor.fetchall()
    query = "UPDATE Clientes SET"
    params = []
    if DNI:
        if comprobaciones.Comprobacion_Clientes(DNI,str(Clientexd[0][2]),Clientexd[0][3],Clientexd[0][4],
                                                str(Clientexd[0][5]),Clientexd[0][6]):
            query += " DNI = ?,"
            params.append(DNI)
            ban = True

    if CUIT:
        if comprobaciones.Comprobacion_Clientes(str(Clientexd[0][1]), CUIT, Clientexd[0][3], Clientexd[0][4],
                                                str(Clientexd[0][5]), Clientexd[0][6]):
            query += " CUIT = ?,"
            params.append(CUIT)
            ban = True
    if Nombre:
        if comprobaciones.Comprobacion_Clientes(str(Clientexd[0][1]), Clientexd[0][2], Nombre, Clientexd[0][4],
                                                str(Clientexd[0][5]), Clientexd[0][6]):
            query += " Nombre = ?,"
            params.append(Nombre)
            ban = True
    if Dir:
        if comprobaciones.Comprobacion_Clientes(str(Clientexd[0][1]), Clientexd[0][2], Clientexd[0][3], Dir,
                                                str(Clientexd[0][5]), Clientexd[0][6]):
            query += " Direccion = ?,"
            params.append(Dir)
            ban = True

    if Tel:
        if comprobaciones.Comprobacion_Clientes(str(Clientexd[0][1]), Clientexd[0][2], Clientexd[0][3], Clientexd[0][4],
                                                Tel, Clientexd[0][6]):
            query += " Telefono = ?,"
            params.append(Tel)
            ban = True

    if Correo:
        if comprobaciones.Comprobacion_Clientes(str(Clientexd[0][1]), Clientexd[0][2], Clientexd[0][3], Clientexd[0][4],
                                                Clientexd[0][5], Correo):
            query += " Correo = ?,"
            params.append(Correo)
            ban = True

    if Socio == 1:
        ultimosIDvar = obtener_ultimos_ids()
        print(ultimosIDvar)
        cursor.execute(
            "INSERT INTO Socios(ID_Socios,DNI,SocioGerente) VALUES (?, ?, ?)",
            (ultimosIDvar["ultimo_id_socios"] + 1, Clientexd[0][1], Gerente,))
        conn.commit()

    if ban:
        query = query.rstrip(',')
        query += "WHERE ID_Clientes = ?"
        params.append(id)

        cursor.execute(query, params)
        conn.commit()

def buscar_proveedores(id=None, Nombre=None, CUIT=None):
    # Construir la consulta para buscar en la tabla Proveedores
    query = "SELECT * FROM Proveedores WHERE 1=1"
    params = []

    if id:
        query += " AND ID_Proveedor LIKE ?"
        params.append(f"%{id}%")

    if Nombre:
        query += " AND Nombre LIKE ?"
        params.append(f"%{Nombre}%")

    if CUIT:
        query += " AND CUIT LIKE ?"
        params.append(f"%{CUIT}%")

    cursor.execute(query, params)
    resultados = cursor.fetchall()

    return resultados

def modificar_proveedores(id, CUIT=None, Nombre=None, Dir=None, Tel=None, Correo=None, Categoria=None):
    cursor.execute("SELECT * FROM Proveedores WHERE ID_Proveedor = ?", (id,))
    proveedor = cursor.fetchall()

    query = "UPDATE Proveedores SET"
    params = []
    ban = False

    # Validación y actualización de CUIT
    if CUIT:
        if comprobaciones.Comprobacion_Proveedores(CUIT, proveedor[0][2], proveedor[0][3], proveedor[0][4],
                                                   str(proveedor[0][5]), proveedor[0][6]):
            query += " CUIT = ?,"
            params.append(CUIT)
            ban = True

    # Validación y actualización de Nombre
    if Nombre:
        if comprobaciones.Comprobacion_Proveedores(str(proveedor[0][1]), Nombre, proveedor[0][3], proveedor[0][4],
                                                   str(proveedor[0][5]), proveedor[0][6]):
            query += " Nombre = ?,"
            params.append(Nombre)
            ban = True

    # Validación y actualización de Dirección
    if Dir:
        if comprobaciones.Comprobacion_Proveedores(str(proveedor[0][1]), proveedor[0][2], Dir, proveedor[0][4],
                                                   str(proveedor[0][5]), proveedor[0][6]):
            query += " Direccion = ?,"
            params.append(Dir)
            ban = True

    # Validación y actualización de Teléfono
    if Tel:
        if comprobaciones.Comprobacion_Proveedores(str(proveedor[0][1]), proveedor[0][2], proveedor[0][3],
                                                   Tel,proveedor[0][5], proveedor[0][6]):
            query += " Telefono = ?,"
            params.append(Tel)
            ban = True

    # Validación y actualización de Correo
    if Correo:
        if comprobaciones.Comprobacion_Proveedores(str(proveedor[0][1]), proveedor[0][2], proveedor[0][3],
                                                   proveedor[0][4],
                                                   Correo, proveedor[0][6]):
            query += " Correo = ?,"
            params.append(Correo)
            ban = True

    # Validación y actualización de Categoría
    if Categoria:
        if comprobaciones.Comprobacion_Proveedores(str(proveedor[0][1]), proveedor[0][2], proveedor[0][3],
                                                   proveedor[0][4],
                                                   str(proveedor[0][5]), Categoria):
            print("a")
            query += " Categoria = ?,"
            params.append(Categoria)
            ban = True

    if ban:
        query = query.rstrip(',')
        query += " WHERE ID_Proveedor = ?"
        params.append(id)

        cursor.execute(query, params)
        conn.commit()

def buscar_pedido(id_pedido):
    cursor.execute('''SELECT * FROM Pedidos WHERE ID_Pedidos = ?''', (id_pedido,))
    pedido = cursor.fetchone()
    return pedido

def editar_pedido(id_pedido, nueva_fecha, nueva_condicion):
    cursor.execute('''UPDATE Pedidos SET Fecha = ?, Condicion = ? 
                      WHERE ID_Pedidos = ?''', (nueva_fecha, nueva_condicion, id_pedido))
    conn.commit()

def buscar_detalle_pedido(id_pedido):
    cursor.execute('''SELECT * FROM Detalle_Pedidos WHERE ID_Pedidos = ?''', (id_pedido,))
    detalles = cursor.fetchall()
    return detalles

def editar_detalle_pedido(id_detalle, nueva_cantidad, nuevo_precio_unitario):
    nuevo_precio_total = nueva_cantidad * nuevo_precio_unitario  # Recalcular el precio total
    cursor.execute('''UPDATE Detalle_Pedidos SET Cantidad = ?, PrecioUnitario = ?, PrecioTotal = ? 
                      WHERE ID_Detalle = ?''', (nueva_cantidad, nuevo_precio_unitario, nuevo_precio_total, id_detalle))
    conn.commit()

def buscar_factura(nro_factura):
    cursor.execute('''SELECT * FROM Factura WHERE Nro_Factura = ?''', (nro_factura,))
    factura = cursor.fetchone()
    return factura

def editar_factura(nro_factura, nueva_forma_pago, nueva_cantidad_cuotas):
    cursor.execute('''UPDATE Factura SET FormaPago = ?, CantidadCuotas = ? 
                      WHERE Nro_Factura = ?''', (nueva_forma_pago, nueva_cantidad_cuotas, nro_factura))
    conn.commit()

def buscar_presupuesto(nro_presupuesto):
    cursor.execute('''SELECT * FROM Presupuestos WHERE Nro_Presupuesto = ?''', (nro_presupuesto,))
    presupuesto = cursor.fetchone()
    return presupuesto

def editar_presupuesto(nro_presupuesto, nueva_forma_pago, nueva_cantidad_cuotas):
    cursor.execute('''UPDATE Presupuestos SET FormaPago = ?, CantidadCuotas = ? 
                      WHERE Nro_Presupuesto = ?''', (nueva_forma_pago, nueva_cantidad_cuotas, nro_presupuesto))
    conn.commit()

#-------------------------------------------ELIMINAR-------------------------------------------------------------------
# Función para eliminar un registro
def eliminar_hardware(id_hard):
    cursor.execute("DELETE FROM Hardware WHERE ID_Hard = ?", (id_hard,))
    conn.commit()
#Función para eliminar una marca
def eliminar_marca(id_marca):
    id_marca = int(id_marca[:4])
    cursor.execute("DELETE FROM Marca WHERE ID_Marca = ?", (id_marca,))
    cursor.execute("DELETE FROM Hardware WHERE ID_Marca = ?", (id_marca,))
    conn.commit()
#Función para eliminar un tipo
def eliminar_tipo(id_tipo):
    id_tipo = int(id_tipo[:4])
    print(id_tipo)
    cursor.execute("DELETE FROM TipoHard WHERE Id_Tipohard = ?", (id_tipo,))
    cursor.execute("DELETE FROM Hardware WHERE ID_Tipohard = ?", (id_tipo,))
    conn.commit()

def eliminar_clientes(id_cliente):
    cursor.execute("DELETE FROM Clientes WHERE ID_Clientes = ?", (id_cliente,))
    conn.commit()
#Funcion para eliminar proveedores
def eliminar_proveedores(id_cliente):
    cursor.execute("DELETE FROM Proveedores WHERE ID_Proveedor = ?", (id_cliente,))
    conn.commit()

def eliminar_pedido(id_pedido):
    cursor.execute('''DELETE FROM Pedidos WHERE ID_Pedidos = ?''', (id_pedido,))
    conn.commit()

def eliminar_factura(nro_factura):
    cursor.execute('''DELETE FROM Factura WHERE Nro_Factura = ?''', (nro_factura,))
    conn.commit()

def eliminar_detalle_pedido(id_detalle):
    cursor.execute('''DELETE FROM Detalle_Pedidos WHERE ID_Detalle = ?''', (id_detalle,))
    conn.commit()

def eliminar_presupuesto(nro_presupuesto):
    cursor.execute('''DELETE FROM Presupuestos WHERE Nro_Presupuesto = ?''', (nro_presupuesto,))
    conn.commit()

#----------------------------------------------OBTENER------------------------------------------------------------------
def obtener_ultimos_ids():
    # Obtener el último ID de Hardware
    cursor.execute("SELECT MAX(ID_Hard) FROM Hardware")
    ultimo_id_hardware = cursor.fetchone()[0]

    # Obtener el último ID de Marca
    cursor.execute("SELECT MAX(ID_Marca) FROM Marca")
    ultimo_id_marca = cursor.fetchone()[0]

    # Obtener el último ID de TipoHard
    cursor.execute("SELECT MAX(ID_Tipohard) FROM TipoHard")
    ultimo_id_tipohard = cursor.fetchone()[0]

    # Obtener el último ID de Clientes
    cursor.execute("SELECT MAX(ID_Clientes) FROM Clientes")
    ultimo_id_clientes = cursor.fetchone()[0]

    # Obtener el último ID de Socios
    cursor.execute("SELECT MAX(ID_Socios) FROM Socios")
    ultimo_id_socios = cursor.fetchone()[0]

    # Obtener el último ID de Proveedores
    cursor.execute("SELECT MAX(ID_Proveedor) FROM Proveedores")
    ultimo_id_proveedores = cursor.fetchone()[0]

    # Obtener el último ID de Pedidos
    cursor.execute("SELECT MAX(ID_Pedidos) FROM Pedidos")
    ultimo_id_pedidos = cursor.fetchone()[0]

    # Obtener el último ID de Detalle_Pedidos
    cursor.execute("SELECT MAX(ID_Detalle) FROM Detalle_Pedidos")
    ultimo_id_detalle_pedidos = cursor.fetchone()[0]

    # Obtener el último ID de Factura
    cursor.execute("SELECT MAX(Nro_Factura) FROM Factura")
    ultimo_id_factura = cursor.fetchone()[0]

    # Obtener el último ID de Presupuestos
    cursor.execute("SELECT MAX(Nro_Presupuesto) FROM Presupuestos")
    ultimo_id_presupuesto = cursor.fetchone()[0]

    return {
        "ultimo_id_hardware": ultimo_id_hardware,
        "ultimo_id_tipohard": ultimo_id_tipohard,
        "ultimo_id_marca": ultimo_id_marca,
        "ultimo_id_clientes": ultimo_id_clientes,
        "ultimo_id_socios": ultimo_id_socios,
        "ultimo_id_proveedores": ultimo_id_proveedores,
        "ultimo_id_pedidos": ultimo_id_pedidos,
        "ultimo_id_detalle_pedidos": ultimo_id_detalle_pedidos,
        "ultimo_id_factura": ultimo_id_factura,
        "ultimo_id_presupuesto": ultimo_id_presupuesto
    }

def obtener_marca():
    cursor.execute("SELECT * FROM Marca")
    lista_marcas = cursor.fetchall()  # Obtiene todas las filas
    cursor.execute("SELECT * FROM Marca")
    indexes = cursor.fetchall()
    indexes = [marca[0] for marca in indexes]
    lista_marcas = [marca[1] for marca in lista_marcas]
    i=0
    for item in lista_marcas:
        lista_marcas[i] = str(indexes[i])+". " + item
        i = i+1
    return lista_marcas

def obtener_tipos():
    cursor.execute("SELECT * FROM TipoHard")
    lista_tipos = cursor.fetchall()  # Obtiene todas las filas
    cursor.execute("SELECT * FROM TipoHard")
    indexes = cursor.fetchall()
    # Extraer las descripciones de la lista de tuplas
    lista_tipos = [marca[1] for marca in lista_tipos]
    indexes=[marca[0] for marca in indexes]
    i=0
    for item in lista_tipos:
        lista_tipos[i] = str(indexes[i])+". " + item
        i = i+1
    return lista_tipos

def buscar_todos_detalle_pedidos():
    cursor.execute('''SELECT * FROM Detalle_Pedidos''',)
    detalles = cursor.fetchall()
    return detalles

def buscar_todas_facturas():
    cursor.execute('''SELECT * FROM Factura''',)
    factura = cursor.fetchone()
    return factura

def buscar_todos_presupuestos():
    cursor.execute('''SELECT * FROM Presupuestos''',)
    presupuesto = cursor.fetchone()
    return presupuesto

def buscar_todos_pedidos():
    cursor.execute('''SELECT * FROM Pedidos''',)
    pedido = cursor.fetchall()
    return pedido

def buscar_todos_clientes():
    cursor.execute("SELECT * FROM ClientesSocios")
    resultados = cursor.fetchall()
    return resultados
def buscar_todos_hardware():
    cursor.execute("SELECT * FROM Hardware")
    resultados = cursor.fetchall()
    return resultados
# -------------------------------------CREACION-------------------------------------------------------------------------
# Función para añadir un nuevo registro
def agregar_hardware(IdHard,caracteristicas, precio_unitario, unidades_disponibles, tipo_hardware_descripcion,
                     marca_descripcion):
    # Insertar en la tabla Hardware
    id_tipohard = tipo_hardware_descripcion[:4]
    id_marca = marca_descripcion[:4]
    cursor.execute(
        """INSERT INTO Hardware (ID_Hard,ID_Tipohard, ID_Marca, Caracteristicas, Precio_Unitario, Unidades_Disponibles)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (IdHard, id_tipohard, id_marca, caracteristicas, precio_unitario, unidades_disponibles)
    )

    conn.commit()
    print("Registro agregado con éxito.")

def agregar_marca(id, nombre):
    cursor.execute("INSERT INTO Marca(ID_Marca,Descripcion) VALUES(?, ?)", (id, nombre,))
    conn.commit()

def agregar_tipo(id, nombre):
    cursor.execute("INSERT INTO TipoHard(ID_Tipohard, Descripcion) VALUES (?, ?)", (id, nombre,))
    conn.commit()

def agregar_cliente(id,DNI,CUIT,Nombre,Dir,Tel,Correo,Socio,Gerente):
    if obtener_ultimos_ids()["ultimo_id_socios"] != None:
        UltimoIDSocio = obtener_ultimos_ids()["ultimo_id_socios"]
    else:
        UltimoIDSocio = 1000

    try:
        cursor.execute("INSERT INTO Clientes(ID_Clientes,DNI,CUIT,Nombre,Direccion,Telefono,Correo ) VALUES (?, ?, ?, ?, ?, ?, ?)", (id,DNI,CUIT,Nombre,Dir,Tel,Correo,))
        conn.commit()
        if Socio == 1:
            cursor.execute(
                "INSERT INTO Socios(ID_Socios,DNI,SocioGerente) VALUES (?, ?, ?)",
                (UltimoIDSocio, DNI, Gerente,))
            conn.commit()
    except sqlite3.IntegrityError as er:
        tkinter.messagebox.showerror(title="Error en el ingreso de datos",
                                     message= f"ERROR DE INTEGRIDAD DEDATOS,REVISAR SI LOS DATOS SON UNICOS, {er.sqlite_errorname}")

def agregar_proveedor(id_proveedor, CUIT, Nombre, Dir, Tel, Correo, Categoria):

    # Obtener el último ID de socios o asignar un valor por defecto
    if obtener_ultimos_ids()["ultimo_id_socios"] is not None:
        UltimoIDSocio = obtener_ultimos_ids()["ultimo_id_socios"]
    else:
        UltimoIDSocio = 1000

    try:
        # Insertar los datos del proveedor en la tabla Proveedores
        cursor.execute(
            "INSERT INTO Proveedores(ID_Proveedor, CUIT, Nombre, Direccion, Telefono, Correo, Categoria) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (id_proveedor, CUIT, Nombre, Dir, Tel, Correo, Categoria))
        conn.commit()


    except sqlite3.IntegrityError as er:
        tkinter.messagebox.showerror(title="Error en el ingreso de datos",
                                     message=f"ERROR DE INTEGRIDAD DE DATOS, REVISAR SI LOS DATOS SON ÚNICOS. Error: {er.sqlite_errorname}")
        
def crear_pedido(id_cliente, nombre_cliente, fecha, condicion):
    cursor.execute('''INSERT INTO Pedidos (ID_Clientes, NombreCliente, Fecha, Condicion) 
                      VALUES (?, ?, ?, ?)''', (id_cliente, nombre_cliente, fecha, condicion))
    conn.commit()

def crear_detalle_pedido(id_pedido, id_hard, nombre_prod, cantidad, stock, precio_unitario,precio_total):
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO Detalle_Pedidos (ID_Pedidos, ID_Hard, NombreProd, Cantidad, Stock, PrecioUnitario, PrecioTotal)
                      VALUES (?, ?, ?, ?, ?, ?, ?)''', (id_pedido, id_hard, nombre_prod, cantidad, stock, precio_unitario, precio_total))
    conn.commit()

def crear_factura(id_cliente, nombre_cliente, fecha, monto_final, monto_total, forma_pago, id_pedido):
    cursor.execute('''INSERT INTO Factura (ID_Cliente, NombreCliente, Fecha, MontoFinal, MontoTotal, FormaPago, ID_Pedidos)
                      VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                   (id_cliente, nombre_cliente, fecha, monto_final, monto_total, forma_pago, id_pedido))
    conn.commit()

def crear_presupuesto(fecha, monto_final, monto_total, forma_pago, cantidad_cuotas, id_pedido):
    cursor.execute('''INSERT INTO Presupuestos (Fecha, MontoFinal, MontoTotal, FormaPago, CantidadCuotas, ID_Pedidos)
                      VALUES (?, ?, ?, ?, ?, ?)''', 
                   (fecha, monto_final, monto_total, forma_pago, cantidad_cuotas, id_pedido))
    conn.commit()
