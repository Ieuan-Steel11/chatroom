import socket
import threading


class Client:

    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 9009

        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
        except:
            print("Error: could not connect to server")
        # trying to connect to server

        self.name = input("Username: ")
        self.client_socket.sendall(self.name.encode("ascii"))
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
                print(self.client_socket.recv(1024).decode("ascii"))
            except:
                print("Error: could not receive message from server")
            # trying to receive message from server

    def sendMessage(self):
        while True:
            try:
                message = input(f"{self.name}: ")
                self.client_socket.sendall(message.encode("ascii"))
            except:
                print("Error: Could not send message to server")
            # trying to send message to server


client = Client()
