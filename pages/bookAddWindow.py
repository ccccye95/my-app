from ui_book_add import Ui_Dialog as UiDialog
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QDialog, QMessageBox

class bookAddWindow(UiDialog, QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.data = None
        # 连接信号槽
        self.form_btn_submit.clicked.connect(self.submit)
        self.form_btn_reset.clicked.connect(self.resetForm)

    # 提交表单
    def submit(self):
        data = self.collectForm()

        if not self.validateForm(data):
            # QMessageBox.warning(self, "提示", "校验失败")
            return

        # 验证通过后把数据保存到窗口对象中，主窗口通过self.data读取。
        self.data = data
        self.accept()

    # 收集表单数据
    def collectForm(self):
        tags = []
        if self.form_tag_1.isChecked():
            tags.append("新书")
        if self.form_tag_2.isChecked():
            tags.append("推荐")
        if self.form_tag_3.isChecked():
            tags.append("工具书")

        # 把表单数据放入data对象
        data = {
            "book_code": self.form_book_code.text().strip(),
            "book_name": self.form_book_name.text().strip(),
            "author": self.form_author.text().strip(),
            "type": self.form_type.currentText(),
            "publish_date": self.form_date.date().toString("yyyy-MM-dd"),
            "can_borrow": self.form_ok.isChecked(),
            "tags": ",".join(tags),
            "remark": self.form_remark.toPlainText().strip()
        }
        return data

    # 校验表单数据
    def validateForm(self, data):
        if not data["book_code"]:
            QMessageBox.warning(self, "提示", "图书编号不能为空")
            self.form_book_code.setFocus()
            return False

        if not data["book_name"]:
            QMessageBox.warning(self, "提示", "书名不能为空")
            self.form_book_code.setFocus()
            return False

        if not data["author"]:
            QMessageBox.warning(self, "提示", "作者不能为空")
            self.form_book_code.setFocus()
            return False

        return True

    # 重置表单
    def resetForm(self):
        self.form_book_code.clear()
        self.form_book_name.clear()
        self.form_author.clear()
        self.form_type.setCurrentIndex(0)
        self.form_date.setDate(QDate.currentDate())
        self.form_ok.setChecked(True)
        self.form_no.setChecked(False)
        self.form_tag_1.setChecked(False)
        self.form_tag_2.setChecked(False)
        self.form_tag_3.setChecked(False)
        self.form_remark.clear()
