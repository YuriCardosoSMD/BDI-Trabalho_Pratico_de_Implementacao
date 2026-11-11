from dataclasses import dataclass


# Classe que representa a entidade venda
@dataclass
class Venda:
    codigo: int = None
    data_hora: object = None
    filial: str = ""
    cliente: str = ""
    funcionario: str = ""


# Classe que representa um item de uma venda
@dataclass
class ItemVenda:
    medicamento: str = ""
    quantidade: int = 0
    preco_unitario: float = 0.0
