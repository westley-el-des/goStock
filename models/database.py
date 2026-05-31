import psycopg2
from psycopg2.extras import RealDictCursor


def get_connection():
    conn = psycopg2.connect(
        dbname="gostock",
        user="macbookpro",
        host="localhost"
    )
    return conn


def inicializar_banco():
    from models.usuario import Usuario
    from models.produto import Produto

    Usuario.criar_tabela()
    Produto.criar_tabela()

    print("✅ Banco PostgreSQL inicializado com sucesso.")
