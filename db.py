import sqlite3
import os


class SqlLite:

    conn = None

    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.conn = sqlite3.connect(BASE_DIR+'/data.db')
        self.conn.row_factory = sqlite3.Row

    def query(self, sql):
        c = self.conn.cursor()
        c.execute(sql)
        self.conn.commit()

    def insert(self, sql, params):
        c = self.conn.cursor()
        c.execute(sql, params)
        self.conn.commit()

    def fetch(self, sql):
        c = self.conn.cursor()
        c.execute(sql)
        self.conn.commit()

    def fetchAll(self, sql):
        c = self.conn.cursor()
        c.execute(sql)
        return c.fetchall()

    def fetchOne(self, sql):
        c = self.conn.cursor()
        c.execute(sql)
        return c.fetchone()