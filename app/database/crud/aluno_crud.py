from app.database.conexao import executar_queries, obter_resultados
from app.database.crud.usuario_crud import deletar_usuario

def criar_aluno(conexao, id_user, id_curso, matricula):
    """Cria um novo aluno"""
    # Validação de campos obrigatórios
    if not id_user or not id_curso or not matricula:
        print("Erro: id_user, id_curso e matricula são obrigatórios.")
        return False

    # Validação de unicidade de matrícula
    if buscar_aluno_por_matricula(conexao, matricula):
        print(f"Erro: A matrícula '{matricula}' já existe no sistema.")
        return False

    query = "INSERT INTO aluno (id_user, id_curso, matricula) VALUES (%s, %s, %s)"
    parametros = (id_user, id_curso, matricula)
    
    if executar_queries(conexao, query, parametros):
        print(f"Aluno ID {id_user} criado com sucesso!")
        return True
    return False

def buscar_aluno_por_id(conexao, id_user):
    """Busca aluno pelo ID"""
    query = "SELECT id_user, id_curso, matricula FROM aluno WHERE id_user = %s"
    resultado = obter_resultados(conexao, query, (id_user,))
    return resultado


def buscar_aluno_por_matricula(conexao, matricula):
    """Busca aluno pela matrícula"""
    query = "SELECT id_user, id_curso, matricula FROM aluno WHERE matricula = %s"
    resultado = obter_resultados(conexao, query, (matricula,))
    return resultado


def buscar_alunos_por_curso(conexao, id_curso):
    """Busca todos os alunos de um curso"""
    query = "SELECT id_user, id_curso, matricula FROM aluno WHERE id_curso = %s"
    resultado = obter_resultados(conexao, query, (id_curso,))
    return resultado


def buscar_todos_alunos(conexao):
    """Busca todos os alunos"""
    query = "SELECT id_user, id_curso, matricula FROM aluno"
    resultado = obter_resultados(conexao, query)
    return resultado


def update_aluno(conexao, matricula, id_curso=None):
    query= "UPDATE aluno SET id_curso = %s WHERE matricula = %s"
    executar_queries(conexao, query, parametros= (id_curso, matricula))
    print("Curso atualizado")


def deletar_aluno(conexao, id_user):
    """Deleta aluno e usuário associado"""
    # Primeiro deleta de Aluno
    query = "DELETE FROM aluno WHERE id_user = %s"
    executar_queries(conexao, query, parametros= (id_user,))
    
    # Depois deleta de Usuario
    deletar_usuario(conexao, id_user)
    print(f"Aluno ID {id_user} deletado com sucesso!")