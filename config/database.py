import sqlite3

class Database:
    def __init__(self):
        conn = sqlite3.connect('ma.db')
        self.cur = conn.cursor()
        #self.t = table_name
        #self.check_table()

    def check_table(self):
        try:
            self.cols = self.cur.execute(f"SELECT * FROM {self.table_name}")
        except:
            if self.table_name == 'texts':
                self.cur.execute("CREATE TABLE texts (text_pwd text, content text, nr_sentence real, last_open real)")
            self.check_table(self.table_name)
    
    def insert_into(self, data):
        sql = f"({','.join([repr(line) if type(line)==str else str(line) for line in data])})"
        self.cur.execute(f"INSERT INTO {self.table_name} VALUES {sql}")
        self.check_table(self.table_name)
    def raw_query(self, query):
        self.cols = list(self.cur.execute(f"{query}"))
        return self.cols
