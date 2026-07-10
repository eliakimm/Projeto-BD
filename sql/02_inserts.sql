INSERT INTO Curso (nome, descricao, total_horas, nivel) VALUES
(
    'Ciência da Computação',
    'Curso voltado para fundamentos da computação, desenvolvimento de software, inteligência artificial, bancos de dados e sistemas computacionais.',
    3200,
    'Graduação - Bacharelado'
),
(
    'Licenciatura em Computação',
    'Curso destinado à formação de professores de Computação para a educação básica e profissional, integrando tecnologia e educação.',
    3200,
    'Graduação - Licenciatura'
),
(
    'Matemática',
    'Curso voltado para formação em matemática pura, aplicada e educação matemática, desenvolvendo raciocínio lógico e científico.',
    3000,
    'Graduação - Bacharelado'
);

INSERT INTO Disciplina (codigo, nome, descricao, carga_horaria) VALUES
('CIC0004','Algoritmos e Programação de Computadores',
'Introdução à lógica de programação e desenvolvimento de algoritmos.',
90),

('CIC0005','Técnicas de Programação 1',
'Programação estruturada utilizando linguagem de programação.',
90),

('CIC0006','Técnicas de Programação 2',
'Programação orientada a objetos e estruturas de dados básicas.',
90),

('CIC0007','Estruturas de Dados',
'Estudo de listas, filas, pilhas, árvores e grafos.',
60),

('CIC0008','Organização e Arquitetura de Computadores',
'Funcionamento interno dos computadores e arquitetura de processadores.',
60),

('CIC0009','Sistemas Operacionais',
'Gerenciamento de processos, memória, arquivos e dispositivos.',
60),

('CIC0010','Banco de Dados',
'Modelagem conceitual, lógica, SQL e administração de bancos de dados.',
60),

('CIC0011','Engenharia de Software',
'Processos de desenvolvimento de software, requisitos e testes.',
60),

('CIC0012','Redes de Computadores',
'Protocolos, arquitetura TCP/IP e comunicação entre computadores.',
60),

('CIC0013','Compiladores',
'Construção de compiladores e análise léxica e sintática.',
60),

('CIC0014','Inteligência Artificial',
'Fundamentos de IA, busca, representação de conhecimento e aprendizado.',
60),

('CIC0015','Computação Gráfica',
'Técnicas de modelagem, renderização e animação gráfica.',
60),

('CIC0016','Segurança Computacional',
'Princípios de segurança da informação, criptografia e autenticação.',
60),

('CIC0017','Projeto de Software',
'Desenvolvimento de projetos utilizando metodologias de engenharia de software.',
60),

('CIC0018','Programação Concorrente',
'Threads, sincronização e programação paralela.',
60),

('MAT0001','Cálculo 1',
'Limites, derivadas e aplicações.',
90),

('MAT0002','Cálculo 2',
'Integrais, séries e aplicações.',
90),

('MAT0003','Álgebra Linear',
'Matrizes, espaços vetoriais, transformações lineares e autovalores.',
60),

('MAT0004','Matemática Discreta',
'Lógica, conjuntos, relações, funções e combinatória.',
60),

('EST0001','Probabilidade e Estatística',
'Probabilidade, variáveis aleatórias, inferência estatística e aplicações.',
60);

##Ciência da Computação:
INSERT INTO curso_disciplina VALUES
(10,21),
(10,22),
(10,23),
(10,24),
(10,25),
(10,26),
(10,27),
(10,28),
(10,29),
(10,30),
(10,31),
(10,32),
(10,33),
(10,34),
(10,35),
(10,36),
(10,37),
(10,38),
(10,39),
(10,40);

##Licenciatura em Computação:
INSERT INTO curso_disciplina VALUES
(11,21),
(11,22),
(11,23),
(11,24),
(11,25),
(11,26),
(11,27),
(11,28),
(11,29),
(11,30);

##Matemática:
INSERT INTO curso_disciplina VALUES
(12,36),
(12,37),
(12,38),
(12,39),
(12,30);

##Estatística:
INSERT INTO curso_disciplina VALUES
(13,36),
(13,37),
(13,38),
(13,39),
(13,30);


##Engenharia de Software:
INSERT INTO curso_disciplina VALUES
(14,21),
(14,22),
(14,23),
(14,24),
(14,25),
(14,26),
(14,27),
(14,28),
(14,29),
(14,30),
(14,31),
(14,32),
(14,33),
(14,34),
(14,35),
(14,36),
(14,37),
(14,38),
(14,39),
(14,40);