from PyQt6.QtWidgets import QMainWindow, QMessageBox
from ui_login import Ui_Form as LoginForm
from views.mainWindow import mainWindow as MainWindow

class loginWindow(LoginForm, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_reset.clicked.connect(self.loginReset)
        self.btn_login.clicked.connect(self.login)

    def login(self):
        # 选择框
        check_pwd = self.check_pwd.isChecked()
        print("是否记住密码：" + str(check_pwd))
        # 单选框
        radio_user = self.radio_user.isChecked()
        login_name = "管理员"
        if radio_user:
            print("普通用户登录")
            login_name = "普通用户"
        else:
            print("管理员登录")

        username = self.txt_username.text()
        pwd = self.txt_pwd.text()
        if username == "admin" and pwd == "123":
            QMessageBox.information(self, "提示", "登录成功")
            self.mainWindow = MainWindow(self, login_name)
            self.mainWindow.show()
            self.close()
        else:
            QMessageBox.warning(self, "提示", "登录失败")

    def loginReset(self):
        self.txt_username.clear()
        self.txt_pwd.clear()