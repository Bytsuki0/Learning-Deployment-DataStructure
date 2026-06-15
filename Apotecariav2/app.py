from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from models import (
    mysql,
    get_all_pacientes, adicionar_paciente,
    get_all_profissionais, adicionar_profissional,
    get_all_atendimentos, adicionar_atendimento,
    get_all_diagnosticos, adicionar_diagnostico,
    get_all_receitas, adicionar_receita,
    get_all_ingredientes, adicionar_ingrediente,
    get_atendimentos_com_diagnostico,
    get_pacientes_com_tratamento,
    get_receitas_com_ingredientes,
    get_view_resumo_clinica,
)

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = '153226@#'
mysql.init_app(app)


# ───────────── INDEX ─────────────
@app.route('/')
def index():
    return render_template('index.html')


# ───────────── PACIENTES ─────────────
@app.route('/pacientes')
def pacientes():
    dados = get_all_pacientes()
    return render_template('pacientes.html', pacientes=dados)

@app.route('/cadastro_paciente', methods=['GET', 'POST'])
def cadastro_paciente():
    if request.method == 'POST':
        try:
            adicionar_paciente(
                request.form['codigo'],
                request.form['nome'],
                request.form['idade'],
                request.form['cargo'],
                request.form['historico'],
                request.form['data_nascimento'],
            )
            flash('Paciente cadastrado com sucesso!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Erro ao cadastrar paciente: {e}', 'danger')
            return redirect(url_for('cadastro_paciente'))
    return render_template('cadastro_paciente.html')


# ───────────── PROFISSIONAIS ─────────────
@app.route('/profissionais')
def profissionais():
    dados = get_all_profissionais()
    return render_template('profissionais.html', profissionais=dados)

@app.route('/cadastro_profissional', methods=['GET', 'POST'])
def cadastro_profissional():
    if request.method == 'POST':
        try:
            adicionar_profissional(
                request.form['codigo'],
                request.form['nome'],
                request.form['funcao'],
                request.form['especialidade'],
            )
            flash('Profissional cadastrado com sucesso!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Erro ao cadastrar profissional: {e}', 'danger')
            return redirect(url_for('cadastro_profissional'))
    return render_template('cadastro_profissional.html')


# ───────────── ATENDIMENTO ─────────────
@app.route('/atendimentos')
def atendimentos():
    dados = get_all_atendimentos()
    return render_template('atendimentos.html', atendimentos=dados)

@app.route('/cadastro_atendimento', methods=['GET', 'POST'])
def cadastro_atendimento():
    if request.method == 'POST':
        try:
            adicionar_atendimento(
                request.form['codigo'],
                request.form['codigo_profissional'],
                request.form['codigo_paciente'],
                request.form['data'],
                request.form['hora'],
                request.form['status'],
            )
            flash('Atendimento cadastrado com sucesso!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Erro ao cadastrar atendimento: {e}', 'danger')
            return redirect(url_for('cadastro_atendimento'))
    pacientes = get_all_pacientes()
    profissionais = get_all_profissionais()
    return render_template('cadastro_atendimento.html',
                           pacientes=pacientes,
                           profissionais=profissionais)


# ───────────── DIAGNÓSTICO ─────────────
@app.route('/diagnosticos')
def diagnosticos():
    dados = get_all_diagnosticos()
    return render_template('diagnosticos.html', diagnosticos=dados)

@app.route('/cadastro_diagnostico', methods=['GET', 'POST'])
def cadastro_diagnostico():
    if request.method == 'POST':
        try:
            adicionar_diagnostico(
                request.form['codigo'],
                request.form['id_paciente'],
                request.form['id_profissional'],
                request.form['descricao'],
                request.form['suspeita'],
                request.form['data_avaliacao'],
            )
            flash('Diagnóstico cadastrado com sucesso!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Erro ao cadastrar diagnóstico: {e}', 'danger')
            return redirect(url_for('cadastro_diagnostico'))
    pacientes = get_all_pacientes()
    profissionais = get_all_profissionais()
    return render_template('cadastro_diagnostico.html',
                           pacientes=pacientes,
                           profissionais=profissionais)


# ───────────── RECEITAS / TRATAMENTOS ─────────────
@app.route('/receitas')
def receitas():
    dados = get_all_receitas()
    return render_template('receitas.html', receitas=dados)

@app.route('/cadastro_receita', methods=['GET', 'POST'])
def cadastro_receita():
    if request.method == 'POST':
        try:
            adicionar_receita(
                request.form['codigo_receita'],
                request.form['codigo_tratamento'],
                request.form['dosagem'],
                request.form['nome_formula'],
                request.form['data_prescricao'],
                request.form['duracao'],
                request.form['status'],
                request.form['nome_tratamento'],
            )
            flash('Receita/Tratamento cadastrado com sucesso!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Erro ao cadastrar receita: {e}', 'danger')
            return redirect(url_for('cadastro_receita'))
    return render_template('cadastro_receita.html')


# ───────────── INGREDIENTES ─────────────
@app.route('/ingredientes')
def ingredientes():
    dados = get_all_ingredientes()
    return render_template('ingredientes.html', ingredientes=dados)

@app.route('/cadastro_ingrediente', methods=['GET', 'POST'])
def cadastro_ingrediente():
    if request.method == 'POST':
        try:
            adicionar_ingrediente(
                request.form['codigo'],
                request.form['nome'],
                request.form['tipo'],
                request.form['quantidade'],
                request.form['origem'],
                request.form['toxicidade'],
            )
            flash('Ingrediente cadastrado com sucesso!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Erro ao cadastrar ingrediente: {e}', 'danger')
            return redirect(url_for('cadastro_ingrediente'))
    return render_template('cadastro_ingrediente.html')


# ───────────── CONSULTAS (JOIN / LEFT JOIN / VIEW) ─────────────
@app.route('/consultas')
def consultas():
    return render_template('consultas.html')

@app.route('/consulta/atendimentos_diagnostico')
def consulta_atendimentos_diagnostico():
    dados = get_atendimentos_com_diagnostico()
    return render_template('consulta_join.html',
                           titulo='Atendimentos com Diagnóstico (INNER JOIN)',
                           descricao='Exibe apenas os atendimentos que possuem um diagnóstico associado, '
                                     'cruzando Atendimento → Paciente → Profissional → Diagnóstico.',
                           tipo='join',
                           dados=dados)

@app.route('/consulta/pacientes_tratamento')
def consulta_pacientes_tratamento():
    dados = get_pacientes_com_tratamento()
    return render_template('consulta_join.html',
                           titulo='Pacientes e seus Tratamentos (LEFT JOIN)',
                           descricao='Lista todos os pacientes, incluindo os que ainda não possuem '
                                     'diagnóstico ou tratamento registrado.',
                           tipo='left',
                           dados=dados)

@app.route('/consulta/receitas_ingredientes')
def consulta_receitas_ingredientes():
    dados = get_receitas_com_ingredientes()
    return render_template('consulta_join.html',
                           titulo='Receitas e seus Ingredientes (INNER JOIN)',
                           descricao='Mostra cada receita com os ingredientes utilizados, quantidades e '
                                     'nível de toxicidade, via Receita_Tratamentos → Criacao → Ingredientes.',
                           tipo='join',
                           dados=dados)

@app.route('/consulta/view_resumo')
def consulta_view_resumo():
    dados = get_view_resumo_clinica()
    return render_template('consulta_join.html',
                           titulo='Visão Geral da Clínica (VIEW)',
                           descricao='Relatório consolidado simulando uma VIEW de banco de dados: '
                                     'paciente, profissional, atendimento, diagnóstico e tratamento em uma única consulta.',
                           tipo='view',
                           dados=dados)


if __name__ == '__main__':
    app.run(debug=True)