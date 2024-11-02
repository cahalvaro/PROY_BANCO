import conexion as con
from model.movimientos import Transferencia
from datetime import datetime

class TransferenciaData():

    def __init__(self):
        self.db=con.Conexion().conectar()
        self.cursor=self.db.cursor()
        try:
            sql_create_transferencias="""CREATE TABLE IF NOT EXISTS transferencias(id INTEGER PRIMARY KEY 
                            AUTOINCREMENT, monto NUMERIC, tipo TEXT, documento TEXT,internacional BOOLEAN,
                              dolares BOOLEAN,verificado BOOLEAN DEFAULT 'false', 
                               fecha_registro DATE, motivo TEXT)"""
            self.execute(sql_create_transferencias)
            self.close()
            self.db.close()
            print("Tabla transferencias Creada")
        except Exception as ex:
            print("Tabla transferencias OK")

