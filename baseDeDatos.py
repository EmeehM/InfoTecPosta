import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('HardwareDB.db')
cursor = conn.cursor()

#--------------------------------BUSQUEDA Y MODIFICACION--------------------------------------------------------------
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
    query = "UPDATE Hardware SET"
    params = []

    if nuevas_caracteristicas:
        query += " Caracteristicas = ?,"
        params.append(nuevas_caracteristicas)

    if nuevo_precio:
        query += " Precio_Unitario = ?,"
        params.append(nuevo_precio)

    if nuevas_unidades:
        query += " Unidades_Disponibles = ?,"
        params.append(nuevas_unidades)

    # Eliminar la última coma
    query = query.rstrip(',')

    query += " WHERE ID_Hard = ?"
    params.append(id_hard)

    cursor.execute(query, params)
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


#----------------------------------OBTENER-------------------------------------------------------
# Función para obtener los últimos IDs
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

    # Obtener el último ID de TipoHard
    cursor.execute("SELECT MAX(ID_Clientes) FROM Clientes")
    ultimo_id_clientes = cursor.fetchone()[0]


    return {
        "ultimo_id_hardware": ultimo_id_hardware,
        "ultimo_id_tipohard": ultimo_id_tipohard,
        "ultimo_id_marca": ultimo_id_marca,
        "ultimo_id_clientes": ultimo_id_clientes
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

# -------------------------------------CREACION-------------------------------------------------------------------------
# Función para añadir un nuevo registro
def agregar_hardware(IdHard,caracteristicas, precio_unitario, unidades_disponibles, tipo_hardware_descripcion, marca_descripcion):
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


def agregar_marca(nombre):
    cursor.execute("INSERT INTO Marca(Descripcion) VALUES(?)", (nombre,))
    conn.commit()

def agregar_tipo(nombre):
    print(nombre)
    cursor.execute("INSERT INTO TipoHard(Descripcion) VALUES (?)", (nombre,))
    conn.commit()