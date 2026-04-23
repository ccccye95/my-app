from PyQt6.QtWidgets import QDialog, QMainWindow
from ui_sys_version import Ui_Dialog

class sysVersionWindow(Ui_Dialog, QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)