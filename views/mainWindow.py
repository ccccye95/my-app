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

        # 图书集合对象
        # 2个初始书信息
        # 之后对接数据库
        self.books = [{
            "book_code": "ABC",
            "book_name": "Python高级开发",
            "author": "25软件5班",
            "type": "A",
            "publish_date": "2026-04-26",
            "can_borrow": "可借",
            "tags": "新书",
            "remark": "备注"
        }, {
            "book_code": "12345",
            "book_name": "Java开发",
            "author": "25软件5班",
            "type": "A",
            "publish_date": "2026-04-26",
            "can_borrow": "可借",
            "tags": "新书",
            "remark": "备注"
        }]

        self.actionexit.triggered.connect(self.backToLogin)
        self.actionclose.triggered.connect(self.exitApp)
        self.statusbar.showMessage(f"当前用户：{self.login_name}，欢迎使用系统！")
        self.btn_book_add.clicked.connect(self.showBookAdd)
        self.btn_book_search.clicked.connect(self.searchBook)
        self.btn_book_delete.clicked.connect(self.deleteBook)
        self.btn_book_all.clicked.connect(self.showAllBooks)
        self.btn_book_save.clicked.connect(self.saveBooks)
        self.actionabout_sys.triggered.connect(self.showSysVersion)

        self.initBookTable()
        self.showBookList(self.books)

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

        # Accepted 校验成功的新图书
        if result == bookAddWindow.DialogCode.Accepted:
            # 录入页面的data给book
            book = self.book_add_window.data

            if self.isBookCodeExists(book["book_code"]):
                QMessageBox.warning(self, "提示", "图书编码已存在，请重新录入")
                return

            # 加入books集合
            # append 在集合最后插入数据
            self.books.append(book)
            # 刷新最新数据
            self.showBookList(self.books)
        # 非模态弹窗
        # self.book_add_window.show()

    # 判断图书编码是否已经存在，图书编码作为删除时定位图书的唯一标识
    def isBookCodeExists(self, book_code):
        for book in self.books:
            if book["book_code"] == book_code:
                return True
        return False

    # 根据传入的图书列表刷新表格，搜索、删除、显示全部都会调用这个方法
    def showBookList(self, book_list):
        # 1. 设置数据表格列数量
        # self.table_book.setColumnCount(len(book_list))
        # ！ 设置行数量
        self.table_book.setRowCount(len(book_list))

        # 2. 遍历集合，行
        for row, book in enumerate(book_list):
            # 转换状态，保证要么是可借，要么是借出
            # 丢失  状态
            status = "可借" if book["can_borrow"] else "借出"
            # 临时的行数据
            # 对象  字段无序的
            # List  集合    有序的

            #  ["ABC", "Python开发", ........]
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

            # 3. 遍历列
            # 遍历行数据，设置每列的值
            for column, value in enumerate(row_data):
                self.table_book.setItem(row, column, QTableWidgetItem(str(value)))

    # 搜索+筛选
    def searchBook(self):
        keyword = self.txt_search.text().strip()
        status_index = self.cb_book_status.currentIndex()

        result = []

        for book in self.books:
            if keyword and keyword not in book["book_name"]:
                continue

            # 索引1 = 可借，排除借出的图书
            # 索引2 = 借出，排除可借的图书
            if status_index == 1 and book["can_borrow"] == "借出":
                continue

            if status_index == 2 and book["can_borrow"] == "可借":
                continue

            result.append(book)

        self.showBookList(result)

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
            # 删掉图书编码为 book_code的书籍
            new_books = []
            for book in self.books:
                if book["book_code"] != book_code:
                    new_books.append(book)
            self.books = new_books
            self.searchBook()

    # 清空搜索条件并显示所有图书
    def showAllBooks(self):
        self.txt_search.clear()
        self.cb_book_status.setCurrentIndex(0)
        self.searchBook()

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
