from app.database.conexao import executar_queries, obter_resultados

def vincular_atividade_agenda(conexao, id_agenda, id_atividade):
    """Vincula uma atividade a um item da agenda (tabela associativa)"""
    query = "INSERT INTO novo_evento (id_agenda, id_atividade) VALUES (%s, %s)"
    parametros = (id_agenda, id_atividade)
    executar_queries(conexao, query, parametros)
    print("Atividade vinculada à agenda com sucesso.")

def buscar_atividades_agenda(conexao, id_agenda):
    """Busca as atividades associadas a um registro de agenda"""
    query = """
        SELECT a.* FROM atividade a
        JOIN novo_evento ne ON a.id_atividade = ne.id_atividade
        WHERE ne.id_agenda = %s
    """
    return obter_resultados(conexao, query, (id_agenda,))