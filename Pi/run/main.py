import cam
import motor
import ultra
import socket
import threading
import time

camera = cam.MyCam(320, 240)

command = ['ND', 'ND', 'ND', 'ND', 'NS']

IP = '211.47.107.198'
PORT = 19827

sock = socket.socket()
sock.connect((IP, PORT))


def Motor():
    speed = 40
    while(True):
        if(command[0] == 'ND'):
            motor.Forward(speed)
            speed = 35
        if(command[0] == 'RD'):
            motor.ForwardRight()
        if(command[0] == 'LD'):
            motor.ForwardLeft()
        if(command[0] == 'NS'):
            motor.Stop()
            print("Stop")
        if(command[0] == 'NR'):
            motor.Reverse(speed)
            speed = 35
        if(command[0] == 'RR'):
            motor.ReverseRight()
        if(command[0] == 'LR'):
            motor.ReverseLeft()
        time.sleep(2)
        if(len(command) > 1):
# del command[0]
            pass
        else:
            motor.Stop()


def SendVideo():
    while(camera.isOpened()):
        try:
            camera.run()
            if(cam.send_image(sock, camera.result) is False):
                break
            if(camera.average >= 91):
                motor.Right(70)
            if(camera.average <= 89):
                motor.Left(70)
            if(camera.average == 90):
                motor.Left(0)
            if(camera.waitkey(1) & 0xFF == 27):
                break
        except Exception as e:
            print("[-] Cam Exception")
            print(e)


def ReadCommand():
    while(True):
        data = sock.recv(1024).decode('utf-8')
        length = int(data[:2])
        print(length)
        if(length == 0):
            continue
        print(data[2:])
        if(length >= 2):
            for i in range(int(length/2)):
                command.append(data[2*(i+1):2*(i+2)])
        print(command)


def Ultra():
    while True:
        try:
            distance = ultra.get_ultra()
            if(distance < 15):
                motor.Stop()
                command[0] = 'NS'
            else:
                command[0] = 'ND'
            time.sleep(1)
        except:
            print("ultra sensor failed")


try:
    motorThread = threading.Thread(target=Motor, args=())
    videoThread = threading.Thread(target=SendVideo, args=())
    ultraThread = threading.Thread(target=Ultra, args=())
    commandThread = threading.Thread(target=ReadCommand, args=())

    threadList = []
    threadList.append(motorThread)
    threadList.append(videoThread)
    threadList.append(ultraThread)
    threadList.append(commandThread)

    for i in threadList:
        i.start()

except Exception as e:
    print(e)
