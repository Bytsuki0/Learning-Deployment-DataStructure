# Importa as principais funções e classes do Flask
# - Flask: cria a aplicação
# - render_template: renderiza páginas HTML da pasta /templates
# - request: acessa dados enviados por formulários (POST/GET)
# - redirect e url_for: redirecionam para outras rotas
# - flash: mostra mensagens temporárias ao usuário (ex: sucesso ou erro)
from flask import Flask, render_template, request, redirect, url_for, flash

# Importa configurações (por exemplo: conexão com banco de dados)
from config import Config

# Importa o objeto MySQL e funções auxiliares de manipulação de dados
from models import mysql, get_all_emprestimos, get_all_usuarios, adicionar_usuario


# Cria a aplicação Flask
app = Flask(__name__)

# Carrega configurações do arquivo config.py (ex: dados do banco)
app.config.from_object(Config)

# Define uma chave secreta (necessária para usar mensagens flash e sessões)
app.secret_key = '153226@#'  # <-- troque aqui por uma chave mais segura em produção

# Inicializa a extensão MySQL
mysql.init_app(app)

# Rota principal
@app.route('/')
def index():
    # Renderiza o template index.html
    return render_template('index.html')

# Rota para exibir os empréstimos com detalhes (usando a view SQL)
@app.route('/emprestimos')
def emprestimos():
    # Busca os dados no banco de dados via função auxiliar
    dados = get_all_emprestimos()
    # Passa os dados para o template emprestimos.html
    return render_template('emprestimos.html', 
                           emprestimos=dados)


@app.route('/usuarios')
def usuarios():
    dados = get_all_usuarios()
    return render_template('usuarios.html',
                            usuarios=dados)

# Rota para cadastrar novos usuários
# Aceita tanto GET (mostrar formulário) 
# quanto POST (enviar dados)
@app.route('/cadastro_usuario', methods=['GET', 'POST'])
def cadastro_usuario():
    # Se o formulário for enviado (POST)
    if request.method == 'POST':
        # Captura os dados do formulário
        cpf = request.form['cpf']
        rg = request.form['rg']
        nome = request.form['nome']
        telefone = request.form['telefone']
        celular = request.form['celular']
        endereco = request.form['endereco']

        try:
            # Tenta inserir o novo usuário no banco
            adicionar_usuario(cpf, rg, nome,
                               telefone, celular,
                                 endereco)
            # Mostra mensagem de sucesso
            flash('Usuário cadastrado com sucesso!')
            # Redireciona para a página de usuários
            return redirect(url_for('usuarios'))
        except Exception as e:
            flash(f'Erro ao cadastrar usuário: {e}')
            return redirect(url_for('cadastro_usuario'))
    return render_template('cadastro_usuario.html')

# =============================
# 🚀 EXECUÇÃO LOCAL DO APP
# =============================
if __name__ == '__main__':
    # Executa o servidor Flask em modo debug
    # (atualiza automaticamente ao salvar alterações)
    app.run(debug=True)