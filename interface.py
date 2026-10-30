from datetime import datetime
from decimal import Decimal, InvalidOperation
from consultas import listar_referencia


# ---------------------------------------------------------------------
# Leitura e validação de entradas
# ---------------------------------------------------------------------
def ler_texto(mensagem):
    """Lê um texto obrigatório (repete até não ser vazio)."""
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("Valor obrigatório.")


def ler_inteiro(mensagem, minimo=1, opcional=False):
    """Lê um inteiro >= minimo. Se opcional, Enter vazio devolve None."""
    while True:
        valor = input(mensagem).strip()
        if opcional and valor == "":
            return None
        try:
            numero = int(valor)
        except ValueError:
            print("Digite um número inteiro.")
            continue
        if numero < minimo:
            print(f"O valor deve ser maior ou igual a {minimo}.")
            continue
        return numero


def ler_decimal(mensagem):
    """Lê um valor monetário >= 0 (aceita vírgula ou ponto)."""
    while True:
        valor = input(mensagem).strip().replace(",", ".")
        try:
            numero = Decimal(valor)
        except InvalidOperation:
            print("Digite um valor numérico (ex.: 12.50).")
            continue
        if not numero.is_finite() or numero < 0:
            print("O valor não pode ser negativo.")
            continue
        return numero


# ---------------------------------------------------------------------
# Exibição e formatação
# ---------------------------------------------------------------------
def formatar(valor):
    if isinstance(valor, Decimal):
        return f"{valor:.2f}"
    if isinstance(valor, datetime):
        return valor.strftime("%d/%m/%Y %H:%M")
    return str(valor)


def imprimir_tabela(cabecalhos, linhas):
    if not linhas:
        print("Nenhum registro encontrado.")
        return
    dados = [[formatar(c) for c in linha] for linha in linhas]
    larguras = [
        max(len(cabecalhos[i]), *(len(l[i]) for l in dados))
        for i in range(len(cabecalhos))
    ]
    print("  ".join(c.ljust(larguras[i]) for i, c in enumerate(cabecalhos)))
    print("  ".join("-" * w for w in larguras))
    for linha in dados:
        print("  ".join(c.ljust(larguras[i]) for i, c in enumerate(linha)))


def mostrar_referencia(conn, tabela, titulo):
    print(f"\n{titulo}:")
    imprimir_tabela(["Cód.", "Nome"], listar_referencia(conn, tabela))