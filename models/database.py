# models/database.py
# Gerenciamento da conexão com o SQLite

import sqlite3
import os

# Caminho absoluto do banco de dados
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, "database.db")


def get_connection():
    """
    Retorna uma conexão com o banco de dados SQLite.
    row_factory permite acessar colunas por nome (ex: row["nome"]).
    """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Acesso por nome de coluna
    return conn


def inicializar_banco():
    """
    Inicializa o banco de dados criando todas as tabelas necessárias.
    Chamado uma vez na inicialização da aplicação.
    """
    # Importa aqui para evitar importação circular
    from models.usuario import Usuario
    from models.produto import Produto

    Usuario.criar_tabela()
    Produto.criar_tabela()
    print("✅ Banco de dados inicializado com sucesso.")
