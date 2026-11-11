from Conexao import conectar
from Medicamento import Medicamento


# Classe DAO da entidade medicamento
class MedicamentoDAO:

    # Lista todos os medicamentos com categoria e fabricante (SELECT com JOIN)
    def listar_todos(self):
        resultado = []
        try:
            with conectar() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT m.id_medicamento, m.descricao, m.preco, c.descricao, f.razao_social "
                        "FROM medicamento m "
                        "JOIN categoria c ON c.cod_categoria = m.cod_categoria "
                        "JOIN fabricante f ON f.cod_fabricante = m.cod_fabricante "
                        "ORDER BY m.id_medicamento"
                    )
                    for linha in cursor.fetchall():
                        resultado.append(Medicamento(linha[0], linha[1], linha[2], linha[3], linha[4]))
        except Exception as erro:
            print(f"Erro ao listar medicamentos: {erro}")
        return resultado

    # Busca um medicamento pelo código (SELECT)
    def buscar(self, codigo):
        try:
            with conectar() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT id_medicamento, descricao, preco FROM medicamento WHERE id_medicamento = %s",
                        (codigo,)
                    )
                    linha = cursor.fetchone()
                    if linha:
                        return Medicamento(linha[0], linha[1], linha[2])
        except Exception as erro:
            print(f"Erro ao buscar medicamento: {erro}")
        return None

    # Insere um novo medicamento (INSERT)
    def inserir(self, descricao, preco, cod_categoria, cod_fabricante):
        try:
            with conectar() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO medicamento (descricao, preco, cod_categoria, cod_fabricante) "
                        "VALUES (%s, %s, %s, %s)",
                        (descricao, preco, cod_categoria, cod_fabricante)
                    )
                    return cursor.rowcount == 1
        except Exception as erro:
            print(f"Erro ao inserir medicamento: {erro}")
        return False

    # Atualiza a descrição e o preço de um medicamento (UPDATE)
    def atualizar(self, descricao, preco, codigo):
        try:
            with conectar() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE medicamento SET descricao = %s, preco = %s WHERE id_medicamento = %s",
                        (descricao, preco, codigo)
                    )
                    return cursor.rowcount == 1
        except Exception as erro:
            print(f"Erro ao atualizar medicamento: {erro}")
        return False
