# Importa a classe MySQL do pacote flask_mysqldb
# Essa classe faz a ponte entre o Flask e o banco de dados MySQL
from flask_mysqldb import MySQL

# Cria a instância do MySQL
# Essa instância será inicializada posteriormente no app Flask
# Exemplo no app.py:
#   mysql.init_app(app)
mysql = MySQL()

def get_all_emprestimos():
    # Cria um cursor a partir da conexão MySQL
    # O cursor é usado para executar comandos SQL
    cur = mysql.connection.cursor()
    # Executa a consulta SQL que seleciona todos os registros
    # da tabela 'emprestimo'
    cur.execute("SELECT * FROM emprestimo")
    # Recupera todos os registros retornados pela consulta
    # O resultado será normalmente uma lista de tuplas
    result = cur.fetchall()
    # Fecha o cursor para liberar recursos do banco de dados
    cur.close()
    # Retorna os dados obtidos na consulta
    return result

def get_all_usuarios() -> object:
    # Cria um cursor a partir da conexão MySQL
    # Esse cursor permitirá executar comandos SQL
    cur = mysql.connection.cursor()
    # Executa a consulta SQL que seleciona todos os registros
    # da tabela 'usuario'
    cur.execute("SELECT * FROM usuario")
    # Recupera todos os registros retornados pela consulta
    # O resultado geralmente é uma lista de tuplas
    result = cur.fetchall()
    # Fecha o cursor após o uso para evitar vazamento de recursos
    cur.close()
    # Retorna a lista de usuários obtida do banco
    return result

def adicionar_usuario(cpf, rg, nome, telefone, 
                      celular, endereco):
    # Cria um cursor a partir da conexão MySQL
    # Ele será usado para executar o comando INSERT
    cur = mysql.connection.cursor()
    # Executa o comando SQL de inserção de um novo usuário
    # Os %s são placeholders que evitam SQL Injection
    # Os valores reais são passados separadamente na tupla
    cur.execute("""
        INSERT INTO usuario (CPF, RG, Nome, 
                Telefone, Celular, Endereco)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (cpf, rg, nome, telefone, celular, endereco))
    # Confirma a transação, salvando definitivamente os dados no banco
    mysql.connection.commit()
    # Fecha o cursor após a execução do comando
    cur.close()