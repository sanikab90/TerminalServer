import socket
import threading

class server:
    def __init__(self):
        self.startServer()

    def startServer(self):
        #initalize socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #get host name
        host = socket.gethostbyname(socket.gethostname())
        #reserve a port
        port = 7976

        #array of people in the chat room
        self.clientList = []

        #bind host and port to the socket
        self.sock.bind((host, port))
        self.sock.listen(100)

        print("Server is now running.")

        #dictionary of socket objects
        self.username = {}

        while True:
            #create socket object and address by waiting for a connection with the client
            usr, address = self.sock.accept()

            #get the name of the client that just joined
            name = usr.recv(1024).decode()

            #broadcast that a new user joined to all other users
            self.broadcast('User ' + name + ' just joined!')

            #add the socket object to dictionary
            self.username[usr] = name

            #to keep track of all users add it to the list
            self.clientList.append(usr)

            #create a seperate thread for each client's messaging functionality
            threading.Thread(target=self.clientMsg,args=(usr,address,)).start()

    #loop to broadcast a user's message to all other users
    def broadcast(self, msg):
        for usr in self.clientList:
            usr.send(msg.encode())

    def clientMsg(self, usr, address):

        #loop until client cannot access server
        while True:
            try:
                #try to recieve a message from client object
                msg = usr.recv(1024)
            except:
                #if program can't do that remove the client from all lists and notify server and other users
                #that this user has left
                usr.shutdown(socket.SHUT_RDWR)
                self.clientList.remove(usr)
                self.broadcast(str(self.username[usr] + ' left'))
                break

            #if the message is not empty print it to the terminal for a server copy
            if msg.decode() != '':
                print(str(msg.decode()))

                #then send that message to all clients in the list
                for users in self.clientList:
                    if users != usr:
                        users.send(msg)

#start the server
s = server()