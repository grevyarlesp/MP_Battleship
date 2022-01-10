import socket
from ClientThread import ClientThread

PORT = 55342
HOST = '127.0.0.1'

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))


    print("Server started")
    print("Waiting for client request..")

    while True:
        server.listen(1)
        clientsock, clientAddress = server.accept()
        newthread = ClientThread(clientAddress, clientsock)
        newthread.start()

if __name__=='__main__':
    main()
