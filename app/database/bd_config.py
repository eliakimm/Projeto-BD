from functools import wraps
import os

from flask import flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from app.database.conexao import *


garantir_colunas_compatibilidade()


USUARIOS = {
    "admin@sisaa.com": {
        "nome": "Admin Demo",
        "senha": "admin123",
        "perfil": "admin",
        "identificacao": "Administrador",
    },
    "aluno@sisaa.com": {
        "nome": "Aluno Demo",
        "senha": "aluno123",
        "perfil": "aluno",
        "identificacao": "20240001",
    },
}


VAZIO = {
    "cursos": [],
    "disciplinas": [],
    "atividades": [],
    "avisos": [],
    "agenda": [],
    "materiais": [],
    "perguntas": [],
    "respostas_por_pergunta": {},
}


def _normalizar_lista(valor):
    if valor is None:
        return []
    if isinstance(valor, list):
        return valor
    if isinstance(valor, dict):
        return [valor]
    return []


def consultar(sql, parametros=None, unico=False):
    conexao = conectar()

    if not conexao:
        return None

    try:
        cursor = conexao.cursor()
        cursor.execute(sql, parametros or ())
        colunas = [coluna[0] for coluna in cursor.description]
        linhas = [dict(zip(colunas, linha)) for linha in cursor.fetchall()]
        cursor.close()
        return linhas[0] if unico and linhas else (None if unico else linhas)
    except Error as erro:
        print(f"Erro ao consultar banco: {erro}")
        return None
    finally:
        encerrar(conexao)


def executar(sql, parametros=None, retornar=False):
    conexao = conectar()

    if not conexao:
        return None

    try:
        cursor = conexao.cursor()
        cursor.execute(sql, parametros or ())
        resultado = cursor.fetchone() if retornar else True
        conexao.commit()
        cursor.close()
        return resultado
    except Error as erro:
        print(f"Erro ao executar comando no banco: {erro}")
        conexao.rollback()
        return None
    finally:
        encerrar(conexao)


def senha_valida(senha_digitada, senha_armazenada):
    if not senha_armazenada:
        return False

    if senha_armazenada.startswith("$2"):
        try:
            import bcrypt

            return bcrypt.checkpw(
                senha_digitada.encode("utf-8"),
                senha_armazenada.encode("utf-8"),
            )
        except ImportError:
            return False

    try:
        return check_password_hash(senha_armazenada, senha_digitada)
    except ValueError:
        return senha_digitada == senha_armazenada


def email_em_uso(email, id_user=None):
    if not email:
        return False

    if id_user is None:
        if email in USUARIOS:
            return True

        usuario = consultar(
            "SELECT id_user FROM usuario WHERE email = %s",
            (email,),
            unico=True,
        )
        return bool(usuario)

    usuario = consultar(
        "SELECT id_user FROM usuario WHERE email = %s AND id_user != %s",
        (email, id_user),
        unico=True,
    )

    if isinstance(usuario, dict):
        return usuario.get("id_user") != id_user

    return bool(usuario)


def remover_conta(id_user):
    if not id_user:
        return False

    conexao = conectar()
    if not conexao:
        return False

    try:
        with conexao.cursor() as cursor:
            cursor.execute("DELETE FROM forum_resposta WHERE id_user = %s", (id_user,))
            cursor.execute("DELETE FROM forum_pergunta WHERE id_user = %s", (id_user,))
            cursor.execute("DELETE FROM agenda WHERE id_user = %s", (id_user,))
            cursor.execute("DELETE FROM aluno WHERE id_user = %s", (id_user,))
            cursor.execute("DELETE FROM admin_sistema WHERE id_user = %s", (id_user,))
            cursor.execute("DELETE FROM usuario WHERE id_user = %s", (id_user,))
        conexao.commit()
        return True
    except Error as erro:
        print(f"Erro ao remover conta: {erro}")
        conexao.rollback()
        return False
    finally:
        encerrar(conexao)


def buscar_usuario_login(email):
    usuario = consultar(
        """
        SELECT
            u.id_user,
            u.nome,
            u.email,
            u.senha,
            CASE
                WHEN adm.id_user IS NOT NULL THEN 'admin'
                WHEN al.id_user IS NOT NULL THEN 'aluno'
                ELSE 'usuario'
            END AS perfil,
            COALESCE(adm.cargo, al.matricula, 'Usuario') AS identificacao
        FROM usuario u
        LEFT JOIN admin_sistema adm ON adm.id_user = u.id_user
        LEFT JOIN aluno al ON al.id_user = u.id_user
        WHERE u.email = %s AND u.ativo = true
        """,
        (email,),
        unico=True,
    )
    return usuario


def carregar_dados_banco(id_user=None):
    cursos = consultar(
        "SELECT id_curso, nome, descricao, total_horas, nivel FROM curso ORDER BY nome"
    )
    disciplinas = consultar(
        """
        SELECT
            d.id_disciplina,
            d.codigo,
            d.nome,
            d.descricao,
            d.carga_horaria,
            COALESCE(string_agg(c.nome, ', '), 'Sem curso') AS curso
        FROM disciplina d
        LEFT JOIN curso_disciplina cd ON cd.id_disciplina = d.id_disciplina
        LEFT JOIN curso c ON c.id_curso = cd.id_curso
        GROUP BY d.id_disciplina, d.codigo, d.nome, d.descricao, d.carga_horaria
        ORDER BY d.nome
        """
    )
    atividades = consultar(
        """
        SELECT
            a.id_atividade,
            ag.id_agenda,
            a.titulo,
            a.descricao,
            TO_CHAR(a.data_entrega, 'DD/MM/YYYY') AS data_entrega,
            COALESCE(d.nome, 'Sem disciplina') AS disciplina,
            CASE
                WHEN COALESCE(ag.concluida, false) THEN 'concluida'
                ELSE 'pendente'
            END AS status,
            COALESCE(ag.concluida, false) AS concluida
        FROM atividade a
        LEFT JOIN disciplina d ON d.id_disciplina = a.id_disciplina
        LEFT JOIN novo_evento ne ON ne.id_atividade = a.id_atividade
        LEFT JOIN agenda ag ON ag.id_agenda = ne.id_agenda
        ORDER BY a.data_entrega
        """
    )
    avisos = consultar(
        """
        SELECT
            id_aviso,
            titulo,
            texto,
            TO_CHAR(data_postagem, 'DD/MM/YYYY') AS data_postagem
        FROM aviso
        ORDER BY data_postagem DESC, id_aviso DESC
        """
    )
    materiais = consultar(
    """
    SELECT
        m.id_material,
        m.id_user,
        m.tipo,
        m.titulo,
        m.descricao,
        COALESCE(d.nome, 'Sem disciplina') AS disciplina
    FROM material_apoio m
    LEFT JOIN disciplina d
        ON d.id_disciplina = m.id_disciplina
    ORDER BY m.titulo
    """

    )
    perguntas = consultar(
        """
        SELECT *
        FROM vw_dashboard_forum
        ORDER BY data_postagem DESC
        """
    )
    respostas = consultar(
        """
        SELECT
            fr.id_resposta,
            fr.id_pergunta,
            fr.id_user,
            fr.texto,
            fr.solucao,
            u.nome AS autor_nome
        FROM forum_resposta fr
        LEFT JOIN usuario u ON u.id_user = fr.id_user
        ORDER BY fr.id_pergunta, fr.id_resposta
        """
    )

    respostas_por_pergunta = {}
    for resposta in _normalizar_lista(respostas):
        id_pergunta = resposta.get("id_pergunta")
        if id_pergunta is None:
            continue
        respostas_por_pergunta.setdefault(id_pergunta, []).append(resposta)

    agenda = consultar(
        """
        SELECT
            id_agenda,
            titulo,
            descricao,
            TO_CHAR(data_entrega, 'DD/MM/YYYY') AS data_entrega,
            COALESCE(concluida, false) AS concluida
        FROM agenda
        WHERE id_user = %s
        ORDER BY data_entrega
        """,
        (id_user,),
    ) if id_user else None

    if cursos is None:
        return None

    return {
        "cursos": _normalizar_lista(cursos),
        "disciplinas": _normalizar_lista(disciplinas),
        "atividades": _normalizar_lista(atividades),
        "avisos": _normalizar_lista(avisos),
        "agenda": _normalizar_lista(agenda),
        "materiais": _normalizar_lista(materiais),
        "perguntas": _normalizar_lista(perguntas),
        "respostas_por_pergunta": respostas_por_pergunta,
    }


def contexto_base():
    usuario = session.get("usuario", {})
    dados_banco = carregar_dados_banco(usuario.get("id_user"))
    usando_banco = dados_banco is not None
    total_usuarios = consultar("SELECT COUNT(*) AS total FROM usuario", unico=True) if usando_banco else None

    dados = dados_banco or VAZIO

    total_usuarios_valor = 0
    if isinstance(total_usuarios, dict):
        total_usuarios_valor = total_usuarios.get("total", 0)
    elif isinstance(total_usuarios, (int, float)):
        total_usuarios_valor = total_usuarios

    return {
        **dados,
        "total_disciplinas": len(dados["disciplinas"]),
        "total_atividades": len(dados["atividades"]),
        "total_avisos": len(dados["avisos"]),
        "total_materiais": len(dados["materiais"]),
        "total_cursos": len(dados["cursos"]),
        "total_usuarios": total_usuarios_valor,
        "usuario_logado": usuario,
        "usando_banco": usando_banco,
    }


def login_obrigatorio(perfil=None):
    def decorator(view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            usuario = session.get("usuario")

            if not usuario:
                flash("Faca login para acessar essa pagina.", "erro")
                return redirect(url_for("login"))

            if perfil and usuario.get("perfil") != perfil:
                flash("Voce nao tem permissao para acessar essa area.", "erro")
                if usuario.get("perfil") == "admin":
                    return redirect(url_for("admin_dashboard"))
                return redirect(url_for("aluno_dashboard"))

            return view(*args, **kwargs)

        return wrapper

    return decorator