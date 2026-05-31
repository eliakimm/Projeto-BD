# Projeto de Banco de dados: SisAA- Sistema de Acompanhamento Acadêmico

## O que é?

<p>O projeto consiste no desenvolvimento de um sistema de acompanhamento acadêmico voltado para estudantes universitários. O objetivo principal é permitir o gerenciamento e monitoramento das disciplinas cursadas, desempenho acadêmico e progresso do aluno ao longo dos semestres.</p>
<p>A aplicação contará com interface gráfica para facilitar a interação do usuário e utilizará um banco de dados relacional para armazenamento seguro e organizado das informações acadêmicas.</p>

### Stack de desenvolvimento:
- Editor de código: __Visual Studio Code__;
- Linguagem principal: __Python__;
    - FrameWork: __Flask__.
- Banco de dados: __PostgreSql__;
- Ferramenta para modelagem: __brmodelo__.

### Estrutura do projeto:

- *| app*
    - app.py
    - *| database*
         - conexao.py
- *| sql*
    - 01_schema.sql
    - 02_inserts.sql
    - 03_queries.sql

### Entidades:

- 1-usuario
- 2-aluno
- 3-admin
- 4-curso
- 5-disciplina
- 6-material_apoio
- 7-aviso
- 8-agenda
- 9-atividade
- 10-forum_perguntas
- 11-forum_respostas

### Modelos feitos com brmodelo:

- [Modelo conceitual;](https://app.brmodeloweb.com/publicview/6a1c80c00b63d48fa75beda8)
- [Modelo relacional.](https://app.brmodeloweb.com/publicview/6a1c83c60b63d48fa75bee04)
