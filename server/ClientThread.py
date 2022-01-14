from os import wait
import socket, threading
import json
import hashlib
from Server import Server
from dbservice import DBService

import time

from GameThread import GameThread

from utils import to_json_dumps

class  ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket, server):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.clientAddress = clientAddress

        print ("New connection added: ", clientAddress)

        self.cur_user = None

        self.server = server

        self.ship = None

    def send_status(self, m):
        m = {
                    'type': 'status',
                    'mes': m
            }
        data = to_json_dumps(m)
        self.csocket.send(bytes(data, 'utf-8'))

    def run(self):
        print ("Connection from : ", self.clientAddress)
        self.dbservice = DBService()
        msg = ''
        while True:
            if (self.server.checkInGame(self.cur_user)):
                time.sleep(2)
                continue

            data = self.csocket.recv(2048).decode()
            if (not data):
                break
            msgs = data.split('|')

            term = False
            for msg in msgs:
                if (not msg):
                    continue
                if msg=='close':
                    term = True
                    break
                print ("from client", msg)
                m = json.loads(msg)
                self.control_handler(m)
            if (term):
                break

            # if in game -> hand control to other thread

        print ("Client at ", self.clientAddress , " disconnected...")
        if (self.cur_user != None):
            self.server.removeOnline(self.cur_user)

    def control_handler(self, m):
        if (m['type'] == 'register'):
            self.register(m['username'], m['password'], m['enc'])

        if (m['type'] == 'login'):
            self.login(m['username'], m['password'], m['enc'])

        if (m['type'] == 'request_user_info'):
            self.send_user_info(m['username'])
        if (m['type'] == 'update_user_info'):
            self.update_user_info(m)
        if (m['type'] == 'change_password'):
            self.change_password(m['username'], m['oldpass'], m['newpass'], m['enc'])

        if (m['type'] == 'get_online'):
            self.send_online_users()

        if (m['type'] == 'startgame'):
            self.invite_and_start_game(m)
            
        if (m['type'] == 'accept'):
            self.accept_handler(m)

        if (m['type'] == 'decline'):
            self.decline_handler(m)


    def login(self, username, password, enc):
        if (not enc):
            password = hashlib.md5(bytes(password, 'utf8')).hexdigest()
        res, m = self.dbservice.login(username, password)
        if (not res):
            m = "Login failed\n" + m
            m = {
                    'type': 'status',
                    'mes': m
                }
            data = to_json_dumps(m)
            self.csocket.send(bytes(data, 'utf-8'))
        else:
            # Login successful
            # Success login
            self.send_user_info(username, t = 'status_login')

            if (self.cur_user != None):
                self.server.removeOnline(self.cur_user)

            self.cur_user = username
            self.server.addOnline(self.cur_user, self.csocket)

    def send_user_info(self, username, t = 'user_info'):
        assert t in ['user_info', 'status_login']
        res, m = self.dbservice.get_user_info(username)
        if (not res):
            self.send_status(m)
            return

        online = self.server.checkOnline(username)

        m = {
            'type' : t,
            'username' : m[0],
            'fullname' : str(m[1] or ''),
            'date' : str(m[2] or ''),
            'note' : str(m[3] or ''),
            'point' : str(m[4] or ''),
            'online': online
                }

        data = to_json_dumps(m)
        print(data)
        self.csocket.send(bytes(data, 'utf-8'))

    def register(self, username, password, enc):
        if (not enc):
            password = hashlib.md5(bytes(password, 'utf8')).hexdigest()
        print('Register' , username, password)
        res = self.dbservice.register(username, password)
        m = "Register success"
        if (res):
            m = "Register success\nPlease login"
        else:
            m = "Register failed: Username exists\nPlease login"
        m = {
                'type': 'status',
                'mes': m
            }
        data = to_json_dumps(m)

        self.csocket.send(bytes(data, 'utf-8'))

    def change_password(self, username, oldpass, newpass, enc):
        if (not enc):
            oldpass = hashlib.md5(bytes(oldpass, 'utf8')).hexdigest()
            newpass = hashlib.md5(bytes(newpass, 'utf8')).hexdigest()
        res, m = self.dbservice.change_password(username, oldpass, newpass)
        if (not res):
            m = "Password change failed\n" + m
        self.send_status(m)

    def update_user_info(self, m):
        fullname = m['fullname']
        username = m['username']
        date = m['date']
        note = m['note']

        m = "Update user info failed"
        if (self.dbservice.update_user_info(username, fullname, date, note)):
            m = "Update user info success";
        self.send_status(m)

    def send_online_users(self):
        t = self.server.getOnlineUsers()
        print(t)
        m = {
                'type' : 'online_users',
                'users': t
                }
        data = to_json_dumps(m)
        self.csocket.send(bytes(data, 'utf-8'))

    def invite_and_start_game(self, m):
        self.ship = m['ship']
        self.server.setBoard(self.cur_user, m['ship'])
        self.server.sendInvitation(m['user1'], m['user2'])

    # _from send rep invite
    # cur_user is rep 
    # rep asks server to start a game
    def accept_handler(self, m):
        rep = m['rep']
        _from = m['from']

        self.server.setBoard(self.cur_user, m['ship'])
        sock = self.server.getSock(_from)
        m = {
                'type': 'rep_accept', 
                'rep' : rep,
                'from' : _from
                }


        data = to_json_dumps(m)
        sock.send(bytes(data, 'utf-8'))

        self.server.setInGame(rep)
        self.server.setInGame(_from)
        # Start game
        gamethread = GameThread(self.server, _from, rep)
        gamethread.start()

    def decline_handler(self, m):
        rep = m['rep']
        _from = m['from']
        sock = self.server.getSock(_from)
        m = {
                'type': 'rep_decline', 
                'rep' : rep,
                'from' : _from
                }
        data = to_json_dumps(m)
        sock.send(bytes(data, 'utf-8'))
