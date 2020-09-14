import socket
import sys


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

        self.handle_clients()
        # starts up the server

    def handle_clients(self):
        print("control + c to quit")
        while True:
            self.getNewClients()
            self.getNewClientMessages()
            # puts it neatly in one loop in stead of failing parallelism

    def getNewClientMessages(self):
        # gets clients messages
        for client in self.connections:
            message = client.recv(1024)
            self.writeToLog(message.decode())

            if message:
                if message != "":
                    self._broadcast(message, client)
            elif not client:
                break
            else:
                break

    def getNewClients(self):
        # gets new clients
        connection, address = self.listening_socket.accept()
        self.connections.append(connection)
        # gets accepts connections and stores them in a list

        username = connection.recv(1024)

        self.writeToLog(f"{address} connected to the server!")
        self.writeToLog(f"{username.decode()} has joined the chat.\n")

        if connection not in self.connections:
            connection.sendall("Welcome to the chat- Type 'QUIT' to leave - Type HELP for help".encode())
            # so it doesn't repeatedly send the message

    def _broadcast(self, message, sender):
        for client in self.connections:
            if client != sender:
                client.sendall(f"{message}\n".encode())
                self.writeToLog(f"{message}\n")

    def shutdown(self):
        self._broadcast("Server: The server is being shut down", self.listening_socket)
        # sends msg
        for conn in self.connections:
            conn.close()
            # closes every connection
        self.writeToLog("\t\tEnd of Session\t\t \n\n")
        sys.exit(0)

    @classmethod
    def writeToLog(cls, log_message):
        with open("log.txt", "a") as log:
            # opens a log file to note down server activity
            log.write(log_message + "\n")


server = Server()
