# BDI — Trabalho Prático de Implementação

Aplicação em Python via terminal (CLI) para **Controle de Vendas e Estoque de Farmácia**, utilizando **PostgreSQL** e `psycopg2`.

## Integrantes da Equipe
- Dália Freitas da Silva Mariano
- Isabele Alessandra Fernandes Lobão
- Thaíssa Victória Nunes Serafim
- Yuri da Silva Cardoso

## Atendimento aos Requisitos Mínimos

### Banco de Dados Relacional
| Requisito | Mínimo Exigido | Implementado no Projeto |
| --- | :---: | :---: |
| Tabelas | 5 | **13** |
| Chaves primárias (`PK`) | 5 | **13** (7 simples e 6 compostas) |
| Chaves estrangeiras (`FK`) | 3 | **13** |
| Colunas por tabela | 2 | **2 a 5** colunas |

### Operações SQL DML
| Operação | Mínimo Exigido | Implementado no Projeto | Módulo |
| --- | :---: | :---: | --- |
| Leitura (`SELECT`) | 5 | **5** (`S1` a `S5`) | `consultas.py` |
| Inserção (`INSERT`) | 3 | **3** (`I1` a `I3`) | `insercoes.py` |
| Atualização (`UPDATE`) | 2 | **2** (`U1` e `U2`) | `atualizacoes.py` |
| Remoção (`DELETE`) | 2 | **2** (`D1` e `D2`) | `remocoes.py` |

## Como Executar o Projeto

### 1. Pré-requisitos
- Python 3.10+
- PostgreSQL ativo localmente

### 2. Configurar o Ambiente Python
```bash
# Criar e ativar o ambiente virtual
python -m venv venv

# No Windows:
venv\Scripts\activate
# No Linux/macOS:
source venv/bin/activate

# Instalar as dependências
pip install -r requirements.txt