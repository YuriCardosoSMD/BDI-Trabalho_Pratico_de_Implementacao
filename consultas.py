import psycopg2


def _consultar(conn, sql, params=None):
    """Executa um SELECT e devolve todas as linhas (lista vazia em caso de erro)."""
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            linhas = cursor.fetchall()
        conn.commit()
        return linhas
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Erro na consulta: {e}")
        return []


# S1 - Listar os medicamentos cadastrados, com categoria e fabricante
def listar_medicamentos(conn):
    sql = """
        SELECT m.id_medicamento, m.descricao, m.preco,
               c.descricao AS categoria,
               f.razao_social AS fabricante
        FROM medicamento m
        JOIN categoria c  ON c.cod_categoria  = m.cod_categoria
        JOIN fabricante f ON f.cod_fabricante = m.cod_fabricante
        ORDER BY m.descricao;
    """
    return _consultar(conn, sql)


# S2 - Consultar medicamentos por categoria e/ou fabricante
def consultar_medicamentos_filtro(conn, cod_categoria=None, cod_fabricante=None):
    sql = """
        SELECT m.id_medicamento, m.descricao, m.preco
        FROM medicamento m
        WHERE (%(cat)s::int IS NULL OR m.cod_categoria  = %(cat)s)
          AND (%(fab)s::int IS NULL OR m.cod_fabricante = %(fab)s)
        ORDER BY m.descricao;
    """
    return _consultar(conn, sql, {"cat": cod_categoria, "fab": cod_fabricante})


# S3 - Consultar o estoque de uma filial
def consultar_estoque_filial(conn, cod_filial):
    sql = """
        SELECT m.descricao, e.quantidade
        FROM estoque e
        JOIN medicamento m ON m.id_medicamento = e.id_medicamento
        WHERE e.cod_filial = %s
        ORDER BY m.descricao;
    """
    return _consultar(conn, sql, (cod_filial,))


# S4 - Consultar as vendas realizadas
def consultar_vendas(conn):
    sql = """
        SELECT v.id_venda, v.data_hora,
               f.razao_social AS filial,
               c.nome AS cliente, u.nome AS funcionario
        FROM venda v
        JOIN filial f      ON f.cod_filial     = v.cod_filial
        JOIN cliente c     ON c.id_cliente     = v.id_cliente
        JOIN funcionario u ON u.id_funcionario = v.id_funcionario
        ORDER BY v.data_hora DESC;
    """
    return _consultar(conn, sql)


# S5 - Consultar os itens de determinada venda
def consultar_itens_venda(conn, id_venda):
    sql = """
        SELECT m.descricao, i.quantidade, i.preco_unitario,
               i.quantidade * i.preco_unitario AS subtotal
        FROM item_venda i
        JOIN medicamento m ON m.id_medicamento = i.id_medicamento
        WHERE i.id_venda = %s;
    """
    return _consultar(conn, sql, (id_venda,))



# Listas de referência e preço vigente.

def buscar_preco_medicamento(conn, id_medicamento):
    """Preço vigente do medicamento, ou None se ele não existir."""
    linhas = _consultar(
        conn,
        "SELECT preco FROM medicamento WHERE id_medicamento = %s;",
        (id_medicamento,),
    )
    return linhas[0][0] if linhas else None


_REFERENCIAS = {
    "categoria": "SELECT cod_categoria, descricao FROM categoria ORDER BY cod_categoria;",
    "fabricante": "SELECT cod_fabricante, razao_social FROM fabricante ORDER BY cod_fabricante;",
    "filial": "SELECT cod_filial, razao_social FROM filial ORDER BY cod_filial;",
    "cliente": "SELECT id_cliente, nome FROM cliente ORDER BY id_cliente;",
    "funcionario": "SELECT id_funcionario, nome FROM funcionario ORDER BY id_funcionario;",
    "medicamento": "SELECT id_medicamento, descricao FROM medicamento ORDER BY id_medicamento;",
}


def listar_referencia(conn, tabela):
    """Lista (id, nome) de categoria, fabricante, filial, cliente, funcionario ou medicamento."""
    return _consultar(conn, _REFERENCIAS[tabela])