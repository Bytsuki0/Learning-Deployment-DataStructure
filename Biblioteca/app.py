from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from models import mysql, get_all_emprestimos, get_all_usuarios, adicionar_usuario, adicionar_emprestimo

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = '153226@#'
mysql.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/emprestimos')
def emprestimos():
    dados = get_all_emprestimos()
    return render_template('emprestimos.html', emprestimos=dados)

@app.route('/usuarios')
def usuarios():
    dados = get_all_usuarios()
    return render_template('usuarios.html', usuarios=dados)

@app.route('/cadastro_usuario', methods=['GET', 'POST'])
def cadastro_usuario():
    if request.method == 'POST':
        cpf = request.form['cpf']
        rg = request.form['rg']
        nome = request.form['nome']
        telefone = request.form['telefone']
        celular = request.form['celular']
        endereco = request.form['endereco']
        try:
            adicionar_usuario(cpf, rg, nome, telefone, celular, endereco)
            flash('Usuário cadastrado com sucesso!')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Erro ao cadastrar usuário: {e}')
            return redirect(url_for('cadastro_usuario'))
    return render_template('cadastro_usuario.html')

# BUG FIX 1: function name changed from cadastrar_emprestimo to cadastro_emprestimo
# so it matches the url_for() calls in the HTML and in the except redirect below
@app.route('/cadastro_emprestimo', methods=['GET', 'POST'])
def cadastro_emprestimo():
    if request.method == 'POST':
        fk_usuario_cpf = request.form['fk_usuario_cpf']
        fk_usuario_rg = request.form['fk_usuario_rg']
        data_do_emprestimo = request.form['data_do_emprestimo']
        data_da_devolucao = request.form['data_da_devolucao']
        quantidade_de_livros = request.form['quantidade_de_livros']
        codigo = request.form['codigo']
        try:
            adicionar_emprestimo(codigo, data_do_emprestimo, data_da_devolucao,
                                 quantidade_de_livros,
                                 fk_usuario_cpf, fk_usuario_rg)
            flash('Empréstimo cadastrado com sucesso!')
            return redirect(url_for('index'))
        except Exception as e:
            # BUG FIX 2: rollback so the broken transaction doesn't block the next request
            mysql.connection.rollback()
            flash(f'Erro ao cadastrar empréstimo: {e}')
            # BUG FIX 1 (continued): url_for now matches the function name above
            return redirect(url_for('cadastro_emprestimo'))
    return render_template('cadastro_emprestimo.html', usuarios=get_all_usuarios())

if __name__ == '__main__':
    app.run(debug=True)