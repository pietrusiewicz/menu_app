import sqlite3

class Database:
    def __init__(self):
        self.con = sqlite3.connect('db.db')
        self.cur = self.con.cursor()

class Create(Database):
    def create(self, cols):
        "cols is string what defines columns real or text"
        self.cur.execute(f'CREATE TABLE {self.table} ({cols})')
    
    def append(self, values):
        self.cur.execute(f'INSERT INTO {self.table} VALUES ({cols})')

class Read(Database):
    def read(self, where='1', cols='*'):
        rows = list(self.cur.execute(f"SELECT {cols} FROM {self.table} WHERE {where}"))
        return rows

class Update(Database):
    def update(self, col, val, where='1'):
        self.cur.execute(f"UPDATE {self.table} SET {col}={val} WHERE 1")
