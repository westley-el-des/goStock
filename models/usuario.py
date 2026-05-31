from werkzeug.security import generate_password_hash, check_password_hash
from psycopg2 import IntegrityError
from psycopg2.extras import RealDictCursor
from models.database import get_connection


class Usuario:

    @staticmethod
    def criar_tabela():
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def cadastrar(nome, email, senha):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            senha_hash = generate_password_hash(senha)

            cursor.execute("""
                INSERT INTO usuarios (nome, email, senha)
                VALUES (%s, %s, %s)
            """, (nome, email, senha_hash))

            conn.commit()
            cursor.close()
            conn.close()

            return True

        except IntegrityError:
            return False

    @staticmethod
    def autenticar(email, senha):
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("""
            SELECT * FROM usuarios WHERE email = %s
        """, (email,))

        usuario = cursor.fetchone()

        conn.close()

        if usuario and check_password_hash(usuario["senha"], senha):
            return dict(usuario)

        return None

    @staticmethod
    def buscar_por_id(id):
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("""
            SELECT * FROM usuarios WHERE id = %s
        """, (id,))

        usuario = cursor.fetchone()

        conn.close()

        return dict(usuario) if usuario else None