import socket, threading
import json
import hashlib
from Server import Server
from dbservice import DBService
import selectors

from utils import bfs, to_json_dumps, load_msg
from dbservice import DBService
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

        self.sel = selectors.DefaultSelector()
        self.sel.register(self.c1sock, selectors.EVENT_READ, data = None)
        self.sel.register(self.c2sock, selectors.EVENT_READ, data = None)

        print(self.rem1, self.rem2)


    def initGame(self):
        # 0 -> client 1, 1 -> client 2
        self.server.setInGame(self.user1)
        self.server.setInGame(self.user2)
        self.cur_turn = 0
        self.board1 = self.server.getBoard(self.user1)
        self.board2 = self.server.getBoard(self.user2)
        self.rem1 = SHIP_COUNT
        self.rem2 = SHIP_COUNT
        self.ingame = True

    def run(self):

        self.dbservice = DBService()
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
            msgs = msg.split('|')

            for msg in msgs:
                if (not msg):
                    continue

                print('game', msg)
                m = json.loads(msg)
                self.game_handler(m)
                if (not self.ingame):
                    self.endgame_and_cleanup()
                    return

        self.endgame_and_cleanup()
            
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
                else:
                    self.rem1 -= 1
            else:
                self.cur_turn = not self.cur_turn
                mes = {
                        'type' : 'miss', 
                        'pos' : pos
                        }

            # Send the mess for both cases
            data = to_json_dumps(mes)
            self.c1sock.send(bytes(data, 'utf-8'))
            self.c2sock.send(bytes(data, 'utf-8'))

            if (self.rem1 == 0):
                # User 1 lose
                self.endgame_and_send_rematch(self.user2, self.user1)
            elif (self.rem2 == 0):
                # User 2 lose
                self.endgame_and_send_rematch(self.user1, self.user2)

    def endgame_and_send_rematch(self, win, lose):
        m = {
                'type'  : 'rematch', 
                'win' : win, 
                'lose' : lose
                }

        self.dbservice.update_point_add_1(win)

        sel = self.sel

        print("OK, game end!")


        data = to_json_dumps(m)
        self.c1sock.send(bytes(data, 'utf-8'))
        self.c2sock.send(bytes(data, 'utf-8'))
        
        cnt = 0
        num_accept = 0
        acc = set()
        cnt = set()
        while (len(cnt) < 2):
            events = sel.select(timeout = None)
            for key, mask in events:
                sock = key.fileobj 
                data = sock.recv(2048)
                msgs = data.decode().split('|')
                for msg in msgs:
                    if (not msg):
                        continue
                    m = json.loads(msg)
                    if (m['type'] == 'rematch_accept'):
                        acc.add(m['user'])
                    cnt.add(m['user'])
        num_accept = len(acc)
        print(acc)
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

        data = to_json_dumps(m)
        self.c1sock.send(bytes(data, 'utf-8'))
        self.c2sock.send(bytes(data, 'utf-8'))
        self.initGame()

    def endgame_and_cleanup(self):
        print('Game ended')
        mes = {
            'type' : 'game_close', 
            }

        data = to_json_dumps(mes)
        self.c1sock.send(bytes(data, 'utf-8'))
        self.c2sock.send(bytes(data, 'utf-8'))

        self.server.unsetInGame(self.user1)
        self.server.unsetInGame(self.user2)

        # Close this thread
        self.ingame = False
        self.sel.close()


