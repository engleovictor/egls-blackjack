import egls_inteface

def replyMannager(dados: dict):
    if 'payload' in dados:
        params = dados['payload'].values()
    else:
        params = []

    if  dados['code'] == 1: # payload dinheiro inicial
        return inicioRequest(*params)
    
    elif  dados['code'] == 11: # Pedido Invalido!
        print('Erro no lado do servidor, aposta enviada maior que o dinheiro que voce possui\nColoque um valor válido!!\n')
        return inicioRequest(*params)
    
    elif  dados['code'] == 12: # Ok, Payload full
        return acaoRequest(*params)
    
    elif  dados['code'] == 24: # Ok, full
        return acaoRequest(*params)
    
    elif  dados['code'] == 25: # Pedido Dobrar negado, full?
        print('Erro no lado do servidor, aposta enviada maior que o dinheiro que voce possui\nColoque um valor válido!!\n')
        return acaoRequest(*params)
    
    elif  dados['code'] == 26: # Full mas fim de rodada
        return fimDeRodadaRequest(*params)
    
    elif  dados['code'] == 28: # sem payload fim de jogo
        fimDeJogoMessage(*params)

def inicioRequest(dinheiro):
    print(egls_inteface.mensagemInicial(dinheiro), end='')
    
    while(True):
        try:
            opt = int(input())
        
        except ValueError:
            print("    Opção Invalida!!, por favor escolha uma opção válida: ", end='')
            continue

        except KeyboardInterrupt:
            return {'code':27}
        
        if opt > dinheiro:
            print("    Opção Invalida!!, por favor escolha uma opção válida: ", end='')
            continue
            
        return {'code': 10, 'payload': {'bet': opt}}
    
def fimDeJogoMessage():
    print(egls_inteface.mensagemFimDeJogo())
    return {'code': 27}

def fimDeRodadaRequest(*args):
    print(egls_inteface.mensagemFimDeRodada(*args), end='')
    
    while(True):
        try:
            opt = int(input())
        
        except ValueError:
            print("    Opção Invalida!!, por favor escolha uma opção válida: ", end='')
            continue

        except KeyboardInterrupt:
            return {'code': 27}
        
        if opt > int(args[0]):
            print("    Opção Invalida!!, por favor escolha uma opção válida: ", end='')
            
        return {'code': 10, 'payload': {'bet': opt}}

def acaoRequest(dinheiro, aposta, rodada, cartas_dealer, suas_cartas):

    print(egls_inteface.mensagemNormal(dinheiro, aposta, rodada, cartas_dealer, suas_cartas), end='')

    while(True):
        try:
            opt = int(input())
        except ValueError:
            print("    Opção Invalida!!, por favor escolha uma opção válida: ", end='')
            continue

        except KeyboardInterrupt:
            return {'code': 27}

        if opt < 1 or opt > 5:
            print("    Opção Invalida!!, por favor escolha uma opção válida: ", end='')
            continue

        elif opt == 1: # Pedir mais uma carta.
            return {'code': 20}
        elif opt == 2: # Manter Mão.
            return {'code': 21}
        elif opt == 3: # Dobrar Aposta e pedir mais uma carta.
            if dinheiro >= aposta:
                return {'code': 22}
            else:
                print("    Voce não pode dobrar aposta!!\n    Escolha uma opção válida: ", end='')
        elif opt == 4: # Desistir.
            return {'code': 23}
        else: # opt == 5 Sair do Jogo
            return {'code': 27}
