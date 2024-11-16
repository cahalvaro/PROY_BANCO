from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox




class RegistroWindow():
    def __init__(self):
        self.v = uic.loadUi("gui/registroTransacciones.ui")
        self.v.show()