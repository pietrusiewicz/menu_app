import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('ma.db')
        self.cur = self.conn.cursor()
        #self.t = table_name
        #self.check_table()

    def check_table(self):
        try:
            self.cols = self.cur.execute(f"SELECT * FROM {self.table_name}")
            return 0
        except:
            if self.table_name == 'texts':
                self.cur.execute("CREATE TABLE texts (text_pwd text, content text, nr_sentence real, last_open real)")
            self.check_table()
            return 1
    
    def insert_into(self, data):
        sql = f"({','.join([repr(line) if type(line)==str else str(line) for line in data])})"
        self.cur.execute(f"INSERT INTO {self.table_name} VALUES {sql}")
        self.conn.commit()
        #self.check_table(self.table_name)

    def select(self, cols='*', where='WHERE 1'):
        self.cols = list(self.cur.execute(f"SELECT {cols} FROM {self.table_name} {where}"))
        return self.cols

    def update_row(self, column, value, where='WHERE 1'):
        sql = f"UPDATE {self.table_name} SET {column}='{value}' {where}"
