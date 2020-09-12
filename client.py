import socket
import threading
import sys


class Client:

    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 9009

        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
        except ConnectionRefusedError:
            print("ConnectionError: could not connect to server")
            quit(ConnectionRefusedError)
            # trying to connect to server
        except ConnectionError:
            print("ConnectionError: could not connect to server")
            quit(ConnectionError)
            # trying to connect to server
        except ConnectionAbortedError:
            print("ConnectionError: could not connect to server")
            quit(ConnectionAbortedError)
            # trying to connect to server

        self.name = input("Username: ")
        self.client_socket.sendall(self.name.encode())
        # gets username and broadcasts that the user joined

        server_handler = threading.Thread(target=self.getServerMessages)
        server_handler.start()
        # gets messages from server

        client_handler = threading.Thread(target=self.sendMessage)
        client_handler.start()
        # sends messages to server

    def getServerMessages(self):
        while True:
            try:
                print(f"\n{self.client_socket.recv(1024).decode()}")
            except socket.error:
                print("MessageError: could not receive message from server")
            # trying to receive message from server
            except ConnectionAbortedError:
                print("ConnectionError: Server disconnected")

    def sendMessage(self):
        while True:
            try:
                message = input(f"{self.name}: ")
                if message != "":
                    if "QUIT" in message:
                        self.client_socket.sendall(f"{self.name} has disconnected from the server".encode())
                        self.client_socket.close()
                        sys.exit()
                    else:
                        self.client_socket.sendall(f"{self.name}: {message}".encode())
            except socket.error:
                print("MessageError: Could not send message to server")
                # trying to send message to server


client = Client()
