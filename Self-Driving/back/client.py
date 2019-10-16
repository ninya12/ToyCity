import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

localHost = '127.0.0.1'
bufSize = 1024
port = 13424

dest = (localHost, port)
sock.connect(dest)

while(1):
    try:
        data = input()
        sock.send(data.encode())
        if(data=="exit"):
            print("[-] Communication Terminate")
            break

    except KeyboardInterrupt:
        break

sock.shutdown
sock.close()