from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout,QHBoxLayout, QLabel,QListWidget, QListWidgetItem, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QPaintEvent, QPen, QColor, QPainter
from PyQt5.QtCore import pyqtSlot, QEvent, QRectF, Qt

from copy import copy


SHOT_COUNT = 1
AIM = 1009
NOTHING = 0
HIT = 1001
MISS = 1002

SHIP_COLORS = {
        1: Qt.yellow,
        2: Qt.magenta,
        3: Qt.magenta,
        4: Qt.blue,
        5: Qt.blue,
        6: Qt.blue,
        7: Qt.cyan,
        8: Qt.cyan,
        9: Qt.cyan,
        10: Qt.green,
        11: Qt.green,
        12: Qt.green,
        }

STATUS_COLORS = {
        MISS : Qt.black, 
        HIT: Qt.red
        }


class Board(QWidget):
    def __init__(self, clickable : bool, color = Qt.blue):
        super().__init__()
        self.board_sz = 20
        self.board_v = [0] * self.board_sz * self.board_sz
        self.clickable = clickable
        self.gridColor = color
        self.shotCount = SHOT_COUNT

        self.curAim = None

    def size(self):
        return self.board_sz

    def setHit(self, pos):
        self.board_v[pos] = HIT
        self.update()

    def setMiss(self, pos):
        self.board_v[pos] = MISS
        self.update()

    def boundingRect(self):
        return QRectF(0, 0, self.x, self.y)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setPen(QPen(self.gridColor, 1))
        bound = min(self.width(), self.height()) - 10

        bound = (bound // self.board_sz) * self.board_sz

        m_GridDistance = bound /self.board_sz

        self.m_GridDistance = m_GridDistance

        i = 0
        while (i < bound):
            p.drawLine(i, 0, i, bound)
            p.drawLine(0, i, bound, i)
            i += m_GridDistance

        p.drawLine(i, 0, i, bound)
        p.drawLine(0, i, bound, i)

        p.setPen(Qt.red)

        t = m_GridDistance // 2

        board_sz = self.board_sz
        board_v = self.board_v
        for x in range(self.board_sz):
            for y in range(self.board_sz):
                val = board_v[y * board_sz + x]
                if (val == AIM):
                    p.setPen(Qt.red)
                    p.drawEllipse(x * m_GridDistance + 1, y * m_GridDistance + 1, m_GridDistance - 2, m_GridDistance - 2)
                    p.drawLine(x * m_GridDistance, y * m_GridDistance + t, x * m_GridDistance + m_GridDistance, y * m_GridDistance + t)
                    p.drawLine(x * m_GridDistance + t, y * m_GridDistance, x * m_GridDistance + t, y * m_GridDistance + m_GridDistance)
                
                if (val >= 1 and val <= 12):
                    p.fillRect(x * m_GridDistance + 1, y * m_GridDistance + 1, m_GridDistance - 1, m_GridDistance - 1, SHIP_COLORS[val]);

                if (val == HIT or val == MISS):
                    p.fillRect(x * m_GridDistance + 1, y * m_GridDistance + 1, m_GridDistance - 1, m_GridDistance - 1, STATUS_COLORS[val]);

        if (self.clickable):
            last_y = int(m_GridDistance * self.board_sz) + 20
            last_x = 0
            p.drawText(last_x, last_y, str(self.shotCount))

    def mouseReleaseEvent(self, event):
        if (not self.clickable):
            return

        x = event.pos().x()
        y = event.pos().y()
        x //= self.m_GridDistance
        y //= self.m_GridDistance

        # print(x, y)

        if (x >= self.board_sz or x < 0):
            return
        if (y >= self.board_sz or y < 0):
            return

        board_v = self.board_v

        pos = int(y * self.board_sz  + x)

        if (event.button() == Qt.LeftButton):
            if (board_v[pos] != NOTHING):
                return
            if (self.shotCount == 0):
                return
            board_v[pos] = AIM
            self.shotCount = 0
            self.curAim = pos
        elif (event.button() == Qt.RightButton):
            if (board_v[pos] == AIM):
                board_v[pos] = NOTHING
                self.shotCount = 1
                self.curAim = None
        self.update()

    def setBoard(self, ships):
        self.board_v = copy(ships)
        self.update()

    def clear(self):
        for i in range(len(self.board_v)):
            self.board_v[i] = NOTHING
        self.shotCount = SHOT_COUNT
        self.curAim = None
        self.update()

    def getAiming(self):
        pos = self.curAim
        self.board_v[pos] = NOTHING
        self.curAim = None
        self.update()
        return pos


    def resetShotCount(self):
        self.shotCount = SHOT_COUNT

    def checkCellEmpty(self, pos):
        return self.board_v[pos] == 0

