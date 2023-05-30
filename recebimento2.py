import spidev

# Inicializar a comunicação SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # (bus, device)
spi.max_speed_hz = 500000  # Definir a velocidade de comunicação SPI (500 kHz)

# Função para receber mensagens do dispositivo LoRa
def receive_message():
    # Configurar o pino Chip Select como LOW para selecionar o dispositivo LoRa
    spi.xfer([0x80])
    
    # Esperar até que o dispositivo LoRa esteja pronto para enviar os dados
    while spi.xfer([0x00])[0] & 0x80 == 0:
        pass
    
    # Enviar comandos para receber dados do dispositivo LoRa
    spi.xfer([0x00])
    spi.xfer([0x00])
    
    # Ler até 32 bytes de dados do dispositivo LoRa
    data = spi.readbytes(32)
    
    # Converter os bytes lidos em uma string
    message = ''.join([chr(byte) for byte in data if byte != 0])
    
    # Configurar o pino Chip Select como HIGH para deselecionar o dispositivo LoRa
    spi.xfer([0x81])
    
    # Retornar a mensagem recebida
    return message

# Exemplo de uso: receber uma mensagem e exibir na tela
received_message = receive_message()
print("Mensagem recebida:", received_message)
