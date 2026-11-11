from dataclasses import dataclass


# Classe que representa a quantidade de um medicamento no estoque de uma filial
@dataclass
class Estoque:
    medicamento: str = ""
    quantidade: int = 0
