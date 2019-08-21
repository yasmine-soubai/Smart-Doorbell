import RPi.GPIO as GPIO
import time
import os
from picamera import PiCamera
from datetime import datetime
import serial


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setwarnings(False)
GPIO.setup(4,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)

while True:
    btn =GPIO.input(17)
    if btn == False:
        # Turn on the light
        GPIO.output(18,1)
        # Turn on the buzzer
        GPIO.output(4,1)
        time.sleep(0.2)
        GPIO.output(4,0)
        print('Buzzer on..')
        # Turn off the livestreaming
        os.system('cd /opt/mjpg-streamer')
        os.system('sudo killall mjpg_streamer')
        os.system('cd')
        print('Live off..')
        # Take a picture, save in the website, name is the time
        camera = PiCamera()
        camera.resolution = (320,240)
        camera.capture('/var/www/html/images/person.jpg')
        camera.close()
        print('Picture taken..')
        time.sleep(1)
        # Turn on the livestreaming
        os.system('LD_LIBRARY_PATH=/opt/mjpg-streamer/ /opt/mjpg-streamer/mjpg_streamer -i "input_raspicam.so -fps 10 -q 50 -x 320 -y 240" -o "output_http.so -p 9000 -w /opt/mjpg-streamer/www" &')
        print('Live on..')
        time.sleep(1)
        # Turn on the GSM module
        GPIO.output(23,1)
        time.sleep(1)
        GPIO.output(23,0)
        # Send the msg and the website link
        ser=serial.Serial("/dev/ttyS0", 9600, timeout = 1)
        ser.write("AT+CMGF=1\r")
        response1= ser.readlines(30 )
        ser.write('AT+CMGS="0661707870"\r')
        response2= ser.readlines(50)
        ser.write("Someone is in the door, http://192.168.1.11/")
        ser.write(chr(26))
        print(response1, " ", response2)
        ser.close()
        # Send an email
        fromEmail = 'yasminesoubai99@gmail.com'
        fromEmailPassword = 'hanayamali99'
        toEmail = 'yasminesoubai99@gmail.com'
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = 'Home Doorbell'
        msgRoot['From'] = fromEmail
        msgRoot['To'] = toEmail
        
        dt = datetime.now().isoformat()
        msgText = MIMEText('A person is at the door at :' + dt)
        msgRoot.attach(msgText)
        
        img_data = open('/var/www/html/images/person.jpg', 'rb')
        msgImage = MIMEImage(img_data.read())
        msgImage.add_header('Content-ID', '<person>')
        msgRoot.attach(msgImage)
        img_data.close()
        
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.login(fromEmail, fromEmailPassword)
        smtp.sendmail(fromEmail, toEmail, msgRoot.as_string())
        smtp.quit()
        print('Email sent..')
        
        # Turn off the light
        GPIO.output(18,0)
