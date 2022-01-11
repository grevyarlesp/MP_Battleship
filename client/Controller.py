from os import wait
from PyQt5.QtCore import pyqtSlot, Qt
from socketwrapper import SocketWrapper
import sys
import json
import hashlib

from PyQt5.QtWidgets import QMessageBox

"""
Controller: takes a widget dicts as input. Access all element of the GUI.
"""
class Controller():
    def __init__(self, widgetsDict):
        self.cur_user = None

        self.widgetsDict = widgetsDict
        self.connected = False
        self.controlsWidget = self.widgetsDict['control']
        self.con = SocketWrapper(self)

    def check_connected(self):
        """
        Check if client is connected to a server
        """
        if (self.con.check_connected()):
            box = QMessageBox()
            box.setWindowTitle('INFO')
            box.setText('Please connect first!')
            box.exec()
            return False
        return True

    def check_logged_in(self):
        """
        Check if client is logged in 
        """
        if (not self.check_connected()):
            return False
        if (self.cur_user is None):
            box = QMessageBox()
            box.setWindowTitle('INFO')
            box.setText('Not logged in, please log in!')
            box.exec()
            return False
        return True

    def connect(self, ip, port):
        self.connected = True
        port = port.rstrip()
        ip = ip.rstrip()
        if (not self.con.connect(ip, port)):
            sys.exit(0)

    def close(self):
        if (not self.connected):
            return
        self.connected = False
        self.con.writeData('close')
        self.con.disconnect()

    def login(self, user, password, enc):
        if (not self.check_connected()):
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
        data = json.dumps(m)
        self.con.writeData(data)
        self.con.waitForReadyRead()

    def register(self, user, password, enc):
        if (not self.check_connected()):
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
        data = json.dumps(m)
        self.con.writeData(data)
        self.con.waitForReadyRead()

    def handler(self, msg):
        print(msg)
        msg = json.loads(msg)

        if (msg['type'] == 'status'):
            box = QMessageBox()
            box.setWindowTitle('INFO')
            box.setText(msg['mes'])
            box.exec()
            return

        if (msg['type'] == 'status_login'):
            box = QMessageBox()
            box.setWindowTitle('INFO')
            box.setText('login success')
            box.exec()
            self.cur_user = msg['username']
            return
        if (msg['type'] == 'user_info'):

    def setInfoEdit(self, msg):
        setup_info = self.controlsWidget['setup_info']
        setup_info['username_label'].setText(msg['username'])
        setup_info['fullname_edit'].setText(msg['fullname'])
        setup_info['date_edit'].setText(msg['date'])
        setup_info['note_edit'].setText(msg['note'])

    def fetch(self):
        if (not self.check_logged_in()):
            return
        m = 'request_user_info'
        m = {
                'type' : m,
                'username' : self.cur_user
                }
        data = json.dumps(m)
        self.con.writeData(data)
        self.con.waitForReadyRead()
        
        
