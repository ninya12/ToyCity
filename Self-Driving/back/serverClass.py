import socket

class MySocket:
    def __init__(self, host, port):
        print("[+] socket running !!")
        self.host = host
        self.port = port
        self.sock = None
        self.retryAttempts = 0

        self.createSocket()

    def createSocket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print("[+] socket bind !!")
            self.sock.bind((self.host, self.port))
            print("[+] socket listen !!")
            self.sock.listen(5)
            print("[+] waiting client...")
            c_sock, addr = self.sock.accept()
            print("[+] connected from {}:{}".format(addr[0], addr[1]))
            while(1):
                data = c_sock.recv(1024)
                if(len(data)==0):
                    break
                print("[*] {}".format(data.decode()))
                
        except Exception as e:
            print(e)

        finally:
            self.closeSocket()

    def closeSocket(self):
        print("[-] socket closed !!")
        self.sock.close()
        self.sock = None


MySocket('', 13424)
