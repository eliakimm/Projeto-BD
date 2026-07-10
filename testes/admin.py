from app.database.conexao import *
from app.database.crud.usuario_crud import *
from app.database.crud.admin_crud import *

conexao = conectar()

if conexao:
    while True:
        chave= input("->")
        if(chave == "new admin"):
            nome= input("Nome: ")
            email= input("Email: ")
            senha= input("Senha: ")
            cargo= input("Cargo: ")
            criar_usuario(conexao, nome, email, senha)
            busca= buscar_usuario_por_email(conexao, email)
            id_user= busca[0][0]
            criar_admin(conexao, id_user, cargo)
            print("->Admin criado com sucesso")
        if(chave == "del admin"):
            email= input("Email: ")
            busca= buscar_usuario_por_email(conexao, email)
            if(len(busca) == 0):
                print("->Usuário não encontrado")
                continue
            senha= input("Senha: ")
            if verificar_senha(senha, busca[0][3]):
                print(f"->usuario: {busca[0][1]}")
                chave= input("Confirmar exclusão da conta? (s/n)")
                if(chave == "s"):
                    deletar_admin(conexao, busca[0][0])
                    print("->Admin deletado do sistema")
                else:
                    continue
            else:
                print("[ERRO] Usuário ou senha incorretos")
        if(chave == "show admin"):
            querie= "SELECT nome, cargo FROM usuario INNER JOIN admin_sistema ON usuario.id_user = admin_sistema.id_user;"
            busca= obter_resultados(conexao, querie)
            print(f"{'Nome': ^25} | {'Cargo': ^29}")
            for admin in busca:
                print("-" * 54)
                print(f"{admin[0]: ^25} | {admin[1]: ^29}")
            
        if(chave == "end"):
            break
        if(chave == "help"):
            print("->lista de comandos:")
            print("new admin : para cadastrar um novo admin;")
            print("del : para deletar sua conta de admin;")
        # else:
        #     print("->Comando não enconrtrado, use o camando help para ver a lista de comandos")


    encerrar(conexao)
            
            

            
