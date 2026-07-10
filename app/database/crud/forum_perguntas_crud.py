from app.database.conexao import executar_queries, obter_resultados

def criar_pergunta(conexao, titulo, conteudo, data_publicacao, id_user, id_disciplina):
    """Cria uma nova pergunta no fórum usando o esquema atual do projeto."""
    if not titulo or not conteudo or not id_user or not id_disciplina:
        print("Erro: Todos os campos (título, conteúdo, usuário e disciplina) são obrigatórios.")
        return False

    query = "INSERT INTO forum_pergunta (id_disciplina, id_user, titulo, texto, ativa) VALUES (%s, %s, %s, %s, true)"
    parametros = (id_disciplina, id_user, titulo, conteudo)

    cursor = executar_queries(conexao, query, parametros)
    if cursor:
        print(f"Pergunta '{titulo}' criada no fórum com sucesso!")
        return True
    return False

def buscar_pergunta_por_id(conexao, id_pergunta):
    """Busca pergunta do fórum pelo ID"""
    query = "SELECT * FROM forum_perguntas WHERE id_pergunta = %s"
    resultado = obter_resultados(conexao, query, (id_pergunta,))
    return resultado

def buscar_perguntas_por_disciplina(conexao, id_disciplina):
    """Busca todas as perguntas de uma disciplina no fórum"""
    query = "SELECT * FROM forum_perguntas WHERE id_disciplina = %s"
    resultado = obter_resultados(conexao, query, (id_disciplina,))
    return resultado

def buscar_perguntas_por_usuario(conexao, id_user):
    """Busca todas as perguntas de um usuário no fórum"""
    query = "SELECT * FROM forum_perguntas WHERE id_user = %s"
    resultado = obter_resultados(conexao, query, (id_user,))
    return resultado

def update_pergunta(conexao, id_pergunta, titulo=None, conteudo=None, data_publicacao=None, id_user=None, id_disciplina=None):
    """Atualiza campos específicos de uma pergunta do fórum"""
    campos = []
    parametros = []

    if titulo:
        campos.append("titulo = %s")
        parametros.append(titulo)
    if conteudo:
        campos.append("conteudo = %s")
        parametros.append(conteudo)
    if data_publicacao:
        campos.append("data_publicacao = %s")
        parametros.append(data_publicacao)
    if id_user:
        campos.append("id_user = %s")
        parametros.append(id_user)
    if id_disciplina:
        campos.append("id_disciplina = %s")
        parametros.append(id_disciplina)

    if not campos:
        print("Nenhum campo informado para atualização.")
        return

    parametros.append(id_pergunta)
    query = f"UPDATE forum_perguntas SET {', '.join(campos)} WHERE id_pergunta = %s"
    executar_queries(conexao, query, parametros=tuple(parametros))
    print(f"Pergunta do fórum ID {id_pergunta} atualizada.")

def deletar_pergunta(conexao, id_pergunta):
    """Remove uma pergunta do fórum pelo ID"""
    query = "DELETE FROM forum_perguntas WHERE id_pergunta = %s"
    executar_queries(conexao, query, parametros=(id_pergunta,))
    print(f"Pergunta do fórum ID {id_pergunta} deletada.")