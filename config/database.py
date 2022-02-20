import sqlite3

class Database:
    def __init__(self, table_name):
        conn = sqlite3.connect('ma.db')
        self.cur = conn.cursor()
        self.t = table_name
        self.check_table()

    def check_table(self):
        try:
            self.cur.execute(f"SELECT * FROM {t}")
        except:
            if self.t == 'texts':
                self.cur.execute("CREATE TABLE texts (text_pwd text, content text)")
            self.check_table(self.t)
    
    def insert_into(self, data):
        self.cur.execute(f"INSERT INTO {self.t} VALUES ({','.join(data)})")
    
    def get_data(self):
        self.cols = list(self.cur.execute(f"SELECT * FROM {self.t}"))
