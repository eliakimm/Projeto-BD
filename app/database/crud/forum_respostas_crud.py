from app.database.conexao import executar_queries, obter_resultados

def criar_resposta(conexao, conteudo, data_publicacao, id_user, id_pergunta):
    """Cria uma nova resposta para uma pergunta no fórum usando o esquema atual do projeto."""
    if not conteudo or not id_user or not id_pergunta:
        print("Erro: Todos os campos (conteúdo, usuário e pergunta) são obrigatórios.")
        return False

    query = "INSERT INTO forum_resposta (id_pergunta, id_user, texto) VALUES (%s, %s, %s)"
    parametros = (id_pergunta, id_user, conteudo)

    cursor = executar_queries(conexao, query, parametros)
    if cursor:
        print(f"Resposta criada para a pergunta ID {id_pergunta} com sucesso!")
        return True
    return False

def buscar_resposta_por_id(conexao, id_resposta):
    """Busca resposta do fórum pelo ID"""
    query = "SELECT * FROM forum_respostas WHERE id_resposta = %s"
    resultado = obter_resultados(conexao, query, (id_resposta,))
    return resultado

def buscar_respostas_por_pergunta(conexao, id_pergunta):
    """Busca todas as respostas para uma pergunta específica"""
    query = "SELECT * FROM forum_respostas WHERE id_pergunta = %s"
    resultado = obter_resultados(conexao, query, (id_pergunta,))
    return resultado

def buscar_respostas_por_usuario(conexao, id_user):
    """Busca todas as respostas de um usuário no fórum"""
    query = "SELECT * FROM forum_respostas WHERE id_user = %s"
    resultado = obter_resultados(conexao, query, (id_user,))
    return resultado

def update_resposta(conexao, id_resposta, conteudo=None, data_publicacao=None, id_user=None, id_pergunta=None):
    """Atualiza campos específicos de uma resposta do fórum"""
    campos = []
    parametros = []

    if conteudo:
        campos.append("conteudo = %s")
        parametros.append(conteudo)
    if data_publicacao:
        campos.append("data_publicacao = %s")
        parametros.append(data_publicacao)
    if id_user:
        campos.append("id_user = %s")
        parametros.append(id_user)
    if id_pergunta:
        campos.append("id_pergunta = %s")
        parametros.append(id_pergunta)

    if not campos:
        print("Nenhum campo informado para atualização.")
        return

    parametros.append(id_resposta)
    query = f"UPDATE forum_respostas SET {', '.join(campos)} WHERE id_resposta = %s"
    executar_queries(conexao, query, parametros=tuple(parametros))
    print(f"Resposta do fórum ID {id_resposta} atualizada.")

def deletar_resposta(conexao, id_resposta):
    """Remove uma resposta do fórum pelo ID"""
    query = "DELETE FROM forum_respostas WHERE id_resposta = %s"
    executar_queries(conexao, query, parametros=(id_resposta,))
    print(f"Resposta do fórum ID {id_resposta} deletada.")