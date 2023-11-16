import random

class Baralho:
    def __init__(self):
        self.baralho = getBaralho()
        random.shuffle(self.baralho)

    def recomecar(self):
        self.baralho = getBaralho()
        random.shuffle(self.baralho)

    def pegarCarta(self):
        return self.baralho.pop()

def getBaralho():
    baralho = []
    
    hops = {
        1:'A',
        11:'Q',
        12:'J',
        13:'K'
    }

    for naipe in (chr(9830), chr(9824), chr(9829), chr(9827)):
        for valor in range(1,14):
            baralho.append(f'{valor}{naipe}') if valor > 1 and valor < 11 else baralho.append(f'{hops[valor]}{naipe}')
    
    return baralho.copy()

if __name__ == '__main__':
    print(getBaralho())