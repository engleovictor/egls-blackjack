import socket
import json
import time

# Endereço IP e porta do servidor
server_ip = "172.15.4.211"  # Altere para o endereço IP do seu servidor
server_port = 8888

# Cria um objeto de socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta ao servidor
client_socket.connect((server_ip, server_port))

hasInit = False

while True:
    if not hasInit:
    # Obtém a mensagem do usuário
        mensagem = {
            "code": 0
        }

        client_socket.send(json.dumps(mensagem).encode('utf-8'))
        resposta = client_socket.recv(1024).decode('utf-8')
        print(f"{resposta}")
        hasInit = True

        mensagem = {
            "code": 10,
            "payload":{
                "bet":50
            }
        }

        client_socket.send(json.dumps(mensagem).encode('utf-8'))
        resposta = client_socket.recv(1024).decode('utf-8')
        print(f"{resposta}")

    mensagem = {
        "code": 21,
    }

    # Envia a mensagem para o servidor
    client_socket.send(json.dumps(mensagem).encode('utf-8'))

    # Recebe a resposta do servidor
    resposta = client_socket.recv(1024).decode('utf-8')
    print(f"{resposta}")
    time.sleep(10)
    # Se o servidor enviar uma mensagem vazia, encerra o loop
    if not resposta:
        break

# Fecha a conexão com o servidor
client_socket.close()
