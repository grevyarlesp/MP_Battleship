from PyQt5.QtCore import pyqtSlot, Qt
from socketwrapper import SocketWrapper
import sys
import json
import hashlib

import csv

from PyQt5.QtWidgets import QMessageBox, QListWidget, QListWidgetItem, QFileDialog

from utils import *


DEFAULT_SHIP = 'def.csv'

"""
Controller: takes a widget dicts as input. Access all element of the GUI.
"""
class Controller():
    def __init__(self, widgetsDict):
        self.checkFlag = False
        self.cur_user = None
        self.widgetsDict = widgetsDict
        self.controlsWidget = self.widgetsDict['control']
        self.con = SocketWrapper(self)
        self.playerBoard = self.widgetsDict['PlayerBoard']
        self.enemyBoard = self.widgetsDict['EnemyBoard']
        self.ingame = False


        # Own turn: 1, 0, op turn
        self.turn = False
        self.turnlabel = self.widgetsDict['turnlabel']

        self.setTurn(True)

        _, self.ship = self.loadShip(DEFAULT_SHIP)
        self.playerBoard.setBoard(self.ship)

    def check_connected_or_in_game(self):
        """
        Check if client is connected to a server
        """
        if (self.con.check_not_connected()):
            displayMessageBox('INFO', 'Please connect first!')
            return False

        return not self.ingame

    def check_logged_in_or_in_game(self):
        """
        Check if client is logged in  and if the client is not in game.
        """
        if (not self.check_connected_or_in_game()):
            return False
        if (self.cur_user is None):
            displayMessageBox('INFO', 'Not logged in, please log in!')
            return False
        return not self.ingame


    def loadShip(self, fileName):
        if not fileName:
            return False, None
        file = open(fileName)
        csvreader = csv.reader(file)
        rows = []
        for row in csvreader:
            rows.extend(row)
        if (len(rows) != self.playerBoard.size()  *self.playerBoard.size()):
            return False, None

        rows = [int(x) for x in rows]

        return True, rows

    def send_no_wait(self, m):
        data = json.dumps(m) + '|'
        self.con.writeData(data)
    
    def send_and_wait(self, m):
        data = json.dumps(m) + '|'
        self.con.writeData(data)
        self.con.waitForReadyRead()

    def connect(self, ip, port):
        if (not self.con.check_not_connected()):
            displayMessageBox('INFO', 'Already connected')
            return

        self.connected = True
        port = port.rstrip()
        ip = ip.rstrip()
        if (not self.con.connect(ip, port)):
            displayMessageBox('INFO', 'Not connected!')
        else:
            displayMessageBox('INFO', 'Connected!')

    def close(self):
        if (not self.connected):
            return
        self.con.writeData('close')
        self.con.disconnect()

    def login(self, user, password, enc):
        if (not self.check_connected_or_in_game()):
            return
        user = user.rstrip()
        password = password.rstrip()
        if (not user or not password):
            return
        if (enc):
            password = hashlib.md5(bytes(password, 'utf8')).hexdigest()
        m = {
                'type': 'login',
                'username': user,
                'password': password, 
                'enc': enc
                }
        self.send_and_wait(m)

    def register(self, user, password, enc):
        if (not self.check_connected_or_in_game()):
            return

        user = user.rstrip()
        password = password.rstrip()
        if (not user or not password):
            return
        if (enc):
            password = hashlib.md5(bytes(password, 'utf8')).hexdigest()
        m = {
                'type': 'register',
                'username': user,
                'password': password, 
                'enc': enc
                }

        self.send_and_wait(m)

    def setInfoEdit(self, msg):
        setup_info = self.controlsWidget['setup_info']
        setup_info['username_label'].setText(msg['username'])
        setup_info['fullname_edit'].setText(msg['fullname'])
        setup_info['date_edit'].setText(msg['date'])
        setup_info['note_edit'].setText(msg['note'])

    def fetch(self):
        if (not self.check_logged_in_or_in_game()):
            return
        m = 'request_user_info'
        m = {
                'type' : m,
                'username' : self.cur_user
                }

        self.send_and_wait(m)

    def update(self):
        if (not self.check_logged_in_or_in_game()):
            return
        m  = 'update_user_info'

        setup_info = self.controlsWidget['setup_info']
        note = setup_info['note_edit'].text()
        fullname = setup_info['fullname_edit'].text()
        date = setup_info['date_edit'].text()
        m = {
                'type' : m,
                'username': self.cur_user,
                'fullname' : fullname,
                'date': date,
                'note': note
                }
        self.send_and_wait(m)

    def check_user(self):
        if (not self.check_connected_or_in_game()):
            return
        checkWidget = self.controlsWidget['check_user']
        self.checkFlag = True
        username = checkWidget['username'].text().rstrip()

        m = {
                'type' : 'request_user_info',
                'username' : username
                }

        self.send_and_wait(m)

    def change_password(self):
        if (not self.check_logged_in_or_in_game()):
            return

        item = self.controlsWidget['change_password']
        oldpass = item['oldpass'].text().rstrip()
        newpass = item['newpass'].text().rstrip()
        checked = item['checkbox'].isChecked()
        if (checked):
            oldpass = hashlib.md5(bytes(oldpass, 'utf8')).hexdigest()
            newpass = hashlib.md5(bytes(newpass, 'utf8')).hexdigest()

        m = {
            'type': 'change_password', 
            'username': self.cur_user,
            'oldpass' : oldpass,
            'newpass': newpass,
            'enc' : checked
                }
        
        self.send_and_wait(m)

    def refreshOnlineUsers(self):
        if (not self.check_logged_in_or_in_game()):
            return
        m = {
                'type': 'get_online'
                }

        self.send_and_wait(m)

    def handler(self, msg):
        print(msg)
        msg = json.loads(msg)
        if (self.ingame):
            self.gameHandler(msg)
        else:
            self.controlHandler(msg)

    def startGame(self):
        if (not self.check_logged_in_or_in_game()):
            return
        ls = self.controlsWidget['startgame']['userlist']
        sel = ls.currentItem()

        if (sel is None):
            return

        sel = sel.text()
        
        user1 = self.cur_user
        user2 = sel

        m = {
                'type': 'startgame',
                'user1': user1,
                'user2': user2,
                'ship' : self.ship
        }
        self.send_and_wait(m)
        
    def uploadShip(self):
        dialog = QFileDialog.getOpenFileName(None, "Open file", ".", "(*.csv)")
        fileName = dialog[0]
        _, __  = self.loadShip(fileName)
        if (_):
            self.ship = __
            self.playerBoard.setBoard(__)
            displayMessageBox('INFO', 'Upload ship success')
        else:
            displayMessageBox('INFO', 'Upload ship failed! Invalid board!')

    def changeTurn(self):
        self.turn = not self.turn
        if (self.turn):
            self.turnlabel.setText('Your turn!')
        else:
            self.turnlabel.setText('Opponent\'s turn')

    def setTurn(self, val):
        self.turn = val
        if (self.turn):
            self.turnlabel.setText('Your turn!')
        else:
            self.turnlabel.setText('Opponent\'s turn')

    def shoot(self):
        if (not self.ingame):
            return

        if (not self.turn):
            return

        pos = self.enemyBoard.getAiming()
        if (pos is None):
            return
        m = {
                'type' : 'shoot',
                'pos' : pos
                }

        self.enemyBoard.resetShotCount()
        self.send_no_wait(m)

    def acceptInvite(self, rep, _from):
        self.ingame = True 
        self.setTurn(False)
        m = {
                'type' : 'accept',
                'rep' : rep, 
                'from': _from,
                'ship' : self.ship
                }
        self.send_no_wait(m)

    def declineInvite(self, rep, _from):
        self.ingame = False 
        m = {
                'type' : 'decline',
                'rep' : rep, 
                'from': _from
                }
        self.send_no_wait(m)

    # Handler if the user is not in game
    def controlHandler(self, msg):
        t = msg['type']
        if (t == 'status'):
            displayMessageBox('INFO', msg['mes'])
        if (t == 'status_login'):
            displayMessageBox('INFO', 'Login success')
            self.cur_user = msg['username']
            self.setInfoEdit(msg)
            return

        if (t == 'user_info'):
            if (msg['username'] == self.cur_user):
                self.setInfoEdit(msg)
            if (self.checkFlag):
                self.checkFlag = False
                check_user = self.controlsWidget['check_user']
                opt = str(check_user['box'].currentText()).lower()
                mes = f"""
                User {msg['username']}
                """
                if (opt == 'all'):
                    mes = mes + f"""
                        Fullname {msg['fullname']}
                        Date {msg['date']}
                        Note {msg['note']}
                        Point {msg['point']}
                        Online {msg['online']}
                    """
                elif (opt == 'find'):
                    mes = mes + 'User exists!'
                else:
                    mes = mes + f"""
                    {opt} {msg[opt]}
                    """
                displayMessageBox('INFO', mes)
                return

        if (t == 'online_users'):
            list_widget = self.controlsWidget['startgame']['userlist']
            list_widget.clear()
            for user in msg['users']:
                if (user == self.cur_user):
                    continue
                item = QListWidgetItem(user)
                list_widget.addItem(item)

        if (t == 'invite'):
            text = f"""
                {msg['from']} invite you.
            """
            _from = msg['from']
            rep = msg['rep']

            reply = displayYesNoBox('Invitation', text)

            if (reply):
                self.acceptInvite(rep, _from)
            else:
                self.declineInvite(rep, _from)

        if (t == 'rep_accept'):
            # The recipient accepted your invitation
            self.ingame = True
            self.playerBoard.setBoard(self.ship)
            self.enemyBoard.clear()
            rep = msg['rep']
            self.setTurn(True)
            displayMessageBox('INFO', f'{rep} accepted')

        if (t == 'rep_decline'):
            self.ingame = False
            rep = msg['rep']
            displayMessageBox('INFO', f'{rep} declined')

    # Handler if the user is in game
    def gameHandler(self, msg):
        t = msg['type']
        if (t == 'status'):
            pass

        if (t == 'hit'):
            poss = msg['pos']
            if (self.turn):
                # own turn
                for pos in poss:
                    self.enemyBoard.setHit(pos)
            else:
                for pos in poss:
                    self.playerBoard.setHit(pos)
            return

        if (t == 'miss'):
            pos = int(msg['pos'])
            if (self.turn):
                # own turn
                self.enemyBoard.setMiss(pos)
            else:
                self.playerBoard.setMiss(pos)
            self.changeTurn()
            return

        if (t == 'rematch'):
            self.setTurn(False)
            win = msg['win']
            text = ''
            if (win == self.cur_user):
                text = 'You win! Rematch?'
            else:
                text = 'You lose! Rematch?'
            want = displayYesNoBox('Rematch', text)

            if (want):
                # want a rematch
                self.rematch_accept()
            else:
                # don't want
                self.rematch_decline()
            return

        if (t == 'rematch_on'):
            user = msg['user1']
            self.ingame = True
            self.playerBoard.setBoard(self.ship)
            self.enemyBoard.clear()

            if (user == self.cur_user):
                self.setTurn(True)
            else:
                self.setTurn(False)

        if (t == 'game_close'):
            self.ingame = False

    def rematch_decline(self):
        print('Declined a rematch')
        m = {'type' : 'rematch_decline',
                'user':self.cur_user
                }
        self.send_no_wait(m)

    def rematch_accept(self):
        m = { 'type': 'rematch_accept',
                'user':self.cur_user
                }
        self.send_no_wait(m)
