import sqlite3

class Database:
    def __init__(self):
        self.con = sqlite3.connect('db.db')
        self.cur = self.con.cursor()
        self.table_name = ''

    def create(self, cols):
        "cols is string what defines columns real or text"
        self.cur.execute(f'CREATE TABLE {self.table} ({cols})')

    def read(self, rows='*', where=1):
        "select sql' command"
        self.cur.execute(f'SELECT {rows} FROM {self.table_name} WHERE {where}}')
