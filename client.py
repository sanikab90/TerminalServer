import socket
import threading

class client:
    def __init__(self):
        self.connectUsers()

    def connectUsers(self):
        #initalize socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #get client to connect to the server
        while True:
            try:
                #get host name and the port
                host = socket.gethostbyname(socket.gethostname())
                port = 7976
                #connect to the host and port
                self.sock.connect((host, port))
                break
            except:
                #if that doesn't work print an error message
                print("Could not connect to the server.")

        #get user's name
        self.username = input('Please enter your username: ')

        #send that to the server to broadcast
        self.sock.send(self.username.encode())

        #create a seperate thread for all incoming messages
        msg = threading.Thread(target=self.recieveMsg, args=())
        msg.start()


        sendMsg = threading.Thread(target=self.sendMsg,args=())
        sendMsg.start()

    def recieveMsg(self):
        while True:
            print(self.sock.recv(1024).decode())

    def sendMsg(self):
        while True:
            self.sock.send((self.username + '> ' + input() + '\n').encode())

c = client()