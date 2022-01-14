import socket, threading
import json
import hashlib
from Server import Server
from dbservice import DBService
import selectors

from utils import bfs
SHIP_COUNT = 12

class GameThread(threading.Thread):
    def __init__(self, server, user1, user2):
        threading.Thread.__init__(self)
        self.server = server

        self.user1 = user1
        self.user2 = user2

        self.c1sock = self.server.getSock(user1)
        self.c2sock = self.server.getSock(user2)

        self.initGame()

        self.ingame = True

        print(self.rem1, self.rem2)

    def initGame(self):
        # 0 -> client 1, 1 -> client 2
        self.cur_turn = 0
        self.board1 = self.server.getBoard(self.user1)
        self.board2 = self.server.getBoard(self.user2)
        self.rem1 = SHIP_COUNT
        self.rem2 = SHIP_COUNT

    def run(self):
        print(f'New game started between {self.user1} and {self.user2}')
        while (True):
            if (self.cur_turn):
                print(f'{self.user2} turn')
                data = self.c2sock.recv(2048)
            else:
                print(f'{self.user1} turn')
                data = self.c1sock.recv(2048)
            
            msg = data.decode()
            if (not msg):
                break
            m = json.loads(msg)

            print('game', m)
            self.game_handler(m)
            if (not self.ingame):
                break
        
        print('Game ended because one of the client disconnected or game finished')

        mes = {
            'type' : 'game_close', 
            }
        data= json.dumps(mes)
        self.c1sock.send(bytes(data, 'utf-8'))
        self.c2sock.send(bytes(data, 'utf-8'))

        self.cleanup()
            
    def game_handler(self, m):
        if (m['type'] == 'shoot'):
            # check
            hit = None
            pos = int(m['pos'])
            board = []
            if (self.cur_turn == 0):
                # PLayer 1 turn 
                board = self.board2
            else:
                # player 2 turn 
                board = self.board1

            if (board[pos] != 0):
                hit = True
            else:
                hit = False

            mes = {}
            if (hit):
                ret = bfs(board, pos, 0)
                mes = {
                        'type' : 'hit', 
                        'pos' : ret
                        }

                if (self.cur_turn == 0):
                    # player 1 turn 
                    self.rem2 -= 1
                    if (self.rem2 == 0):
                        # User 2 lose
                        self.endgame_and_send_rematch(self.user1, self.user2)
                        pass
                else:
                    self.rem1 -= 1
                    if (self.rem1 == 0):
                        # User 1 lose
                        self.endgame_and_send_rematch(self.user2, self.user1)
                        pass
            else:
                self.cur_turn = not self.cur_turn
                mes = {
                        'type' : 'miss', 
                        'pos' : pos
                        }
                data = json.dumps(mes)
                self.c1sock.send(bytes(data, 'utf-8'))
                self.c2sock.send(bytes(data, 'utf-8'))

    def endgame_and_send_rematch(self, win, lose):
        m = {
                'type'  : 'rematch', 
                'win' : win, 
                'lose' : lose
                }

        sel = selectors.DefaultSelector()
        sel.register(self.c1sock, selectors.EVENT_READ, data = None)
        sel.register(self.c2sock, selectors.EVENT_READ, data = None)
        print("OK, game end!")

        data = json.dumps(m)
        self.c1sock.send(bytes(data, 'utf-8'))
        self.c2sock.send(bytes(data, 'utf-8'))
        
        cnt = 0
        num_accept = 0
        while (cnt < 2):
            events = sel.select(timeout = None)
            for key, mask in events:
                sock = key.fileobj 
                data = sock.recv(2048)
                msg = data.decode()
                m = json.loads(msg)
                if (m['type'] == 'rematch_accept'):
                    num_accept += 1
                cnt = cnt + 1
        if (num_accept == 2):
            self.init_rematch()
        else:
            self.ingame = False

    def init_rematch(self):
        m = {
                'type' : 'rematch_on',
                'user1' : self.user1,
                'user2' : self.user2
                }
        data = json.dumps(m)
        self.c1sock.send(bytes(data, 'utf-8'))
        self.c2sock.send(bytes(data, 'utf-8'))

    def cleanup(self):
        self.server.unsetInGame(self.user1)
        self.server.unsetInGame(self.user2)
        m = {
                'type' : 'game_off',
                }

        data = json.dumps(m)
        self.c1sock.send(bytes(data, 'utf-8'))
        self.c2sock.send(bytes(data, 'utf-8'))

        # Close this thread
        self.ingame = False


