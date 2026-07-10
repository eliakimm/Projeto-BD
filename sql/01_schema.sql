CREATE Table Curso(
    id_curso SERIAL PRIMARY KEY,
    nome varchar(100) not null,
    descricao text,
    total_horas int not null,
    nivel varchar(100) not null
);

CREATE table disciplina(
    id_disciplina SERIAL PRIMARY KEY,
    codigo VARCHAR(100) not null,
    nome VARCHAR(100) not null,
    descricao TEXT,
    carga_horaria int not null
);

CREATE table curso_disciplina(
    id_curso int REFERENCES curso(id_curso),
    id_disciplina int REFERENCES disciplina(id_disciplina),
    PRIMARY KEY(id_curso, id_disciplina)
);

CREATE table Usuario(
    id_user serial PRIMARY KEY,
    nome VARCHAR(100) not NULL,
    email VARCHAR(100) not NULL UNIQUE,
    senha VARCHAR(100) not NULL,
    data_cadastro DATE DEFAULT now(),
    ativo BOOLEAN DEFAULT true
);

CREATE table Admin_Sistema(
    id_user int REFERENCES Usuario(id_user) PRIMARY KEY,
    cargo VARCHAR(100) not NULL
);

CREATE table Aluno(
    id_user int REFERENCES Usuario(id_user) PRIMARY KEY,
    id_curso int REFERENCES Curso(id_curso),
    matricula VARCHAR(100) not null UNIQUE
);

CREATE table aviso(
    id_aviso serial PRIMARY KEY,
    id_user int REFERENCES Admin_Sistema(id_user),
    titulo VARCHAR(100) not NULL,
    texto TEXT not NULL,
    data_postagem DATE DEFAULT now()
);

CREATE table agenda(
    id_agenda serial PRIMARY KEY,
    id_user int REFERENCES Aluno(id_user),
    titulo VARCHAR(100) not NULL,
    descricao TEXT,
    data_entrega DATE not NULL
);

CREATE table atividade(
    id_atividade serial PRIMARY KEY,
    id_disciplina int REFERENCES disciplina(id_disciplina),
    titulo VARCHAR(100) not NULL,
    descricao TEXT,
    data_entrega DATE not NULL
);

CREATE table novo_evento(
    id_agenda int REFERENCES agenda(id_agenda),
    id_atividade int REFERENCES atividade(id_atividade),
    PRIMARY KEY(id_agenda, id_atividade)
);

CREATE table material_apoio(
    id_material serial PRIMARY KEY,
    id_disciplina int REFERENCES disciplina(id_disciplina),
    tipo VARCHAR(100) not NULL,
    titulo VARCHAR(100) not NULL,
    descricao TEXT
);

CREATE table forum_pergunta(
    id_pergunta serial PRIMARY KEY,
    id_disciplina int REFERENCES disciplina(id_disciplina),
    id_user int REFERENCES usuario(id_user),
    titulo VARCHAR(100) not NULL,
    texto TEXT not NULL,
    data_postagem TIMESTAMP DEFAULT now(),
    ativa BOOLEAN DEFAULT false
);

CREATE table forum_resposta(
    id_resposta serial PRIMARY KEY,
    id_pergunta int REFERENCES forum_pergunta(id_pergunta) on delete CASCADE,
    id_user int REFERENCES usuario(id_user),
    texto TEXT not NULL,
    data_postagem TIMESTAMP DEFAULT now(),
    id_resposta_pai int REFERENCES forum_resposta(id_resposta) on delete CASCADE,
    solucao BOOLEAN DEFAULT false
);
