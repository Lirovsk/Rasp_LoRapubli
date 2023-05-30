import spidev

# Definir os pinos
PIN_MOSI = 10
PIN_MISO = 9
PIN_SCLK = 11
PIN_CS = 8

# Inicializar a comunicação SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # (bus, device)
spi.max_speed_hz = 500000  # Definir a velocidade de comunicação SPI (500 kHz)

# Configurar os pinos GPIO
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_CS, GPIO.OUT)
GPIO.output(PIN_CS, GPIO.HIGH)

# Função para receber mensagens do dispositivo LoRa
def receive_message():
    # Selecionar o dispositivo LoRa
    GPIO.output(PIN_CS, GPIO.LOW)
    
    # Enviar comandos para receber dados do dispositivo LoRa
    spi.xfer([0x00])
    spi.xfer([0x00])
    
    # Ler até 32 bytes de dados do dispositivo LoRa
    data = spi.readbytes(32)
    
    # Converter os bytes lidos em uma string
    message = ''.join([chr(byte) for byte in data if byte != 0])
    
    # Deselecionar o dispositivo LoRa
    GPIO.output(PIN_CS, GPIO.HIGH)
    
    # Retornar a mensagem recebida
    return message

# Exemplo de uso: receber uma mensagem e exibir na tela
received_message = receive_message()
print("Mensagem recebida:", received_message)
