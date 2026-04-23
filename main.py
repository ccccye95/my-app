import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from views.loginWindow import loginWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = loginWindow()
    window.show()
    sys.exit(app.exec())
