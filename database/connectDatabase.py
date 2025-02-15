import sqlite3
class ConnectDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('puzzlegame.db')
          # Bật hỗ trợ khóa ngoại

        if not self.databaseExists():
            self.createDatabase()

    def databaseExists(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        # Kiểm tra nếu có bảng nào trong cơ sở dữ liệu
        if not tables:
            return False  # Không có bảng nào, cơ sở dữ liệu chưa tồn tại

        return True  # Có ít nhất một bảng, cơ sở dữ liệu đã tồn tại

    def createDatabase(self):
        self.conn.execute("PRAGMA foreign_keys = ON")
        cursor = self.conn.cursor()

        # Tạo bảng player
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS player (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                points INTEGER,
                hex_selected TEXT
            )
        ''')

        # Tạo bảng color
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS color (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                hex TEXT,
                points INTEGER
            )
        ''')

        # Tạo bảng color_purchased
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS color_purchased (
                id INTEGER,
                hex TEXT,
                FOREIGN KEY (id) REFERENCES player(id) ON DELETE CASCADE,
                PRIMARY KEY (id, hex)
            )
        ''')

        # Tạo bảng puzzle
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS puzzle (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                value TEXT
            )
        ''')

        # Tạo bảng game
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game (
                id_init INTEGER,
                status INTEGER DEFAULT 0,
                steps INTEGER,
                FOREIGN KEY (id_init) REFERENCES puzzle(id) ON DELETE CASCADE
            )
        ''')

        # Thêm dữ liệu mặc định cho bảng player
        cursor.execute("INSERT INTO player (points, hex_selected) VALUES (?, ?)", (0, "130,105,77"))

        # Thêm dữ liệu mặc định cho bảng color
        arr_color = [
            ("130,105,77", 0),
            ("112,170,0", 178),
            ("76,163,169", 234),
            ("255,0,4", 183),
            ("212,117,118", 186),
            ("193,70,90", 184),
            ("255,0,72", 293),
            ("255,0,179", 199),
            ("102,16,76", 286),
            ("123,0,255", 189),
            ("77,55,100", 336),
            ("55,0,255", 205),
            ("133,128,154", 112),
            ("32,28,44", 234),
            ("4,35,94", 370),
            ("239,27,123", 256),
            ("159,141,182", 226),
            ("0,255,128", 174),
            ("0,255,9", 185),
            ("255,179,0", 224),
            ("255,85,0", 164),
            ("134,85,85", 243)
        ]
        cursor.executemany("INSERT INTO color (hex, points) VALUES (?, ?)", arr_color)

        # Thêm dữ liệu mặc định cho bảng color_purchased
        cursor.execute("INSERT INTO color_purchased (id, hex) VALUES (?, ?)", (1, "130,105,77"))
        
        # Thêm dữ liệu mặc định cho bảng puzzle
        arr_puzzle = [
            ('1,2,3,8,0,4,7,6,5',),
            ('1,2,3,8,4,5,7,0,6',),
            ('1,3,4,8,0,2,7,6,5',),
            ('1,2,3,7,0,4,6,8,5',)
        ]
        cursor.executemany("INSERT INTO puzzle (value) VALUES (?)", arr_puzzle)

        # Thêm dữ liệu mặc định cho bảng game
        arr_game = [
            (2, 3),
            (3, 4),
            (4, 4)
        ]
        cursor.executemany("INSERT INTO game (id_init, steps) VALUES (?, ?)", arr_game)

        # Lưu thay đổi
        self.conn.commit()

    def execute(self, query, params=None):
        cursor = self.conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cursor.close()  # Đảm bảo con trỏ luôn được đóng


    def query(self, query, params=None):
        cursor = self.conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        except Exception as e:
            print(f"An error occurred: {e}")
            return []  # Trả về danh sách rỗng nếu có lỗi
        finally:
            cursor.close()  # Đảm bảo con trỏ luôn được đóng


    def closeConnection(self):
        self.conn.close()
