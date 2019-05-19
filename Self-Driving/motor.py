import RPi.GPIO as GPIO
import time

# Forward Pwm Pin : 19
pwmPin1 = 19
# Steering Pwm Pin : 24
pwmPin2 = 24

# Forward Pin : 16 // Reverse Pin : 12
dirPin1 = 16
dirPin2 = 12

# Right Pin : 13 // Left Pin : 6
rirPin1 = 13
rirPin2 = 6

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(rirPin1, GPIO.OUT)
GPIO.setup(rirPin2, GPIO.OUT)
GPIO.setup(pwmPin1, GPIO.OUT)
GPIO.setup(pwmPin2, GPIO.OUT)
GPIO.setup(dirPin1, GPIO.OUT)
GPIO.setup(dirPin2, GPIO.OUT)

p = GPIO.PWM(pwmPin1, 100)
p2 = GPIO.PWM(pwmPin2, 100)
p.start(0)
p2.start(0)
p.ChangeDutyCycle(0)
p2.ChangeDutyCycle(100)

while 1:
    print("Mode : ")
    a = input()
    if(int(a) == 1):
        print("speed : ")
        speed = input()
        p.ChangeDutyCycle(float(speed))
        GPIO.output(dirPin1, True)
        GPIO.output(rirPin1, True)
        GPIO.output(dirPin2, False)
        GPIO.output(rirPin2, False)
    elif(int(a) == 2):
        print("speed : ")
        speed = input()
        p.ChangeDutyCycle(float(speed))
        GPIO.output(dirPin1, True)
        GPIO.output(rirPin2, True)
        GPIO.output(dirPin2, False)
        GPIO.output(rirPin1, False)
    elif(int(a) == 3):
        print("speed : ")
        speed = input()
        p.ChangeDutyCycle(float(speed))
        GPIO.output(dirPin2, True)
        GPIO.output(rirPin1, True)
        GPIO.output(dirPin1, False)
        GPIO.output(rirPin2, False)
    elif(int(a) == 4):
        print("speed : ")
        speed = input()
        p.ChangeDutyCycle(float(speed))
        GPIO.output(dirPin2, True)
        GPIO.output(rirPin2, True)
        GPIO.output(dirPin1, False)
        GPIO.output(rirPin1, False)
    else:
        GPIO.output(dirPin2, False)
        GPIO.output(rirPin2, False)
        GPIO.output(dirPin1, False)
        GPIO.output(rirPin1, False)
