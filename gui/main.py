from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt6.QtCore import QDate
from data.ciudad import CiudadData
from data.historial import HistorialData
from model.movimientos import DepositoInternacional, Transferencia
from data.transferencia import TransferenciaData
from data.deposito import DepositoData

class MainWindow():
    def __init__(self):
        self.main = uic.loadUi("gui/main.ui")
        self.initGUI()
        self.main.showMaximized()

    def initGUI(self):
        self.main.btnRegistrarTransferencias.triggered.connect(self.abrirRegistro)
        self.main.btnReportarTransferencia.triggered.connect(self.abrirDeposito)
        self.main.btnHistorialTransferencias.triggered.connect(self.abrirHistorial)
        self.registro = uic.loadUi("gui/registroTransacciones.ui")
        self.deposito = uic.loadUi("gui/deposito.ui")
        self.historial = uic.loadUi("gui/historial.ui")

    def abrirRegistro(self):
        self.registro.btnRegistrar.clicked.connect(self.registrarTransferencia)
        self.registro.show()

    def abrirDeposito(self):
        self.deposito.btnRegistrar.clicked.connect(self.registrarDeposito)
        self.deposito.show()
        self.llenarComboCiudades()

    def abrirHistorial(self):
        self.historial.btnBuscar.clicked.connect(self.buscar)
        self.historial.tblHistorial.setColumnWidth(1, 20)
        self.historial.tblHistorial.setColumnWidth(1, 250)
        self.historial.tblHistorial.setColumnWidth(3, 250)
        self.historial.tblHistorial.setColumnWidth(4, 190)
        self.historial.show()
        self.llenarTablaHistorial()

    def registrarTransferencia(self):
        if self.registro.cbTipo.currentText() == "--- Seleccione una opción":
            mBox = QMessageBox()
            mBox.setText("Debe seleccionar el tipo de documento")
            mBox.exec()
            self.registro.cbTipo.setFocus()
        elif len(self.registro.txtDocumento.text()) < 4:
            mBox = QMessageBox()
            mBox.setText("Debe ingresar un documento válido")
            mBox.exec()
            self.registro.txtDocumento.setFocus()
        elif self.registro.cbMotivo.currentText() == "--- Seleccione una opción":
            mBox = QMessageBox()
            mBox.setText("Debe seleccionar el motivo")
            mBox.exec()
            self.registro.cbMotivo.setFocus()
        elif not self.registro.txtMonto.text().isnumeric():
            mBox = QMessageBox()
            mBox.setText("Debe ingresar un monto válido")
            mBox.exec()
            self.registro.txtMonto.setText("0")
            self.registro.txtMonto.setFocus()
        else:
            transferencia = Transferencia(
                tipo=self.registro.cbTipo.currentText(),
                documento=self.registro.txtDocumento.text(),
                monto=float(self.registro.txtMonto.text()),
                motivo=self.registro.cbMotivo.currentText(),
                dolares=self.registro.checkDolares.isChecked(),
                internacional=self.registro.checkInternacional.isChecked()
            )
            objData = TransferenciaData()
            mBox = QMessageBox()
            if objData.registrar(info=transferencia):
                mBox.setText("Transferencia registrada")
                self.limpiarCamposTranferencias()
            else:
                mBox.setText("Transferencia NO registrada")
            mBox.exec()

    def limpiarCamposTranferencias(self):
        self.registro.cbTipo.setCurrentIndex(0)
        self.registro.cbMotivo.setCurrentIndex(0)
        self.registro.txtDocumento.setText("")
        self.registro.txtMonto.setText("0")
        self.registro.checkDolares.setChecked(False)
        self.registro.checkInternacional.setChecked(False)
        self.registro.txtDocumento.setFocus()

    def llenarComboCiudades(self):
        objData = CiudadData()
        datos = objData.listaCiudades()
        for item in datos:
            self.deposito.cbLugar.addItem(item[1])

    def validarCamposObligatorios(self) -> bool:
        if not self.deposito.txtDocumento.text() or not self.deposito.txtPrimerNombre.text() or not self.deposito.txtPrimerApellido.text() or not self.deposito.txtMonto.text() or self.deposito.cbMotivo.currentText() == "--- Seleccione una opción" or self.deposito.cbLugar.currentText() == "--- Seleccione una opción" or self.deposito.cbSexo.currentText() == "--- Seleccione una opción" or self.deposito.cbTipo.currentText() == "--- Seleccione una opción":
            return False
        else:
            return True

    def registrarDeposito(self):
        mBox = QMessageBox()
        if not self.validarCamposObligatorios():
            mBox.setText("Debe llenar los campos obligatorios (*)")
            mBox.exec()
        elif self.deposito.checkTerminos.isChecked() == False:
            mBox.setText("Debe aceptar los términos")
            mBox.exec()
            self.deposito.checkTerminos.setFocus()
        elif not self.deposito.txtMonto.text().isnumeric() or float(self.deposito.txtMonto.text()) < 1:
            mBox.setText("El monto debe ser mayor a cero")
            self.deposito.txtMonto.setText("0")
            mBox.exec()
            self.deposito.txtMonto.setFocus()
        else:
            fechaN = self.deposito.txtFecha.date().toPyDate()
            deposito = DepositoInternacional(
                tipo=self.deposito.cbTipo.currentText(),
                documento=self.deposito.txtDocumento.text(),
                monto=float(self.deposito.txtMonto.text()),
                motivo=self.deposito.cbMotivo.currentText(),
                sexo=self.deposito.cbSexo.currentText(),
                lugarNacimi=self.deposito.cbLugar.currentText(),
                nombre1=self.deposito.txtPrimerNombre.text(),
                nombre2=self.deposito.txtSegundoNombre.text(),
                apellido1=self.deposito.txtPrimerApellido.text(),
                apellido2=self.deposito.txtSegundoApellido.text(),
                terminos=self.deposito.checkTerminos.isChecked(),
                fechaNacimiento=fechaN
            )
            objData = DepositoData()
            if objData.registrar(info=deposito):
                mBox.setText("Deposito registrado")
                mBox.exec()
                self.limpiarCamposDeposito()
            else:
                mBox.setText("Deposito NO registrado")
                mBox.exec()

    def limpiarCamposDeposito(self):
        self.deposito.cbTipo.setCurrentIndex(0)
        self.deposito.cbMotivo.setCurrentIndex(0)
        self.deposito.cbSexo.setCurrentIndex(0)
        self.deposito.cbLugar.setCurrentIndex(0)
        self.deposito.txtDocumento.setText("")
        self.deposito.txtPrimerNombre.setText("")
        self.deposito.txtSegundoNombre.setText("")
        self.deposito.txtPrimerApellido.setText("")
        self.deposito.txtSegundoApellido.setText("")
        miFecha = QDate(2000, 1, 1)
        self.deposito.txtFecha.setDate(miFecha)
        self.deposito.txtMonto.setText("0")
        self.deposito.checkTerminos.setChecked(False)
        self.deposito.txtDocumento.setFocus()

    def buscar(self):
        his = HistorialData()
        data = his.buscarPorFecha(self.historial.txtFechaDesde.date().toPyDate(), self.historial.txtFechaHasta.date().toPyDate(), self.historial.cbTipo.currentText(), self.historial.txtDocumento.text())
        nombre = None
        fila = 0
        self.historial.tblHistorial.setRowCount(len(data))
        for item in data:
            self.historial.tblHistorial.setItem(fila, 0, QTableWidgetItem(str(item[0])))
            if nombre:
                self.historial.tblHistorial.setItem(fila, 1, QTableWidgetItem(nombre))
            else:
                self.historial.tblHistorial.setItem(fila, 1, QTableWidgetItem("{} {} {} {}".format(str(item[10]), str(item[11]), str(item[12]), str(item[13]))))
                nombre = "{} {} {} {}".format(str(item[10]), str(item[11]), str(item[12]), str(item[13]))
            if str(item[6]) == 'True':
                self.historial.tblHistorial.setItem(fila, 2, QTableWidgetItem("USD " + str(item[2])))
            else:
                self.historial.tblHistorial.setItem(fila, 2, QTableWidgetItem("COP " + str(item[2])))
            if str(item[5]) == 'True':
                self.historial.tblHistorial.setItem(fila, 3, QTableWidgetItem("Internacional - " + str(item[9])))
            else:
                self.historial.tblHistorial.setItem(fila, 3, QTableWidgetItem("Transferencia Nacional"))
            self.historial.tblHistorial.setItem(fila, 4, QTableWidgetItem(str(item[7])))
            if str(item[17]) == 'True':
                self.historial.tblHistorial.setItem(fila, 5, QTableWidgetItem("SI"))
            else:
                self.historial.tblHistorial.setItem(fila, 5, QTableWidgetItem("NO"))
            fila = fila + 1

    def llenarTablaHistorial(self):
        pass
