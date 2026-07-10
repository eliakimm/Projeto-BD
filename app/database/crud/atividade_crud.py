from app.database.conexao import executar_queries, obter_resultados

def criar_atividade(conexao, titulo, descricao, data_entrega, id_disciplina):
    """Cria uma nova atividade"""
    # Validação de campos obrigatórios e textos vazios
    if not titulo or not descricao or not data_entrega or not id_disciplina:
        print("Erro: Todos os campos (título, descrição, data de entrega e disciplina) são obrigatórios.")
        return False

    query = "INSERT INTO atividade (titulo, descricao, data_entrega, id_disciplina) VALUES (%s, %s, %s, %s)"
    parametros = (titulo, descricao, data_entrega, id_disciplina)
    
    if executar_queries(conexao, query, parametros):
        print(f"Atividade '{titulo}' criada com sucesso!")
        return True
    return False

def buscar_atividade_por_id(conexao, id_atividade):
    """Busca atividade pelo ID"""
    query = "SELECT * FROM atividade WHERE id_atividade = %s"
    resultado = obter_resultados(conexao, query, (id_atividade,))
    return resultado

def buscar_atividades_por_disciplina(conexao, id_disciplina):
    """Busca todas as atividades de uma disciplina"""
    query = "SELECT * FROM atividade WHERE id_disciplina = %s"
    resultado = obter_resultados(conexao, query, (id_disciplina,))
    return resultado

def update_atividade(conexao, id_atividade, titulo=None, descricao=None, data_entrega=None, id_disciplina=None):
    """Atualiza campos específicos de uma atividade"""
    campos = []
    parametros = []

    if titulo:
        campos.append("titulo = %s")
        parametros.append(titulo)
    if descricao:
        campos.append("descricao = %s")
        parametros.append(descricao)
    if data_entrega:
        campos.append("data_entrega = %s")
        parametros.append(data_entrega)
    if id_disciplina:
        campos.append("id_disciplina = %s")
        parametros.append(id_disciplina)

    if not campos:
        print("Nenhum campo informado para atualização.")
        return

    parametros.append(id_atividade)
    query = f"UPDATE atividade SET {', '.join(campos)} WHERE id_atividade = %s"
    executar_queries(conexao, query, parametros=tuple(parametros))
    print(f"Atividade ID {id_atividade} atualizada.")

def deletar_atividade(conexao, id_atividade):
    """Remove uma atividade pelo ID"""
    query = "DELETE FROM atividade WHERE id_atividade = %s"
    executar_queries(conexao, query, parametros=(id_atividade,))
    print(f"Atividade ID {id_atividade} deletada.")