from config import conectar
from config import encerrar

conexao= conectar()

if conexao:
    print(f"Conexão: {type(conexao)}")

    chave= input("enter para encerrar a conexão:")
    if(len(chave) >= 0):
        encerrar(conexao)
else:
    print("falha ao conectar")