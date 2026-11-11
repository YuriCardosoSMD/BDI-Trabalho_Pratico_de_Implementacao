from dao.Conexao import conectar
from entidades.Venda import Venda, ItemVenda


# Classe DAO da entidade venda
class VendaDAO:

    # Lista todas as vendas
    def listar_todas(self):
        resultado = []
        try:
            with conectar() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT v.id_venda, v.data_hora, "
                        "       f.razao_social AS filial, c.nome AS cliente, u.nome AS funcionario "
                        "FROM venda v "
                        "JOIN filial f ON f.cod_filial = v.cod_filial "
                        "JOIN cliente c ON c.id_cliente = v.id_cliente "
                        "JOIN funcionario u ON u.id_funcionario = v.id_funcionario "
                        "ORDER BY v.id_venda"
                    )
                    for linha in cursor.fetchall():
                        resultado.append(Venda(linha[0], linha[1], linha[2], linha[3], linha[4]))
        except Exception as erro:
            print(f"Erro ao listar vendas: {erro}")
        return resultado

    # Lista os itens de uma venda
    def listar_itens(self, id_venda):
        resultado = []
        try:
            with conectar() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT m.descricao, i.quantidade, i.preco_unitario "
                        "FROM item_venda i "
                        "JOIN medicamento m ON m.id_medicamento = i.id_medicamento "
                        "WHERE i.id_venda = %s",
                        (id_venda,)
                    )
                    for linha in cursor.fetchall():
                        resultado.append(ItemVenda(linha[0], linha[1], linha[2]))
        except Exception as erro:
            print(f"Erro ao listar itens da venda: {erro}")
        return resultado

    # Insere uma venda e seus itens (INSERT)
    def inserir(self, cod_filial, id_cliente, id_funcionario, itens):
        try:
            with conectar() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO venda (cod_filial, id_cliente, id_funcionario) "
                        "VALUES (%s, %s, %s) RETURNING id_venda",
                        (cod_filial, id_cliente, id_funcionario)
                    )
                    id_venda = cursor.fetchone()[0]
                    for id_medicamento, quantidade, preco in itens:
                        cursor.execute(
                            "INSERT INTO item_venda (id_venda, id_medicamento, quantidade, preco_unitario) "
                            "VALUES (%s, %s, %s, %s)",
                            (id_venda, id_medicamento, quantidade, preco)
                        )
                    return id_venda
        except Exception as erro:
            print(f"Erro ao registrar venda (nada foi gravado): {erro}")
        return None

    # Remove uma venda (DELETE)
    def remover(self, id_venda):
        try:
            with conectar() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM venda WHERE id_venda = %s", (id_venda,))
                    return cursor.rowcount == 1
        except Exception as erro:
            print(f"Erro ao cancelar venda: {erro}")
        return False
