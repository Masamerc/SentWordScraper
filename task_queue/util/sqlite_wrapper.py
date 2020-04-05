import sqlite3


class SqliteWrapper:
    '''Context manager for sqlite3, closes connection and commits everything when exiting'''
    def __init__(self, db_name):
        self.name = db_name

    def __enter__(self):
        self.con = sqlite3.connect(self.name)
        self.cur = self.con.cursor()
        return self.cur

    def __exit__(self, exc_class, exc, traceback):
        self.con.commit()
        self.con.close()