import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

localHost = '127.0.0.1'
bufSize = 1024
port = 7887

dest = (localHost, port)
data = "a"
count = 0
while(1):
    if(count >= 10):
        data = "exit"
    sock.sendto(data.encode(), dest)
    if(data=="exit"):
        print("[-] Communication Terminate")
        break
    rdata, addr = sock.recvfrom(bufSize)
    print("--- * * * ---")
    print("[*] Data : ", rdata.decode())
    print("[*] IP : ", addr[0])
    time.sleep(5)
    count += 1
sock.close()
