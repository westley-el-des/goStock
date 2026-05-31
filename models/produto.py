# models/produto.py

from datetime import date, timedelta
from models.database import get_connection
from psycopg2.extras import RealDictCursor

LIMITE_ESTOQUE_BAIXO = 10
DIAS_VENCIMENTO_PROXIMO = 30


class Produto:

    def __init__(self, id=None, nome=None, quantidade=None, data_vencimento=None):
        self.id = id
        self.nome = nome
        self.quantidade = quantidade
        self.data_vencimento = data_vencimento

    @staticmethod
    def criar_tabela():
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id SERIAL PRIMARY KEY,
                nome TEXT NOT NULL,
                quantidade INTEGER NOT NULL DEFAULT 0,
                data_vencimento DATE,
                usuario_id INTEGER NOT NULL
            )
        """)

        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def listar_todos():
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("SELECT * FROM produtos ORDER BY nome ASC")
        produtos = cursor.fetchall()

        conn.close()

        hoje = date.today()
        limite_vencimento = hoje + timedelta(days=DIAS_VENCIMENTO_PROXIMO)

        resultado = []

        for p in produtos:
            produto = dict(p)
            produto["estoque_baixo"] = produto["quantidade"] <= LIMITE_ESTOQUE_BAIXO

            if produto["data_vencimento"]:
                venc = produto["data_vencimento"]
                if isinstance(venc, str):
                    venc = date.fromisoformat(venc)

                produto["vencido"] = venc < hoje
                produto["vencimento_proximo"] = hoje <= venc <= limite_vencimento
            else:
                produto["vencido"] = False
                produto["vencimento_proximo"] = False

            resultado.append(produto)

        return resultado

    @staticmethod
    def buscar_por_id(id):
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("SELECT * FROM produtos WHERE id = %s", (id,))
        produto = cursor.fetchone()

        conn.close()
        return dict(produto) if produto else None

    @staticmethod
    def cadastrar(nome, quantidade, data_vencimento, usuario_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO produtos (nome, quantidade, data_vencimento, usuario_id)
            VALUES (%s, %s, %s, %s)
        """, (nome, quantidade, data_vencimento, usuario_id))

        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def atualizar(id, nome, quantidade, data_vencimento):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE produtos
            SET nome = %s, quantidade = %s, data_vencimento = %s
            WHERE id = %s
        """, (nome, quantidade, data_vencimento, id))

        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def excluir(id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM produtos WHERE id = %s", (id,))

        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def contar_alertas(usuario_id):
        produtos = Produto.listar_por_usuario(usuario_id)

        return {
            "estoque_baixo": sum(1 for p in produtos if p["estoque_baixo"]),
            "vencendo": sum(1 for p in produtos if p["vencimento_proximo"]),
            "vencidos": sum(1 for p in produtos if p["vencido"]),
            "total": len(produtos)
        }

    @staticmethod
    def listar_por_usuario(usuario_id):
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("""
            SELECT * FROM produtos
            WHERE usuario_id = %s
            ORDER BY nome ASC
        """, (usuario_id,))

        produtos = cursor.fetchall()
        conn.close()

        hoje = date.today()
        limite_vencimento = hoje + timedelta(days=DIAS_VENCIMENTO_PROXIMO)

        resultado = []

        for p in produtos:
            produto = dict(p)

            produto["estoque_baixo"] = produto["quantidade"] <= LIMITE_ESTOQUE_BAIXO

            if produto["data_vencimento"]:
                venc = produto["data_vencimento"]
                if isinstance(venc, str):
                    venc = date.fromisoformat(venc)

                produto["vencido"] = venc < hoje
                produto["vencimento_proximo"] = hoje <= venc <= limite_vencimento
            else:
                produto["vencido"] = False
                produto["vencimento_proximo"] = False

            resultado.append(produto)

        return resultado