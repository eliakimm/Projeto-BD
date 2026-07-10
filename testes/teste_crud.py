from app.database.conexao import *
from app.database.crud.usuario_crud import *

conexao = conectar()

if(conexao):
    while(True):
        chave= input("->")
        if(chave == "-cad_user"):
            user_nome= input("nome:")
            user_email= input("email:")
            user_senha= input("senha:")
            
            criar_usuario(conexao, user_nome, user_email, user_senha)
        
        elif(chave == "-busca"):
            user_email= input("email:")
            result= buscar_usuario(conexao, user_email)
            if not result:
                print("Usuário não encontrado")
                continue
            
            for usuario in result:
                print(f"ID: {usuario[0]} \nNome: {usuario[1]} \nEmail: {usuario[2]} \nSenha: {usuario[3]}")

        elif(chave == "-enc"):
            break
        
        elif(chave == "-up"):
            user_email= input("email:")
            result= buscar_usuario(conexao, user_email)
            if not result:
                print("usuário não encontrado")
                continue

            user_id= result[0][0]
            user_nome= input("digite o novo nome ou enter para pular:").strip()
            user_email= input("digite o novo email ou enter para pular:").strip()
            user_senha= input("digite a nova senha ou enter para pular:").strip()

            update_usuario(conexao,
                        user_id,
                        nome= user_nome if user_nome else None,
                        email= user_email if user_email else None,
                        senha= user_senha if user_senha else None)
            

        elif(chave == "-del"):
            user_email= input("email:")
            user_senha= input("digite sua senha para confirmar:")
            result= buscar_usuario(conexao, user_email)
            if verificar_senha(user_senha, result[0][3]):
                delete_user_por_email(conexao, user_email)
                print("Usuário deletado")
            else:
                print("falha ao fazer login")

        else:
            print("comando não encontrado")
    
    encerrar(conexao)

else:
    print("sem conexão")




