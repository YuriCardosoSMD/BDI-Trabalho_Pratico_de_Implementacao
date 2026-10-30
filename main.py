import psycopg2

from conexao import conectar
from interface import (
    ler_texto,
    ler_inteiro,
    ler_decimal,
    formatar,
    imprimir_tabela,
    mostrar_referencia,
)
from insercoes import inserir_cliente, inserir_medicamento, inserir_venda
from consultas import (
    listar_medicamentos,
    consultar_medicamentos_filtro,
    consultar_estoque_filial,
    consultar_vendas,
    consultar_itens_venda,
    buscar_preco_medicamento,
)
from atualizacoes import atualizar_medicamento, atualizar_estoque
from remocoes import excluir_cliente, cancelar_venda


# ---------------------------------------------------------------------
# Ações do menu
# ---------------------------------------------------------------------
def acao_cadastrar_cliente(conn):
    inserir_cliente(conn, ler_texto("Nome do cliente: "))


def acao_cadastrar_medicamento(conn):
    descricao = ler_texto("Descrição: ")
    preco = ler_decimal("Preço: ")
    mostrar_referencia(conn, "categoria", "Categorias")
    cod_categoria = ler_inteiro("Código da categoria: ")
    mostrar_referencia(conn, "fabricante", "Fabricantes")
    cod_fabricante = ler_inteiro("Código do fabricante: ")
    inserir_medicamento(conn, descricao, preco, cod_categoria, cod_fabricante)


def acao_registrar_venda(conn):
    mostrar_referencia(conn, "filial", "Filiais")
    cod_filial = ler_inteiro("Código da filial: ")
    mostrar_referencia(conn, "cliente", "Clientes")
    id_cliente = ler_inteiro("Código do cliente: ")
    mostrar_referencia(conn, "funcionario", "Funcionários")
    id_funcionario = ler_inteiro("Código do funcionário: ")

    mostrar_referencia(conn, "medicamento", "Medicamentos")
    print("\nItens da venda (Enter vazio no código do medicamento encerra).")
    itens = {}  # id_medicamento -> [quantidade, preco]
    while True:
        id_med = ler_inteiro("Código do medicamento: ", opcional=True)
        if id_med is None:
            break
        preco = buscar_preco_medicamento(conn, id_med)
        if preco is None:
            print("Medicamento não encontrado.")
            continue
        quantidade = ler_inteiro("Quantidade: ")
        if id_med in itens:  # a chave (venda, medicamento) não pode repetir
            itens[id_med][0] += quantidade
        else:
            itens[id_med] = [quantidade, preco]
        print(f"  Item adicionado (preço unitário vigente: {formatar(preco)}).")

    lista = [(i, q, p) for i, (q, p) in itens.items()]
    inserir_venda(conn, cod_filial, id_cliente, id_funcionario, lista)


def acao_listar_medicamentos(conn):
    imprimir_tabela(
        ["Cód.", "Descrição", "Preço", "Categoria", "Fabricante"],
        listar_medicamentos(conn),
    )


def acao_medicamentos_filtro(conn):
    print("Deixe em branco para não filtrar.")
    mostrar_referencia(conn, "categoria", "Categorias")
    cod_categoria = ler_inteiro("Código da categoria: ", opcional=True)
    mostrar_referencia(conn, "fabricante", "Fabricantes")
    cod_fabricante = ler_inteiro("Código do fabricante: ", opcional=True)
    imprimir_tabela(
        ["Cód.", "Descrição", "Preço"],
        consultar_medicamentos_filtro(conn, cod_categoria, cod_fabricante),
    )


def acao_estoque_filial(conn):
    mostrar_referencia(conn, "filial", "Filiais")
    cod_filial = ler_inteiro("Código da filial: ")
    imprimir_tabela(
        ["Medicamento", "Quantidade"], consultar_estoque_filial(conn, cod_filial)
    )


def acao_listar_vendas(conn):
    imprimir_tabela(
        ["Venda", "Data/hora", "Filial", "Cliente", "Funcionário"],
        consultar_vendas(conn),
    )


def acao_itens_venda(conn):
    id_venda = ler_inteiro("Código da venda: ")
    linhas = consultar_itens_venda(conn, id_venda)
    imprimir_tabela(["Medicamento", "Qtd.", "Preço unit.", "Subtotal"], linhas)
    if linhas:
        print(f"\nTotal da venda: {formatar(sum(l[3] for l in linhas))}")


def acao_atualizar_medicamento(conn):
    mostrar_referencia(conn, "medicamento", "Medicamentos")
    id_med = ler_inteiro("Código do medicamento: ")
    descricao = ler_texto("Nova descrição: ")
    preco = ler_decimal("Novo preço: ")
    atualizar_medicamento(conn, id_med, descricao, preco)


def acao_atualizar_estoque(conn):
    mostrar_referencia(conn, "filial", "Filiais")
    cod_filial = ler_inteiro("Código da filial: ")
    mostrar_referencia(conn, "medicamento", "Medicamentos")
    id_med = ler_inteiro("Código do medicamento: ")
    quantidade = ler_inteiro("Nova quantidade em estoque: ", minimo=0)
    atualizar_estoque(conn, cod_filial, id_med, quantidade)


def acao_excluir_cliente(conn):
    mostrar_referencia(conn, "cliente", "Clientes")
    id_cliente = ler_inteiro("Código do cliente a excluir: ")
    if input("Confirma a exclusão? (s/n): ").strip().lower() == "s":
        excluir_cliente(conn, id_cliente)
    else:
        print("Operação cancelada.")


def acao_cancelar_venda(conn):
    id_venda = ler_inteiro("Código da venda a cancelar: ")
    if input("Confirma o cancelamento? (s/n): ").strip().lower() == "s":
        cancelar_venda(conn, id_venda)
    else:
        print("Operação cancelada.")


# ---------------------------------------------------------------------
# Menu principal
# ---------------------------------------------------------------------
MENU = """
===== SISTEMA DA FARMÁCIA =====
 Cadastros
   1 - Cadastrar cliente
   2 - Cadastrar medicamento
   3 - Registrar venda
 Consultas
   4 - Listar medicamentos
   5 - Consultar medicamentos por categoria/fabricante
   6 - Consultar estoque de uma filial
   7 - Consultar vendas realizadas
   8 - Consultar itens de uma venda
 Atualizações
   9 - Atualizar medicamento (descrição/preço)
  10 - Atualizar estoque
 Remoções
  11 - Excluir cliente
  12 - Cancelar venda
   0 - Sair"""

ACOES = {
    "1": acao_cadastrar_cliente,
    "2": acao_cadastrar_medicamento,
    "3": acao_registrar_venda,
    "4": acao_listar_medicamentos,
    "5": acao_medicamentos_filtro,
    "6": acao_estoque_filial,
    "7": acao_listar_vendas,
    "8": acao_itens_venda,
    "9": acao_atualizar_medicamento,
    "10": acao_atualizar_estoque,
    "11": acao_excluir_cliente,
    "12": acao_cancelar_venda,
}


def main():
    conn = None
    try:
        conn = conectar()
        while True:
            print(MENU)
            opcao = input("Opção: ").strip()
            if opcao == "0":
                break
            acao = ACOES.get(opcao)
            if acao is None:
                print("Opção inválida.")
                continue
            acao(conn)
    except psycopg2.OperationalError as e:
        print(f"Erro de conexão com o banco: {e}")
    except (KeyboardInterrupt, EOFError):
        print("\nEncerrando.")
    finally:
        if conn:
            conn.close()
        print("Conexão encerrada.")


if __name__ == "__main__":
    main()