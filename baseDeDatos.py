import sqlite3
import tkinter

import comprobaciones

# Conectar a la base de datos
conn = sqlite3.connect('HardwareDB.db')
cursor = conn.cursor()

#-------------------------------------------BUSQUEDA--------------------------------------------------------------------
# Función para buscar registros
def buscar_hardware(caracteristicas=None, tipo=None, id_hard=None):
    query = "SELECT * FROM Hardware WHERE 1=1"
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
        cursor.execute("SELECT * FROM Socios")
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

def editar_pedido(id_pedido, nueva_fecha=None, nueva_condicion=None):
    # Lista para almacenar partes de la consulta y valores
    columnas = []
    valores = []

    # Agregar columnas y valores solo si no son None
    if nueva_fecha is not None:
        columnas.append("Fecha = ?")
        valores.append(nueva_fecha)

    if nueva_condicion is not None:
        columnas.append("Condicion = ?")
        valores.append(nueva_condicion)

    # Agregar el ID del pedido al final de los valores
    valores.append(id_pedido)

    # Solo ejecutar la consulta si hay columnas para actualizar
    if columnas:
        query = f"UPDATE Pedidos SET {', '.join(columnas)} WHERE ID_Pedidos = ?"
        cursor.execute(query, valores)
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
    cursor.execute("SELECT * FROM Clientes")
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
    id_tipohard = tipo_hardware_descripcion.split(" - ")[0]
    id_marca = marca_descripcion.split(" - ")[0]
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
                                     message= f"ERROR DE INTEGRIDAD DE DATOS,REVISAR SI LOS DATOS SON UNICOS, {er.sqlite_errorname}")

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

#------------------------ID FACTURA VENTA---------------------------------------------------------------------------
# Función para insertar un nuevo registro
def crear_factura_venta(nro_factura, deuda):
    cursor.execute('''
        INSERT INTO Facturas_Venta (Nro_Factura, Deuda) VALUES (?, ?)
    ''', (nro_factura, deuda))
    conn.commit()
    print("Registro creado exitosamente.")

# Función para editar un registro existente
def editar_factura_venta(id_fv, nuevo_nro_factura=None, nueva_deuda=None):
    columnas = []
    valores = []

    if nuevo_nro_factura is not None:
        columnas.append("Nro_Factura = ?")
        valores.append(nuevo_nro_factura)
    
    if nueva_deuda is not None:
        columnas.append("Deuda = ?")
        valores.append(nueva_deuda)
    
    valores.append(id_fv)

    if columnas:
        query = f"UPDATE Facturas_Venta SET {', '.join(columnas)} WHERE ID_FV = ?"
        cursor.execute(query, valores)
        conn.commit()
        print("Registro actualizado exitosamente.")

# Función para eliminar un registro
def eliminar_factura_venta(id_fv):
    cursor.execute('DELETE FROM Facturas_Venta WHERE ID_FV = ?', (id_fv,))
    conn.commit()
    print("Registro eliminado exitosamente.")

# Función para buscar un registro por ID_FV
def buscar_factura_venta(id_fv):
    cursor.execute('SELECT * FROM Facturas_Venta WHERE ID_FV = ?', (id_fv,))
    resultado = cursor.fetchone()
    if resultado:
        return resultado
    else:
        print("No se encontró ningún registro con ese ID.")
        
def buscar_todas_facturas_venta():
    query = 'SELECT * FROM Facturas_Venta'
    cursor.execute(query)
    resultados = cursor.fetchall()
    if resultados:
        return resultados
    else:
        print("No se encontraron facturas de venta.")
    


#---------------------------------------Pagos-----------------------------------------------
# Función para crear un registro en la tabla Pagos
def crear_pago(id_fv, monto, fecha, forma_pago):
    query = '''
        INSERT INTO Pagos (ID_FV, Monto, Fecha, FormaPago)
        VALUES (?, ?, ?, ?)
    '''
    cursor.execute(query, (id_fv, monto, fecha, forma_pago))
    conn.commit()
    print("Pago creado exitosamente.")

# Función para editar un registro en la tabla Pagos
def editar_pago(id_pagos, nuevo_id_fv=None, nuevo_monto=None, nueva_fecha=None, nueva_forma_pago=None):
    columnas = []
    valores = []
    
    if nuevo_id_fv is not None:
        columnas.append("ID_FV = ?")
        valores.append(nuevo_id_fv)
    
    if nuevo_monto is not None:
        columnas.append("Monto = ?")
        valores.append(nuevo_monto)
    
    if nueva_fecha is not None:
        columnas.append("Fecha = ?")
        valores.append(nueva_fecha)
    
    if nueva_forma_pago is not None:
        columnas.append("FormaPago = ?")
        valores.append(nueva_forma_pago)
    
    valores.append(id_pagos)

    if columnas:
        query = f"UPDATE Pagos SET {', '.join(columnas)} WHERE ID_Pagos = ?"
        cursor.execute(query, valores)
        conn.commit()
        print("Pago actualizado exitosamente.")

# Función para eliminar un registro en la tabla Pagos
def eliminar_pago(id_pagos):
    query = 'DELETE FROM Pagos WHERE ID_Pagos = ?'
    cursor.execute(query, (id_pagos,))
    conn.commit()
    print("Pago eliminado exitosamente.")

# Función para buscar un registro en la tabla Pagos por ID_Pagos
def buscar_pago_por_id(id_pagos):
    query = 'SELECT * FROM Pagos WHERE ID_Pagos = ?'
    cursor.execute(query, (id_pagos,))
    resultado = cursor.fetchone()
    if resultado:
        print("Pago encontrado:", resultado)
    else:
        print("No se encontró ningún pago con ese ID.")

# Función para buscar todos los registros en la tabla Pagos
def buscar_todos_pagos():
    query = 'SELECT * FROM Pagos'
    cursor.execute(query)
    resultados = cursor.fetchall()
    if resultados:
        return resultados
    else:
        print("No se encontraron pagos.")