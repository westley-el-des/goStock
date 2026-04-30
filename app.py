# app.py
# Ponto de entrada principal do GoStock
# Inicializa o Flask, registra blueprints e configura a sessão

import os
from flask import Flask, redirect, url_for
from models.database import inicializar_banco
from controllers.auth_controller import auth_bp
from controllers.produto_controller import produtos_bp


def create_app():
    """Factory function que cria e configura a aplicação Flask."""
    app = Flask(__name__)

    # Chave secreta para sessões (em produção, use variável de ambiente)
    app.secret_key = os.environ.get("SECRET_KEY", "gostock-secret-2025-dev")

    # Configura cookies de sessão
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

    # Registra blueprints (controllers)
    app.register_blueprint(auth_bp)               # /login, /logout, /registro
    app.register_blueprint(produtos_bp)           # /, /novo, /editar/<id>, /excluir/<id>

    # Rota raiz redireciona para lista de produtos (ou login)
    @app.route("/")
    def index():
        return redirect(url_for("produtos.listar"))

    return app


# Inicializa o banco de dados e sobe o servidor
if __name__ == "__main__":
    inicializar_banco()

    app = create_app()
    print("🚀 GoStock rodando em: http://127.0.0.1:5000")
    app.run(debug=True, host="127.0.0.1", port=5000)
