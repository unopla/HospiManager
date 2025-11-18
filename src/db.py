import mysql.connector
from mysql.connector import Error

def conectar():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="hospitamanager"
        )

        if conexao.is_connected():
            print("Conectado ao MySQL!")
            return conexao

    except Error as e:
        print(f"Erro ao conectar: {e}")

    return None