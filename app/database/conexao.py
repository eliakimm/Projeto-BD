import psycopg2

def conectar():
    conexao = psycopg2.connect(
        host="localhost",
        database= "sistema_academico",
        user="postgres",
        password="2521"
    )

    return conexao