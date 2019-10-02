import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

localHost = ''
bufSize = 1024
port = 7887


sock.bind((localHost, port))
while(1):
    data, addr = sock.recvfrom(bufSize)
    
    print("--- * * * ---")
    print("[*] Data : ", data.decode())
    print("[*] Client IP : ", addr[0])
    print("[*] Client PORT : ", addr[1])
    if(data.decode() == "exit"):
        print("[-] Communication Terminate")
        break

    sock.sendto(data, addr)

sock.close()