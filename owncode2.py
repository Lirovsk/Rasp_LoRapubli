import RPi.GPIO as GPIO
import time
import serial

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

ser=serial.Serial('/dev/serial0',9600)
time.sleep(3)

while(1):
    print("Aguardando as informacoes")
    msg= ser.readline()
    print("mesnsagem recebida: ", msg.decode('utf-8'))
    time.sleep(1)