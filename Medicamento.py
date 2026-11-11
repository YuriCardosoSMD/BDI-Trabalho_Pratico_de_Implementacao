from dataclasses import dataclass


# Classe que representa a entidade medicamento
@dataclass
class Medicamento:
    codigo: int = None
    descricao: str = ""
    preco: float = 0.0
    categoria: str = ""
    fabricante: str = ""
