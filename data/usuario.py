import conexion as con
from model.usuario import Usuario

class UsuarioData():
    
    def __init__(self):
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()
            sql_insert = """ INSERT INTO usuarios values(null,'{}','{}','{}')""".format("Administrador","admin","admin2050.")
            self.cursor.execute(sql_insert)
            self.db.commit()
        except Exception as ex:
            print("Ya se creó el usuario admin",ex)

    def login(self,usuario:Usuario):
        self.db = con.Conexion().conectar()
        self.cursor = self.db.cursor()
        res = self.cursor.execute("SELECT * FROM usuarios WHERE usuario='{}' AND clave='{}'".format(usuario._usuario,usuario._clave))
        fila = res.fetchone()
        if fila:
            usuario = Usuario(nombre=fila[1],usuario=fila[2])
            self.cursor.close()
            self.db.close()
            return usuario
        else:
            self.cursor.close()
            self.db.close()
            return None
            


    