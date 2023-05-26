import socket
import serial
import time

#declarando a porta serial e a velocidade de transmissão
ser = serial.Serial('/dev/ttyS0', 9600)
while True:
    msgRe=ser.readline()
    msgleft=ser.inWainting()
    print(msgRe,msgleft)
    time.sleep(1)