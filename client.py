import socket
import sys
import select
import time
from cryptography.fernet import Fernet, InvalidToken


class Client:

    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 6000

        self.cipher = None
        self.key = b""
        self.server_msg = ""
        self.client_socket = None
        self.username = None
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
                if sockets == self.client_socket and self.client_socket:
                    self.getServerMessages()
                else:
                    self.sendMessagesToServer()

    def getServerMessages(self):
        try:
            self.server_msg = self.client_socket.recv(1024)
            self.server_msg.replace(b"b'", b"")
            self.server_msg.replace(b"'", b"")
            # gets rid of the b and '' that show up on a bytes string

            if self.server_msg:
                print(self._decryptMessage(self.server_msg))

        except socket.error:
            print("SocketError: could not receive message from server, socket failed")
            # trying to receive message from server
        except ConnectionAbortedError:
            print("ConnectionError: Server disconnected")

    def sendMessagesToServer(self):
        message_to_send = sys.stdin.readline()

        if "QUIT" in message_to_send:
            self.disconnectFromServer()
        elif "HELP" in message_to_send:
            print("- Simply type your text in the input then press enter ")
        else:
            message_to_send = bytes(message_to_send, "utf-8")
            self._broadcastMessage(f"{self.username}: {message_to_send} \t\t\t\t {time.time()}")

    def _encryptMessage(self, message):
        self.key.replace(b"b'", b"")
        self.key.replace(b"'", b"")
        # gets rid of byte string label so it can work properly

        self.cipher = Fernet(self.key)
        message = self.cipher.encrypt(bytes(message, "utf-8"))
        # encrypts message with key from server
        return message

    def _decryptMessage(self, message):
        try:
            self.cipher = Fernet(self.key)
            message = self.cipher.decrypt(message)
            return message.decode()
        except InvalidToken:
            quit("Server offline, messages stopped coming through")

    def _broadcastMessage(self, message):
        try:
            self.client_socket.sendall(self._encryptMessage(message))
        except socket.error:
            print("SocketError: could not send message to server, socket failed")
        except ConnectionAbortedError:
            print("ServerError: connection to server failed")

    def disconnectFromServer(self):
        self._broadcastMessage(f"{self.username} has disconnected from the server")
        self.client_socket.close()
        sys.exit(0)
        # sends a message closes connection then script

    def connectToServer(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            # gets username and broadcasts that the user joined

            print("Welcome to the chat: QUIT to quit and HELP for help")
            # welcome message

            self.key = self.client_socket.recv(1024)
            # get encryption key from server

            self.username = input("Username: ")
            self.client_socket.sendall(bytes(self.username, "utf-8"))
            # gets and sends username

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


client = Client()
