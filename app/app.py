from app.database.bd_config import *
from app.database.crud.agenda_crud import criar_evento_agenda
from app.database.crud.aluno_crud import criar_aluno
from app.database.crud.forum_perguntas_crud import criar_pergunta as crud_criar_pergunta
from app.database.crud.forum_respostas_crud import criar_resposta as crud_criar_resposta
from app.database.crud.material_apoio_crud import criar_material_apoio
from app.database.crud.usuario_crud import criar_usuario, update_usuario
from app.database.crud.curso_crud import deletar_curso
from app.database.crud.material_apoio_crud import deletar_material_apoio
from app.database.crud.disciplina_crud import deletar_disciplina

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "sisaa-dev-secret")


@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        usuario = buscar_usuario_login(email)

        if usuario and senha_valida(senha, usuario["senha"]):
            session["usuario"] = {
                "id_user": usuario["id_user"],
                "nome": usuario["nome"],
                "email": usuario["email"],
                "perfil": usuario["perfil"],
                "identificacao": usuario["identificacao"],
            }

            if usuario["perfil"] == "admin":
                return redirect(url_for("admin_dashboard"))

            return redirect(url_for("aluno_dashboard"))

        usuario_demo = USUARIOS.get(email)

        if not usuario_demo or usuario_demo["senha"] != senha:
            flash("Email ou senha invalidos.", "erro")
            return render_template("login.html"), 401

        session["usuario"] = {
            "id_user": None,
            "nome": usuario_demo["nome"],
            "email": email,
            "perfil": usuario_demo["perfil"],
            "identificacao": usuario_demo["identificacao"],
        }

        if usuario_demo["perfil"] == "admin":
            return redirect(url_for("admin_dashboard"))

        return redirect(url_for("aluno_dashboard"))

    return render_template("login.html")


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    cursos = contexto_base()["cursos"]

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        matricula = request.form.get("matricula", "").strip()
        id_curso = request.form.get("id_curso")
        senha = request.form.get("senha", "")
        confirmar_senha = request.form.get("confirmar_senha", "")

        if not nome or not email or not matricula or not id_curso or not senha:
            flash("Preencha todos os campos obrigatorios.", "erro")
            return render_template("cadastro.html", cursos=cursos), 400

        if senha != confirmar_senha:
            flash("As senhas nao conferem.", "erro")
            return render_template("cadastro.html", cursos=cursos), 400

        if buscar_usuario_login(email) or email in USUARIOS:
            flash("Ja existe um usuario cadastrado com esse email.", "erro")
            return render_template("cadastro.html", cursos=cursos), 409

        conexao = conectar()
        if not conexao:
            flash("Nao foi possivel cadastrar no banco. Verifique a conexao.", "erro")
            return render_template("cadastro.html", cursos=cursos), 500

        try:
            resultado_usuario = criar_usuario(conexao, nome, email, senha)
            if not resultado_usuario:
                flash("Nao foi possivel criar o usuario. Verifique os dados.", "erro")
                return render_template("cadastro.html", cursos=cursos), 500

            id_user = resultado_usuario if isinstance(resultado_usuario, int) else None
            if id_user is None:
                usuario_cadastrado = consultar(
                    "SELECT id_user FROM usuario WHERE email = %s",
                    (email,),
                    unico=True,
                )
                if isinstance(usuario_cadastrado, dict):
                    id_user = usuario_cadastrado.get("id_user")

            aluno_criado = True
            if id_user is not None:
                aluno_criado = criar_aluno(conexao, id_user, id_curso, matricula)

            if not aluno_criado and id_user is not None:
                executar("DELETE FROM usuario WHERE id_user = %s", (id_user,))
                flash("Nao foi possivel criar o aluno. Verifique curso e matricula.", "erro")
                return render_template("cadastro.html", cursos=cursos), 500
        finally:
            encerrar(conexao)

        USUARIOS[email] = {
            "nome": nome,
            "senha": senha,
            "perfil": "aluno",
            "identificacao": matricula,
        }
        session["usuario"] = {
            "id_user": id_user if isinstance(id_user, int) else id_user[0] if isinstance(id_user, tuple) else None,
            "nome": nome,
            "email": email,
            "perfil": "aluno",
            "identificacao": matricula,
        }

        return redirect(url_for("aluno_dashboard"))

    return render_template("cadastro.html", cursos=cursos)


@app.route("/admin", methods=["GET", "POST"])
@login_obrigatorio("admin")
def admin_dashboard():
    if request.method == "POST":
        acao = request.form.get("acao")

        if acao == "curso":
            criado = executar(
                """
                INSERT INTO curso (nome, descricao, total_horas, nivel)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    request.form.get("nome"),
                    request.form.get("descricao"),
                    request.form.get("total_horas"),
                    request.form.get("nivel"),
                ),
            )
            flash("Curso cadastrado com sucesso." if criado else "Nao foi possivel cadastrar o curso.", "sucesso" if criado else "erro")

        elif acao == "disciplina":
            conexao = conectar()
            id_disciplina = None
            if conexao:
                try:
                    from app.database.crud.disciplina_crud import criar_disciplina

                    criado = criar_disciplina(
                        conexao,
                        request.form.get("nome"),
                        request.form.get("id_curso"),
                        request.form.get("carga_horaria"),
                    )
                    if criado:
                        disciplina_criada = consultar(
                            "SELECT id_disciplina FROM disciplina WHERE nome = %s",
                            (request.form.get("nome"),),
                            unico=True,
                        )
                        if isinstance(disciplina_criada, dict):
                            id_disciplina = disciplina_criada.get("id_disciplina")
                finally:
                    encerrar(conexao)

            if id_disciplina:
                executar(
                    "INSERT INTO curso_disciplina (id_curso, id_disciplina) VALUES (%s, %s)",
                    (request.form.get("id_curso"), id_disciplina),
                )
                flash("Disciplina cadastrada com sucesso.", "sucesso")
            else:
                flash("Nao foi possivel cadastrar a disciplina.", "erro")

        elif acao == "aviso":
            conexao = conectar()
            criado = False
            if conexao:
                try:
                    from app.database.crud.aviso_crud import criar_aviso

                    criado = criar_aviso(
                        conexao,
                        session["usuario"].get("id_user"),
                        request.form.get("titulo"),
                        request.form.get("texto"),
                    )
                finally:
                    encerrar(conexao)
            flash("Aviso publicado com sucesso." if criado else "Nao foi possivel publicar o aviso.", "sucesso" if criado else "erro")

        return redirect(url_for("admin_dashboard"))

    return render_template("admin_dashboard.html", active_page="admin", perfil="admin", **contexto_base())


@app.route("/cursos/deletar/<int:id_curso>", methods=["POST"])
@login_obrigatorio("admin")
def excluir_curso(id_curso):
    conexao = conectar()

    if not conexao:
        flash("Erro ao conectar ao banco de dados.", "erro")
        return redirect(url_for("admin_dashboard"))

    try:
        sucesso = deletar_curso(conexao, id_curso)

        if sucesso:
            flash("Curso excluído com sucesso!", "sucesso")
        else:
            flash(
                "Não foi possível excluir o curso.",
                "erro"
            )

    except psycopg2.errors.ForeignKeyViolation:
        conexao.rollback()
        flash(
            "Não é possível excluir este curso, pois existem alunos ou disciplinas vinculados a ele.",
            "erro"
        )

    finally:
        encerrar(conexao)

    return redirect(url_for("cursos"))

@app.route("/aluno")
@login_obrigatorio("aluno")
def aluno_dashboard():
    return render_template("aluno_dashboard.html", active_page="aluno", perfil="aluno", **contexto_base())


@app.route("/dashboard")
@login_obrigatorio()
def dashboard():
    return redirect(url_for("aluno_dashboard"))


@app.route("/perfil", methods=["GET", "POST"])
@login_obrigatorio()
def perfil():
    usuario = session.get("usuario", {})

    if request.method == "POST":
        acao = request.form.get("acao", "atualizar")

        if acao == "deletar":
            if remover_conta(usuario.get("id_user")):
                session.clear()
                flash("Conta removida com sucesso.", "sucesso")
                return redirect(url_for("login"))

            flash("Nao foi possivel remover sua conta no momento.", "erro")
            return redirect(url_for("perfil"))

        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        confirmar_senha = request.form.get("confirmar_senha", "")
        matricula = request.form.get("matricula", "").strip()

        dados_form = {"nome": nome, "email": email, "matricula": matricula}

        if not nome or not email:
            flash("Nome e e-mail sao obrigatorios.", "erro")
            return render_template("perfil.html", active_page="perfil", perfil=usuario.get("perfil"), dados=dados_form, **contexto_base())

        if senha and senha != confirmar_senha:
            flash("As senhas nao conferem.", "erro")
            return render_template("perfil.html", active_page="perfil", perfil=usuario.get("perfil"), dados=dados_form, **contexto_base())

        if email_em_uso(email, usuario.get("id_user")):
            flash("Ja existe um usuario cadastrado com esse e-mail.", "erro")
            return render_template("perfil.html", active_page="perfil", perfil=usuario.get("perfil"), dados=dados_form, **contexto_base())

        conexao = conectar()
        atualizado = False

        if conexao:
            try:
                atualizado = update_usuario(conexao, usuario.get("id_user"), nome=nome, email=email, senha=senha or None)
            finally:
                encerrar(conexao)

        if not atualizado and usuario.get("id_user") is not None:
            flash("Nao foi possivel atualizar o perfil.", "erro")
            return render_template("perfil.html", active_page="perfil", perfil=usuario.get("perfil"), **contexto_base())

        if usuario.get("perfil") == "aluno" and usuario.get("id_user") is not None:
            conexao = conectar()
            if conexao:
                try:
                    executar(
                        "UPDATE aluno SET matricula = %s WHERE id_user = %s",
                        (matricula or None, usuario.get("id_user")),
                    )
                finally:
                    encerrar(conexao)

        session["usuario"]["nome"] = nome
        session["usuario"]["email"] = email
        session["usuario"]["identificacao"] = matricula or session["usuario"].get("identificacao")

        if usuario.get("email") in USUARIOS:
            USUARIOS[email] = {
                "nome": nome,
                "senha": USUARIOS[usuario.get("email")].get("senha"),
                "perfil": usuario.get("perfil"),
                "identificacao": matricula or session["usuario"].get("identificacao"),
            }

        flash("Perfil atualizado com sucesso.", "sucesso")
        return redirect(url_for("perfil"))

    dados = None
    if usuario.get("id_user") is not None:
        dados = consultar(
            """
            SELECT
                u.nome,
                u.email,
                COALESCE(a.matricula, '') AS matricula
            FROM usuario u
            LEFT JOIN aluno a ON a.id_user = u.id_user
            WHERE u.id_user = %s
            """,
            (usuario.get("id_user"),),
            unico=True,
        )

    return render_template(
        "perfil.html",
        active_page="perfil",
        perfil=usuario.get("perfil"),
        dados=dados or {"nome": usuario.get("nome"), "email": usuario.get("email"), "matricula": usuario.get("identificacao")},
        **contexto_base(),
    )


@app.route("/agenda/toggle/<int:id_agenda>", methods=["POST"])
@login_obrigatorio("aluno")
def toggle_agenda(id_agenda):
    usuario = session.get("usuario", {})
    tarefa = consultar(
        "SELECT id_agenda, concluida FROM agenda WHERE id_agenda = %s AND id_user = %s",
        (id_agenda, usuario.get("id_user")),
        unico=True,
    )

    if not tarefa:
        flash("Tarefa nao encontrada.", "erro")
        return redirect(url_for("agenda"))

    novo_status = not bool(tarefa.get("concluida"))
    atualizado = executar(
        "UPDATE agenda SET concluida = %s WHERE id_agenda = %s AND id_user = %s",
        (novo_status, id_agenda, usuario.get("id_user")),
    )

    if atualizado:
        flash("Tarefa atualizada com sucesso.", "sucesso")
    else:
        flash("Nao foi possivel atualizar a tarefa.", "erro")

    return redirect(url_for("agenda"))


@app.route("/atividades/toggle/<int:id_agenda>", methods=["POST"])
@login_obrigatorio("aluno")
def toggle_atividade(id_agenda):
    usuario = session.get("usuario", {})
    tarefa = consultar(
        "SELECT id_agenda, concluida FROM agenda WHERE id_agenda = %s AND id_user = %s",
        (id_agenda, usuario.get("id_user")),
        unico=True,
    )

    if not tarefa:
        flash("Atividade nao encontrada.", "erro")
        return redirect(url_for("atividades"))

    novo_status = not bool(tarefa.get("concluida"))
    atualizado = executar(
        "UPDATE agenda SET concluida = %s WHERE id_agenda = %s AND id_user = %s",
        (novo_status, id_agenda, usuario.get("id_user")),
    )

    if atualizado:
        flash("Atividade atualizada com sucesso.", "sucesso")
    else:
        flash("Nao foi possivel atualizar a atividade.", "erro")

    return redirect(url_for("atividades"))


@app.route("/logout")
def logout():
    session.clear()
    flash("Voce saiu do sistema.", "sucesso")
    return redirect(url_for("login"))


@app.route("/cursos")
@login_obrigatorio()
def cursos():
    return render_template("cursos.html", active_page="cursos", **contexto_base())


@app.route("/disciplinas")
@app.route("/disciplinas-forum")
@login_obrigatorio()
def disciplinas():
    return render_template("disciplinas_forum.html", active_page="disciplinas_forum", **contexto_base())


@app.route("/agenda", methods=["GET", "POST"])
@login_obrigatorio("aluno")
def agenda():
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descricao = request.form.get("descricao", "").strip()
        data_entrega = request.form.get("data_entrega", "").strip()

        if not titulo or not data_entrega:
            flash("Titulo e data de entrega sao obrigatorios.", "erro")
            return render_template("agenda.html", active_page="agenda", **contexto_base())

        conexao = conectar()
        criado = False

        if conexao:
            try:
                criado = criar_evento_agenda(
                    conexao,
                    session["usuario"].get("id_user"),
                    titulo,
                    descricao or None,
                    data_entrega,
                    None,
                )
            finally:
                encerrar(conexao)

        if criado:
            flash("Tarefa criada com sucesso.", "sucesso")
        else:
            flash("Nao foi possivel criar a tarefa.", "erro")

        return redirect(url_for("agenda"))

    return render_template("agenda.html", active_page="agenda", **contexto_base())


@app.route("/atividades", methods=["GET", "POST"])
@login_obrigatorio("aluno")
def atividades():
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descricao = request.form.get("descricao", "").strip()
        data_entrega = request.form.get("data_entrega", "").strip()
        id_disciplina = request.form.get("id_disciplina", "").strip()

        if not titulo or not data_entrega:
            flash("Titulo e data de entrega sao obrigatorios.", "erro")
            return render_template("atividades.html", active_page="atividades", **contexto_base())

        atividade_criada = executar(
            """
            INSERT INTO atividade (id_disciplina, titulo, descricao, data_entrega)
            VALUES (%s, %s, %s, %s)
            RETURNING id_atividade
            """,
            (id_disciplina or None, titulo, descricao or None, data_entrega),
            retornar=True,
        )

        agenda_criada = executar(
            """
            INSERT INTO agenda (id_user, titulo, descricao, data_entrega, concluida)
            VALUES (%s, %s, %s, %s, false)
            RETURNING id_agenda
            """,
            (
                session["usuario"].get("id_user"),
                titulo,
                descricao or None,
                data_entrega,
            ),
            retornar=True,
        )

        evento_criado = False
        if atividade_criada and agenda_criada:
            evento_criado = executar(
                """
                INSERT INTO novo_evento (id_agenda, id_atividade)
                VALUES (%s, %s)
                """,
                (agenda_criada[0], atividade_criada[0]),
            )

        if atividade_criada and agenda_criada and evento_criado:
            flash("Atividade cadastrada com sucesso.", "sucesso")
        else:
            flash("Nao foi possivel cadastrar a atividade.", "erro")

        return redirect(url_for("atividades"))

    return render_template("atividades.html", active_page="atividades", **contexto_base())


@app.route("/avisos")
@login_obrigatorio()
def avisos():
    return render_template("avisos.html", active_page="avisos", **contexto_base())


@app.route("/materiais", methods=["GET", "POST"])
@login_obrigatorio()
def materiais():

    if request.method == "POST":

        titulo = request.form.get("titulo", "").strip()
        descricao = request.form.get("descricao", "").strip()
        tipo = request.form.get("tipo", "").strip()
        id_disciplina = request.form.get("id_disciplina") or None
        id_user = session["usuario"]["id_user"]

        arquivo = request.files.get("arquivo")

        # Validação dos campos obrigatórios
        if not titulo or not tipo:
            flash("Título e tipo do material são obrigatórios.", "erro")
            return redirect(url_for("materiais"))

        if arquivo is None or arquivo.filename == "":
            flash("Selecione um arquivo PDF.", "erro")
            return redirect(url_for("materiais"))

        # Aceita apenas PDF
        if arquivo.mimetype != "application/pdf":
            flash("Apenas arquivos PDF são permitidos.", "erro")
            return redirect(url_for("materiais"))

        # Lê o conteúdo do arquivo
        dados_arquivo = arquivo.read()

        conexao = conectar()
        criado = False

        if conexao:
            try:
                criado = criar_material_apoio(
                    conexao,
                    titulo,
                    descricao or None,
                    tipo,
                    id_disciplina,
                    dados_arquivo,
                    id_user
                )
            finally:
                encerrar(conexao)

        if criado:
            flash("Material compartilhado com sucesso.", "sucesso")
        else:
            flash("Não foi possível compartilhar o material.", "erro")

        return redirect(url_for("materiais"))

    return render_template(
        "materiais.html",
        active_page="materiais",
        **contexto_base()
    )

from flask import send_file
from io import BytesIO

@app.route("/materiais/<int:id_material>/download")
@login_obrigatorio()
def baixar_material(id_material):
    conexao = conectar()

    try:
        material = consultar(
            """
            SELECT
                titulo,
                arquivo
            FROM material_apoio
            WHERE id_material = %s
            """,
            (id_material,),
            unico=True
        )
    finally:
        encerrar(conexao)

    if not material:
        flash("Material não encontrado.", "erro")
        return redirect(url_for("materiais"))

    return send_file(
        BytesIO(material["arquivo"]),
        mimetype="application/pdf",
        download_name=f"{material['titulo']}.pdf",
        as_attachment=True
    )

@app.route("/materiais/excluir/<int:id_material>", methods=["POST"])
@login_obrigatorio()
def excluir_material(id_material):

    material = consultar(
        """
        SELECT id_user
        FROM material_apoio
        WHERE id_material = %s
        """,
        (id_material,),
        unico=True
    )

    if not material:
        flash("Material não encontrado.", "erro")
        return redirect(url_for("materiais"))

    if material["id_user"] != session["usuario"]["id_user"]:
        flash("Você não tem permissão para excluir este material.", "erro")
        return redirect(url_for("materiais"))

    conexao = conectar()

    try:
        deletar_material_apoio(conexao, id_material)
    finally:
        encerrar(conexao)

    flash("Material excluído com sucesso.", "sucesso")
    return redirect(url_for("materiais"))

@app.route(
    "/disciplinas/excluir/<int:id_disciplina>",
    methods=["POST"]
)
@login_obrigatorio("admin")
def excluir_disciplina(id_disciplina):

    conexao = conectar()

    if not conexao:
        flash(
            "Erro ao conectar ao banco.",
            "erro"
        )
        return redirect(url_for("disciplinas"))


    try:

        sucesso = deletar_disciplina(
            conexao,
            id_disciplina
        )


        if sucesso:
            flash(
                "Disciplina excluída com sucesso!",
                "sucesso"
            )

        else:
            flash(
                "Não foi possível excluir a disciplina.",
                "erro"
            )


    except psycopg2.errors.ForeignKeyViolation:

        conexao.rollback()

        flash(
            "Não é possível excluir esta disciplina, pois ela possui vínculos com cursos ou atividades.",
            "erro"
        )


    finally:

        encerrar(conexao)


    return redirect(url_for("disciplinas"))

@app.route("/forum/pergunta/<int:id_pergunta>/editar", methods=["POST"])
@login_obrigatorio()
def editar_pergunta(id_pergunta):
    titulo = request.form.get("titulo", "").strip()
    texto = request.form.get("texto", "").strip()

    if not titulo or not texto:
        flash("Titulo e mensagem sao obrigatorios.", "erro")
        return redirect(url_for("forum"))

    pergunta = consultar(
        "SELECT id_user FROM forum_pergunta WHERE id_pergunta = %s",
        (id_pergunta,),
        unico=True,
    )

    if not pergunta:
        flash("Pergunta nao encontrada.", "erro")
        return redirect(url_for("forum"))

    if pergunta.get("id_user") != session.get("usuario", {}).get("id_user"):
        flash("Apenas o autor da pergunta pode editar esta pergunta.", "erro")
        return redirect(url_for("forum"))

    executado = executar(
        "UPDATE forum_pergunta SET titulo = %s, texto = %s WHERE id_pergunta = %s",
        (titulo, texto, id_pergunta),
    )

    if executado:
        flash("Pergunta atualizada com sucesso.", "sucesso")
    else:
        flash("Nao foi possivel atualizar a pergunta.", "erro")

    return redirect(url_for("forum"))


@app.route("/forum/pergunta/<int:id_pergunta>/excluir", methods=["POST"])
@login_obrigatorio()
def excluir_pergunta(id_pergunta):
    pergunta = consultar(
        "SELECT id_user FROM forum_pergunta WHERE id_pergunta = %s",
        (id_pergunta,),
        unico=True,
    )

    if not pergunta:
        flash("Pergunta nao encontrada.", "erro")
        return redirect(url_for("forum"))

    if pergunta.get("id_user") != session.get("usuario", {}).get("id_user"):
        flash("Apenas o autor da pergunta pode excluir esta pergunta.", "erro")
        return redirect(url_for("forum"))

    executado = executar(
        "DELETE FROM forum_resposta WHERE id_pergunta = %s",
        (id_pergunta,),
    )
    executado = executar("DELETE FROM forum_pergunta WHERE id_pergunta = %s", (id_pergunta,))

    if executado:
        flash("Pergunta excluida com sucesso.", "sucesso")
    else:
        flash("Nao foi possivel excluir a pergunta.", "erro")

    return redirect(url_for("forum"))


@app.route("/forum/resposta/<int:id_resposta>/editar", methods=["POST"])
@login_obrigatorio()
def editar_resposta(id_resposta):
    texto = request.form.get("texto", "").strip()

    if not texto:
        flash("A resposta nao pode ficar vazia.", "erro")
        return redirect(url_for("forum"))

    resposta = consultar(
        "SELECT id_user FROM forum_resposta WHERE id_resposta = %s",
        (id_resposta,),
        unico=True,
    )

    if not resposta:
        flash("Resposta nao encontrada.", "erro")
        return redirect(url_for("forum"))

    if resposta.get("id_user") != session.get("usuario", {}).get("id_user"):
        flash("Apenas o autor da resposta pode editar esta resposta.", "erro")
        return redirect(url_for("forum"))

    executado = executar("UPDATE forum_resposta SET texto = %s WHERE id_resposta = %s", (texto, id_resposta))

    if executado:
        flash("Resposta atualizada com sucesso.", "sucesso")
    else:
        flash("Nao foi possivel atualizar a resposta.", "erro")

    return redirect(url_for("forum"))


@app.route("/forum/resposta/<int:id_resposta>/excluir", methods=["POST"])
@login_obrigatorio()
def excluir_resposta(id_resposta):
    resposta = consultar(
        "SELECT id_user FROM forum_resposta WHERE id_resposta = %s",
        (id_resposta,),
        unico=True,
    )

    if not resposta:
        flash("Resposta nao encontrada.", "erro")
        return redirect(url_for("forum"))

    if resposta.get("id_user") != session.get("usuario", {}).get("id_user"):
        flash("Apenas o autor da resposta pode excluir esta resposta.", "erro")
        return redirect(url_for("forum"))

    executado = executar("DELETE FROM forum_resposta WHERE id_resposta = %s", (id_resposta,))

    if executado:
        flash("Resposta excluida com sucesso.", "sucesso")
    else:
        flash("Nao foi possivel excluir a resposta.", "erro")

    return redirect(url_for("forum"))


@app.route("/forum/resposta/<int:id_resposta>/solucao", methods=["POST"])
@login_obrigatorio()
def marcar_resposta_solucao(id_resposta):
    pergunta = consultar(
        """
        SELECT fp.id_pergunta, fp.id_user
        FROM forum_resposta fr
        JOIN forum_pergunta fp ON fp.id_pergunta = fr.id_pergunta
        WHERE fr.id_resposta = %s
        """,
        (id_resposta,),
        unico=True,
    )

    if not pergunta:
        flash("Resposta nao encontrada.", "erro")
        return redirect(url_for("forum"))

    usuario_logado = session.get("usuario", {}).get("id_user")
    if pergunta.get("id_user") != usuario_logado:
        flash("Apenas o autor da pergunta pode marcar uma resposta como solução.", "erro")
        return redirect(url_for("forum"))

    executado = executar(
        """
        UPDATE forum_resposta
        SET solucao = CASE WHEN id_resposta = %s THEN true ELSE false END
        WHERE id_pergunta = %s
        """,
        (id_resposta, pergunta.get("id_pergunta")),
    )

    if executado:
        flash("Resposta marcada como solução.", "sucesso")
    else:
        flash("Nao foi possivel marcar a resposta.", "erro")

    return redirect(url_for("forum"))


@app.route("/forum", methods=["GET", "POST"])
@login_obrigatorio()
def forum():
    termo_busca = request.args.get("q", "").strip().lower()

    if request.method == "POST":
        if "id_pergunta" in request.form and "resposta_texto" in request.form:
            id_pergunta = request.form.get("id_pergunta", "").strip()
            texto = request.form.get("resposta_texto", "").strip()

            if not id_pergunta or not texto:
                flash("Resposta e pergunta sao obrigatorios.", "erro")
                return redirect(url_for("forum"))

            conexao = conectar()
            criado = False
            if conexao:
                try:
                    criado = crud_criar_resposta(conexao, texto, None, session["usuario"].get("id_user"), id_pergunta)
                finally:
                    encerrar(conexao)

            if criado:
                flash("Resposta enviada com sucesso.", "sucesso")
            else:
                flash("Nao foi possivel enviar a resposta.", "erro")

            return redirect(url_for("forum"))

        titulo = request.form.get("titulo", "").strip()
        texto = request.form.get("texto", "").strip()
        id_disciplina = request.form.get("id_disciplina", "").strip()

        if not titulo or not texto:
            flash("Titulo e mensagem sao obrigatorios.", "erro")
            return render_template("disciplinas_forum.html", active_page="disciplinas_forum", **contexto_base())

        conexao = conectar()
        criado = False
        if conexao:
            try:
                criado = crud_criar_pergunta(conexao, titulo, texto, None, session["usuario"].get("id_user"), id_disciplina or None)
            finally:
                encerrar(conexao)

        if criado:
            flash("Pergunta enviada com sucesso.", "sucesso")
        else:
            flash("Nao foi possivel enviar a pergunta.", "erro")

        return redirect(url_for("forum"))

    contexto = contexto_base()
    perguntas = contexto.get("perguntas", [])

    if termo_busca:
        perguntas_filtradas = []
        for pergunta in perguntas:
            texto = " ".join([
                pergunta.get("titulo", ""),
                pergunta.get("texto", ""),
                pergunta.get("disciplina", ""),
            ]).lower()
            if termo_busca in texto:
                perguntas_filtradas.append(pergunta)
        contexto["perguntas"] = perguntas_filtradas
    else:
        contexto["perguntas"] = perguntas

    contexto["termo_busca"] = termo_busca
    return render_template("disciplinas_forum.html", active_page="disciplinas_forum", **contexto)


if __name__ == "__main__":
    app.run(debug=True)
