import socket
import threading
import sys



# TODO: get rid of failed multithreading and put into one loop
# TODO: set up logic so that if there's a message from the server it automatically stops the input and prints the msg
#       maybe using pyunpt for key pressing or some form of prioritising messages from the server


class Client:

    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 9009

        self.server_msg = ""
        # init var to store server messages

        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
        except ConnectionRefusedError:
            print("ConnectionError: could not connect to server")
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

        server_handler = threading.Thread(target=self.getServerMessages)
        server_handler.start()
        # gets messages from server

        client_handler = threading.Thread(target=self.sendMessagesToServer)
        client_handler.start()
        # sends messages to server

    def getServerMessages(self):
        while True:
            try:
                self.server_msg = self.client_socket.recv(1024).decode()
            except socket.error:
                print("SocketError: could not receive message from server, socket failed")
            # trying to receive message from server
            except ConnectionAbortedError:
                print("ConnectionError: Server disconnected")

    def sendMessagesToServer(self):
        while True:
            if self.server_msg:
                print(self.server_msg[2:-2])
                self.server_msg = ""
                # if the message from the server isn't empty print the message
                # should get rid of required to press enter to get message bug
            message = input(f"{self.name}: ")
            # repeatedly prints out the name then input box to get messages

            if message != "":
                if "QUIT" in message:
                    self.shutdown()
                if "HELP" in message:
                    print("- Simply type your text in the input then press enter \n- you may have to press enter to "
                          "get the responses from the other clients")
                else:
                    self._broadcast(f"{self.name}: {message}")

    def _broadcast(self, message):
        try:
            self.client_socket.sendall(message.encode())
        except socket.error:
            print("SocketError: could not send message to server, socket failed")
        except:
            print("MessageError: (catch all err msg) could not send message to server")

    def shutdown(self):
        self.client_socket.sendall(f"{self.name} has disconnected from the server".encode())
        self.client_socket.close()
        sys.exit(0)
        # sends a message closes connection then script


client = Client()
