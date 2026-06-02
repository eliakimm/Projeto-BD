import psycopg2
from psycopg2 import Error
import os
from dotenv import load_dotenv

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