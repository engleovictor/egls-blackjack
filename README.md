# EGLS - blackjack

EGLS (Evelyn, Gandolfi, Leo, Sakai) é uma implementação em Python 3.11 para Blackjack

## Requisitos

Python 3.11.X

## Instalação

```bash
pip install psutil==5.9.4
pip install colorama==0.4.5
git clone https://github.com/engleovictor/egls-blackjack
cd egls-blackjack
```

## Uso

### Servidor

Deve-se acessar Server/server_info e modificar a porta na qual deseja rodar o servidor.

Depois, deve-se executar:

```bash
python3 Server/server.py
```

### Cliente

Para o cliente se conectar ao servidor, ele deve executar:

```bash
python3 Client/MainClient.py IP_DO_SERVIDOR PORTA
```
Se o usuário cliente tem dúvida do IP_DO_SERVIDOR ou da PORTA, ele deve consultar a mensagem que é mostrada no início da execução do servidor

## Licença

[MIT](https://choosealicense.com/licenses/mit/)
