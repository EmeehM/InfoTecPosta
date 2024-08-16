import sqlite3

def create_database():
    # Connect to the SQLite database (or create it if it doesn't exist)

    conn = sqlite3.connect("HardwareDB.db")
    curHard = conn.cursor()


    # Commit the changes and close the connection
    conn.commit()
    conn.close()


#asignar el resultado a una variable y hacerle fetch al retirar y commit al insertar