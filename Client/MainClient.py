import jogoClient
import socket
import json
import sys

def main():
    server_ip = sys.argv[1]              # Substituir pelo IP do servidor 
    server_port = int(sys.argv[2])       # Porta do servidor

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

        # print(f'{resposta}')

        dadosDoServidor: dict = json.loads(resposta)

        if dadosDoServidor['code'] in [12,24,25,26]:
            dinheiroDoClient = dadosDoServidor['payload']['money']
            aposta           = dadosDoServidor['payload']['bet'] 
            rodada           = dadosDoServidor['payload']['round']

        if dadosDoServidor['code'] == 1:
            dinheiroDoClient = dadosDoServidor['payload']['total']

        if dadosDoServidor['code'] == 11:
            dadosDoServidor.update({'payload':{'total': dinheiroDoClientAnterior}})

        if dadosDoServidor['code'] == 26:
            status=''
            if dinheiroDoClient == dinheiroDoClientAnterior + 2*apostaAntiga:
                status='ganhou'
            elif dinheiroDoClient == dinheiroDoClientAnterior + apostaAntiga:
                status='empatou'
            elif dinheiroDoClient == dinheiroDoClientAnterior + apostaAntiga//2:
                status='desistiu'
            else:
                status='perdeu'
            dadosDoServidor['payload'].update({'perdeu_ou_ganhou': status})

        if dadosDoServidor['code'] == 28:
            dadosProServidor = jogoClient.replyMannager(dadosDoServidor)
            break

        dadosProServidor = jogoClient.replyMannager(dadosDoServidor)

        client_socket.send(json.dumps(dadosProServidor).encode('utf-8'))

        if not resposta:
            break

    client_socket.close()

if __name__ == '__main__':
    main()
