import socket
import serial
import time

#declarando a porta serial e a velocidade de transmissão
ser = serial.Serial('/dev/ttyS0', 9600)

#loop principal
while True:
    print("Aguardando mensagem...")
    msgRe=ser.readline()
    msgleft=ser.inWainting()
    print("Mensagem recebida: ")
    print(msgRe,msgleft)
    print("processo terminado")
    time.sleep(1)