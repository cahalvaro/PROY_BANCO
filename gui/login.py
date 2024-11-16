from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox

from data.usuario import UsuarioData
from gui.main import MainWindow
from model.usuario import Usuario

class Login():
    def __init__(self):
        self.login = uic.loadUi("gui/login.ui")
        self.initGUI()
        self.login.lblMensaje.setText("")
        self.login.show()

    def ingresar(self):
        if len(self.login.txtUsuario.text()) < 2:
            self.login.lblMensaje.setText("Ingrese un usuario válido")
            self.login.txtUsuario.setFocus()
        elif len(self.login.txtClave.text()) < 3:
            self.login.lblMensaje.setText("Ingrese una contraseña válida")
            self.login.txtClave.setFocus()
        else:
            self.login.lblMensaje.setText("")
            usu = Usuario(usuario=self.login.txtUsuario.text(),clave=self.login.txtClave.text())
            usuData = UsuarioData()
            res=usuData.login(usu)
            if res:
                self.main = MainWindow()
                self.login.hide()
            else:
                self.login.lblMensaje.setText("Datos de acceso incorrectos")
            
    
    def initGUI(self):
        self.login.btnAcceder.clicked.connect(self.ingresar)
              
