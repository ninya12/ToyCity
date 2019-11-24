import cam
import motor
import ultra
import socket
import threading
import time

camera = cam.MyCam(320, 240)

command = ['S','LD','RD',]

IP = '211.47.107.198'
PORT = 19827


def Motor():
    while(True):
        if(command[0] == 'D'):
            motor.Forward()
        if(command[0] == 'RD'):
            motor.ForwardRight()
        if(command[0] == 'LD'):
            motor.ForwardLeft()
        if(command[0] == 'S'):
            motor.Stop()
        if(command[0] == 'R'):
            motor.Reverse()
        if(command[0] == 'RR'):
            motor.ReverseRight()
        if(command[0] == 'LR'):
            motor.ReverseLeft()
        time.sleep(1.2)
        if(len(command) > 1):
            del command[0]
        else:
            motor.Stop()


def SendVideo():
    with socket.socket() as sock:
        sock.connect((IP, PORT))
        while(camera.isOpened()):
            try:
                camera.run()
                if(cam.send_image(sock, camera.result) is False):
                    break
                if(camera.average >= 91):
                    motor.Right(80)
                if(camera.average <= 89):
                    motor.Left(80)
                if(camera.average < 91 and camera.average > 89):
                    motor.Left(0)
                if(camera.waitkey(1) & 0xFF == 27):
                    break
            except Exception as e:
                print("[-] Cam Exception")
                print(e)


def Ultra():
    while True:
        distance = ultra.get_ultra()
        if(distance < 15):
            command[0] = 'S'
            print(distance, "cm")


try:
    motorThread = threading.Thread(target=Motor, args=())
    videoThread = threading.Thread(target=SendVideo, args=())
    ultraThread = threading.Thread(target=Ultra, args=())

    threadList = []
    threadList.append(motorThread)
    threadList.append(videoThread)
    threadList.append(ultraThread)

    for i in threadList:
        i.start()

    while(True):
        command.append(input())
        print(command)
except Exception as e:
    print(e)
