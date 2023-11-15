def mensagemInicial(dinheiro_inicial):
    return f'''
    Bem vindo ao EGLS-Blackjack!
    Você acabou de receber ${dinheiro_inicial}!!
    Quanto você quer apostar?
    Valor: '''

def mensagemNormal(dinheiro, aposta, rodada, cartas_dealer, suas_cartas):
    return f'''
    
    SALDO: ${dinheiro: <6}   VALOR APOSTADO: ${aposta: <6}   RODADA: {rodada: <3}
    
    Cartas Dealer: {cartas_dealer}

    Suas Cartas: {suas_cartas}

    1- Pegar Carta
    2- Manter Mão
    3- Dobrar Aposta
    4- Desistir
    5- Sair do Jogo

    Opção: '''

def mensagemFimDeRodada(dinheiro, aposta_velha, rodada, cartas_dealer, suas_cartas, perdeu_ou_ganhou):
    valor_apostado = 0
    
    perdeu_ou_ganhou = 'ganhou' if perdeu_ou_ganhou else 'perdeu'

    return f'''
    
    SALDO: ${dinheiro: <6}   VALOR APOSTADO: ${valor_apostado : <6}   RODADA: {rodada: <3}

    Cartas Dealer: {cartas_dealer}

    Suas Cartas: {suas_cartas}

    Você {perdeu_ou_ganhou} ${aposta_velha} na rodada 3
    Quanto Você quer apostar?
    Valor: '''

def mensagemFimDeJogo():
    return f'''

    Você perdeu o Jogo!!
    Reconecte-se se quiser jogar novamente.
    '''