import socket
from ClientThread import ClientThread
from Server import Server

PORT = 55342
HOST = '0.0.0.0'

def main():
    serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversock.bind((HOST, PORT))


    print("Server started")
    print("Waiting for client request..")

    server = Server()

    while True:
        serversock.listen(1)
        clientsock, clientAddress = serversock.accept()
        newthread = ClientThread(clientAddress, clientsock, server)
        newthread.start()

if __name__=='__main__':
    main()
