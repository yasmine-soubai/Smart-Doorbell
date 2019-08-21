import RPi.GPIO as GPIO
import serial
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(22,GPIO.OUT)

ser=serial.Serial("/dev/ttyS0", 9600, timeout = 1)

while True:
    spk = GPIO.input(22)
    if spk == True:
        ser.write(bytes("ATD0661707870;\r", 'UTF-8'))
        #The line above works with Python 3
        #The line under in comment works with the Terminal
        #ser.write("ATD0661707870;\r")
        response= ser.readlines(30)
        print(response)
        GPIO.output(22,0)
    #else:
    #    ser.write(bytes("ATH;\r", 'UTF-8'))
    #    response= ser.readlines(30)
    #    print(response)
        