from PyQt6.QtWidgets import QMainWindow, QMessageBox

from pages.sysVersionWindow import sysVersionWindow
from ui_mainwindow import Ui_MainWindow as MainForm
from pages.bookAddWindow import bookAddWindow
from pages.sysVersionWindow import sysVersionWindow

class mainWindow(MainForm, QMainWindow):
    def __init__(self, loginWindow, loginName):
        super().__init__()
        self.setupUi(self)
        self.login_window = loginWindow
        self.login_name = loginName
        self.actionexit.triggered.connect(self.backToLogin)
        self.actionclose.triggered.connect(self.exitApp)
        self.statusbar.showMessage(f"当前用户：{self.login_name}，欢迎使用系统！")
        self.btn_book_add.clicked.connect(self.showBookAdd)
        self.actionabout_sys.triggered.connect(self.showSysVersion)

    # 显示新增
    def showBookAdd(self):
        self.book_add_window = bookAddWindow()
        # 模态弹窗
        self.book_add_window.exec()
        # 非模态弹窗
        # self.book_add_window.show()

    def showSysVersion(self):
        self.sysversion_window = sysVersionWindow()
        self.sysversion_window.exec()

    def backToLogin(self):
        reply = QMessageBox.information(self, "提示", "是否返回登录页", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.Yes)
        if reply == QMessageBox.StandardButton.Yes:
            self.login_window.show()
            self.close()

    def exitApp(self):
        reply = QMessageBox.information(self, "提示", "关闭程序",
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                        QMessageBox.StandardButton.Yes)
        if reply == QMessageBox.StandardButton.Yes:
            self.close()