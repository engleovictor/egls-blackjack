import socket
import threading
import psutil
import pathlib
import colorama
import json
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

def blackJack(cartas):
    sum = 0
    count = 0
    for i in cartas:
        if (i[0]=='K') | (i[0]=='Q') | (i[0]=='J') | ((i[0]=='1') & (i[1]=='0')):
            sum+=10
        elif i[0]=='A':
            sum+=11
            count+=1
        else:
            sum+=int(i[0])

    if sum<=21 or count==0:
        return sum
    
    while count>0 and sum > 21:
        sum-=10
        count-=1
    
    return sum

def handle_client(csocket, endereco):
    print(f"Novo jogador: {endereco}")

    total=0
    round=0
    bet=0
    dealerCards = []
    playerCards = []
    baralho = Baralho()
    
    while True:
        mensagem = csocket.recv(1024).decode('utf-8')
        # Se a mensagem estiver vazia, o cliente se desconectou
        if not mensagem:
            print(f"Jogador {endereco} se desconectou")
            break

        data = json.loads(mensagem)
        resposta = {}

        match data['code']:
            case 0:
                # Inicio do jogo
                total=100
                resposta = {
                    "code": 1,
                    "payload": {
                        "total": 100
                    }
                }
            case 10:
                # Aposta inicial
                if data['payload']['bet'] > total:
                    # Aposta invalida
                    resposta = {
                        "code":11
                    }
                else:
                    # Aposta válida
                    round+=1
                    bet = data['payload']['bet']
                    total -= bet
                    playerCards += [baralho.pegarCarta(), baralho.pegarCarta()]
                    dealerCards += [baralho.pegarCarta(), baralho.pegarCarta()]

                    resposta = {
                        "code": 12,
                        "payload": {
                            "money": total,
                            "bet": bet,
                            "round": round,
                            "dealerCards": dealerCards,
                            "playerCards": playerCards,
                        }
                    }
            case 20:
                # Jogador pega uma nova carta
                playerCards += [baralho.pegarCarta()]

                # Verifica se jogador passou de 21 pontos
                if blackJack(playerCards) <= 21:
                    # OK
                    resposta = {
                        "code": 24,
                        "payload": {
                            "money": total,
                            "bet": bet,
                            "round": round,
                            "dealerCards": dealerCards,
                            "playerCards": playerCards,
                        }
                    }
                else:
                    # Jogador passou de 21 pontos: Fim da rodada
                    resposta = {
                        "code": 26,
                        "payload": {
                            "money": total,
                            "bet": bet,
                            "round": round,
                            "dealerCards": dealerCards,
                            "playerCards": playerCards,
                        }
                    }
                    dealerCards = []
                    playerCards = []
                    baralho = Baralho()
                    if total==0:
                        resposta = {
                            "code": 28
                        }

            case 21:
                # Jogador escolheu Manter
                # Dealer vai pegar novas cartas enquanto a soma de suas cartas for menor que 21 pontos ou maior que os pontos do jogador
                while (blackJack(dealerCards) < 21) & (blackJack(dealerCards) < blackJack(playerCards)):
                    dealerCards += [baralho.pegarCarta()]
                
                if blackJack(dealerCards) <= 21:
                    # Mesa ganhou e fim da rodada
                    resposta = {
                        "code": 26,
                        "payload": {
                            "money": total,
                            "bet": bet,
                            "round": round,
                            "dealerCards": dealerCards,
                            "playerCards": playerCards,
                        }
                    }                    
                else:
                    # Mesa perdeu e fim da rodada
                    total += 2*bet
                    resposta = {
                        "code": 26,
                        "payload": {
                            "money": total,
                            "bet": bet,
                            "round": round,
                            "dealerCards": dealerCards,
                            "playerCards": playerCards,
                        }
                    }
                if(blackJack(dealerCards)==blackJack(playerCards)):
                    # Empate
                    total+=bet
                    resposta = {
                        "code": 26,
                        "payload": {
                            "money": total,
                            "bet": bet,
                            "round": round,
                            "dealerCards": dealerCards,
                            "playerCards": playerCards,
                        }
                    }
                dealerCards = []
                playerCards = []
                baralho = Baralho()
                if total==0:
                    resposta = {
                        "code": 28
                    }
            case 22:
                # Dobrar
                if bet > total:
                    # Caso invalido
                    resposta = {
                        "code":25,
                        "payload": {
                            "money": total,
                            "bet": bet,
                            "round": round,
                            "dealerCards": dealerCards,
                            "playerCards": playerCards,
                        }
                    }
                else:
                    # Caso valido
                    total -= bet
                    bet += bet
                    playerCards += [baralho.pegarCarta()]
                    playerBlackJack = blackJack(playerCards)

                    if (playerBlackJack < 21):
                        while (blackJack(dealerCards) < 21) & (blackJack(dealerCards) < playerBlackJack):
                            dealerCards += [baralho.pegarCarta()]

                    if (playerBlackJack > 21) | (blackJack(dealerCards) <= 21):
                        # Mesa ganhou e fim da rodada
                        resposta = {
                            "code": 26,
                            "payload": {
                                "money": total,
                                "bet": bet,
                                "round": round,
                                "dealerCards": dealerCards,
                                "playerCards": playerCards,
                            }
                        }
                    else:
                        # Player ganhou e fim da rodada
                        total += 2*bet
                        resposta = {
                            "code": 26,
                            "payload": {
                                "money": total,
                                "bet": bet,
                                "round": round,
                                "dealerCards": dealerCards,
                                "playerCards": playerCards,
                            }
                        }
                    if(blackJack(dealerCards)==blackJack(playerCards)):
                        # Empate
                        total+=bet
                        resposta = {
                            "code": 26,
                            "payload": {
                                "money": total,
                                "bet": bet,
                                "round": round,
                                "dealerCards": dealerCards,
                                "playerCards": playerCards,
                            }
                        }
                    dealerCards = []
                    playerCards = []
                    baralho = Baralho()
                    if total==0:
                        resposta = {
                            "code": 28
                        }
            case 23:
                # Desistir // fim da rodada
                total += bet/2
                resposta = {
                    "code": 26,
                    "payload": {
                        "money": total,
                        "bet": bet,
                        "round": round,
                        "dealerCards": dealerCards,
                        "playerCards": playerCards,
                    }
                }
                dealerCards = []
                playerCards = []
                baralho = Baralho()
                if total==0:
                    resposta = {
                        "code": 28
                    }
            case 27:
                # Sair
                resposta = {
                    "code": 28
                }
                dealerCards = []
                playerCards = []
                baralho = Baralho()

        csocket.send(json.dumps(resposta).encode('utf-8'))
    csocket.close()

def main(handle, server_info):
    ssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssocket.bind((getIPAddress(), int(server_info['port'])))
    ssocket.listen(5)

    print(f"Server up and running on {getIPAddress()}:{server_info['port']}!")

    while True:
        csocket, address = ssocket.accept()
        cthread = threading.Thread(target=handle, args=(csocket, address))
        cthread.start()
        
if __name__ == '__main__':
    main(handle_client, getServerInfo())
