import socket, threading
import json
import hashlib
from Server import Service

class  ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket):

        print ("New connection added: ", clientAddress)
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.clientAddress = clientAddress

    def run(self):
        print ("Connection from : ", self.clientAddress)
        self.service = Service()
        msg = ''
        while True:
            data = self.csocket.recv(2048)
            msg = data.decode()
            if msg=='close' or not msg:
              break

            print ("from client", msg)
            m = json.loads(msg)
            if (m['type'] == 'register'):
                self.register(m['username'], m['password'], m['enc'])
            if (m['type'] == 'login'):
                self.login(m['username'], m['password'], m['enc'])

            if (m['type'] == 'request_user_info'):
                self.send_user_info(m['username'])

        print ("Client at ", self.clientAddress , " disconnected...")

    def login(self, username, password, enc):
        if (not enc):
            password = hashlib.md5(bytes(password, 'utf8')).hexdigest()
        res, m = self.service.login(username, password)
        if (not res):
            m = "Login failed\n" + m
            m = {
                    'type': 'status',
                    'mes': m
                }
            data = json.dumps(m)
            self.csocket.send(bytes(data, 'utf-8'))
        else:
            self.send_user_info(username, t = 'status_login')

    def send_user_info(self, username, t = 'user_info'):
        assert t in ['user_info', 'status_login']
        res, m = self.service.get_user_info(username)
        if (not res):
            m = {
                    'type': 'status',
                    'mes': m
            }
            data = json.dumps(m)
            self.csocket.send(bytes(data, 'utf-8'))
            return
        m = {
            'type' : t,
            'username' : m[0],
            'fullname' : str(m[1] or ''),
            'date' : str(m[2] or ''),
            'note' : str(m[3] or ''),
            'point' : str(m[4] or '')
                }
        data = json.dumps(m)
        print(data)
        self.csocket.send(bytes(data, 'utf-8'))

    def register(self, username, password, enc):
        if (not enc):
            password = hashlib.md5(bytes(password, 'utf8')).hexdigest()

        print('Register' , username, password)
        res = self.service.register(username, password)
        m = "Register success"
        if (res):
            m = "Register success\nPlease login"
        else:
            m = "Register failed: Username exists\nPlease login"
        m = {
                'type': 'status',
                'mes': m
            }
        data = json.dumps(m)
        self.csocket.send(bytes(data, 'utf-8'))

    def change_password(self, username, oldpass, newpass, enc):
        if (not enc):
            oldpass = hashlib.md5(bytes(oldpass, 'utf8')).hexdigest()
            newpass = hashlib.md5(bytes(newpass, 'utf8')).hexdigest()

