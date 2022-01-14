from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLineEdit, QCheckBox, QListWidget, QLabel, QComboBox

from mytabwidget import MyTabWidget


import sys
import json
import os
import logging

from board import Board
from Controller import Controller

def get_open_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("",0))
    s.listen(1)
    port = s.getsockname()[1]
    return port



class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Battleship'
        self.left = 0
        self.top = 0

        self.height = 300
        self.width = 800
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.InitWidget()
        self.controller = Controller(self.widgetsDict)
        self.InitUI()

    def InitWidget(self):
        self.widgetsDict = {
                'control': {
                    'connect': {
                        'title' : 'Connect',
                        'label1' : QLabel('Server IP'),
                        'ip': QLineEdit(),
                        'label2' : QLabel('Server Port'),
                        'port': QLineEdit(),
                        'connectbutton' : QPushButton('Connect'),
                        'closebutton' : QPushButton('Close')
                        },

                    'register': {
                        'title' : 'Register',
                        'label1' : QLabel('Username'),
                        'username': QLineEdit(),
                        'label2' : QLabel('Password'),
                        'pass': QLineEdit(),
                        'checkbox': QCheckBox('Encrypt?'),
                        'button' : QPushButton('Register')
                    },
                    'login': {
                        'title' : 'Login',
                        'label1' : QLabel('Username'),
                        'username': QLineEdit(),
                        'label2' : QLabel('Password'),
                        'pass': QLineEdit(),
                        'checkbox': QCheckBox('Encrypt?'),
                        'button' : QPushButton('Login')
                    },
                    'change_password': {
                        'title' : 'Change Password',
                        'label1' : QLabel('Old password'),
                        'oldpass': QLineEdit(),
                        'label2' : QLabel('New password'),
                        'newpass': QLineEdit(),
                        'checkbox': QCheckBox('Encrypt?'),
                        'button' : QPushButton('Change')
                    },
                    'check_user': {
                        'title' : 'Check',
                        'username': QLineEdit(),
                        'box' : QComboBox(),
                        'button' : QPushButton('Check')
                    },
                    'setup_info': {
                        'title' : 'User Info', 
                        'username_label': QLabel(),
                        'label1' :QLabel('Fullname'),
                        'fullname_edit': QLineEdit(),
                        'label2' : QLabel('Date'),
                        'date_edit': QLineEdit(),
                        'label3' : QLabel('Note'),
                        'note_edit': QLineEdit(),
                        'fetch_button' : QPushButton('Fetch'),
                        'update_button' : QPushButton('Update'),
                    },
                    'startgame': {
                        'title': 'Start game',
                        'uploadshipbutton' : QPushButton('Upload Ship'),
                        'refreshbutton' : QPushButton('Refresh'),
                        'userlist' : QListWidget(),
                        'startbutton' : QPushButton('Start Game')
                    },

                },
                'PlayerBoard': Board(clickable = False, color = Qt.blue),
                'EnemyBoard': Board(clickable = True, color = Qt.red),
                'turnlabel' : QLabel()
                }

        self.widgetsDict['control']['login']['pass'].setEchoMode(QLineEdit.Password)
        self.widgetsDict['control']['register']['pass'].setEchoMode(QLineEdit.Password)
        self.widgetsDict['control']['change_password']['oldpass'].setEchoMode(QLineEdit.Password)
        self.widgetsDict['control']['change_password']['newpass'].setEchoMode(QLineEdit.Password)

        combobox = ['Find', 'Online', 'Date', 'Fullname', 'Note', 'Point', 'All']

        for item in combobox:
            self.widgetsDict['control']['check_user']['box'].addItem(item)

        return self.widgetsDict

    def InitUI(self):
        self.centralWidget = QWidget()
        self.centralLayout = QVBoxLayout()
        self.centralWidget.setLayout(self.centralLayout)
        self.tab_widget = MyTabWidget(self, self.widgetsDict, self.controller)
        self.setCentralWidget(self.centralWidget)
        self.centralLayout.addWidget(self.tab_widget)
        self.show()

def main():

    logging.basicConfig(level = logging.DEBUG)


    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

if __name__=='__main__':
    main()
