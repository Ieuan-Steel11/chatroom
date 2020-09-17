import socket
import sys
import select


class Client:

    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 6000

        self.server_msg = ""
        self.client_socket = None
        self.name = None
        # init var to store server messages, server connection, username

        self.connectToServer()
        self.handle_messages()

    def handle_messages(self):
        while True:
            sockets_list = [sys.stdin, self.client_socket]
            read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])
            # selects a socket once they become readable or writable
            # but we only want readable

            for sockets in read_sockets:
                # iterates through the sockets to see if its the server that sent a message
                if sockets == self.client_socket:
                    self.getServerMessages()
                else:
                    self.sendMessagesToServer()

    def getServerMessages(self):
        try:
            self.server_msg = self.client_socket.recv(1024).decode()

            self.server_msg.replace("b'", "")
            self.server_msg.replace("'", "")
            # gets rid of the b and '' that show up on a bytes string

            print(self.server_msg)

        except socket.error:
            print("SocketError: could not receive message from server, socket failed")
            # trying to receive message from server
        except ConnectionAbortedError:
            print("ConnectionError: Server disconnected")

    def sendMessagesToServer(self):
        message_to_send = sys.stdin.readline()
        # read input from console

        if message_to_send != "":
            if "QUIT" in message_to_send:
                self.shutdown()
            elif "HELP" in message_to_send:
                print("- Simply type your text in the input then press enter ")
            else:
                self._broadcast(f"{self.name}: {message_to_send}")

    def _broadcast(self, message):
        try:
            self.client_socket.sendall(message.encode())
        except socket.error:
            print("SocketError: could not send message to server, socket failed")
        except ConnectionAbortedError:
            print("ServerError: connection to server failed")

    def shutdown(self):
        self.client_socket.sendall(f"{self.name} has disconnected from the server".encode())
        self.client_socket.close()
        sys.exit(0)
        # sends a message closes connection then script

    def connectToServer(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
        except ConnectionRefusedError:
            print("ConnectionError: could not connect to server, server offline")
            quit(ConnectionRefusedError)
            # trying to connect to server
        except ConnectionAbortedError:
            print("ConnectionError: could not connect to server")
            quit(ConnectionAbortedError)
            # trying to connect to server
        except ConnectionError:
            print("ConnectionError: could not connect to server")
            quit(ConnectionError)
            # trying to connect to server

        self.name = input("Username: ")
        self.client_socket.sendall(self.name.encode())
        # gets username and broadcasts that the user joined


client = Client()
