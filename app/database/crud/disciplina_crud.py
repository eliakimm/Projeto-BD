from app.database.conexao import executar_queries, obter_resultados

def criar_disciplina(conexao, nome, id_curso, carga_horaria):
    """Cria uma nova disciplina usando o esquema atual do projeto."""
    query = "INSERT INTO disciplina (codigo, nome, descricao, carga_horaria) VALUES (%s, %s, %s, %s)"
    parametros = (nome.upper()[:10], nome, None, carga_horaria)
    cursor = executar_queries(conexao, query, parametros)
    print(f"Disciplina '{nome}' criada com sucesso!")
    return cursor is not None

def buscar_disciplina_por_id(conexao, id_disciplina):
    """Busca disciplina pelo seu ID"""
    query = "SELECT * FROM disciplina WHERE id_disciplina = %s"
    resultado = obter_resultados(conexao, query, (id_disciplina,))
    return resultado

def buscar_disciplinas_por_curso(conexao, id_curso):
    """Busca todas as disciplinas de um curso específico"""
    query = "SELECT * FROM disciplina WHERE id_curso = %s"
    resultado = obter_resultados(conexao, query, (id_curso,))
    return resultado

def update_disciplina(conexao, id_disciplina, nome=None, id_curso=None, carga_horaria=None):
    """Atualiza campos específicos de uma disciplina de forma dinâmica"""
    campos = []
    parametros = []

    if nome:
        campos.append("nome = %s")
        parametros.append(nome)
    
    if id_curso:
        campos.append("id_curso = %s")
        parametros.append(id_curso)
    
    if carga_horaria:
        campos.append("carga_horaria = %s")
        parametros.append(carga_horaria)

    if not campos:
        print("Nenhum campo informado para atualização.")
        return

    parametros.append(id_disciplina)
    query = f"UPDATE disciplina SET {', '.join(campos)} WHERE id_disciplina = %s"
    executar_queries(conexao, query, parametros=tuple(parametros))
    print(f"Disciplina ID {id_disciplina} atualizada.")

def deletar_disciplina(conexao, id_disciplina):
    """Remove uma disciplina pelo ID"""
    query = "DELETE FROM disciplina WHERE id_disciplina = %s"
    executar_queries(conexao, query, parametros=(id_disciplina,))
    print(f"Disciplina ID {id_disciplina} deletada.")