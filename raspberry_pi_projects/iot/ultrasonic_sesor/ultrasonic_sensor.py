import RPi.GPIO as GPIO 
import time


led = 18


GPIO.setmode(GPIO.BOARD)
GPIO.setup(led, GPIO.OUT)

while(True):    
    GPIO.output(led, GPIO.HIGH)
    print("Led encendido")
    time.sleep(2)
    GPIO.output(led, GPIO.LOW)
    print("Led apagado")
    time.sleep(2)

GPIO.cleanup()


