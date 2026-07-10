from app.database.conexao import executar_queries, obter_resultados

def criar_aviso(conexao, id_user, titulo, texto):
    """Cria um novo aviso usando o esquema atual do projeto."""
    query = "INSERT INTO aviso (id_user, titulo, texto) VALUES (%s, %s, %s)"
    parametros = (id_user, titulo, texto)
    cursor = executar_queries(conexao, query, parametros)
    print(f"Aviso '{titulo}' criado com sucesso!")
    return cursor is not None

def buscar_aviso_por_id(conexao, id_aviso):
    """Busca aviso pelo ID"""
    query = "SELECT * FROM aviso WHERE id_aviso = %s"
    resultado = obter_resultados(conexao, query, (id_aviso,))
    return resultado

def buscar_todos_avisos(conexao):
    """Busca todos os avisos"""
    query = "SELECT * FROM aviso"
    resultado = obter_resultados(conexao, query)
    return resultado

def update_aviso(conexao, id_aviso, titulo=None, conteudo=None, data_publicacao=None, id_admin=None):
    """Atualiza campos específicos de um aviso"""
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
    if id_admin:
        campos.append("id_admin = %s")
        parametros.append(id_admin)

    if not campos:
        print("Nenhum campo informado para atualização.")
        return

    parametros.append(id_aviso)
    query = f"UPDATE aviso SET {', '.join(campos)} WHERE id_aviso = %s"
    executar_queries(conexao, query, parametros=tuple(parametros))
    print(f"Aviso ID {id_aviso} atualizado.")

def deletar_aviso(conexao, id_aviso):
    """Remove um aviso pelo ID"""
    query = "DELETE FROM aviso WHERE id_aviso = %s"
    executar_queries(conexao, query, parametros=(id_aviso,))
    print(f"Aviso ID {id_aviso} deletado.")