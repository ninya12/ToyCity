import cam
import motor
import ultra
import socket
import time

camera = cam.MyCam(320, 240)

command = ['D', 'N']

IP = '172.31.23.143'
PORT = 5001
start = time.time()

while(camera.isOpened()):
    try:
        if(time.time()-start >= 15):
            command[0] = 'R'
            command[1] = 'R'
        camera.run()
        distance = ultra.get_ultra()
        if(distance < 15):
            command[0] = 'S'
            print(distance, "cm")
            motor.Stop()
        else:
            if(command[1] == 'N'):
                command[0] = 'D'
        if(command[0] == 'D'):
            motor.Forward(45)
            if(camera.average > 91):
                motor.ForwardRight(80, 45)
            if(camera.average < 89):
                motor.ForwardLeft(80, 45)
        if(command[0] == 'R'):
            if(command[1] == 'R'):
                for i in range(9):
                    motor.ForwardRight(80,60)
                    time.sleep(0.7)
                    motor.ReverseLeft(80,60)
                    time.sleep(0.5)
                motor.Stop()
                command[0] = 'D'
                command[1] = 'N'
            if(command[1] == 'L'):
                for i in range(9):
                    motor.ForwardLeft(80,60)
                    time.sleep(0.7)
                    motor.ReverseRight(80,60)
                    time.sleep(0.5)
                motor.Stop()
                command[0] = 'D'
                command[1] = 'N'
        if(camera.waitkey(1) & 0xFF == 27):
            break
    except Exception as e:
        print(e)
