from PyQt5.QtNetwork import QTcpSocket, QHostAddress, QAbstractSocket
import sys
import logging
import time

"""
Managing connections, sending message...
"""
DEFAULT_SERVER_PORT = 55342

class SocketWrapper():
    def __init__(self, controller):
        self.__socket = QTcpSocket()
        self.__socket.bind(QHostAddress.LocalHost)
        self.port = self.__socket.localPort()
        self.controller = controller
        self.logger = logging.getLogger("Connection")
        self.logger.debug(self.port)

    def connect(self, remoteAddress, port):
        self.__socket = QTcpSocket()

        if not port:
            port = DEFAULT_SERVER_PORT
        else:
            port = int(port)

        if not remoteAddress:
            remoteAddress = QHostAddress.LocalHost

        self.logger.debug(f'Attempting to connect to {remoteAddress} {port}')
        self.__socket.connectToHost(remoteAddress, port)
        self.__socket.waitForConnected()
        if (self.__socket.state() != QAbstractSocket.ConnectedState):
            self.logger.debug('Connection Fail')
            return False

        self.__socket.setSocketOption(QAbstractSocket.KeepAliveOption, 1)
        self.__socket.setSocketOption(QAbstractSocket.LowDelayOption, 1)
        self.__socket.disconnected.connect(self.__onDisconnected) 
        self.__socket.readyRead.connect(self.readyRead)
        return True

    def disconnect(self):
        self.__socket.disconnectFromHost()


    def writeData(self, data):
        self.__socket.write(bytes(data, 'utf-8'))

    def readyRead(self):
        msg = str(self.__socket.readAll(), 'utf-8')
        self.controller.handler(msg)

    def waitForReadyRead(self):
        self.__socket.waitForReadyRead()

    def __onDisconnected(self):
        self.logger.debug('Disconnected')

