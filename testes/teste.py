from app.database.conexao import conectar
from app.database.conexao import encerrar
from app.database.conexao import executar_queries
from app.database.conexao import obter_resultados

conexao= conectar()

if conexao:
    print(f"Conexão ok: {type(conexao)}")

    while(True):
        chave= input("->")
        if(chave == "-exe"): #executa queries (não há retorno de dados)
            query= input("query->")
            parametros_input= input("parametros->")
            parametros= tuple(parametros_input.split(","))
            executar_queries(conexao, query, parametros)
        
        elif(chave == "-busca"): #realiza buscas, com base em select (pois há retorno de dados)
            query= input("query->")
            parametros_input= input("parametros->")
            parametros= tuple(parametros_input.split(","))
            result=obter_resultados(conexao, query, parametros)
            print(result)
        
        elif(chave == "-enc"): #encerra o loop
            break
        
        elif(chave == "-help"): #mostra lista de comandos
            print("->Lista de comandos:")
            print("|executar: -exe |")
            print("|buscar: -busca |")
            print("|encerrar: -enc |")

        else:
            print("comando não encontrado")
            print("digite -help para ver lista de comandos")

    encerrar(conexao) #encerra a conexão
        
else:
    print("falha ao conectar")