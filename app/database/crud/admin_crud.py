from app.database.conexao import executar_queries, obter_resultados
from app.database.crud.usuario_crud import deletar_usuario

def criar_admin(conexao, id_user, cargo):
    query= "INSERT INTO admin_sistema(id_user, cargo) VALUES (%s, %s)"
    executar_queries(conexao, query, parametros= (id_user, cargo))
    print("admin criado")

def buscar_admin_por_id(conexao, id_user):
    query= "SELECT * FROM admin_sistema WHERE id_user = %s"
    busca= obter_resultados(conexao, query, parametros= (id_user,))
    return busca

def buscar_admin_por_cargo(conexao, cargo):
    query= "SELECT * FROM admin_sistema WHERE cargo = %s"
    busca= obter_resultados(conexao, query, parametros= (cargo,))
    return busca

def busca_todos_admins(conexao):
    query= "SELECT * FROM admin_sistema"
    busca= obter_resultados(conexao, query)
    return busca

def update_cargo_admin(conexao, id_user, cargo= None):
    if cargo:
        query= "UPDATE admin_sistema SET cargo = %s WHERE id_user = %s"
        executar_queries(conexao, query, parametros= (cargo, id_user))
        print("Cargo atualizado")
    else:
        print("nenhum campo para atualizar")

def deletar_admin(conexao, id_user):
    query= "DELETE FROM admin_sistema WHERE id_user = %s"
    executar_queries(conexao, query, parametros= (id_user,))
    deletar_usuario(conexao, id_user)
    print("Usuário deletado")