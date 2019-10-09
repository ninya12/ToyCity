import cam
import motor
import ultra
import socket

camera = cam.MyCam(320, 240)

command = ['D']

IP = '172.31.23.143'
PORT = 5001

with socket.socket() as sock:
    sock.connect((IP, PORT))
    while(camera.isOpened()):
        try:
            camera.run()
            distance = ultra.get_ultra()
            if(cam.send_image(sock, camera.result) is False):
                break
            if(distance < 15):
                command[0] = 'S'
                print(distance, "cm")
                motor.Stop()
            else:
                command[0] = 'D'
            if(command[0] == 'D'):
                motor.Forward(30)
                if(camera.average > 91):
                    motor.ForwardRight(80, 30)
                if(camera.average < 89):
                    motor.ForwardLeft(80, 30)
            if(camera.waitkey(1) & 0xFF == 27):
                break
        except Exception as e:
            print(e)
