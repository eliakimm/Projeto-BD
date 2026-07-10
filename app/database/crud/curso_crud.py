import psycopg2
from app.database.conexao import executar_queries, obter_resultados

def criar_curso(conexao, nome, total_horas, nivel, descricao=None):
    # Validação de campos obrigatórios
    if not nome or not total_horas or not nivel:
        print("Erro: Nome, total_horas e nivel são obrigatórios.")
        return False

    # Validação de unicidade (Nome do Curso)
    if buscar_curso(conexao, nome):
        print(f"Erro: O curso '{nome}' já está cadastrado.")
        return False

    if descricao:
        query= "INSERT INTO curso(nome, descricao, total_horas, nivel) VALUES (%s, %s, %s, %s)"
        parametros= (nome, descricao, total_horas, nivel)
    else:
        query= "INSERT INTO curso(nome, total_horas, nivel) VALUES (%s, %s, %s)" 
        parametros= (nome, total_horas, nivel)

    return executar_queries(conexao, query, parametros) is not None

def buscar_curso(conexao, nome):
    query= "SELECT * FROM curso WHERE nome = %s"
    busca= obter_resultados(conexao, query, parametros= (nome,))
    return busca

def update_curso(conexao, id_curso, nome= None, descricao= None, total_horas= None, nivel= None):
    campos= []
    parametros= []

    if nome: 
        campos.append("nome = %s")
        parametros.append(nome)
    
    if descricao:
        campos.append("descricao = %s")
        parametros.append(descricao)
    
    if total_horas:
        campos.append("total_horas = %s")
        parametros.append(total_horas)
    
    if nivel:
        campos.append("nivel = %s")
        parametros.append(nivel)

    parametros.append(id_curso)
    query= f"UPDATE curso SET {', '.join(campos)} WHERE id_curso = %s"
    executar_queries(conexao, query, parametros= tuple(parametros))

def deletar_curso(conexao, id_curso):
    query = "DELETE FROM curso WHERE id_curso = %s"

    try:
        executar_queries(conexao, query, (id_curso,))
        return True

    except psycopg2.errors.ForeignKeyViolation:
        conexao.rollback()
        raise