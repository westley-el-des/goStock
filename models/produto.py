# models/produto.py
# Responsável por toda lógica de dados dos produtos

from datetime import date, timedelta
from models.database import get_connection


# Limite de quantidade para considerar "estoque baixo"
LIMITE_ESTOQUE_BAIXO = 10
# Dias para considerar "próximo do vencimento"
DIAS_VENCIMENTO_PROXIMO = 30


class Produto:
    """Modelo de produto com métodos para CRUD e alertas inteligentes."""

    def __init__(self, id=None, nome=None, quantidade=None, data_vencimento=None):
        self.id = id
        self.nome = nome
        self.quantidade = quantidade
        self.data_vencimento = data_vencimento

        

    @staticmethod
    def criar_tabela():
        """Cria a tabela de produtos se não existir."""
        conn = get_connection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                quantidade INTEGER NOT NULL DEFAULT 0,
                data_vencimento DATE,
                usuario_id INTEGER NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def listar_todos():
        """
        Retorna todos os produtos com flags de alerta:
        - estoque_baixo: True se quantidade <= limite
        - vencimento_proximo: True se vence nos próximos 30 dias
        - vencido: True se a data de vencimento já passou
        """
        conn = get_connection()
        cursor = conn.execute(
            "SELECT * FROM produtos ORDER BY nome ASC"
        )
        produtos = cursor.fetchall()
        conn.close()

        hoje = date.today()
        limite_vencimento = hoje + timedelta(days=DIAS_VENCIMENTO_PROXIMO)
        resultado = []

        for p in produtos:
            produto = dict(p)
            produto["estoque_baixo"] = produto["quantidade"] <= LIMITE_ESTOQUE_BAIXO

            # Verifica vencimento
            if produto["data_vencimento"]:
                # SQLite retorna string, converte para date
                if isinstance(produto["data_vencimento"], str):
                    venc = date.fromisoformat(produto["data_vencimento"])
                else:
                    venc = produto["data_vencimento"]

                produto["vencido"] = venc < hoje
                produto["vencimento_proximo"] = hoje <= venc <= limite_vencimento
            else:
                produto["vencido"] = False
                produto["vencimento_proximo"] = False

            resultado.append(produto)

        return resultado

    @staticmethod
    def buscar_por_id(id):
        """Retorna um produto pelo ID."""
        conn = get_connection()
        cursor = conn.execute("SELECT * FROM produtos WHERE id = ?", (id,))
        produto = cursor.fetchone()
        conn.close()
        return dict(produto) if produto else None

    @staticmethod
    def cadastrar(nome, quantidade, data_vencimento, usuario_id):
        """Insere um novo produto no banco de dados."""
        conn = get_connection()
        conn.execute(
            "INSERT INTO produtos (nome, quantidade, data_vencimento, usuario_id) VALUES (?, ?, ?, ?)",
            (nome, quantidade, data_vencimento or None, usuario_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def atualizar(id, nome, quantidade, data_vencimento):
        """Atualiza os dados de um produto existente."""
        conn = get_connection()
        conn.execute(
            "UPDATE produtos SET nome = ?, quantidade = ?, data_vencimento = ? WHERE id = ?",
            (nome, quantidade, data_vencimento or None, id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def excluir(id):
        """Remove um produto do banco de dados."""
        conn = get_connection()
        conn.execute("DELETE FROM produtos WHERE id = ?", (id,))
        conn.commit()
        conn.close()

    @staticmethod
    def contar_alertas(usuario_id):
        """Retorna contagem de alertas para o dashboard."""
        produtos = Produto.listar_por_usuario(usuario_id)

        estoque_baixo = sum(1 for p in produtos if p["estoque_baixo"])
        vencendo = sum(1 for p in produtos if p["vencimento_proximo"])
        vencidos = sum(1 for p in produtos if p["vencido"])

        return {
            "estoque_baixo": estoque_baixo,
            "vencendo": vencendo,
            "vencidos": vencidos,
            "total": len(produtos)
        }
    
    @staticmethod
    def listar_por_usuario(usuario_id):
        conn = get_connection()
        cursor = conn.execute(
            "SELECT * FROM produtos WHERE usuario_id = ? ORDER BY nome ASC",
            (usuario_id,)
        )
        produtos = cursor.fetchall()
        conn.close()

        from datetime import date, timedelta

        hoje = date.today()
        limite_vencimento = hoje + timedelta(days=30)
        resultado = []

        for p in produtos:
            produto = dict(p)

            #estoque baixo
            produto["estoque_baixo"] = produto["quantidade"] <= 10

            #vencimento
            if produto["data_vencimento"]:
                if isinstance(produto["data_vencimento"], str):
                    venc = date.fromisoformat(produto["data_vencimento"])
                else:
                    venc = produto["data_vencimento"]

                produto["vencido"] = venc < hoje
                produto["vencimento_proximo"] = hoje <= venc <= limite_vencimento
            else:
                produto["vencido"] = False
                produto["vencimento_proximo"] = False

            resultado.append(produto)

        return resultado 
