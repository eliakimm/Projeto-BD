import psycopg2
from psycopg2 import Error
import os
from flask import Flask

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv():
        return None

load_dotenv()

def conectar():
    try:
        conexao = psycopg2.connect(
            host= os.getenv("DB_HOST", "localhost"),
            database= os.getenv("DB_NAME"),
            user= os.getenv("DB_USER"),
            password= os.getenv("DB_PASSWORD"),
            port= os.getenv("DB_PORT", "5432")
        )
        print("conectado ao banco de dados")

        return conexao
    
    except Error as erro:
        print(f"erro de conexão com o banco de dados: {erro}")
        return None
    

def encerrar(conexao):
    if conexao:
        try:
            conexao.close()
            print("conexão encerrada")
        except Error as erro:
            print(f"erro ao encerrar conexão: {erro}")

    else:
        print("sem conexão para encerrar")


def executar_queries(conexao, query, parametros= None):
    if not conexao:
        print("Sem conexão com o banco de dados")
        return None
    
    try:
        cursor= conexao.cursor()

        if parametros:
            cursor.execute(query, parametros)
        else: 
            cursor.execute(query)
    
        conexao.commit()
        print("Query executada com sucesso")
        return cursor

    except Error as erro:
        print(f"falha ao executar query: {erro}")
        conexao.rollback()
        raise erro

def obter_resultados(conexao, query, parametros= None):
    if not conexao:
        print("Sem conexão com o banco de dados")
        return None
    
    try:
        cursor= conexao.cursor()

        if parametros:
            cursor.execute(query, parametros)
        else:
            cursor.execute(query)

        resultados= cursor.fetchall()
        cursor.close()

        return resultados
    
    except Error as erro:
        print("Erro ao obter resultados")
        return None

def garantir_colunas_compatibilidade():
    conexao = conectar()
    if not conexao:
        return False

    try:
        with conexao.cursor() as cursor:
            cursor.execute("ALTER TABLE agenda ADD COLUMN IF NOT EXISTS concluida BOOLEAN DEFAULT false")
            cursor.execute("ALTER TABLE forum_resposta ADD COLUMN IF NOT EXISTS solucao BOOLEAN DEFAULT false")
            conexao.commit()
        return True
    except Error as erro:
        print(f"Erro ao ajustar esquema do fórum: {erro}")
        conexao.rollback()
        return False
    finally:
        encerrar(conexao)