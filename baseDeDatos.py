import sqlite3

conHard = sqlite3.connect("HardwareDB.db")
curHard = conHard.cursor()
curHard.execute("IF")

#asignar el resultado a una variable y hacerle fetch al retirar y commit al insertar