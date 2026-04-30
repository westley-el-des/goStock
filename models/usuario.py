# models/usuario.py
# Responsável por toda lógica de dados do usuário

import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from models.database import get_connection


class Usuario:
    """Modelo de usuário com métodos para CRUD e autenticação."""

    def __init__(self, id=None, nome=None, email=None, senha=None, created_at=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.created_at = created_at

    @staticmethod
    def criar_tabela():
        """Cria a tabela de usuários se não existir."""
        conn = get_connection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def cadastrar(nome, email, senha):
        """
        Cadastra um novo usuário com senha criptografada.
        Retorna True se sucesso, False se email já existe.
        """
        try:
            conn = get_connection()
            senha_hash = generate_password_hash(senha)
            conn.execute(
                "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
                (nome, email, senha_hash)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            # Email já cadastrado (UNIQUE constraint)
            return False

    @staticmethod
    def autenticar(email, senha):
        """
        Verifica email e senha.
        Retorna o usuário como dict se válido, None caso contrário.
        """
        conn = get_connection()
        cursor = conn.execute(
            "SELECT * FROM usuarios WHERE email = ?", (email,)
        )
        usuario = cursor.fetchone()
        conn.close()

        if usuario and check_password_hash(usuario["senha"], senha):
            return dict(usuario)
        return None

    @staticmethod
    def buscar_por_id(id):
        """Retorna um usuário pelo ID."""
        conn = get_connection()
        cursor = conn.execute("SELECT * FROM usuarios WHERE id = ?", (id,))
        usuario = cursor.fetchone()
        conn.close()
        return dict(usuario) if usuario else None
