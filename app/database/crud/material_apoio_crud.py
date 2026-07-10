from app.database.conexao import executar_queries, obter_resultados
import psycopg2 

def criar_material_apoio(
    conexao,
    titulo,
    descricao,
    tipo,
    id_disciplina,
    arquivo,
    id_user
):
    """
    Cria um novo material de apoio.
    """

    # Validação dos campos obrigatórios
    if not titulo or not tipo or not arquivo:
        print("Erro: título, tipo e arquivo são obrigatórios.")
        return False

    query = """
        INSERT INTO material_apoio
        (
            id_disciplina,
            id_user,
            tipo,
            titulo,
            descricao,
            arquivo
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    parametros = (
        id_disciplina,
        id_user,
        tipo,
        titulo,
        descricao,
        psycopg2.Binary(arquivo)
    )

    return executar_queries(conexao, query, parametros) is not None


def buscar_material_apoio_por_id(conexao, id_material):
    """
    Busca um material pelo ID.
    """

    query = """
        SELECT *
        FROM material_apoio
        WHERE id_material = %s
    """

    resultado = obter_resultados(conexao, query, (id_material,))

    if resultado:
        return resultado[0]

    return None


def buscar_materiais_por_disciplina(conexao, id_disciplina):
    """
    Busca todos os materiais de uma disciplina.
    """

    query = """
        SELECT *
        FROM material_apoio
        WHERE id_disciplina = %s
    """

    return obter_resultados(conexao, query, (id_disciplina,))


def listar_materiais(conexao):
    """
    Lista todos os materiais cadastrados.
    """

    query = """
        SELECT *
        FROM material_apoio
        ORDER BY id_material DESC
    """

    return obter_resultados(conexao, query)


def update_material_apoio(
    conexao,
    id_material,
    titulo=None,
    descricao=None,
    tipo=None,
    id_disciplina=None,
    arquivo=None,
):
    """
    Atualiza um material de apoio.
    """

    campos = []
    parametros = []

    if titulo:
        campos.append("titulo = %s")
        parametros.append(titulo)

    if descricao:
        campos.append("descricao = %s")
        parametros.append(descricao)

    if tipo:
        campos.append("tipo = %s")
        parametros.append(tipo)

    if id_disciplina:
        campos.append("id_disciplina = %s")
        parametros.append(id_disciplina)

    if arquivo:
        campos.append("arquivo = %s")
        parametros.append(arquivo)

    if not campos:
        return False

    parametros.append(id_material)

    query = f"""
        UPDATE material_apoio
        SET {', '.join(campos)}
        WHERE id_material = %s
    """

    cursor = executar_queries(conexao, query, tuple(parametros))

    return cursor is not None


def deletar_material_apoio(conexao, id_material):
    """
    Remove um material de apoio.
    """

    query = """
        DELETE FROM material_apoio
        WHERE id_material = %s
    """

    cursor = executar_queries(conexao, query, (id_material,))

    return cursor is not None