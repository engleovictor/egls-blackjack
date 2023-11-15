import jogoClient
import socket
import json

def main():
    server_ip = "172.15.3.141" # Substituir pelo IP do servidor 
    server_port = 8888       # Porta do servidor

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((server_ip, server_port))

    mensagem = {
        'code': 0
    }

    client_socket.send(json.dumps(mensagem).encode('utf-8'))

    dinheiroDoClient = 0

    dinheiroDoClientAnterior = 0

    rodada = 0

    aposta = 0

    apostaAntiga = 0

    while True:
        
        dinheiroDoClientAnterior = dinheiroDoClient

        apostaAntiga = aposta

        resposta = client_socket.recv(1024).decode('utf-8')

        print(f'{resposta}')

        dadosDoServidor: dict = json.loads(resposta)

        if dadosDoServidor['code'] in [12,24,25,26]:
            dinheiroDoClient = dadosDoServidor['payload']['money']
            aposta           = dadosDoServidor['payload']['bet'] 
            rodada           = dadosDoServidor['payload']['round']

        if dadosDoServidor['code'] == 1:
            dinheiroDoClient = dadosDoServidor['payload']['total']

        if dadosDoServidor['code'] == 11:
            dadosDoServidor.update({'payload':{'total':dinheiroDoClientAnterior}})

        if dadosDoServidor['code'] == 26:
            dadosDoServidor['payload'].update({'perdeu_ou_ganhou':dinheiroDoClient >= dinheiroDoClientAnterior + apostaAntiga})

        if dadosDoServidor['code'] == 28:
            break

        dadosProServidor = jogoClient.replyMannager(dadosDoServidor)

        client_socket.send(json.dumps(dadosProServidor).encode('utf-8'))

        if not resposta:
            break

    client_socket.close()

if __name__ == '__main__':
    main()
