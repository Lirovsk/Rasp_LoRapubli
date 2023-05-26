import socket
import serial
# Endereço IP local do Raspberry Pi
HOST = '192.168.1.100'  # Substitua pelo IP do Raspberry Pi

# Porta que será usada para a comunicação
PORT = 12345

# Criação do socket TCP/IP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associa o socket ao endereço IP e à porta
server_socket.bind((HOST, PORT))

# Coloca o socket em modo de escuta
server_socket.listen(1)

print('Aguardando conexão...')

# Aguarda uma conexão
client_socket, client_address = server_socket.accept()
print('Conectado por', client_address)

while True:
    # Recebe os dados enviados pelo cliente
    data = client_socket.recv(1024).decode()
    
    if not data:
        # Se não houver mais dados, encerra a conexão
        break
    
    print('Mensagem recebida:', data)
    
    # Envie uma resposta para o cliente
    response = 'Recebi a mensagem: ' + data
    client_socket.send(response.encode())

# Fecha o socket do cliente
client_socket.close()

# Fecha o socket do servidor
server_socket.close()
