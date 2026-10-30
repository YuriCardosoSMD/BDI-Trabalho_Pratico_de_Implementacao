import psycopg2


# I1 - Cadastrar cliente
def inserir_cliente(conn, nome):
    sql = "INSERT INTO cliente (nome) VALUES (%s);"
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, (nome,))
        conn.commit()
        print("Cliente registrado com sucesso.")
        return True
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Erro ao registrar cliente: {e}")
        return False


# I2 - Cadastrar medicamento (categoria e fabricante obrigatórios)
def inserir_medicamento(conn, descricao, preco, cod_categoria, cod_fabricante):
    sql = """
        INSERT INTO medicamento (descricao, preco, cod_categoria, cod_fabricante)
        VALUES (%s, %s, %s, %s);
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, (descricao, preco, cod_categoria, cod_fabricante))
        conn.commit()
        print("Medicamento registrado com sucesso.")
        return True
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Erro ao registrar medicamento: {e}")
        return False


# I3 - Registrar uma venda e seus itens na mesma transação
def inserir_venda(conn, cod_filial, id_cliente, id_funcionario, itens_venda):
    if not itens_venda:
        print("A venda precisa ter pelo menos um item.")
        return None

    sql_venda = """
        INSERT INTO venda (cod_filial, id_cliente, id_funcionario)
        VALUES (%s, %s, %s) RETURNING id_venda;
    """
    sql_item = """
        INSERT INTO item_venda (id_venda, id_medicamento, quantidade, preco_unitario)
        VALUES (%s, %s, %s, %s);
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql_venda, (cod_filial, id_cliente, id_funcionario))
            id_venda = cursor.fetchone()[0]
            for id_medicamento, quantidade, preco in itens_venda:
                cursor.execute(sql_item, (id_venda, id_medicamento, quantidade, preco))
        conn.commit()
        print(f"Venda {id_venda} registrada com os seus itens.")
        return id_venda
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Erro ao registrar venda (nada foi gravado): {e}")
        return None