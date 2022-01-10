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

        print ("Client at ", self.clientAddress , " disconnected...")

    def login(self, username, password, enc):
        if (not enc):
            password = hashlib.md5(bytes(password, 'utf8')).hexdigest()

        print(username, password)
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


    def register(self, username, password, enc):
        if (not enc):
            password = hashlib.md5(bytes(password, 'utf8')).hexdigest()

        print(username, password)
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

