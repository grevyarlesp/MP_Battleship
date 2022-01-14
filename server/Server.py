import sqlite3
import threading
import socket
import json

from utils import *

class Server:
    def __init__(self):
        self._lock = threading.Lock()
        self._online = {}
        self.boards = {}

        self._ingame = set()

    def setBoard(self, username, board):
        with self._lock:
            self.boards[username] = board

    def setInGame(self, username):
        with self._lock:
            self._ingame.add(username)

    def unsetInGame(self, username):
        with self._lock:
            self._ingame.remove(username)

    def checkInGame(self, username):
        with self._lock:
            return username in self._ingame

    def getBoard(self, username):
        with self._lock:
            return self.boards[username]

    def addOnline(self, username, sock : socket.socket):
        with self._lock:
            self._online[username] = sock

    def removeOnline(self, username):
        with self._lock:
            self._online.pop(username, None)

    def checkOnline(self, username):
        with self._lock:
            return username in self._online

    def getOnlineUsers(self):
        with self._lock:
            return list(self._online.keys())

    def getSock(self, user):
        with self._lock:
            return self._online[user]


    # user 1 invite user 2
    def sendInvitation(self, user1, user2):
        with self._lock:
            sock1 = self._online[user1]
            sock2 = self._online[user2]
            m =  {
                'type' : 'invite',
                'rep' : user2,
                'from' : user1
                    }
            data = json.dumps(m)
            sock2.send(bytes(data, 'utf-8'))
