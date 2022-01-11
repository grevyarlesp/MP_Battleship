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
        query = f"""
        SELECT username, password FROM ACCOUNTS
        WHERE username = ?
        """
        self.db_cur.execute(query, (username, ))
        row = self.db_cur.fetchone()
        if (row is None):
            return False, 'Username does not exists'
        if (row[1] != password):
            return False, 'Username exists, wrong password'
        return True,  'Username and password correct'

    def change_password(self, username, oldpass, newpass):
        query = f""""
            SELECT username, password FROM ACCOUNTS
            WHERE username = ?
        """
        self.db_cur.execute(query, (username, ))

    def get_user_info(self, username):
        query = f"""
            SELECT username, fullname, date, note, point FROM ACCOUNTS
            WHERE username = ?
        """
        self.db_cur.execute(query, (username, ))
        row = self.db_cur.fetchone()
        if (row is None):
            return False, 'Username does not exists'
        return True, row


