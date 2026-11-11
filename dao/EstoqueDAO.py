from dao.Conexao import conectar
from entidades.Estoque import Estoque


# Classe DAO do estoque das filiais
class EstoqueDAO:

    # Lista o estoque de uma filial (SELECT com JOIN)
    def listar_por_filial(self, cod_filial):
        resultado = []
        try:
            with conectar() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT m.descricao, e.quantidade "
                        "FROM estoque e "
                        "JOIN medicamento m ON m.id_medicamento = e.id_medicamento "
                        "WHERE e.cod_filial = %s "
                        "ORDER BY m.descricao",
                        (cod_filial,)
                    )
                    for linha in cursor.fetchall():
                        resultado.append(Estoque(linha[0], linha[1]))
        except Exception as erro:
            print(f"Erro ao listar estoque: {erro}")
        return resultado

    # Atualiza a quantidade de um medicamento no estoque de uma filial (UPDATE)
    def atualizar(self, quantidade, cod_filial, id_medicamento):
        try:
            with conectar() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE estoque SET quantidade = %s WHERE cod_filial = %s AND id_medicamento = %s",
                        (quantidade, cod_filial, id_medicamento)
                    )
                    return cursor.rowcount == 1
        except Exception as erro:
            print(f"Erro ao atualizar estoque: {erro}")
        return False
