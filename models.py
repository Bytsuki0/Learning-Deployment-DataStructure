# models.py — clinica database

from flask_mysqldb import MySQL
from MySQLdb.cursors import DictCursor

mysql = MySQL()

# ─────────────────────────────────────────
# PACIENTES
# ─────────────────────────────────────────
def get_all_pacientes():
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("SELECT * FROM Pacientes ORDER BY Codigo_Paciente DESC")
    result = cur.fetchall()
    cur.close()
    return result

def adicionar_paciente(codigo, nome, idade, cargo, historico, data_nasc):
    cur = mysql.connection.cursor()
    # Chama a função criada no banco de dados passando os parâmetros
    cur.execute("call pr_adicionar_paciente(%s, %s, %s, %s, %s, %s)", 
                (codigo, nome, idade, cargo, historico, data_nasc))
    mysql.connection.commit()
    cur.close()

# ─────────────────────────────────────────
# PROFISSIONAIS
# ─────────────────────────────────────────
def get_all_profissionais():
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("SELECT * FROM Profissionais_enfermaria ORDER BY Codigo_profissional DESC")
    result = cur.fetchall()
    cur.close()
    return result

def adicionar_profissional(codigo, nome, funcao, especialidade):
    cur = mysql.connection.cursor()
    # Chama a função criada no banco de dados passando os parâmetros
    cur.execute("call pr_adicionar_profissional(%s, %s, %s, %s)", 
                (codigo, nome, funcao, especialidade))
    mysql.connection.commit()
    cur.close()
# ─────────────────────────────────────────
# ATENDIMENTO
# ─────────────────────────────────────────
def get_all_atendimentos():
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""
        SELECT
            a.Codigo_atendimento,
            a.Data,
            a.Hora,
            a.Status,
            p.Nome   AS Paciente_Nome,
            pr.Nome  AS Profissional_Nome,
            pr.Funcao
        FROM Atendimento a
        INNER JOIN Pacientes p
            ON a.Codigo_Paciente = p.Codigo_Paciente
        INNER JOIN Profissionais_enfermaria pr
            ON a.Codigo_profissional = pr.Codigo_profissional
        ORDER BY a.Data DESC, a.Hora DESC
    """)
    result = cur.fetchall()
    cur.close()
    return result

def adicionar_atendimento(codigo, cod_prof, cod_pac, data, hora, status):
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO Atendimento
            (Codigo_atendimento, Codigo_profissional, Codigo_Paciente, Data, Hora, Status)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (codigo, cod_prof, cod_pac, data, hora, status))
    mysql.connection.commit()
    cur.close()

# ─────────────────────────────────────────
# DIAGNÓSTICO
# ─────────────────────────────────────────
def get_all_diagnosticos():
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""
        SELECT
            d.Codigo_Diagnostico,
            d.Descricao,
            d.Suspeita_identificada,
            d.Data_avaliacao,
            p.Nome  AS Paciente_Nome,
            pr.Nome AS Profissional_Nome
        FROM Diagnostico d
        INNER JOIN Pacientes p
            ON d.idPacientes = p.Codigo_Paciente
        INNER JOIN Profissionais_enfermaria pr
            ON d.idProfissionais_enfermaria = pr.Codigo_profissional
        ORDER BY d.Data_avaliacao DESC
    """)
    result = cur.fetchall()
    cur.close()
    return result

def adicionar_diagnostico(codigo, id_pac, id_prof, descricao, suspeita, data_av):
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO Diagnostico
            (Codigo_Diagnostico, idPacientes, idProfissionais_enfermaria,
             Descricao, Suspeita_identificada, Data_avaliacao)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (codigo, id_pac, id_prof, descricao, suspeita, data_av))
    mysql.connection.commit()
    cur.close()

# ─────────────────────────────────────────
# RECEITA / TRATAMENTO
# ─────────────────────────────────────────
def get_all_receitas():
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""
        SELECT * FROM Receita_Tratamentos
        ORDER BY Codigo_receita DESC
    """)
    result = cur.fetchall()
    cur.close()
    return result

def adicionar_receita(cod_rec, cod_trat, dosagem, nome_formula,
                      data_presc, duracao, status, nome_trat):
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO Receita_Tratamentos
            (Codigo_receita, Codigo_tratamento, Dosagem, Nome_formula,
             Data_prescricao, Duracao, Status, Nome_tratamento)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (cod_rec, cod_trat, dosagem, nome_formula,
          data_presc, duracao, status, nome_trat))
    mysql.connection.commit()
    cur.close()

# ─────────────────────────────────────────
# INGREDIENTES
# ─────────────────────────────────────────
def get_all_ingredientes():
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("SELECT * FROM Ingredientes ORDER BY Codigo_ingrediente DESC")
    result = cur.fetchall()
    cur.close()
    return result

def adicionar_ingrediente(codigo, nome, tipo, qtd, origem, toxicidade):
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO Ingredientes
            (Codigo_ingrediente, Nome, Tipo, Quantidade_disponivel, Origem, Nivel_toxicidade)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (codigo, nome, tipo, qtd, origem, toxicidade))
    mysql.connection.commit()
    cur.close()


def get_atendimentos_com_diagnostico():
    """
    INNER JOIN: atendimentos que possuem diagnóstico associado.
    Liga Atendimento → Diagnóstico via Paciente + Profissional.
    """
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""
        SELECT
            a.Codigo_atendimento,
            a.Data        AS Data_Atendimento,
            a.Hora,
            a.Status      AS Status_Atendimento,
            p.Nome        AS Paciente_Nome,
            pr.Nome       AS Profissional_Nome,
            pr.Especialidade,
            d.Codigo_Diagnostico,
            d.Suspeita_identificada,
            d.Data_avaliacao
        FROM Atendimento a
        INNER JOIN Pacientes p
            ON a.Codigo_Paciente = p.Codigo_Paciente
        INNER JOIN Profissionais_enfermaria pr
            ON a.Codigo_profissional = pr.Codigo_profissional
        INNER JOIN Diagnostico d
            ON d.idPacientes = p.Codigo_Paciente
           AND d.idProfissionais_enfermaria = pr.Codigo_profissional
        ORDER BY a.Data DESC
    """)
    result = cur.fetchall()
    cur.close()
    return result

def get_pacientes_com_tratamento():
    """
    LEFT JOIN: todos os pacientes, mesmo sem diagnóstico ou tratamento.
    Usa a Stored Procedure 'sp_get_pacientes_com_tratamento'.
    """
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("CALL sp_get_pacientes_com_tratamento()")
    result = cur.fetchall()
    cur.close()
    return result

def get_receitas_com_ingredientes():
    """
    INNER JOIN: receitas com seus ingredientes e quantidades.
    Usa a Stored Procedure 'sp_get_receitas_com_ingredientes'.
    """
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("CALL sp_get_receitas_com_ingredientes()")
    result = cur.fetchall()
    cur.close()
    return result

# ─────────────────────────────────────────
# CONSULTAS AVANÇADAS (GROUP BY / ORDER BY / HAVING / LIKE)
# ─────────────────────────────────────────

# ---- GROUP BY (exemplo 1) ----
def get_atendimentos_por_status():
    """
    GROUP BY: conta quantos atendimentos existem para cada Status.
    """
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""
        SELECT
            Status,
            COUNT(*) AS Total_Atendimentos
        FROM Atendimento
        GROUP BY Status
        ORDER BY Total_Atendimentos DESC
    """)
    result = cur.fetchall()
    cur.close()
    return result

# ---- GROUP BY (exemplo 2) ----
def get_pacientes_por_cargo():
    """
    GROUP BY: agrupa os pacientes por Cargo, contando o total
    e calculando a idade média de cada grupo.
    """
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""
        SELECT
            Cargo,
            COUNT(*) AS Total_Pacientes,
            ROUND(AVG(Idade), 1) AS Idade_Media
        FROM Pacientes
        GROUP BY Cargo
        ORDER BY Total_Pacientes DESC
    """)
    result = cur.fetchall()
    cur.close()
    return result

# ---- ORDER BY (exemplo 1) ----
def get_pacientes_ordenados_idade():
    """
    ORDER BY: lista todos os pacientes ordenados pela idade,
    do mais velho para o mais novo.
    """
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""
        SELECT
            Codigo_Paciente,
            Nome,
            Idade,
            Cargo,
            Data_nascimento
        FROM Pacientes
        ORDER BY Idade DESC
    """)
    result = cur.fetchall()
    cur.close()
    return result

# ---- ORDER BY (exemplo 2) ----
def get_atendimentos_ordenados_data():
    """
    ORDER BY: lista os atendimentos ordenados por data e hora,
    do mais antigo para o mais recente.
    """
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""
        SELECT
            a.Codigo_atendimento,
            p.Nome  AS Paciente_Nome,
            pr.Nome AS Profissional_Nome,
            a.Data,
            a.Hora,
            a.Status
        FROM Atendimento a
        INNER JOIN Pacientes p
            ON a.Codigo_Paciente = p.Codigo_Paciente
        INNER JOIN Profissionais_enfermaria pr
            ON a.Codigo_profissional = pr.Codigo_profissional
        ORDER BY a.Data ASC, a.Hora ASC
    """)
    result = cur.fetchall()
    cur.close()
    return result

# ---- HAVING (exemplo 1) ----
def get_profissionais_com_mais_atendimentos(minimo=2):
    """
    GROUP BY + HAVING: agrupa os atendimentos por profissional
    e retorna apenas aqueles com pelo menos `minimo` atendimentos.
    """
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""
        SELECT
            pr.Codigo_profissional,
            pr.Nome,
            pr.Funcao,
            COUNT(a.Codigo_atendimento) AS Total_Atendimentos
        FROM Profissionais_enfermaria pr
        INNER JOIN Atendimento a
            ON a.Codigo_profissional = pr.Codigo_profissional
        GROUP BY pr.Codigo_profissional, pr.Nome, pr.Funcao
        HAVING COUNT(a.Codigo_atendimento) >= %s
        ORDER BY Total_Atendimentos DESC
    """, (minimo,))
    result = cur.fetchall()
    cur.close()
    return result

# ---- HAVING (exemplo 2) ----
def get_ingredientes_mais_usados(minimo=2):
    """
    GROUP BY + HAVING: agrupa os ingredientes pela quantidade de
    receitas em que aparecem, retornando apenas os usados em
    pelo menos `minimo` receitas.
    """
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""
        SELECT
            i.Codigo_ingrediente,
            i.Nome,
            i.Tipo,
            i.Nivel_toxicidade,
            COUNT(c.Codigo_receita) AS Total_Receitas,
            SUM(c.Quantidade_ingrediente) AS Quantidade_Total
        FROM Ingredientes i
        INNER JOIN Criacao c
            ON c.Codigo_ingrediente = i.Codigo_ingrediente
        GROUP BY i.Codigo_ingrediente, i.Nome, i.Tipo, i.Nivel_toxicidade
        HAVING COUNT(c.Codigo_receita) >= %s
        ORDER BY Total_Receitas DESC
    """, (minimo,))
    result = cur.fetchall()
    cur.close()
    return result

# ---- LIKE (exemplo 1) ----
def buscar_pacientes_por_nome(termo):
    """
    LIKE: busca pacientes cujo Nome contenha o termo informado,
    em qualquer posição (uso de % nos dois lados).
    """
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""
        SELECT
            Codigo_Paciente,
            Nome,
            Idade,
            Cargo,
            Data_nascimento
        FROM Pacientes
        WHERE Nome LIKE %s
        ORDER BY Nome
    """, (f'%{termo}%',))
    result = cur.fetchall()
    cur.close()
    return result

# ---- LIKE (exemplo 2) ----
def buscar_diagnosticos_por_suspeita(termo):
    """
    LIKE: busca diagnósticos cuja Suspeita_identificada contenha
    o termo informado, em qualquer posição (uso de % nos dois lados).
    """
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""
        SELECT
            d.Codigo_Diagnostico,
            d.Descricao,
            d.Suspeita_identificada,
            d.Data_avaliacao,
            p.Nome  AS Paciente_Nome,
            pr.Nome AS Profissional_Nome
        FROM Diagnostico d
        INNER JOIN Pacientes p
            ON d.idPacientes = p.Codigo_Paciente
        INNER JOIN Profissionais_enfermaria pr
            ON d.idProfissionais_enfermaria = pr.Codigo_profissional
        WHERE d.Suspeita_identificada LIKE %s
        ORDER BY d.Data_avaliacao DESC
    """, (f'%{termo}%',))
    result = cur.fetchall()
    cur.close()
    return result


def get_view_resumo_clinica():
    """
    Simulates a DB VIEW: summary of all appointments with patient,
    professional, diagnosis, treatment, and prescription details.
    """
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""
        select * from ViewClinica
    """)
    result = cur.fetchall()
    cur.close()    
    return result



# ─────────────────────────────────────────
# FUNÇÕES DE ATUALIZAÇÃO E EXCLUSÃO (CRUD)
# ─────────────────────────────────────────

# ---- PACIENTES ----
def get_paciente_by_id(codigo):
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("SELECT * FROM Pacientes WHERE Codigo_Paciente = %s", (codigo,))
    result = cur.fetchone()
    cur.close()
    return result

def atualizar_paciente(codigo, nome, idade, cargo, historico, data_nasc):
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE Pacientes
        SET Nome = %s, Idade = %s, Cargo = %s, Historico_medico = %s, Data_nascimento = %s
        WHERE Codigo_Paciente = %s
    """, (nome, idade, cargo, historico, data_nasc, codigo))
    mysql.connection.commit()
    cur.close()

def deletar_paciente(codigo):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Pacientes WHERE Codigo_Paciente = %s", (codigo,))
    mysql.connection.commit()
    cur.close()


# ---- PROFISSIONAIS ----
def get_profissional_by_id(codigo):
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("SELECT * FROM Profissionais_enfermaria WHERE Codigo_profissional = %s", (codigo,))
    result = cur.fetchone()
    cur.close()
    return result

def atualizar_profissional(codigo, nome, funcao, especialidade):
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE Profissionais_enfermaria
        SET Nome = %s, Funcao = %s, Especialidade = %s
        WHERE Codigo_profissional = %s
    """, (nome, funcao, especialidade, codigo))
    mysql.connection.commit()
    cur.close()

def deletar_profissional(codigo):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Profissionais_enfermaria WHERE Codigo_profissional = %s", (codigo,))
    mysql.connection.commit()
    cur.close()


# ---- RECEITAS / TRATAMENTOS ----
def get_receita_by_id(codigo):
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("SELECT * FROM Receita_Tratamentos WHERE Codigo_receita = %s", (codigo,))
    result = cur.fetchone()
    cur.close()
    return result

def atualizar_receita(cod_rec, cod_trat, dosagem, nome_formula, data_presc, duracao, status, nome_trat):
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE Receita_Tratamentos
        SET Codigo_tratamento = %s, Dosagem = %s, Nome_formula = %s,
            Data_prescricao = %s, Duracao = %s, Status = %s, Nome_tratamento = %s
        WHERE Codigo_receita = %s
    """, (cod_trat, dosagem, nome_formula, data_presc, duracao, status, nome_trat, cod_rec))
    mysql.connection.commit()
    cur.close()

def deletar_receita(codigo):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Receita_Tratamentos WHERE Codigo_receita = %s", (codigo,))
    mysql.connection.commit()
    cur.close()


# ---- INGREDIENTES ----
def get_ingrediente_by_id(codigo):
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("SELECT * FROM Ingredientes WHERE Codigo_ingrediente = %s", (codigo,))
    result = cur.fetchone()
    cur.close()
    return result

def atualizar_ingrediente(codigo, nome, tipo, qtd, origem, toxicidade):
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE Ingredientes
        SET Nome = %s, Tipo = %s, Quantidade_disponivel = %s, Origem = %s, Nivel_toxicidade = %s
        WHERE Codigo_ingrediente = %s
    """, (nome, tipo, qtd, origem, toxicidade, codigo))
    mysql.connection.commit()
    cur.close()

def deletar_ingrediente(codigo):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Ingredientes WHERE Codigo_ingrediente = %s", (codigo,))
    mysql.connection.commit()
    cur.close()
    

def get_ingredientes_estoque_baixo(limite=10):
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""
        SELECT
            Codigo_ingrediente,
            Nome,
            Tipo,
            Quantidade_disponivel,
            Origem,
            Nivel_toxicidade
        FROM Ingredientes
        WHERE Quantidade_disponivel <= %s
        ORDER BY Quantidade_disponivel ASC
    """, (limite,))
    result = cur.fetchall()
    cur.close()
    return result

def get_historico_completo_paciente(codigo_paciente):
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""
        SELECT
            p.Nome                  AS Paciente,
            a.Data                  AS Data_Atendimento,
            a.Hora,
            a.Status                AS Status_Atendimento,
            pr.Nome                 AS Profissional,
            pr.Especialidade,
            d.Descricao             AS Descricao_Diagnostico,
            d.Suspeita_identificada,
            d.Data_avaliacao,
            rt.Nome_tratamento      AS Tratamento,
            rt.Dosagem,
            rt.Duracao,
            rt.Status               AS Status_Tratamento
        FROM Pacientes p
        LEFT JOIN Atendimento a
            ON a.Codigo_Paciente = p.Codigo_Paciente
        LEFT JOIN Profissionais_enfermaria pr
            ON a.Codigo_profissional = pr.Codigo_profissional
        LEFT JOIN Diagnostico d
            ON d.idPacientes = p.Codigo_Paciente
           AND d.idProfissionais_enfermaria = pr.Codigo_profissional
        LEFT JOIN Resultado r
            ON r.Codigo_Diagnostico = d.Codigo_Diagnostico
        LEFT JOIN Receita_Tratamentos rt
            ON rt.Codigo_tratamento = r.Codigo_tratamento
        WHERE p.Codigo_Paciente = %s
        ORDER BY a.Data DESC, a.Hora DESC
    """, (codigo_paciente,))
    result = cur.fetchall()
    cur.close()
    return result

def get_estatisticas():
    """
    Busca a linha de métricas e totais da tabela Estatisticas.
    """
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("SELECT * FROM Estatisticas WHERE id = 1")
    result = cur.fetchone()
    cur.close()
    
    # Caso a tabela esteja vazia por algum motivo, retorna valores zerados padrão
    if not result:
        return {
            'numero_pacientes': 0, 
            'numero_profissionais': 0, 
            'numero_pacientes_atendimento': 0
        }
    return result


# ---- ATENDIMENTOS (CRUD) ----
def get_atendimento_by_id(codigo):
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("SELECT * FROM Atendimento WHERE Codigo_atendimento = %s", (codigo,))
    result = cur.fetchone()
    cur.close()
    return result

def atualizar_atendimento(codigo, cod_prof, cod_pac, data, hora, status):
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE Atendimento
        SET Codigo_profissional = %s, Codigo_Paciente = %s, Data = %s, Hora = %s, Status = %s
        WHERE Codigo_atendimento = %s
    """, (cod_prof, cod_pac, data, hora, status, codigo))
    mysql.connection.commit()
    cur.close()

def deletar_atendimento(codigo):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Atendimento WHERE Codigo_atendimento = %s", (codigo,))
    mysql.connection.commit()
    cur.close()


# ---- DIAGNÓSTICOS (CRUD) ----
def get_diagnostico_by_id(codigo):
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("SELECT * FROM Diagnostico WHERE Codigo_Diagnostico = %s", (codigo,))
    result = cur.fetchone()
    cur.close()
    return result

def atualizar_diagnostico(codigo, id_pac, id_prof, descricao, suspeita, data_av):
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE Diagnostico
        SET idPacientes = %s, idProfissionais_enfermaria = %s, Descricao = %s, Suspeita_identificada = %s, Data_avaliacao = %s
        WHERE Codigo_Diagnostico = %s
    """, (id_pac, id_prof, descricao, suspeita, data_av, codigo))
    mysql.connection.commit()
    cur.close()

def deletar_diagnostico(codigo):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Diagnostico WHERE Codigo_Diagnostico = %s", (codigo,))
    mysql.connection.commit()
    cur.close()


# ─────────────────────────────────────────
# CRIA (Profissional ↔ Receita)
# ─────────────────────────────────────────
def get_all_cria():
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""
        SELECT
            c.Codigo_receita,
            c.Codigo_profissional,
            rt.Nome_formula,
            rt.Nome_tratamento,
            pr.Nome  AS Profissional_Nome,
            pr.Funcao
        FROM Cria c
        INNER JOIN Receita_Tratamentos rt
            ON rt.Codigo_receita = c.Codigo_receita
        INNER JOIN Profissionais_enfermaria pr
            ON pr.Codigo_profissional = c.Codigo_profissional
        ORDER BY c.Codigo_receita
    """)
    result = cur.fetchall()
    cur.close()
    return result

def adicionar_cria(cod_receita, cod_profissional):
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO Cria (Codigo_receita, Codigo_profissional)
        VALUES (%s, %s)
    """, (cod_receita, cod_profissional))
    mysql.connection.commit()
    cur.close()

def deletar_cria(cod_receita, cod_profissional):
    cur = mysql.connection.cursor()
    cur.execute("""
        DELETE FROM Cria WHERE Codigo_receita = %s AND Codigo_profissional = %s
    """, (cod_receita, cod_profissional))
    mysql.connection.commit()
    cur.close()


# ─────────────────────────────────────────
# CRIACAO (Receita ↔ Ingrediente)
# ─────────────────────────────────────────
def get_all_criacao():
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""
        SELECT
            c.Codigo_receita,
            c.Codigo_ingrediente,
            c.Quantidade_ingrediente,
            rt.Nome_formula,
            i.Nome  AS Ingrediente_Nome,
            i.Tipo,
            i.Nivel_toxicidade
        FROM Criacao c
        INNER JOIN Receita_Tratamentos rt
            ON rt.Codigo_receita = c.Codigo_receita
        INNER JOIN Ingredientes i
            ON i.Codigo_ingrediente = c.Codigo_ingrediente
        ORDER BY c.Codigo_receita, i.Nome
    """)
    result = cur.fetchall()
    cur.close()
    return result

def get_criacao_by_ids(cod_receita, cod_ingrediente):
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""
        SELECT
            c.Codigo_receita,
            c.Codigo_ingrediente,
            c.Quantidade_ingrediente,
            rt.Nome_formula,
            i.Nome AS Ingrediente_Nome
        FROM Criacao c
        INNER JOIN Receita_Tratamentos rt ON rt.Codigo_receita = c.Codigo_receita
        INNER JOIN Ingredientes i ON i.Codigo_ingrediente = c.Codigo_ingrediente
        WHERE c.Codigo_receita = %s AND c.Codigo_ingrediente = %s
    """, (cod_receita, cod_ingrediente))
    result = cur.fetchone()
    cur.close()
    return result

def adicionar_criacao(cod_receita, cod_ingrediente, quantidade):
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO Criacao (Codigo_receita, Codigo_ingrediente, Quantidade_ingrediente)
        VALUES (%s, %s, %s)
    """, (cod_receita, cod_ingrediente, quantidade))
    mysql.connection.commit()
    cur.close()

def atualizar_criacao(cod_receita, cod_ingrediente, quantidade):
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE Criacao SET Quantidade_ingrediente = %s
        WHERE Codigo_receita = %s AND Codigo_ingrediente = %s
    """, (quantidade, cod_receita, cod_ingrediente))
    mysql.connection.commit()
    cur.close()

def deletar_criacao(cod_receita, cod_ingrediente):
    cur = mysql.connection.cursor()
    cur.execute("""
        DELETE FROM Criacao WHERE Codigo_receita = %s AND Codigo_ingrediente = %s
    """, (cod_receita, cod_ingrediente))
    mysql.connection.commit()
    cur.close()