-- Objetos de banco: trigger, view e procedure para o sistema acadêmico

CREATE OR REPLACE FUNCTION trg_marcar_pergunta_ativa()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.solucao = TRUE THEN
        UPDATE forum_pergunta
        SET ativa = TRUE
        WHERE id_pergunta = NEW.id_pergunta;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trg_forum_resposta_solucao
AFTER INSERT OR UPDATE OF solucao ON forum_resposta
FOR EACH ROW
WHEN (NEW.solucao = TRUE)
EXECUTE FUNCTION trg_marcar_pergunta_ativa();

CREATE OR REPLACE VIEW vw_dashboard_forum AS
SELECT
    fp.id_pergunta,
    fp.titulo,
    fp.texto,
    fp.id_user,

    d.nome AS disciplina,

    u.nome AS autor,

    fp.data_postagem,
    fp.ativa,

    COUNT(fr.id_resposta) AS respostas,

    SUM(
        CASE
            WHEN fr.solucao = TRUE THEN 1
            ELSE 0
        END
    ) AS respostas_solucao

FROM forum_pergunta fp

LEFT JOIN disciplina d
    ON d.id_disciplina = fp.id_disciplina

LEFT JOIN usuario u
    ON u.id_user = fp.id_user

LEFT JOIN forum_resposta fr
    ON fr.id_pergunta = fp.id_pergunta

GROUP BY
    fp.id_pergunta,
    fp.titulo,
    fp.texto,
    fp.id_user,
    d.nome,
    u.nome,
    fp.data_postagem,
    fp.ativa;

CREATE OR REPLACE PROCEDURE sp_criar_atividade_com_agenda(
    p_id_disciplina INT,
    p_titulo VARCHAR(100),
    p_descricao TEXT,
    p_data_entrega DATE,
    p_id_user INT,
    p_titulo_agenda VARCHAR(100),
    p_descricao_agenda TEXT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_id_atividade INT;
    v_id_agenda INT;
BEGIN
    INSERT INTO atividade (id_disciplina, titulo, descricao, data_entrega)
    VALUES (p_id_disciplina, p_titulo, p_descricao, p_data_entrega)
    RETURNING id_atividade INTO v_id_atividade;

    INSERT INTO agenda (id_user, titulo, descricao, data_entrega)
    VALUES (
        p_id_user,
        COALESCE(p_titulo_agenda, p_titulo),
        COALESCE(p_descricao_agenda, p_descricao),
        p_data_entrega
    )
    RETURNING id_agenda INTO v_id_agenda;

    INSERT INTO novo_evento (id_agenda, id_atividade)
    VALUES (v_id_agenda, v_id_atividade);
END;
$$;


