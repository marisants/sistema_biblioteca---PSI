import sqlite3

def criar_conexao():
    conexao = sqlite3.connect('banco.db')
    conexao.row_factory = sqlite3.Row
    return conexao

def inicializar_banco():
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuario(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            nome TEXT NOT NULL, 
            senha INTEGER NOT NULL,
            tipo TEXT NOT NULL
        )
    """)

    conexao.commit()
    conexao.close()