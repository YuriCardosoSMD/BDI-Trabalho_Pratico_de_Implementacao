import psycopg2

# Conectar-se ao banco de dados (altere a senha para a do seu PostgreSQL)
def conectar():
    return psycopg2.connect(user="postgres", password="8945", host="localhost", port="5432", database="sistema_farmacia")
