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
        self.widgetsDict = widgetsDict
        self.connected = False
        self.controlsWidget = self.widgetsDict['control']
        self.con = SocketWrapper(self)

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
        msg = json.loads(msg)
        if (msg['type'] == 'status'):
            box = QMessageBox()
            box.setWindowTitle('INFO')
            box.setText(msg['mes'])
            box.exec()
            


