import sqlite3


class BookDB:
    def __init__(self):
        # 数据库文件放在项目根目录，方便查看和备份。
        self.conn = sqlite3.connect("books.db")
        # 返回字典
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.create_table()

    # 创建图书表；如果表已经存在，SQLite会自动跳过。
    def create_table(self):
        # SQLite中INTEGER常用来保存布尔值：1表示可借，0表示借出。
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS book (
                book_code TEXT PRIMARY KEY,
                book_name TEXT NOT NULL,
                author TEXT NOT NULL,
                type TEXT,
                publish_date TEXT,
                can_borrow INTEGER,
                tags TEXT,
                remark TEXT
            )
        """)
        self.conn.commit()

    # 统计图书总数
    def get_book_total(self):
        self.cursor.execute("""
            SELECT
                COUNT(*) AS total_count
            FROM book
        """)
        # 获取一行记录
        row = self.cursor.fetchone()

        # return row["total_count"] or 0

        return {
            "total_count": row["total_count"] or 0
        }

    # 统计可借的图书
    def get_book_borrow(self):
        self.cursor.execute("""
                    SELECT
                        COUNT(*) AS total_count
                    FROM book WHERE can_borrow = 1
                """)
        row = self.cursor.fetchone()

        return {
            "total_count": row["total_count"] or 0
        }

    # 按分类统计图书数量
    def get_book_type_statistics(self):
        self.cursor.execute("""
            SELECT
                type,
                COUNT(*) AS book_count
            FROM book
            GROUP BY type
        """)
        rows = self.cursor.fetchall()

        result = []
        for row in rows:
            result.append({
                "type_name": row["type"],
                "book_count": row["book_count"]
            })

        return result

    # 查询所有图书，并把数据库记录转换成界面使用的字典。
    def get_books(self):
        self.cursor.execute("""
            SELECT book_code, book_name, author, type, publish_date,
                   can_borrow, tags, remark
            FROM book
            ORDER BY book_code
        """)
        rows = self.cursor.fetchall()

        books = []
        for row in rows:
            # row是普通元组，字段顺序和上面SELECT中的字段顺序一致。
            books.append({
                "book_code": row[0],
                "book_name": row[1],
                "author": row[2],
                "type": row[3] or "",
                "publish_date": row[4] or "",
                "can_borrow": bool(row[5]),
                "tags": row[6] or "",
                "remark": row[7] or ""
            })

        return books

    # 判断图书编码是否已经存在，常用于新增图书前的重复校验。
    def is_book_exists(self, book_code):
        self.cursor.execute("SELECT COUNT(*) FROM book WHERE book_code = ?", (book_code,))
        count = self.cursor.fetchone()[0]
        return count > 0

    # 新增图书，?是SQL参数占位符，可以避免手动拼接SQL。
    def add_book(self, book):
        self.cursor.execute("""
            INSERT INTO book (
                book_code, book_name, author, type, publish_date,
                can_borrow, tags, remark
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            book["book_code"],
            book["book_name"],
            book["author"],
            book["type"],
            book["publish_date"],
            1 if book["can_borrow"] else 0,
            book["tags"],
            book["remark"]
        ))
        self.conn.commit()

    # 修改图书，book_code是主键，用来定位要修改的记录。
    def update_book(self, book):
        self.cursor.execute("""
            UPDATE book
            SET book_name = ?,
                author = ?,
                type = ?,
                publish_date = ?,
                can_borrow = ?,
                tags = ?,
                remark = ?
            WHERE book_code = ?
        """, (
            book["book_name"],
            book["author"],
            book["type"],
            book["publish_date"],
            1 if book["can_borrow"] else 0,
            book["tags"],
            book["remark"],
            book["book_code"]
        ))
        self.conn.commit()

    # 根据图书编码删除图书。
    def delete_book(self, book_code):
        self.cursor.execute("DELETE FROM book WHERE book_code = ?", (book_code,))
        self.conn.commit()

    # 程序关闭时释放数据库连接。
    def close(self):
        self.conn.close()
