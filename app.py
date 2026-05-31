# app.py
# Ponto de entrada principal do GoStock

import os
from flask import Flask, redirect, url_for
from controllers.auth_controller import auth_bp
from controllers.produto_controller import produtos_bp


def create_app():
    """Factory function que cria e configura a aplicação Flask."""
    app = Flask(__name__)

    # Chave secreta
    app.secret_key = os.environ.get("SECRET_KEY", "gostock-secret-2025-dev")

    # Sessão
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

    # Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(produtos_bp)

    @app.route("/")
    def index():
        return redirect(url_for("produtos.listar"))

    return app


# App para o Gunicorn (Render)
app = create_app()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)