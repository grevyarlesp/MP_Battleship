from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLineEdit, QCheckBox, QListWidget, QLabel, QComboBox

from mytabwidget import MyTabWidget


import readline
import sys
import json
import os
import socket


from board import Board
from Controller import Controller


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Battleship'
        self.left = 0
        self.top = 0
        self.width = 1000
        self.height = 680
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
                        'ConnectIpText': QLineEdit(),
                        'label2' : QLabel('Server Pass'),
                        'ConnectIpPort': QLineEdit(),
                        'button' : QPushButton('Connect')
                        },
                    'login': {
                        'title' : 'Login',
                        'label1' : QLabel('Username'),
                        'LoginUsernameText': QLineEdit(),
                        'label2' : QLabel('Password'),
                        'LoginPassText': QLineEdit(),
                        'checkbox': QCheckBox('Encrypt?'),
                        'button' : QPushButton('Login')
                    },
                    'register': {
                        'title' : 'Register',
                        'label1' : QLabel('Username'),
                        'RegisterUserNameText': QLineEdit(),
                        'label2' : QLabel('Password'),
                        'RegisterPassText': QLineEdit(),
                        'checkbox': QCheckBox('Encrypt?'),
                        'button' : QPushButton('Register')
                    },
                    'check_user': {
                        'title' : 'Check',
                        'username': QLineEdit(),
                        'box' : QComboBox(),
                        'button' : QPushButton('Check')
                    },
                    'setup_info': {
                        'title' : 'User Info', 
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
                        'refreshbutton' : QPushButton('Refresh'),
                        'userlist' : QListWidget(),
                        'startbutton' : QPushButton('Start Game')
                    },

                },
                'PlayerBoard': Board(clickable = False, color = Qt.blue),
                'EnemyBoard': Board(clickable = True, color = Qt.red)
                }

        self.widgetsDict['control']['login']['LoginPassText'].setEchoMode(QLineEdit.Password)
        self.widgetsDict['control']['register']['RegisterPassText'].setEchoMode(QLineEdit.Password)
        self.widgetsDict['control']['check_user']['box'].addItem('Find')
        self.widgetsDict['control']['check_user']['box'].addItem('Online')
        self.widgetsDict['control']['check_user']['box'].addItem('Date')
        self.widgetsDict['control']['check_user']['box'].addItem('Fullname')
        self.widgetsDict['control']['check_user']['box'].addItem('Note')
        self.widgetsDict['control']['check_user']['box'].addItem('Point')
        self.widgetsDict['control']['check_user']['box'].addItem('All')

        return self.widgetsDict

    def InitUI(self):
        self.centralWidget = QWidget()
        self.centralLayout = QVBoxLayout()
        self.centralWidget.setLayout(self.centralLayout)
        self.tab_widget = MyTabWidget(self, self.widgetsDict, self.controller)
        self.setCentralWidget(self.centralWidget)
        self.centralLayout.addWidget(self.tab_widget)
        self.show()

user = {
        "username" : None,
        "password" : None,
        "fullname" : None,
        "date": None,
        "note": None,
        }

def get_open_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("",0))
    s.listen(1)
    port = s.getsockname()[1]
    return port

def connect(ip, port):
    pass

def close():
    pass

def login():
    req = {}
    req["type"] = "login"
    username = input('login: ')
    req["username"] = username
    passw = getpass.getpass('password: ')
    req["password"] = passw
    encr = input('encrypt? (y/n): ')
    req["enc"] = False
    if (encr == 'y'):
        # Encrypt with base 64 or sth
        pass

def register():
    req = {}
    req["type"] = "login"
    username = input('login: ')
    req["username"] = username
    passw = getpass.getpass('password: ')
    req["password"] = passw
    encr = input('encrypt? (y/n): ')
    req["enc"] = False

    if (encr == 'y'):
        # Encrypt with base 64 or sth
        pass

def change_password():
    req = {}
    req["type"] = "change_password"
    pass

def check_user():
    req = {}
    req["type"] = "check_user"
    pass
def setup_info():
    req = {}
    req["type"] = "setup_info"
    pass

def start_game():
    assert(user["username"] is not None)
    print("start")


def gameloop():
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server_address = '/tmp/battleship_local_socket'
    prog = '../debug/Socket_Battleship'
    try:
        os.unlink(server_address)
    except:
        pass
    sock.bind(server_address)
    sock.listen(1)

    print('waiting for a connection from gui')
    # os.system(prog)
    connection, client_address = sock.accept()
    print('gui connected!!!', client_address)
    print('prepare your ships and press enter to start the game')
    t = input('> ')
    connection.sendall(b'START 1')
    while True:
        data = connection.recv(4096)
        if (not data):
            break
        print(data.decode('ascii'))
        t = data.split()

def main():
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

if __name__=='__main__':
    main()
