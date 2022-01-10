import sqlite3

class Service:
    def __init__(self):
        self.db = sqlite3.connect('storage.db')
        self.db_cur = self.db.cursor()

    def register(self, username, password):
        query = f"""
        INSERT INTO ACCOUNTS(username, password) 
        VALUES ('{username}', '{password}');
        """
        # print(query)
        res = True
        try:
            self.db_cur.execute(query)
        except sqlite3.Error as err:
            res = False
        self.db.commit()
        return res

    def login(self, username, password):
        return True

