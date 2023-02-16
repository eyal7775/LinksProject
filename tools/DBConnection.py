import sqlite3

class DBConnection:
    def __init__(self, db_path):
        self.db_path = db_path
        self.con = None
        self.cur = None

    def create_table(self):
        try:
            self.con = sqlite3.connect(self.db_path)
            self.cur = self.con.cursor()
            self.cur.execute("""CREATE TABLE IF NOT EXISTS LINKS (
                serial INTEGER PRIMARY KEY,
                link TEXT NOT NULL,
                depth INTEGER,
                access BOOLEAN
            )""")
            self.con.commit()
        except sqlite3.Error as e:
            print(e)

    def select_query(self):
        try:
            self.cur.execute("SELECT * FROM LINKS")
            self.con.commit()
        except sqlite3.Error as e:
            print(e)

    def insert_query(self, dataset):
        try:
            self.cur.execute("INSERT OR IGNORE INTO LINKS VALUES (?,?,?,?)",dataset)
            self.con.commit()
        except sqlite3.Error as e:
            print(e)

    def __del__(self):
        self.con.close()