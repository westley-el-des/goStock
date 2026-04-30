# controllers/auth_controller.py
# Controla login, logout e registro de usuários

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.usuario import Usuario

# Blueprint para agrupar as rotas de autenticação
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Exibe e processa o formulário de login."""

    # Se já estiver logado, redireciona para o dashboard
    if "usuario_id" in session:
        return redirect(url_for("produtos.listar"))

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "")

        # Validação básica
        if not email or not senha:
            flash("Preencha todos os campos.", "danger")
            return render_template("auth/login.html")

        # Tenta autenticar
        usuario = Usuario.autenticar(email, senha)

        if usuario:
            # Cria sessão com dados do usuário
            session["usuario_id"] = usuario["id"]
            session["usuario_nome"] = usuario["nome"]
            flash(f"Bem-vindo, {usuario['nome']}! 👋", "success")
            return redirect(url_for("produtos.listar"))
        else:
            flash("Email ou senha inválidos.", "danger")

    return render_template("auth/login.html")


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    """Exibe e processa o formulário de registro de novos usuários."""

    if "usuario_id" in session:
        return redirect(url_for("produtos.listar"))

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "")
        confirmar_senha = request.form.get("confirmar_senha", "")

        # Validações
        if not nome or not email or not senha:
            flash("Preencha todos os campos.", "danger")
            return render_template("auth/registro.html")

        if len(senha) < 6:
            flash("A senha deve ter pelo menos 6 caracteres.", "danger")
            return render_template("auth/registro.html")

        if senha != confirmar_senha:
            flash("As senhas não coincidem.", "danger")
            return render_template("auth/registro.html")

        # Tenta cadastrar
        sucesso = Usuario.cadastrar(nome, email, senha)

        if sucesso:
            flash("Conta criada com sucesso! Faça login.", "success")
            return redirect(url_for("auth.login"))
        else:
            flash("Este email já está cadastrado.", "danger")

    return render_template("auth/registro.html")


@auth_bp.route("/logout")
def logout():
    """Encerra a sessão do usuário."""
    session.clear()
    flash("Você saiu do sistema.", "info")
    return redirect(url_for("auth.login"))
