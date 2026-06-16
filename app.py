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
    get_atendimentos_por_status,
    get_pacientes_por_cargo,
    get_pacientes_ordenados_idade,
    get_atendimentos_ordenados_data,
    get_profissionais_com_mais_atendimentos,
    get_ingredientes_mais_usados,
    buscar_pacientes_por_nome,
    buscar_diagnosticos_por_suspeita,
    get_paciente_by_id, atualizar_paciente, deletar_paciente,
    get_profissional_by_id, atualizar_profissional, deletar_profissional,
    get_receita_by_id, atualizar_receita, deletar_receita,
    get_ingrediente_by_id, atualizar_ingrediente, deletar_ingrediente,
    get_estatisticas, get_atendimento_by_id, atualizar_atendimento, deletar_atendimento,
    get_diagnostico_by_id, atualizar_diagnostico, deletar_diagnostico,
    get_all_cria, adicionar_cria, deletar_cria,
    get_all_criacao, get_criacao_by_ids, adicionar_criacao, atualizar_criacao, deletar_criacao,
    get_ingredientes_estoque_baixo, get_historico_completo_paciente,
)

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = '153226@#'
mysql.init_app(app)


# ───────────── INDEX ─────────────
@app.route('/')
def index():
    stats = get_estatisticas()
    return render_template('index.html', stats=stats)




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
                           titulo='Atendimentos com Diagnóstico',
                           descricao='Exibe apenas os atendimentos que possuem um diagnóstico associado, '
                                     'cruzando Atendimento → Paciente → Profissional → Diagnóstico.',
                           tipo='join',
                           dados=dados)

@app.route('/consulta/pacientes_tratamento')
def consulta_pacientes_tratamento():
    dados = get_pacientes_com_tratamento()
    return render_template('consulta_join.html',
                           titulo='Pacientes e seus Tratamentos',
                           descricao='Lista todos os pacientes, incluindo os que ainda não possuem '
                                     'diagnóstico ou tratamento registrado.',
                           tipo='left',
                           dados=dados)

@app.route('/consulta/receitas_ingredientes')
def consulta_receitas_ingredientes():
    dados = get_receitas_com_ingredientes()
    return render_template('consulta_join.html',
                           titulo='Receitas e seus Ingredientes',
                           descricao='Mostra cada receita com os ingredientes utilizados, quantidades e '
                                     'nível de toxicidade, via Receita_Tratamentos → Criacao → Ingredientes.',
                           tipo='join',
                           dados=dados)

@app.route('/consulta/view_resumo')
def consulta_view_resumo():
    dados = get_view_resumo_clinica()
    return render_template('consulta_join.html',
                           titulo='Visão Geral da Clínica',
                           descricao='Relatório consolidado simulando uma VIEW de banco de dados: '
                                     'paciente, profissional, atendimento, diagnóstico e tratamento em uma única consulta.',
                           tipo='view',
                           dados=dados)



# ───────────── CONSULTAS AVANÇADAS (GROUP BY / ORDER BY / HAVING / LIKE) ─────────────
@app.route('/consultas_avancadas')
def consultas_avancadas():
    return render_template('consultas_avancadas.html')


# ---- GROUP BY ----
@app.route('/consulta/group_by/atendimentos_status')
def consulta_group_status():
    dados = get_atendimentos_por_status()
    return render_template('consulta_avancada.html',
                           titulo='Atendimentos por Status',
                           descricao='Agrupa todos os atendimentos pelo campo Status e conta quantos '
                                     'registros existem em cada grupo, usando GROUP BY + COUNT(*).',
                           tipo='group',
                           dados=dados)

@app.route('/consulta/group_by/pacientes_cargo')
def consulta_group_pacientes_cargo():
    dados = get_pacientes_por_cargo()
    return render_template('consulta_avancada.html',
                           titulo='Pacientes por Cargo',
                           descricao='Agrupa os pacientes pelo campo Cargo, contando o total de pacientes '
                                     'e calculando a idade média de cada grupo (GROUP BY + COUNT + AVG).',
                           tipo='group',
                           dados=dados)


# ---- ORDER BY ----
@app.route('/consulta/order_by/pacientes_idade')
def consulta_order_pacientes_idade():
    dados = get_pacientes_ordenados_idade()
    return render_template('consulta_avancada.html',
                           titulo='Pacientes Ordenados por Idade',
                           descricao='Lista todos os pacientes ordenados pela Idade, do mais velho '
                                     'para o mais novo (ORDER BY Idade DESC).',
                           tipo='order',
                           dados=dados)

@app.route('/consulta/order_by/atendimentos_data')
def consulta_order_atendimentos_data():
    dados = get_atendimentos_ordenados_data()
    return render_template('consulta_avancada.html',
                           titulo='Atendimentos Ordenados por Data',
                           descricao='Lista os atendimentos ordenados por Data e Hora, do mais antigo '
                                     'para o mais recente (ORDER BY Data ASC, Hora ASC).',
                           tipo='order',
                           dados=dados)


# ---- HAVING ----
@app.route('/consulta/having/profissionais_atendimentos')
def consulta_having_profissionais():
    dados = get_profissionais_com_mais_atendimentos(2)
    return render_template('consulta_avancada.html',
                           titulo='Profissionais com 2 ou mais Atendimentos',
                           descricao='Agrupa os atendimentos por profissional e filtra, com HAVING, '
                                     'apenas aqueles que possuem 2 ou mais atendimentos registrados.',
                           tipo='having',
                           dados=dados)

@app.route('/consulta/having/ingredientes_usados')
def consulta_having_ingredientes():
    dados = get_ingredientes_mais_usados(2)
    return render_template('consulta_avancada.html',
                           titulo='Ingredientes Usados em 2 ou mais Receitas',
                           descricao='Agrupa os ingredientes pela quantidade de receitas em que aparecem '
                                     'e filtra, com HAVING, apenas os usados em 2 ou mais receitas.',
                           tipo='having',
                           dados=dados)


# ---- LIKE ----
@app.route('/consulta/like/pacientes')
def consulta_like_pacientes():
    termo = request.args.get('termo', '').strip()
    dados = buscar_pacientes_por_nome(termo) if termo else []
    return render_template('consulta_avancada.html',
                           titulo='Buscar Pacientes por Nome',
                           descricao='Pesquisa pacientes cujo Nome contenha o termo digitado, em '
                                     'qualquer posição, usando LIKE com % nos dois lados.',
                           tipo='like',
                           dados=dados,
                           termo=termo)

@app.route('/consulta/like/diagnosticos')
def consulta_like_diagnosticos():
    termo = request.args.get('termo', '').strip()
    dados = buscar_diagnosticos_por_suspeita(termo) if termo else []
    return render_template('consulta_avancada.html',
                           titulo='Buscar Diagnósticos por Suspeita',
                           descricao='Pesquisa diagnósticos cuja Suspeita_identificada contenha o termo '
                                     'digitado, em qualquer posição, usando LIKE com % nos dois lados.',
                           tipo='like',
                           dados=dados,
                           termo=termo)

# --- ROTAS DE EDIÇÃO E EXCLUSÃO ---

# Pacientes
@app.route('/editar_paciente/<codigo>', methods=['GET', 'POST'])
def editar_paciente(codigo):
    paciente = get_paciente_by_id(codigo)
    if request.method == 'POST':
        try:
            atualizar_paciente(
                codigo,
                request.form['nome'],
                request.form['idade'],
                request.form['cargo'],
                request.form['historico'],
                request.form['data_nascimento']
            )
            flash('Paciente atualizado com sucesso!', 'success')
            return redirect(url_for('pacientes'))
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Erro ao atualizar paciente: {e}', 'danger')
    return render_template('editar_paciente.html', paciente=paciente)

@app.route('/deletar_paciente/<codigo>', methods=['POST'])
def route_deletar_paciente(codigo):
    try:
        deletar_paciente(codigo)
        flash('Paciente deletado com sucesso!', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Erro ao deletar paciente: {e}', 'danger')
    return redirect(url_for('pacientes'))


# Profissionais
@app.route('/editar_profissional/<codigo>', methods=['GET', 'POST'])
def editar_profissional(codigo):
    profissional = get_profissional_by_id(codigo)
    if request.method == 'POST':
        try:
            atualizar_profissional(
                codigo,
                request.form['nome'],
                request.form['funcao'],
                request.form['especialidade']
            )
            flash('Profissional atualizado com sucesso!', 'success')
            return redirect(url_for('profissionais'))
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Erro ao atualizar profissional: {e}', 'danger')
    return render_template('editar_profissional.html', profissional=profissional)

@app.route('/deletar_profissional/<codigo>', methods=['POST'])
def route_deletar_profissional(codigo):
    try:
        deletar_profissional(codigo)
        flash('Profissional deletado com sucesso!', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Erro ao deletar profissional: {e}', 'danger')
    return redirect(url_for('profissionais'))


# Receitas
@app.route('/editar_receita/<codigo>', methods=['GET', 'POST'])
def editar_receita(codigo):
    receita = get_receita_by_id(codigo)
    if request.method == 'POST':
        try:
            atualizar_receita(
                codigo,
                request.form['codigo_tratamento'],
                request.form['dosagem'],
                request.form['nome_formula'],
                request.form['data_prescricao'],
                request.form['duracao'],
                request.form['status'],
                request.form['nome_tratamento']
            )
            flash('Receita atualizada com sucesso!', 'success')
            return redirect(url_for('receitas'))
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Erro ao atualizar receita: {e}', 'danger')
    return render_template('editar_receita.html', receita=receita)

@app.route('/deletar_receita/<codigo>', methods=['POST'])
def route_deletar_receita(codigo):
    try:
        deletar_receita(codigo)
        flash('Receita deletada com sucesso!', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Erro ao deletar receita: {e}', 'danger')
    return redirect(url_for('receitas'))


# Ingredientes
@app.route('/editar_ingrediente/<codigo>', methods=['GET', 'POST'])
def editar_ingrediente(codigo):
    ingrediente = get_ingrediente_by_id(codigo)
    if request.method == 'POST':
        try:
            atualizar_ingrediente(
                codigo,
                request.form['nome'],
                request.form['tipo'],
                request.form['quantidade'],
                request.form['origem'],
                request.form['toxicidade']
            )
            flash('Ingrediente atualizado com sucesso!', 'success')
            return redirect(url_for('ingredientes'))
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Erro ao atualizar ingrediente: {e}', 'danger')
    return render_template('editar_ingrediente.html', ingrediente=ingrediente)

@app.route('/deletar_ingrediente/<codigo>', methods=['POST'])
def route_deletar_ingrediente(codigo):
    try:
        deletar_ingrediente(codigo)
        flash('Ingrediente deletado com sucesso!', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Erro ao deletar ingrediente: {e}', 'danger')
    return redirect(url_for('ingredientes'))

# ───────────── ATENDIMENTO (EDIÇÃO / EXCLUSÃO) ─────────────
@app.route('/editar_atendimento/<codigo>', methods=['GET', 'POST'])
def editar_atendimento(codigo):
    atendimento = get_atendimento_by_id(codigo)
    if request.method == 'POST':
        try:
            atualizar_atendimento(
                codigo,
                request.form['codigo_profissional'],
                request.form['codigo_paciente'],
                request.form['data'],
                request.form['hora'],
                request.form['status']
            )
            flash('Atendimento atualizado com sucesso!', 'success')
            return redirect(url_for('atendimentos'))
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Erro ao atualizar atendimento: {e}', 'danger')
            
    # Carregamos pacientes e profissionais para preencher os <select> dropdowns
    pacientes = get_all_pacientes()
    profissionais = get_all_profissionais()
    return render_template('editar_atendimento.html', 
                           atendimento=atendimento, 
                           pacientes=pacientes, 
                           profissionais=profissionais)

@app.route('/deletar_atendimento/<codigo>', methods=['POST'])
def route_deletar_atendimento(codigo):
    try:
        deletar_atendimento(codigo)
        flash('Atendimento deletado com sucesso!', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Erro ao deletar atendimento: {e}', 'danger')
    return redirect(url_for('atendimentos'))


# ───────────── DIAGNÓSTICO (EDIÇÃO / EXCLUSÃO) ─────────────
@app.route('/editar_diagnostico/<codigo>', methods=['GET', 'POST'])
def editar_diagnostico(codigo):
    diagnostico = get_diagnostico_by_id(codigo)
    if request.method == 'POST':
        try:
            atualizar_diagnostico(
                codigo,
                request.form['id_paciente'],
                request.form['id_profissional'],
                request.form['descricao'],
                request.form['suspeita'],
                request.form['data_avaliacao']
            )
            flash('Diagnóstico atualizado com sucesso!', 'success')
            return redirect(url_for('diagnosticos'))
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Erro ao atualizar diagnóstico: {e}', 'danger')
            
    # Carregamos pacientes e profissionais para preencher os <select> dropdowns
    pacientes = get_all_pacientes()
    profissionais = get_all_profissionais()
    return render_template('editar_diagnostico.html', 
                           diagnostico=diagnostico, 
                           pacientes=pacientes, 
                           profissionais=profissionais)

@app.route('/deletar_diagnostico/<codigo>', methods=['POST'])
def route_deletar_diagnostico(codigo):
    try:
        deletar_diagnostico(codigo)
        flash('Diagnóstico deletado com sucesso!', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Erro ao deletar diagnóstico: {e}', 'danger')
    return redirect(url_for('diagnosticos'))


# ───────────── CRIA (Profissional ↔ Receita) ─────────────
@app.route('/cria')
def cria():
    dados = get_all_cria()
    return render_template('cria.html', cria=dados)

@app.route('/cadastro_cria', methods=['GET', 'POST'])
def cadastro_cria():
    if request.method == 'POST':
        try:
            adicionar_cria(
                request.form['codigo_receita'],
                request.form['codigo_profissional'],
            )
            flash('Associação Profissional ↔ Receita criada com sucesso!', 'success')
            return redirect(url_for('cria'))
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Erro ao criar associação: {e}', 'danger')
            return redirect(url_for('cadastro_cria'))
    receitas = get_all_receitas()
    profissionais = get_all_profissionais()
    return render_template('cadastro_cria.html', receitas=receitas, profissionais=profissionais)

@app.route('/deletar_cria/<int:cod_receita>/<int:cod_profissional>', methods=['POST'])
def route_deletar_cria(cod_receita, cod_profissional):
    try:
        deletar_cria(cod_receita, cod_profissional)
        flash('Associação removida com sucesso!', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Erro ao remover associação: {e}', 'danger')
    return redirect(url_for('cria'))


# ───────────── CRIACAO (Receita ↔ Ingrediente) ─────────────
@app.route('/criacao')
def criacao():
    dados = get_all_criacao()
    return render_template('criacao.html', criacao=dados)

@app.route('/cadastro_criacao', methods=['GET', 'POST'])
def cadastro_criacao():
    if request.method == 'POST':
        try:
            adicionar_criacao(
                request.form['codigo_receita'],
                request.form['codigo_ingrediente'],
                request.form['quantidade'],
            )
            flash('Ingrediente adicionado à receita com sucesso!', 'success')
            return redirect(url_for('criacao'))
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Erro ao adicionar ingrediente à receita: {e}', 'danger')
            return redirect(url_for('cadastro_criacao'))
    receitas = get_all_receitas()
    ingredientes = get_all_ingredientes()
    return render_template('cadastro_criacao.html', receitas=receitas, ingredientes=ingredientes)

@app.route('/editar_criacao/<int:cod_receita>/<int:cod_ingrediente>', methods=['GET', 'POST'])
def editar_criacao(cod_receita, cod_ingrediente):
    criacao_item = get_criacao_by_ids(cod_receita, cod_ingrediente)
    if request.method == 'POST':
        try:
            atualizar_criacao(cod_receita, cod_ingrediente, request.form['quantidade'])
            flash('Quantidade atualizada com sucesso!', 'success')
            return redirect(url_for('criacao'))
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Erro ao atualizar quantidade: {e}', 'danger')
    receitas = get_all_receitas()
    ingredientes = get_all_ingredientes()
    return render_template('editar_criacao.html',
                           criacao=criacao_item,
                           receitas=receitas,
                           ingredientes=ingredientes)

@app.route('/deletar_criacao/<int:cod_receita>/<int:cod_ingrediente>', methods=['POST'])
def route_deletar_criacao(cod_receita, cod_ingrediente):
    try:
        deletar_criacao(cod_receita, cod_ingrediente)
        flash('Ingrediente removido da receita com sucesso!', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Erro ao remover ingrediente: {e}', 'danger')
    return redirect(url_for('criacao'))


@app.route('/consulta/estoque_baixo')
def consulta_estoque_baixo():
    limite = request.args.get('limite', 10, type=int)
    dados = get_ingredientes_estoque_baixo(limite)
    return render_template('consulta_avancada.html',
                           titulo='Ingredientes com Estoque Baixo',
                           descricao=f'Lista ingredientes com quantidade disponível menor ou igual a {limite}, '
                                     'ordenados do mais crítico para o menos crítico.',
                           tipo='estoque',
                           dados=dados,
                           limite=limite)

@app.route('/consulta/historico_paciente')
def consulta_historico_paciente():
    codigo = request.args.get('codigo', '').strip()
    dados = get_historico_completo_paciente(codigo) if codigo else []
    return render_template('consulta_avancada.html',
                           titulo='Histórico Completo do Paciente',
                           descricao='Exibe todos os atendimentos, diagnósticos e tratamentos de um paciente, '
                                     'em ordem cronológica decrescente.',
                           tipo='historico',
                           dados=dados,
                           termo=codigo)


if __name__ == '__main__':
    app.run(debug=True)