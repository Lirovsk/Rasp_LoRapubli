import RPi.GPIO as GPIO
import spidev
import time

# Definir os pinos GPIO para o módulo LoRa
LORA_RESET_PIN = 22
LORA_NSS_PIN = 24
LORA_DIO0_PIN = 23

# Inicializar a interface SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # O Raspberry Pi Zero W possui apenas uma interface SPI, portanto, usamos 0, 0 para o barramento SPI principal

# Inicializar os pinos GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(LORA_RESET_PIN, GPIO.OUT)
GPIO.setup(LORA_NSS_PIN, GPIO.OUT)
GPIO.setup(LORA_DIO0_PIN, GPIO.IN)

# Função para redefinir o módulo LoRa
def reset_lora():
    GPIO.output(LORA_RESET_PIN, GPIO.LOW)
    time.sleep(0.01)
    GPIO.output(LORA_RESET_PIN, GPIO.HIGH)
    time.sleep(0.01)

# Função para configurar o módulo LoRa
def configure_lora():
    # Definir o modo de operação em modo de transceptor
    write_register(0x01, 0x80)
    
    # Configurar frequência (915 MHz)
    write_register(0x06, 0xD9)
    write_register(0x07, 0x06)
    write_register(0x08, 0x66)
    
    # Configurar potência de transmissão (10 dBm)
    write_register(0x09, 0x0F)
    
    # Configurar fator de espalhamento (SF10) e largura de banda (125 kHz)
    write_register(0x0D, 0x8B)
    
    # Configurar taxa de codificação de correção de erro (4/8)
    write_register(0x0E, 0x02)
    
    # Configurar sincronização de tempo no início do pacote (explicit mode)
    write_register(0x0F, 0x0C)
    
    # Configurar CRC (habilitado)
    write_register(0x11, 0x1D)
    
    # Configurar DIO0 como interrupção em 'cad_detected'
    write_register(0x40, 0x0A)

# Função para escrever em um registrador do módulo LoRa
def write_register(address, value):
    GPIO.output(LORA_NSS_PIN, GPIO.LOW)
    spi.xfer([address | 0x80, value])
    GPIO.output(LORA_NSS_PIN, GPIO.HIGH)

# Função para ler o valor de um registrador do módulo LoRa
def read_register(address):
    GPIO.output(LORA_NSS_PIN, GPIO.LOW)
    spi.xfer([address & 0x7F, 0x00])
    result = spi.xfer([0x00])[0]
    GPIO.output(LORA_NSS_PIN, GPIO.HIGH)
    return result

# Função de callback para tratamento das interrupções
def interrupt_callback(channel):
    # Verificar se a interrupção ocorreu no pino DIO0
    if channel == LORA_DIO0_PIN:
        # Ler o registrador de status
        status = read_register(0x12)
        
        # Verificar se ocorreu uma interrupção de recepção de pacote
        if status & 0x40:
            # Ler o tamanho do pacote recebido
            packet_size = read_register(0x13)
            
            # Ler o conteúdo do pacote
            packet_data = []
            for i in range(packet_size):
                packet_data.append(read_register(0x00))
            
            # Processar os dados recebidos
            process_received_data(packet_data)

# Função para processar os dados recebidos
def process_received_data(data):
    # Implemente sua lógica de processamento de dados aqui
    print("Dados recebidos:", data)

# Configurar a função de interrupção no pino DIO0
GPIO.add_event_detect(LORA_DIO0_PIN, GPIO.RISING, callback=interrupt_callback)

# Redefinir o módulo LoRa
reset_lora()

# Configurar o módulo LoRa
configure_lora()

# Loop principal
while True:
    # Implemente sua lógica de envio de dados aqui
    # Os dados podem ser escritos no registrador 0x00 antes de iniciar a transmissão
    
    time.sleep(1)  # Esperar 1 segundo entre as transmissões
