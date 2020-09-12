import socket
import threading


class Server:

    def __init__(self):
        self.port = 9009
        self.host = "127.0.0.1"
        self.connections = []

        self.listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 5)
        self.listening_socket.bind((self.host, self.port))
        self.listening_socket.listen(5)
        # set up the socket to get new connections

        client_handler = threading.Thread(target=self.getNewConnections)
        client_handler.start()

        message_handler = threading.Thread(target=self.getClientMessage)
        message_handler.start()

    def _broadcast(self, message, sender):
        for client in self.connections:
            if client != sender:
                client.sendall(f"{message}\n".encode())

    def getNewConnections(self):
        while True:
            connection, address = self.listening_socket.accept()
            self.connections.append(connection)
            print(f"{address} connected to the server!")
            # gets accepts connections and stores them in a list

            username = connection.recv(1024)
            print(f"{username.decode()} has joined the chat.\n")

            self._broadcast("Welcome to the chat- Type 'QUIT' to leave - You may have to press enter after sending messages to get response".encode(), self.listening_socket)

    def getClientMessage(self):
        while True:
            for client in self.connections:
                message = client.recv(1024)
                print(message.decode())
                if message:
                    if message != "":
                        self._broadcast(message, client)
                elif not client:
                    break
                else:
                    break


server = Server()
