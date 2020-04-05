import sqlite3


class SqliteWrapper:
    '''
    General Purpose SQLite Wrapper:
    Context manager for sqlite3, closes connection and commits everything when exiting
    '''
    def __init__(self, db_name):
        self.name = db_name

    def __enter__(self):
        self.con = sqlite3.connect(self.name)
        self.cur = self.con.cursor()
        return self.cur

    def __exit__(self, exc_class, exc, traceback):
        self.con.commit()
        self.con.close()


class ValueInserter:
    def __init__(self, table_name, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.cur.execute(f'''
                        CREATE TABLE IF NOT EXISTS {table_name} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        scraped_at timestamp,
                        word TEXT NOT NULL,
                        count INTEGER NOT NULL,
                        source TEXT)''')
        
    def insert(self, tuple, table_name):
        length = len(tuple)
        placeholders = "(" + "null," + "?, " * (length -1) + "?)"

        self.cur.execute(f'''
        INSERT INTO {table_name}
        VALUES{placeholders}
        ''', tuple)

        self.conn.commit()

    def close(self):
        self.conn.close()