from PyQt6.QtWidgets import QAbstractItemView, QMainWindow, QMessageBox, QTableWidgetItem

from ui_mainwindow import Ui_MainWindow as MainForm
from pages.bookAddWindow import bookAddWindow
from pages.sysVersionWindow import sysVersionWindow

class mainWindow(MainForm, QMainWindow):
    def __init__(self, loginWindow, loginName):
        super().__init__()
        self.setupUi(self)
        self.login_window = loginWindow
        self.login_name = loginName

        # books临时保存所有图书数据，后续接入数据库时可以替换这里。
        self.books = []

        self.actionexit.triggered.connect(self.backToLogin)
        self.actionclose.triggered.connect(self.exitApp)
        self.statusbar.showMessage(f"当前用户：{self.login_name}，欢迎使用系统！")
        self.btn_book_add.clicked.connect(self.showBookAdd)
        self.btn_book_search.clicked.connect(self.searchBooks)
        self.btn_book_delete.clicked.connect(self.deleteBook)
        self.btn_book_all.clicked.connect(self.showAllBooks)
        self.btn_book_save.clicked.connect(self.saveBooks)
        self.actionabout_sys.triggered.connect(self.showSysVersion)

        self.initBookTable()
        self.showBooks(self.books)

    # 初始化图书表格的列名和选择方式
    def initBookTable(self):
        headers = ["图书编码", "书名", "作者", "分类", "出版日期", "状态", "标签", "备注"]
        # 设置列数
        self.table_book.setColumnCount(len(headers))
        # 设置列名
        self.table_book.setHorizontalHeaderLabels(headers)
        # 设置表格为不可编辑
        self.table_book.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        # 点击单元格，选择整行
        self.table_book.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        # 一次最多只能选一行
        self.table_book.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        # 最后列自动宽度
        self.table_book.horizontalHeader().setStretchLastSection(True)

    # 显示录入图书弹框
    def showBookAdd(self):
        self.book_add_window = bookAddWindow()
        # 模态弹窗
        result = self.book_add_window.exec()
        if result == bookAddWindow.DialogCode.Accepted:
            book = self.book_add_window.data

            if self.isBookCodeExists(book["book_code"]):
                QMessageBox.warning(self, "提示", "图书编码已存在，请重新录入")
                return

            self.books.append(book)
            self.showBooks(self.books)
        # 非模态弹窗
        # self.book_add_window.show()

    # 判断图书编码是否已经存在，图书编码作为删除时定位图书的唯一标识
    def isBookCodeExists(self, book_code):
        for book in self.books:
            if book["book_code"] == book_code:
                return True
        return False

    # 根据传入的图书列表刷新表格，搜索、删除、显示全部都会调用这个方法
    def showBooks(self, book_list):
        self.table_book.setRowCount(len(book_list))

        for row, book in enumerate(book_list):
            status = "在库" if book["can_borrow"] else "已借出"
            row_data = [
                book["book_code"],
                book["book_name"],
                book["author"],
                book["type"],
                book["publish_date"],
                status,
                book["tags"],
                book["remark"]
            ]

            for column, value in enumerate(row_data):
                self.table_book.setItem(row, column, QTableWidgetItem(str(value)))

    # 按书名和状态筛选图书
    def searchBooks(self):
        keyword = self.txt_search.text().strip()
        status_index = self.cb_book_status.currentIndex()
        result = []

        for book in self.books:
            if keyword and keyword not in book["book_name"]:
                continue

            if status_index == 1 and not book["can_borrow"]:
                continue

            if status_index == 2 and book["can_borrow"]:
                continue

            result.append(book)

        self.showBooks(result)

    # 删除表格中选中的图书，同时从books临时数据中移除真实数据
    def deleteBook(self):
        current_row = self.table_book.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "提示", "请先选择要删除的图书")
            return

        book_code = self.table_book.item(current_row, 0).text()
        reply = QMessageBox.question(
            self,
            "提示",
            "确定要删除选中的图书吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.books = [book for book in self.books if book["book_code"] != book_code]
            self.showBooks(self.books)

    # 清空搜索条件并显示所有图书
    def showAllBooks(self):
        self.txt_search.clear()
        self.cb_book_status.setCurrentIndex(0)
        self.showBooks(self.books)

    # 当前只使用临时变量保存，后续接数据库时替换这里即可
    def saveBooks(self):
        QMessageBox.information(self, "提示", "保存成功")

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
