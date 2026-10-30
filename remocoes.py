import psycopg2
from psycopg2 import errors


# D1 - Excluir cliente sem vendas
def excluir_cliente(conn, id_cliente):
    sql = "DELETE FROM cliente WHERE id_cliente = %s;"
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, (id_cliente,))
            if cursor.rowcount == 0:
                conn.rollback()
                print("Cliente não encontrado.")
                return False
        conn.commit()
        print("Cliente excluído com sucesso.")
        return True
    except (errors.RestrictViolation, errors.ForeignKeyViolation):
        conn.rollback()
        print("Não é possível excluir: o cliente possui vendas registradas.")
        return False
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Erro ao excluir cliente: {e}")
        return False


# D2 - Excluir uma venda
def cancelar_venda(conn, id_venda):
    sql = "DELETE FROM venda WHERE id_venda = %s;"
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, (id_venda,))
            if cursor.rowcount == 0:
                conn.rollback()
                print("Venda não encontrada.")
                return False
        conn.commit()
        print(f"Venda {id_venda} cancelada (itens removidos junto).")
        return True
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Erro ao cancelar venda: {e}")
        return False