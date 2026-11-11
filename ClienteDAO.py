from Conexao import conectar
from Cliente import Cliente


# Classe DAO da entidade cliente
class ClienteDAO:

    # Lista todos os clientes (SELECT)
    def listar_todos(self):
        resultado = []
        try:
            with conectar() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT id_cliente, nome FROM cliente ORDER BY id_cliente")
                    for linha in cursor.fetchall():
                        resultado.append(Cliente(linha[0], linha[1]))
        except Exception as erro:
            print(f"Erro ao listar clientes: {erro}")
        return resultado

    # Busca um cliente pelo código (SELECT)
    def buscar(self, codigo):
        try:
            with conectar() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT id_cliente, nome FROM cliente WHERE id_cliente = %s", (codigo,))
                    linha = cursor.fetchone()
                    if linha:
                        return Cliente(linha[0], linha[1])
        except Exception as erro:
            print(f"Erro ao buscar cliente: {erro}")
        return None

    # Insere um novo cliente (INSERT)
    def inserir(self, nome):
        try:
            with conectar() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO cliente (nome) VALUES (%s)", (nome,))
                    return cursor.rowcount == 1
        except Exception as erro:
            print(f"Erro ao inserir cliente: {erro}")
        return False

    # Atualiza o nome de um cliente (UPDATE)
    def atualizar(self, nome, codigo):
        try:
            with conectar() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE cliente SET nome = %s WHERE id_cliente = %s", (nome, codigo))
                    return cursor.rowcount == 1
        except Exception as erro:
            print(f"Erro ao atualizar cliente: {erro}")
        return False

    # Remove um cliente (DELETE) - falha se o cliente tiver vendas (chave estrangeira)
    def remover(self, codigo):
        try:
            with conectar() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM cliente WHERE id_cliente = %s", (codigo,))
                    return cursor.rowcount == 1
        except Exception as erro:
            print(f"Erro ao remover cliente: {erro}")
        return False
