def mensagemInicial(dinheiro_inicial):
    return f'''
    Bem vindo ao EGLS-Blackjack!
    Você acabou de receber ${dinheiro_inicial}!!
    Quanto você quer apostar?
    Valor: '''

def mensagemNormal(dinheiro, aposta, rodada, cartas_dealer, suas_cartas):
    
    suas_cartas=' '.join(map(str, suas_cartas))

    return f'''
    
    SALDO: ${dinheiro: <6}   VALOR APOSTADO: ${aposta: <6}   RODADA: {rodada: <3}
    
    Cartas Dealer: {cartas_dealer[0]}, XX

    Suas Cartas: {suas_cartas}

    1- Pegar Carta
    2- Manter Mão
    3- Dobrar Aposta
    4- Desistir
    5- Sair do Jogo

    Opção: '''

def mensagemFimDeRodada(dinheiro, aposta_velha, rodada, cartas_dealer, suas_cartas, perdeu_ou_ganhou):
    valor_apostado = 0
    cartas_dealer=' '.join(map(str, cartas_dealer))
    suas_cartas=' '.join(map(str, suas_cartas))

    if perdeu_ou_ganhou == 'empatou':
        return f'''
    
    SALDO: ${dinheiro: <6}   VALOR APOSTADO: ${valor_apostado : <6}   RODADA: {rodada: <3}

    Cartas Dealer: {cartas_dealer}

    Suas Cartas: {suas_cartas}

    Você {perdeu_ou_ganhou} na rodada {rodada} e recebeu sua aposta de volta
    Quanto Você quer apostar?
    Valor: '''
    
    if perdeu_ou_ganhou == 'desistiu':
        return f'''
    
    SALDO: ${dinheiro: <6}   VALOR APOSTADO: ${valor_apostado : <6}   RODADA: {rodada: <3}

    Cartas Dealer: {cartas_dealer}

    Suas Cartas: {suas_cartas}

    Você {perdeu_ou_ganhou} da rodada {rodada} e recebeu ${aposta_velha/2} de volta
    Quanto Você quer apostar?
    Valor: '''

    return f'''
    
    SALDO: ${dinheiro: <6}   VALOR APOSTADO: ${valor_apostado : <6}   RODADA: {rodada: <3}

    Cartas Dealer: {cartas_dealer}

    Suas Cartas: {suas_cartas}

    Você {perdeu_ou_ganhou} ${aposta_velha} na rodada {rodada}
    Quanto Você quer apostar?
    Valor: '''

def mensagemFimDeJogo(dinheiro, valor_apostado, rodada, cartas_dealer, suas_cartas):
    
    cartas_dealer=' '.join(map(str, cartas_dealer))
    suas_cartas=' '.join(map(str, suas_cartas))
    
    return f'''

    SALDO: ${dinheiro: <6}   VALOR APOSTADO: ${valor_apostado : <6}   RODADA: {rodada: <3}

    Cartas Dealer: {cartas_dealer}

    Suas Cartas: {suas_cartas}

    Você perdeu o Jogo!!
    Reconecte-se se quiser jogar novamente.
    '''