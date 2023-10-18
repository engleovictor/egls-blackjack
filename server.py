import socket
import threading
import psutil
import pathlib
import colorama
from Baralho import Baralho


colorama.init(autoreset=True)

def getIPAddress(interface='wlan0'):
    interfaces = psutil.net_if_addrs()

    for fam, addr, *_ in interfaces[interface]:
        if fam == 2:
            return addr
        
    return 'Não Conectado'

def getServerInfo(filename=(str(pathlib.Path(__file__).parent)+'/server_info')):
    server_info = {}
    try:
        with open(filename,"r") as f:
            lines = f.read().splitlines()
            for line in lines:
                dkey, dvalue = line.split("=")
                server_info.update({dkey: dvalue})
            return server_info
    except FileNotFoundError:
        exit(colorama.Back.RED+f"arquivo '{filename}' não encontrado!!")


## Exemplo do handle cliente.
def handle_client(csocket, endereco):
    baralho = Baralho()
    print(f"Novo jogador: {endereco}")
    while True:
        mensagem = csocket.recv(1024).decode('utf-8')
        if not mensagem:
            # Se a mensagem estiver vazia, o cliente se desconectou
            print(f"Jogador {endereco} se desconectou")
            break

        game_status = {}
        headers = mensagem.splitlines()
        for header in headers:
            dkey, dvalue = header.split(":")
            game_status.update({dkey: dvalue})

        resposta = ""

        if game_status['stat'] == 'inicio' or game_status['stat'] == 'meio':
            resposta += "stat:esperar_aposta\n"
            resposta += "seq_maq:\n"
            resposta += "seq_pla:\n"
            resposta += "aposta:0\n"
            resposta += "dinheiro:100" if game_status['stat'] == 'inicio' else f'dinheiro:{game_status["dinheiro"]}'

        elif game_status['stat'] == '2j':
            pass

        elif game_status['stat'] == '1jp':
            pass
        
        elif game_status['stat'] == '1jm':
            pass
        
        elif game_status['stat'] == 'fim':
            csocket.close()

        ##############################################################
        ###                                                        ###
        ###           JOGO ACONTECE E MUDA A RESPOSTA.             ###
        ###                                                        ###
        ##############################################################
        csocket.send(resposta.encode('utf-8'))
    csocket.close()


def main(handle, server_info):
    ssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    port = server_info['port']
    ssocket.bind((getIPAddress(), int(port)))

    ssocket.listen(5)

    print(f"{getIPAddress()}:{server_info['port']}")

    while True:
        csocket, address = ssocket.accept()
        cthread = threading.Thread(target=handle, args=(csocket, address))
        cthread.start()
        

if __name__ == '__main__':
    main(handle_client,getServerInfo())
