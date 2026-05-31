import os
from flask import Flask, redirect, url_for
from controllers.auth_controller import auth_bp
from controllers.produto_controller import produtos_bp


def create_app():
    app = Flask(__name__)

    app.secret_key = os.environ.get("SECRET_KEY", "gostock-secret-2025-dev")

    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

    app.register_blueprint(auth_bp)
    app.register_blueprint(produtos_bp)

    @app.route("/")
    def index():
        return redirect(url_for("produtos.listar"))

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)