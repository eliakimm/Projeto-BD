import unittest
from unittest.mock import patch

from app.app import app as flask_app


class FluxoPerfilAgendaTests(unittest.TestCase):
    def setUp(self):
        flask_app.config["TESTING"] = True
        self.client = flask_app.test_client()

    def test_perfil_pode_ser_atualizado(self):
        with self.client.session_transaction() as sess:
            sess["usuario"] = {
                "id_user": 1,
                "nome": "Ana",
                "email": "ana@email.com",
                "perfil": "aluno",
                "identificacao": "20240001",
            }

        with patch("app.app.consultar", return_value={"id_user": 1, "nome": "Ana", "email": "ana@email.com", "matricula": "20240001"}), patch("app.app.executar", return_value=True):
            response = self.client.post(
                "/perfil",
                data={
                    "nome": "Ana Silva",
                    "email": "ana.nova@email.com",
                    "senha": "",
                    "confirmar_senha": "",
                    "matricula": "20240002",
                },
                follow_redirects=True,
            )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Perfil atualizado", response.get_data(as_text=True))

    def test_toggle_de_agenda_altera_status(self):
        with self.client.session_transaction() as sess:
            sess["usuario"] = {
                "id_user": 1,
                "nome": "Ana",
                "email": "ana@email.com",
                "perfil": "aluno",
                "identificacao": "20240001",
            }

        with patch("app.app.consultar", return_value={"id_agenda": 7, "id_user": 1, "concluida": False}), patch("app.app.executar", return_value=True):
            response = self.client.post("/agenda/toggle/7", follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Tarefa atualizada", response.get_data(as_text=True))

    def test_cadastro_utiliza_crud_de_usuario_e_aluno(self):
        with patch("app.app.buscar_usuario_login", return_value=None), patch("app.app.criar_usuario", return_value=True) as mock_criar_usuario, patch("app.app.criar_aluno", return_value=True) as mock_criar_aluno:
            response = self.client.post(
                "/cadastro",
                data={
                    "nome": "Ana",
                    "email": "ana@email.com",
                    "matricula": "20240003",
                    "id_curso": "1",
                    "senha": "123456",
                    "confirmar_senha": "123456",
                },
                follow_redirects=True,
            )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(mock_criar_usuario.called)
        self.assertTrue(mock_criar_aluno.called)

    def test_criar_tarefa_na_agenda(self):
        with self.client.session_transaction() as sess:
            sess["usuario"] = {
                "id_user": 1,
                "nome": "Ana",
                "email": "ana@email.com",
                "perfil": "aluno",
                "identificacao": "20240001",
            }

        with patch("app.app.consultar", return_value=[]), patch("app.app.executar", return_value=True):
            response = self.client.post(
                "/agenda",
                data={
                    "titulo": "Estudar para prova",
                    "descricao": "Revisar capítulo 3",
                    "data_entrega": "2026-07-10",
                },
                follow_redirects=True,
            )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Tarefa criada", response.get_data(as_text=True))

    def test_criacao_de_atividade_registra_novo_evento(self):
        with self.client.session_transaction() as sess:
            sess["usuario"] = {
                "id_user": 1,
                "nome": "Ana",
                "email": "ana@email.com",
                "perfil": "aluno",
                "identificacao": "20240001",
            }

        chamadas = []

        def fake_executar(sql, parametros=None, retornar=False):
            chamadas.append(sql)
            if "INSERT INTO agenda" in sql:
                return (7,)
            if "INSERT INTO atividade" in sql:
                return (5,)
            return True

        with patch("app.app.executar", side_effect=fake_executar):
            response = self.client.post(
                "/atividades",
                data={
                    "titulo": "Trabalho de BD",
                    "descricao": "Entregar relatório",
                    "data_entrega": "2026-07-12",
                    "id_disciplina": "1",
                },
                follow_redirects=True,
            )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(any("INSERT INTO novo_evento" in sql for sql in chamadas))

    def test_marcar_atividade_como_concluida(self):
        with self.client.session_transaction() as sess:
            sess["usuario"] = {
                "id_user": 1,
                "nome": "Ana",
                "email": "ana@email.com",
                "perfil": "aluno",
                "identificacao": "20240001",
            }

        with patch("app.app.consultar", return_value={"id_agenda": 7, "id_user": 1, "concluida": False}), patch("app.app.executar", return_value=True):
            response = self.client.post("/agenda/toggle/7", follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Tarefa atualizada", response.get_data(as_text=True))

    def test_resposta_no_foro_usa_o_texto_do_formulario(self):
        with self.client.session_transaction() as sess:
            sess["usuario"] = {
                "id_user": 1,
                "nome": "Ana",
                "email": "ana@email.com",
                "perfil": "aluno",
                "identificacao": "20240001",
            }

        parametros_salvos = None

        def fake_executar(sql, parametros=None, retornar=False):
            nonlocal parametros_salvos
            if "INSERT INTO forum_resposta" in sql:
                parametros_salvos = parametros
            return True

        with patch("app.app.consultar", return_value=[]), patch("app.app.executar", side_effect=fake_executar):
            response = self.client.post(
                "/forum",
                data={
                    "id_pergunta": "10",
                    "resposta_texto": "Texto da resposta",
                },
                follow_redirects=True,
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(parametros_salvos[2], "Texto da resposta")

    def test_template_do_foro_envia_formulario_para_rota_forum(self):
        with self.client.session_transaction() as sess:
            sess["usuario"] = {
                "id_user": 1,
                "nome": "Ana",
                "email": "ana@email.com",
                "perfil": "aluno",
                "identificacao": "20240001",
            }

        response = self.client.get("/disciplinas")

        self.assertEqual(response.status_code, 200)
        self.assertIn('action="/forum"', response.get_data(as_text=True))

    def test_forum_exibe_autor_da_resposta(self):
        with self.client.session_transaction() as sess:
            sess["usuario"] = {
                "id_user": 1,
                "nome": "Ana",
                "email": "ana@email.com",
                "perfil": "aluno",
                "identificacao": "20240001",
            }

        def fake_consultar(sql, parametros=None, unico=False):
            if "FROM forum_pergunta" in sql:
                return [{
                    "id_pergunta": 10,
                    "titulo": "Dúvida",
                    "texto": "Texto da pergunta",
                    "data_postagem": "01/01/2026",
                    "disciplina": "BD",
                    "respostas": 1,
                }]
            if "FROM forum_resposta" in sql:
                return [{
                    "id_resposta": 20,
                    "id_pergunta": 10,
                    "id_user": 2,
                    "texto": "Resposta útil",
                    "autor_nome": "Maria",
                }]
            if "COUNT(*)" in sql:
                return {"total": 0}
            if "FROM curso" in sql or "FROM disciplina" in sql or "FROM atividade" in sql or "FROM aviso" in sql or "FROM material_apoio" in sql:
                return []
            return []

        with patch("app.app.consultar", side_effect=fake_consultar):
            response = self.client.get("/forum")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Maria", response.get_data(as_text=True))
        self.assertIn("Resposta útil", response.get_data(as_text=True))

    def test_resposta_pode_ser_marcada_como_solucao(self):
        with self.client.session_transaction() as sess:
            sess["usuario"] = {
                "id_user": 1,
                "nome": "Ana",
                "email": "ana@email.com",
                "perfil": "aluno",
                "identificacao": "20240001",
            }

        executado = []

        def fake_executar(sql, parametros=None, retornar=False):
            executado.append((sql, parametros))
            return True

        with patch("app.app.consultar", return_value={"id_pergunta": 10, "id_user": 1}), patch("app.app.executar", side_effect=fake_executar):
            response = self.client.post("/forum/resposta/20/solucao", follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(any("UPDATE forum_resposta" in sql for sql, _ in executado))

    def test_forum_renderiza_com_perguntas_sem_erro_de_contexto(self):
        with self.client.session_transaction() as sess:
            sess["usuario"] = {
                "id_user": 1,
                "nome": "Ana",
                "email": "ana@email.com",
                "perfil": "aluno",
                "identificacao": "20240001",
            }

        def fake_consultar(sql, parametros=None, unico=False):
            if "COUNT(*)" in sql:
                return {"total": 0}
            if "FROM forum_pergunta" in sql:
                return [{
                    "id_pergunta": 10,
                    "titulo": "Dúvida",
                    "texto": "Texto da pergunta",
                    "data_postagem": "01/01/2026",
                    "disciplina": "BD",
                    "respostas": 0,
                }]
            if "FROM forum_resposta" in sql:
                return []
            if "FROM curso" in sql or "FROM disciplina" in sql or "FROM atividade" in sql or "FROM aviso" in sql or "FROM material_apoio" in sql:
                return []
            return []

        with patch("app.app.consultar", side_effect=fake_consultar):
            response = self.client.get("/forum")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Dúvida", response.get_data(as_text=True))

    def test_forum_filtra_perguntas_pela_busca(self):
        with self.client.session_transaction() as sess:
            sess["usuario"] = {
                "id_user": 1,
                "nome": "Ana",
                "email": "ana@email.com",
                "perfil": "aluno",
                "identificacao": "20240001",
            }

        def fake_consultar(sql, parametros=None, unico=False):
            if "COUNT(*)" in sql:
                return {"total": 0}
            if "FROM forum_pergunta" in sql:
                return [
                    {
                        "id_pergunta": 10,
                        "titulo": "Dúvida de banco",
                        "texto": "Como fazer um select?",
                        "data_postagem": "01/01/2026",
                        "disciplina": "BD",
                        "respostas": 0,
                    },
                    {
                        "id_pergunta": 11,
                        "titulo": "Dúvida de front",
                        "texto": "Como usar CSS?",
                        "data_postagem": "02/01/2026",
                        "disciplina": "Web",
                        "respostas": 0,
                    },
                ]
            if "FROM forum_resposta" in sql:
                return []
            if "FROM curso" in sql or "FROM disciplina" in sql or "FROM atividade" in sql or "FROM aviso" in sql or "FROM material_apoio" in sql:
                return []
            return []

        with patch("app.app.consultar", side_effect=fake_consultar):
            response = self.client.get("/forum?q=banco")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Dúvida de banco", response.get_data(as_text=True))
        self.assertNotIn("Dúvida de front", response.get_data(as_text=True))
