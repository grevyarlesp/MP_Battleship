import json
from collections import deque

BOARD_SZ = 400

offset = [1, -1, -20, +20]


# Flood fill and set
def bfs(board, pos, val):
    assert len(board) == BOARD_SZ
    vis = [False] * BOARD_SZ

    color = board[pos]
    vis[pos] = True

    ret = []
    q = deque([pos])
    while (q):
        u = q.popleft()
        board[u] = val
        ret.append(u)
        for t in offset:
            v = u + t
            if (v < 0 or v >= BOARD_SZ):
                continue
            if (vis[v]):
                continue
            if (color == board[v]):
                vis[v] = True
                q.append(v)
    return ret

def to_json_dumps(msg):
    return json.dumps(msg) + '|'

def load_msg(msg):
    return msg.split('|')
