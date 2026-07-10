import sys
import os

# Adiciona o diretório raiz ao path para permitir imports do pacote app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database.conexao import conectar, encerrar
from app.database.crud import (
    usuario_crud, curso_crud, aluno_crud, admin_crud, 
    disciplina_crud, aviso_crud, agenda_crud, atividade_crud, 
    material_apoio_crud, forum_perguntas_crud, forum_respostas_crud,
    curso_disciplina_crud, novo_evento_crud
)

def executar_testes():
    conexao = conectar()
    if not conexao:
        print("Falha na conexão inicial.")
        return

    try:
        print("\n" + "="*40)
        print("   INICIANDO TESTE INTEGRADO DE CRUDS")
        print("="*40 + "\n")

        # 1. Usuários
        print("[TESTE] Criando usuários base...")
        usuario_crud.criar_usuario(conexao, "Estudante Teste", "aluno@test.com", "senha123")
        usuario_crud.criar_usuario(conexao, "Admin Teste", "admin@test.com", "admin123")
        
        id_aluno_user = usuario_crud.buscar_usuario_por_email(conexao, "aluno@test.com")[0][0]
        id_admin_user = usuario_crud.buscar_usuario_por_email(conexao, "admin@test.com")[0][0]

        # 2. Estrutura Acadêmica
        print("[TESTE] Criando Curso e Disciplina...")
        curso_crud.criar_curso(conexao, "Ciência da Computação", 3200, "Bacharelado", "Curso de TI")
        id_curso = curso_crud.buscar_curso(conexao, "Ciência da Computação")[0][0]
        
        disciplina_crud.criar_disciplina(conexao, "Algoritmos", id_curso, 80)
        id_disciplina = disciplina_crud.buscar_disciplinas_por_curso(conexao, id_curso)[0][0]

        # 3. Perfis e Vínculos
        print("[TESTE] Criando perfis e vínculos associativos...")
        aluno_crud.criar_aluno(conexao, id_aluno_user, id_curso, "20230001TESTE")
        admin_crud.criar_admin(conexao, id_admin_user, "Gestor Acadêmico")
        curso_disciplina_crud.vincular_disciplina_curso(conexao, id_curso, id_disciplina)

        # 4. Conteúdo Acadêmico
        print("[TESTE] Gerando avisos, agenda, atividades e materiais...")
        aviso_crud.criar_aviso(conexao, "Aula Cancelada", "Não haverá aula hoje", "2023-10-27", id_admin_user)
        agenda_crud.criar_evento_agenda(conexao, id_aluno_user, "Prova Final", "Matéria toda", "2023-12-15", "08:00")
        atividade_crud.criar_atividade(conexao, "Exercícios C", "Ponteiros", "2023-11-05", id_disciplina)
        material_apoio_crud.criar_material_apoio(conexao, "Slide 01", "Intro C", "http://github.com/aula", id_disciplina)

        id_agenda = agenda_crud.buscar_eventos_por_usuario(conexao, id_aluno_user)[0][0]
        id_atividade = atividade_crud.buscar_atividades_por_disciplina(conexao, id_disciplina)[0][0]
        novo_evento_crud.vincular_atividade_agenda(conexao, id_agenda, id_atividade)

        # 5. Fórum
        print("[TESTE] Interação no Fórum...")
        forum_perguntas_crud.criar_pergunta(conexao, "Dúvida Recursividade", "Como funciona?", "2023-10-27", id_aluno_user, id_disciplina)
        id_pergunta = forum_perguntas_crud.buscar_perguntas_por_usuario(conexao, id_aluno_user)[0][0]
        forum_respostas_crud.criar_resposta(conexao, "É uma função que chama ela mesma.", "2023-10-27", id_admin_user, id_pergunta)

        # 6. Atualizações (Update)
        print("[TESTE] Verificando atualizações...")
        usuario_crud.update_usuario(conexao, id_aluno_user, nome="Estudante Atualizado")
        curso_crud.update_curso(conexao, id_curso, total_horas=3400)
        
        avisos_atuais = aviso_crud.buscar_todos_avisos(conexao)
        if avisos_atuais:
            aviso_crud.update_aviso(conexao, avisos_atuais[-1][0], titulo="Aula Reagendada")

        # 7. Buscas (Read)
        print("[TESTE] Verificando buscas...")
        print(f" - Usuário por e-mail: {usuario_crud.buscar_usuario_por_email(conexao, 'aluno@test.com')[0][1]}")
        print(f" - Alunos no curso: {len(aluno_crud.buscar_alunos_por_curso(conexao, id_curso))}")
        print(f" - Disciplinas do curso: {len(curso_disciplina_crud.buscar_disciplinas_por_curso(conexao, id_curso))}")

        # 8. Limpeza (Delete) - Ordem cuidadosa para respeitar chaves estrangeiras
        print("\n" + "-"*40)
        print("   LIMPANDO DADOS DO TESTE")
        print("-"*40)

        # Deletar Respostas antes de Pergunta
        respostas = forum_respostas_crud.buscar_respostas_por_pergunta(conexao, id_pergunta)
        for r in respostas: forum_respostas_crud.deletar_resposta(conexao, r[0])
        forum_perguntas_crud.deletar_pergunta(conexao, id_pergunta)

        # Deletar associações e vínculos
        curso_disciplina_crud.remover_vinculo_curso_disciplina(conexao, id_curso, id_disciplina)
        
        # Deletar materiais e atividades
        materiais = material_apoio_crud.buscar_materiais_por_disciplina(conexao, id_disciplina)
        for m in materiais: material_apoio_crud.deletar_material_apoio(conexao, m[0])
        
        atividades = atividade_crud.buscar_atividades_por_disciplina(conexao, id_disciplina)
        for a in atividades: atividade_crud.deletar_atividade(conexao, a[0])

        # Agenda e Avisos
        agenda_ids = [e[0] for e in agenda_crud.buscar_eventos_por_usuario(conexao, id_aluno_user)]
        for aid in agenda_ids: agenda_crud.deletar_evento_agenda(conexao, aid)
        
        todos_avisos = aviso_crud.buscar_todos_avisos(conexao)
        for av in todos_avisos:
            if av[1] in ["Aula Cancelada", "Aula Reagendada"]:
                aviso_crud.deletar_aviso(conexao, av[0])

        # Perfis e Usuários (o padrão deletar_perfil já chama deletar_usuario)
        admin_crud.deletar_admin(conexao, id_admin_user)
        aluno_crud.deletar_aluno(conexao, id_aluno_user)

        # Disciplina e Curso por último
        disciplina_crud.deletar_disciplina(conexao, id_disciplina)
        curso_crud.deletar_curso(conexao, id_curso)

        print("\n" + "="*40)
        print("   TESTES FINALIZADOS COM SUCESSO!")
        print("="*40 + "\n")

    except Exception as e:
        print(f"\n[ERRO] Falha durante a execução dos testes: {e}")
        import traceback
        traceback.print_exc()
        conexao.rollback()
    finally:
        encerrar(conexao)

if __name__ == "__main__":
    executar_testes()