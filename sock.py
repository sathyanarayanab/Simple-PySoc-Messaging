import socket as s
from threading import Thread
import optparse
import getpass

class bcolors:
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'

class Server:
    class newThreadforRecieving(Thread):
        def __init__(self, conn, addr,sock,name):
            Thread.__init__(self)
            self.conn = conn
            self.addr = addr
            self.sock = sock
            self.name = name
            print(f"{bcolors.OKGREEN}Client connected from {self.addr[0]} port {self.addr[1]}{bcolors.ENDC}\n")

        def run(self):
            while not self.conn._closed:
                try:
                    data = self.conn.recv(2028).decode()
                    if not data:
                        break
                    else:
                        print(bcolors.OKGREEN+data+bcolors.ENDC)
                except:
                    pass
            self.conn.close()
    
    class newThreadforSending(Thread):
        def __init__(self,conn,addr,sock,name):
            Thread.__init__(self)
            self.conn = conn
            self.addr = addr
            self.sock = sock
            self.name = name
        
        def run(self):
            while not self.conn._closed:
                try:
                    message = input("\n")
                    message = message + "\n"
                    send = self.conn.sendall(f"{self.name} : {message}".encode())
                except:
                    pass
            self.conn.close()

class Client:
    class newThreadforRecieving(Thread):
        def __init__(self, sock,name):
            Thread.__init__(self)
            self.sock = sock
            self.name = name
            print(f"Connected sucessfully to {HOST} port {PORT}\n")
        def run(self):
            while not self.sock._closed:
                try:
                    data = self.sock.recv(2028).decode()
                    if not data:
                        break
                    else:
                        print(bcolors.OKGREEN+data+bcolors.ENDC)
                except:
                    pass
            self.sock.close()
    
    class newThreadforSending(Thread):
        def __init__(self, sock,name):
            Thread.__init__(self)
            self.sock = sock
            self.name = name
        def run(self):
            while not self.sock._closed:
                try:
                    message = input("\n")
                    message = message + "\n"
                    send = self.sock.sendall(f"{self.name} : {message}".encode())
                except:
                    pass
            self.sock.close()

def fetch_arguments():
    parse_arguments = optparse.OptionParser()
    parse_arguments.add_option("-c", "--client", action="store_true" ,dest="client", help="Use this if you are client")
    parse_arguments.add_option("-s", "--server", action="store_true", dest="server",help="Use this if you are server")
    parse_arguments.add_option("-i", "--ip", dest="HOST", help="Hostname or IP")
    parse_arguments.add_option("-p", "--port", dest="PORT", help="Destination Port")
    parse_arguments.add_option("-n", "--name", dest="NAME", help="Yourname")
    parse_arguments.add_option("-k", "--key", dest="PWD", action = "store_true", help="Use if you want the client to enter password")#Not present as of now
    (options, arguments) = parse_arguments.parse_args()
    return options



option = fetch_arguments()
NAME  = option.NAME
HOST = option.HOST
PORT = int(option.PORT)
PWD = option.PWD
if PWD:
    PWD = getpass.getpass(prompt="Password: ", stream=None)

if option.server:
    sock = s.socket(s.AF_INET,s.SOCK_STREAM)
    sock.setsockopt(s.SOL_SOCKET,s.SO_REUSEADDR,1)
    sock.bind((HOST,PORT))
    sock.listen()
    while True:
        conn, addr = sock.accept()
        Server.newThreadforRecieving(conn,addr,sock,NAME).start()
        Server.newThreadforSending(conn,addr,sock,NAME).start()
    conn.close()

elif option.client:
    sock = s.socket(s.AF_INET,s.SOCK_STREAM)
    sock.connect((HOST,PORT))
    Client.newThreadforRecieving(sock,NAME).start()
    Client.newThreadforSending(sock,NAME).start()
