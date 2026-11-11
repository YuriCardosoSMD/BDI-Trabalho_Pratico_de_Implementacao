from dataclasses import dataclass


# Classe que representa a entidade cliente
@dataclass
class Cliente:
    codigo: int = None
    nome: str = ""
