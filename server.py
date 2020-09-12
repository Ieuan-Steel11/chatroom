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

    def _broadcast(self, sender, message):
        for client in self.connections:
            if client != self.listening_socket and client != sender:
                try:
                    client.sendall(message.encode("ascii"))
                except:
                    print("Error: could not send message")

    def getNewConnections(self):
        while True:
            connection, address = self.listening_socket.accept()
            self.connections.append(connection)
            # gets accepts connections and stores them in memory

            username = connection.recv(1024)
            print(f"{address} connected to the server!")
            print(f"{username} has joined the chat.\n")

    def getClientMessage(self):
        while True:
            for client in self.connections:
                message = client.recv(1024)
                if message:
                    print(message)
                    self._broadcast(sender=client, message=message)
                else:
                    break


server = Server()
