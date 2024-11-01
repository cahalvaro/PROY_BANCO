from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox

from gui.registro import RegistroWindow
from model.movimientos import Transferencia

class MainWindow():
    def __init__(self):
        self.main=uic.loadUi("gui/main.ui")
        self.initGUI()
        self.main.showMaximized()

    
    def initGUI(self):
        self.main.btnRegistrarTransferencias.triggered.connect(self.abrirRegistro)
        self.registro=uic.loadUi("gui/registroTransacciones.ui")

    def abrirRegistro(self):
        self.registro.btnRegistrar.clicked.connect(self.registrarTransaccion)
        self.registro.show()
        

    def registrarTransaccion(self):
        if self.registro.cbTipo.currentText()=="***Seleccione una opcion":
            mBox=QMessageBox()
            mBox.setText("Debe seleccionar un tipo de documento")
            mBox.exec()
            self.registro.cbTipo.setFocus()
        elif len(self.registro.txtDocumento.text())<4:
            mBox=QMessageBox()
            mBox.setText("Debe ingresar un documento valido")
            mBox.exec()
            self.registro.txtDocumento.setFocus()
        elif self.registro.cbMotivo.currentText()=="***Seleccione una opcion":
            mBox=QMessageBox()
            mBox.setText("Debe seleccionar el motivo")
            mBox.exec()
            self.registro.cbMotivo.setFocus()
        elif not self.registro.txtMonto.text().isnumeric():
            mBox=QMessageBox()
            mBox.setText("Debe ingresar un monto valido")
            mBox.exec()
            self.registro.txtMonto.setText("0")
            self.registro.txtMonto.setFocus()
        else:
            transferencia=Transferencia(
                tipo=self.registro.cbTipo.currentText(),
                documento=self.registro.txtDocumento.text(),
                monto=float(self.registro.txtMonto.text()),
                motivo=self.registro.cbMotivo.currentText(),
                dolares=self.registro.checkDolares.isChecked(), 
                internacional=self.registro.checkInternacional.isChecked()
            )