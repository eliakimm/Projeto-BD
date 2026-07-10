from app.database.conexao import executar_queries, obter_resultados

def vincular_disciplina_curso(conexao, id_curso, id_disciplina):
    """Vincula uma disciplina a um curso (tabela associativa)"""
    query = "INSERT INTO curso_disciplina (id_curso, id_disciplina) VALUES (%s, %s)"
    parametros = (id_curso, id_disciplina)
    executar_queries(conexao, query, parametros)
    print("Disciplina vinculada ao curso com sucesso.")

def buscar_disciplinas_por_curso(conexao, id_curso):
    """Retorna todas as disciplinas de um curso específico"""
    query = """
        SELECT d.* FROM disciplina d
        JOIN curso_disciplina cd ON d.id_disciplina = cd.id_disciplina
        WHERE cd.id_curso = %s
    """
    return obter_resultados(conexao, query, (id_curso,))

def remover_vinculo_curso_disciplina(conexao, id_curso, id_disciplina):
    """Remove o vínculo entre curso e disciplina"""
    query = "DELETE FROM curso_disciplina WHERE id_curso = %s AND id_disciplina = %s"
    executar_queries(conexao, query, (id_curso, id_disciplina))