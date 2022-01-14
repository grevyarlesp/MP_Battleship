import sqlite3
import threading
class DBService:
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
        query = f"""
            SELECT username, password FROM ACCOUNTS
            WHERE username = ?
        """

        print("Changing password for username", username)
        self.db_cur.execute(query, (username, ))

        row = self.db_cur.fetchone()
        if (row[1] != oldpass):
            return False, "Wrong old password"

        query = f"""
            UPDATE ACCOUNTS
            SET password = ?
            WHERE username = ?
        """
        self.db_cur.execute(query, (newpass, username, ))
        self.db.commit()
        return True, "Success"
        

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

    def update_user_info(self, username, fullname, date, note):
        query = f"""
            UPDATE ACCOUNTS
            SET fullname = ?, date = ?, note = ?
            WHERE username = ?
        """
        try:
            self.db_cur.execute(query, (fullname, date, note, username))
        except sqlite3.Error as err:
            return False

        self.db.commit()
        return True

    def update_point_add_1(self, username):
        query = f"""
            SELECT username, point
            WHERE username = ?
        """
        self.db_cur.execute(query, (username, ))
        point = self.db_cur.fetchone()[1]
        if (point is None):
            point = 0
        else:
            point = int(point)
        point = point + 1

        query = f"""
            UPDATE ACCOUNTS
            SET point = ?
            WHERE username = ?
        """
        try:
            self.db_cur.execute(query, (point, username))
        except sqlite3.Error as err:
            return False
        self.db.commit()

