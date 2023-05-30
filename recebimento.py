import spidev

# Inicializar a comunicação SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # (bus, device)

# Configurar parâmetros SPI
spi.max_speed_hz = 500000  # Definir a velocidade de comunicação SPI (500 kHz)

# Função para receber mensagens do dispositivo LoRa
def receive_message():
    while True:
        # Enviar comando para receber dados
        spi.xfer2([0x00])
        data=[0]
        
        # Ler até 32 bytes de dados do dispositivo LoRa
        data = spi.readbytes(32)

        if data!=0:
            # Converter os bytes lidos em uma string
            message = ''.join([chr(byte) for byte in data])
        # message=str(data.decode('ascii'))
        # Retornar a mensagem recebida
        return message

# Exemplo de uso: receber uma mensagem e exibir na tela
print("esperando pela mensagem")
received_message = receive_message()
print(received_message)
print("mensagem recebida")