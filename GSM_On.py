import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(23,GPIO.OUT)

GPIO.output(23,1)
time.sleep(1)
GPIO.output(23,0)
