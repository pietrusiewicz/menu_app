import sqlite3

class Database:
    def __init__(self):
        self.con = sqlite3.connect('db.db')
        self.cur = self.con.cursor()

    def create(self, cols):
        "cols is string what defines columns real or text"
        self.cur.execute(f'CREATE TABLE {self.table} ({cols})')

