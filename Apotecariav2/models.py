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
    cur.execute("""
        INSERT INTO Pacientes
            (Codigo_Paciente, Nome, Idade, Cargo, Historico_medico, Data_nascimento)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (codigo, nome, idade, cargo, historico, data_nasc))
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
    cur.execute("""
        INSERT INTO Profissionais_enfermaria
            (Codigo_profissional, Nome, Funcao, Especialidade)
        VALUES (%s, %s, %s, %s)
    """, (codigo, nome, funcao, especialidade))
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

# ─────────────────────────────────────────
# CONSULTAS ESPECIAIS (JOIN / LEFT JOIN / VIEW)
# ─────────────────────────────────────────

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
    Liga Paciente → Diagnóstico → Resultado → Receita_Tratamentos.
    """
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""
        SELECT
            p.Codigo_Paciente,
            p.Nome          AS Paciente_Nome,
            p.Idade,
            p.Cargo,
            d.Suspeita_identificada,
            d.Data_avaliacao,
            rt.Nome_tratamento,
            rt.Dosagem,
            rt.Status       AS Status_Tratamento,
            rt.Duracao
        FROM Pacientes p
        LEFT JOIN Diagnostico d
            ON d.idPacientes = p.Codigo_Paciente
        LEFT JOIN Resultado r
            ON r.Codigo_Diagnostico = d.Codigo_Diagnostico
        LEFT JOIN Receita_Tratamentos rt
            ON rt.Codigo_tratamento = r.Codigo_tratamento
        ORDER BY p.Codigo_Paciente
    """)
    result = cur.fetchall()
    cur.close()
    return result

def get_receitas_com_ingredientes():
    """
    INNER JOIN: receitas com seus ingredientes e quantidades.
    Liga Receita_Tratamentos → Criacao → Ingredientes.
    """
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""
        SELECT
            rt.Codigo_receita,
            rt.Nome_formula,
            rt.Dosagem,
            rt.Data_prescricao,
            i.Nome          AS Ingrediente_Nome,
            i.Tipo,
            i.Nivel_toxicidade,
            c.Quantidade_ingrediente
        FROM Receita_Tratamentos rt
        INNER JOIN Criacao c
            ON c.Codigo_receita = rt.Codigo_receita
        INNER JOIN Ingredientes i
            ON i.Codigo_ingrediente = c.Codigo_ingrediente
        ORDER BY rt.Codigo_receita, i.Nome
    """)
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
        SELECT
            p.Nome              AS Paciente,
            p.Idade,
            pr.Nome             AS Profissional,
            pr.Especialidade,
            a.Data              AS Data_Atendimento,
            a.Status            AS Status_Atendimento,
            d.Suspeita_identificada AS Suspeita,
            rt.Nome_tratamento  AS Tratamento,
            rt.Dosagem,
            rt.Duracao,
            rt.Status           AS Status_Tratamento
        FROM Atendimento a
        INNER JOIN Pacientes p
            ON a.Codigo_Paciente = p.Codigo_Paciente
        INNER JOIN Profissionais_enfermaria pr
            ON a.Codigo_profissional = pr.Codigo_profissional
        LEFT JOIN Diagnostico d
            ON d.idPacientes = p.Codigo_Paciente
           AND d.idProfissionais_enfermaria = pr.Codigo_profissional
        LEFT JOIN Resultado r
            ON r.Codigo_Diagnostico = d.Codigo_Diagnostico
        LEFT JOIN Receita_Tratamentos rt
            ON rt.Codigo_tratamento = r.Codigo_tratamento
        ORDER BY a.Data DESC
    """)
    result = cur.fetchall()
    cur.close()
    return result