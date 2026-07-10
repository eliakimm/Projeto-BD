from app.database.conexao import executar_queries, obter_resultados


def criar_evento_agenda(conexao, id_user, titulo, descricao, data_entrega, hora_evento=None):
    """Cria um novo evento na agenda de um usuário usando o esquema atual do projeto."""
    query = "INSERT INTO agenda (id_user, titulo, descricao, data_entrega, concluida) VALUES (%s, %s, %s, %s, false)"
    parametros = (id_user, titulo, descricao, data_entrega)
    cursor = executar_queries(conexao, query, parametros)
    print(f"Evento '{titulo}' criado na agenda do usuário {id_user} com sucesso!")
    return cursor is not None

def buscar_evento_por_id(conexao, id_agenda):
    """Busca evento da agenda pelo ID"""
    query = "SELECT * FROM agenda WHERE id_agenda = %s"
    resultado = obter_resultados(conexao, query, (id_agenda,))
    return resultado

def buscar_eventos_por_usuario(conexao, id_user):
    """Busca todos os eventos da agenda de um usuário"""
    query = "SELECT * FROM agenda WHERE id_user = %s"
    resultado = obter_resultados(conexao, query, (id_user,))
    return resultado

def update_evento_agenda(conexao, id_agenda, id_user=None, titulo=None, descricao=None, data_evento=None, hora_evento=None):
    """Atualiza campos específicos de um evento da agenda"""
    campos = []
    parametros = []

    if id_user:
        campos.append("id_user = %s")
        parametros.append(id_user)
    if titulo:
        campos.append("titulo = %s")
        parametros.append(titulo)
    if descricao:
        campos.append("descricao = %s")
        parametros.append(descricao)
    if data_evento:
        campos.append("data_evento = %s")
        parametros.append(data_evento)
    if hora_evento:
        campos.append("hora_evento = %s")
        parametros.append(hora_evento)

    if not campos:
        print("Nenhum campo informado para atualização.")
        return

    parametros.append(id_agenda)
    query = f"UPDATE agenda SET {', '.join(campos)} WHERE id_agenda = %s"
    executar_queries(conexao, query, parametros=tuple(parametros))
    print(f"Evento de agenda ID {id_agenda} atualizado.")

def deletar_evento_agenda(conexao, id_agenda):
    """Remove um evento da agenda pelo ID"""
    query = "DELETE FROM agenda WHERE id_agenda = %s"
    executar_queries(conexao, query, parametros=(id_agenda,))
    print(f"Evento de agenda ID {id_agenda} deletado.")