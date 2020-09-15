import socket
import sys
import select


class Server:

    def __init__(self):
        self.port = 6000
        self.host = "127.0.0.1"
        self.listening_socket = None
        # init var to store serverside connection

        self.startServer()

        self.connections = []
        self.connections.append(self.listening_socket)

        self.writeToLog("\t\t End of session \n\n")
        # signifies end of old session when new one boots up

        self.handle_clients()

    def handle_clients(self):
        while True:
            read_sockets, write_sockets, error_sockets = select.select(self.connections, [], [])
            # selects sockets when there's activity we only care about read ones so the others are empty lists

            for sock in read_sockets:
                if sock != self.listening_socket:
                    self.getNewClientMessages(sock)
                    # if its the listening socket connect the new user
                else:
                    self.getNewClients()
                    # else it is a message from one of the clients

    def getNewClientMessages(self, sock):
        message = sock.recv(1024)
        self.writeToLog(message.decode())
        # gets messages from teh socket with activity in readable sockets

        if message:
            self._broadcast(message, sock)
            # send the message if it isn't blank

    def getNewClients(self):
        connection, address = self.listening_socket.accept()

        username = connection.recv(1024)
        # gets username from client

        self.writeToLog(f"{address} connected to the server!")
        self.writeToLog(f"{username.decode()} has joined the chat.\n")

        self.connections.append(connection)
        # gets accepts connections and stores them in a list

    def _broadcast(self, message, sender):
        for client in self.connections:
            if client != sender and client != self.listening_socket:
                # if it isn't the one who sent the message or the server
                client.sendall(message)
                self.writeToLog(f"{message}\n")

    def shutdown(self):
        self._broadcast("Server: The server is being shut down", self.listening_socket)
        # sends msg
        if self.connections:
            for client in self.connections:
                if client != self.listening_socket:
                    client.close()
                    # closes every connection

        self.writeToLog("\t\tEnd of Session\t\t \n\n")
        sys.exit(0)

    def startServer(self):
        self.listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listening_socket.bind((self.host, self.port))
        self.listening_socket.listen(1)
        # set up the socket to get new connections

    @staticmethod
    def writeToLog(log_message):
        with open("log.txt", "a") as log:
            # opens a log file to note down server activity
            log.write(log_message + "\n")


server = Server()
