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

    def registrar(self, info:Transferencia):
        fecha=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.db=con.Conexion().conectar()
        self.cursor=self.db.cursor()
        self.cursor.execute("""
        INSERT INTO transferencias values(null, '{}','{}','{}','{}','{}','{}','{}','{}')
        """.format(info._monto, info._tipo, info._documento, info._internacional, info._dolares,fecha,False,info._motivo))
        self.cursor.commit()
        if self.cursor.rowcount==1:
            return True
        else:
            return False