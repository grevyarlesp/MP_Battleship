import sqlite3

conn = sqlite3.connect("storage.db")
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS
        ACCOUNTS (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
        username TEXT UNIQUE NOT NULL, 
        password TEXT NOT NULL,
        fullname TEXT,
        note TEXT, 
        point INTEGER
        )
        """
        )


conn.commit()
conn.close()
