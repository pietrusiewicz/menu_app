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
        "SELECT sql' command"
        self.cur.execute(f'SELECT {rows} FROM {self.table_name} WHERE {where}}')

    def update(self, sets='*', where=1):
        "UPDATE sql' command
        example: self.update(sets='col1=val1, col2=val2', where='val1 > 0')
        "
        self.cur.execute(f'UPDATE {self.table_name} SET {sets} WHERE {where}}')
