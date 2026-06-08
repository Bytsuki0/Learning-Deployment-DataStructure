# models.py

from flask_mysqldb import MySQL
from MySQLdb.cursors import DictCursor

mysql = MySQL()

def get_all_emprestimos():
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""
        SELECT
            e.Codigo,
            e.Data_do_Emprestimo,
            e.Data_da_Devolucao,
            e.FK_Usuario_CPF,
            e.FK_Usuario_RG,
            u.Nome AS Usuario_Nome,
            u.Telefone AS Usuario_Telefone,
            u.Celular AS Usuario_Celular,
            u.Endereco AS Usuario_Endereco
        FROM emprestimo e
        INNER JOIN usuario u
            ON e.FK_Usuario_CPF = u.CPF
           AND e.FK_Usuario_RG = u.RG
        ORDER BY e.Codigo DESC
    """)
    result = cur.fetchall()
    cur.close()
    return result

def get_all_usuarios():
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("SELECT * FROM usuario")
    result = cur.fetchall()
    cur.close()
    return result

def adicionar_usuario(cpf, rg, nome, telefone, celular, endereco):
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO usuario (CPF, RG, Nome, Telefone, Celular, Endereco)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (cpf, rg, nome, telefone, celular, endereco))
    mysql.connection.commit()
    cur.close()

def adicionar_emprestimo(codigo, data_do_emprestimo, data_da_devolucao,
                         quantidade_de_livros,
                         fk_usuario_cpf, fk_usuario_rg):
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO emprestimo
        (Codigo, Data_do_Emprestimo, Data_da_Devolucao, Quantidade_de_Livros,
         FK_Usuario_CPF, FK_Usuario_RG)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (

        codigo,
        data_do_emprestimo,
        data_da_devolucao,
        quantidade_de_livros,
        fk_usuario_cpf,
        fk_usuario_rg
    ))
    mysql.connection.commit()
    cur.close()