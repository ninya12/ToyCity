import RPi.GPIO as GPIO
import time

# Forward Pwm Pin : 20
pwmPin1 = 20
# Steering Pwm Pin : 5
pwmPin2 = 5

# Forward Pin : 16 // Reverse Pin : 12
dirPin1 = 12
dirPin2 = 16

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
p2.ChangeDutyCycle(90)


def Forward(speed=50):
    p.ChangeDutyCycle(speed)
    GPIO.output(dirPin1, True)
    GPIO.output(dirPin2, False)


def Reverse(speed=50):
    p.ChangeDutyCycle(speed)
    GPIO.output(dirPin2, True)
    GPIO.output(dirPin1, False)


def Left(speed=90):
    p2.ChangeDutyCycle(speed)
    GPIO.output(rirPin1, True)
    GPIO.output(rirPin2, False)


def Right(speed=90):
    p2.ChangeDutyCycle(speed)
    GPIO.output(rirPin2, True)
    GPIO.output(rirPin1, False)


def ForwardLeft(wheelspeed=90, speed=50):
    Forward(speed)
    Left(wheelspeed)


def ForwardRight(wheelspeed=90, speed=50):
    Forward(speed)
    Right(wheelspeed)


def ReverseRight(wheelspeed=90, speed=50):
    Reverse(speed)
    Right(wheelspeed)


def ReverseLeft(wheelspeed=90, speed=50):
    Reverse(speed)
    Left(wheelspeed)

def Stop():
    GPIO.output(dirPin1, False)
    GPIO.output(dirPin2, False)
    GPIO.output(rirPin1, False)
    GPIO.output(rirPin2, False)

