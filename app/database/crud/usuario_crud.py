import bcrypt
import re
from app.database.conexao import executar_queries, obter_resultados

def hash_senha(senha):
    """Converte senha em hash"""
    salt = bcrypt.gensalt()
    hash_bytes = bcrypt.hashpw(senha.encode('utf-8'), salt)
    return hash_bytes.decode('utf-8')  # ← Converter para string


def verificar_senha(senha, hash_armazenado):
    """Verifica se a senha está correta"""
    # Converter hash de string para bytes
    if isinstance(hash_armazenado, str):
        hash_armazenado = hash_armazenado.encode('utf-8')
    
    return bcrypt.checkpw(senha.encode('utf-8'), hash_armazenado)


def criar_usuario(conexao, nome, email, senha):
    # Validação de campos obrigatórios
    if not nome or not email or not senha:
        print("Erro: Nome, email e senha são obrigatórios.")
        return False

    # Validação de formato de e-mail
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        print("Erro: Formato de e-mail inválido.")
        return False

    # Validação de unicidade (E-mail deve ser único)
    if buscar_usuario_por_email(conexao, email):
        print(f"Erro: O e-mail '{email}' já está em uso.")
        return False

    senha_criptografada = hash_senha(senha)
    query = "INSERT INTO usuario (nome, email, senha) VALUES (%s, %s, %s) RETURNING id_user"
    parametros = (nome, email, senha_criptografada)

    cursor = executar_queries(conexao, query, parametros)
    if cursor:
        resultado = cursor.fetchone()
        cursor.close()
        if resultado:
            print(f"Usuário '{nome}' criado com sucesso!")
            return resultado[0]
    return False


def buscar_usuario_por_email(conexao, email):
    query= "SELECT id_user, nome, email, senha FROM usuario WHERE email = %s"
    busca= obter_resultados(conexao, query, parametros= (email,))
    return busca

def buscar_usuario_por_id(conexao, id_user):
    query= "SELECT id_user, nome, email, senha FROM usuario WHERE id_user = %s"
    busca= obter_resultados(conexao, query, parametros= (id_user,))
    return busca
    
def update_usuario(conexao, id_user, nome= None, email= None, senha= None):
    campos= []
    parametros= []

    if nome:
        campos.append("nome = %s")
        parametros.append(nome)
    
    if email:
        campos.append("email = %s")
        parametros.append(email)
    if senha:
        campos.append("senha = %s")
        parametros.append(hash_senha(senha))
    
    if not campos:
        print("nenhum campo para atualizar")
        return False

    parametros.append(id_user)
    query= f"UPDATE usuario SET {', '.join(campos)} WHERE id_user = %s"
    cursor = executar_queries(conexao, query, tuple(parametros))
    return cursor is not None


def delete_user_por_email(conexao, email):

    query= "DELETE FROM usuario WHERE email = %s"
    executar_queries(conexao, query, parametros= (email,)) 

def delete_user_por_id(conexao, id_user):

    query= "DELETE FROM usuario WHERE id_user = %s"
    executar_queries(conexao, query, parametros= (id_user,)) 


def deletar_usuario(conexao, id_user):
    """Alias compatível com outros módulos: deleta usuário por id."""
    return delete_user_por_id(conexao, id_user)


def buscar_usuario(conexao, email):
    """Alias compatível com testes: busca usuário por email."""
    return buscar_usuario_por_email(conexao, email)