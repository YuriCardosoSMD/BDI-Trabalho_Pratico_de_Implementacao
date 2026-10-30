import psycopg2


# U1 - Atualizar os dados e o preço de um medicamento
def atualizar_medicamento(conn, id_medicamento, descricao, preco):
    sql = """
        UPDATE medicamento
        SET descricao = %s, preco = %s
        WHERE id_medicamento = %s;
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, (descricao, preco, id_medicamento))
            if cursor.rowcount == 0:
                conn.rollback()
                print("Medicamento não encontrado.")
                return False
        conn.commit()
        print("Medicamento atualizado com sucesso.")
        return True
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Erro ao atualizar medicamento: {e}")
        return False


# U2 - Atualizar a quantidade em estoque de um medicamento em uma filial
def atualizar_estoque(conn, cod_filial, id_medicamento, quantidade):
    sql = """
        UPDATE estoque
        SET quantidade = %s
        WHERE cod_filial = %s AND id_medicamento = %s;
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, (quantidade, cod_filial, id_medicamento))
            if cursor.rowcount == 0:
                conn.rollback()
                print("Não há registro de estoque desse medicamento nessa filial.")
                return False
        conn.commit()
        print("Estoque atualizado com sucesso.")
        return True
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Erro ao atualizar estoque: {e}")
        return False