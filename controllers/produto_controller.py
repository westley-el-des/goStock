# controllers/produto_controller.py
# Controla todas as operações de CRUD de produtos

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.produto import Produto
from functools import wraps

# Blueprint para agrupar as rotas de produtos
produtos_bp = Blueprint("produtos", __name__)


def login_required(f):
    """
    Decorator que protege rotas, exigindo que o usuário esteja autenticado.
    Redireciona para o login caso não esteja.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if "usuario_id" not in session:
            flash("Faça login para acessar esta página.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


@produtos_bp.route("/")
@login_required
def listar():
    """Lista todos os produtos com alertas de estoque e vencimento."""
    usuario_id = session["usuario_id"]
    produtos = Produto.listar_por_usuario(usuario_id)
    usuario_id = session["usuario_id"]
    alertas = Produto.contar_alertas(usuario_id)

    return render_template("produtos/listar.html", produtos=produtos, alertas=alertas)


@produtos_bp.route("/novo", methods=["GET", "POST"])
@login_required
def novo():
    """Exibe formulário e processa o cadastro de novo produto."""
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        quantidade = request.form.get("quantidade", "").strip()
        data_vencimento = request.form.get("data_vencimento", "").strip()

        # Validações
        if not nome:
            flash("O nome do produto é obrigatório.", "danger")
            return render_template("produtos/form.html", acao="Cadastrar", produto=None)

        if not quantidade or not quantidade.isdigit() or int(quantidade) < 0:
            flash("Informe uma quantidade válida (número inteiro positivo).", "danger")
            return render_template("produtos/form.html", acao="Cadastrar", produto=None)

        # Cadastra o produto
        usuario_id = session["usuario_id"]

        Produto.cadastrar(
            nome, 
            int(quantidade),
            data_vencimento or None, 
            usuario_id
        )
        
        flash(f'Produto "{nome}" cadastrado com sucesso! ✅', "success")
        return redirect(url_for("produtos.listar"))

    return render_template("produtos/form.html", acao="Cadastrar", produto=None)


@produtos_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):
    """Exibe formulário pré-preenchido e processa a edição de um produto."""
    produto = Produto.buscar_por_id(id)

    if not produto:
        flash("Produto não encontrado.", "danger")
        return redirect(url_for("produtos.listar"))

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        quantidade = request.form.get("quantidade", "").strip()
        data_vencimento = request.form.get("data_vencimento", "").strip()

        # Validações
        if not nome:
            flash("O nome do produto é obrigatório.", "danger")
            return render_template("produtos/form.html", acao="Editar", produto=produto)

        if not quantidade or not quantidade.isdigit() or int(quantidade) < 0:
            flash("Informe uma quantidade válida (número inteiro positivo).", "danger")
            return render_template("produtos/form.html", acao="Editar", produto=produto)

        # Atualiza o produto
        Produto.atualizar(id, nome, int(quantidade), data_vencimento or None)
        flash(f'Produto "{nome}" atualizado com sucesso! ✅', "success")
        return redirect(url_for("produtos.listar"))

    return render_template("produtos/form.html", acao="Editar", produto=produto)


@produtos_bp.route("/excluir/<int:id>", methods=["POST"])
@login_required
def excluir(id):
    """Exclui um produto (via POST para segurança)."""
    produto = Produto.buscar_por_id(id)

    if not produto:
        flash("Produto não encontrado.", "danger")
        return redirect(url_for("produtos.listar"))

    nome = produto["nome"]
    Produto.excluir(id)
    flash(f'Produto "{nome}" excluído com sucesso.', "success")
    return redirect(url_for("produtos.listar"))
