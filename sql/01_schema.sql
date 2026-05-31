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
    id_curso REFERENCES Curso(id_curso),
    matricula VARCHAR(100) not null UNIQUE
);

