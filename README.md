# BDI — Trabalho Prático de Implementação

Aplicação em Python (terminal) para **Controle de Vendas e Estoque de Farmácia**, usando **PostgreSQL** e `psycopg2`.

## Integrantes da Equipe
- Dália Freitas da Silva Mariano
- Isabele Alessandra Fernandes Lobão
- Thaíssa Victória Nunes Serafim
- Yuri da Silva Cardoso

## Organização do código

Segue o mesmo padrão do exemplo da disciplina (Entidade + DAO + Interface):

| Arquivo | Função |
|---|---|
| `Conexao.py` | Conexão com o banco |
| `Cliente.py`, `Medicamento.py`, `Estoque.py`, `Venda.py` | Classes das entidades |
| `ClienteDAO.py`, `MedicamentoDAO.py`, `EstoqueDAO.py`, `VendaDAO.py` | Comandos SQL |
| `InterfaceGrafica.py` | Menus da aplicação (arquivo principal) |

## Operações SQL DML

| Operação | Mínimo | Implementado |
|---|---|---|
| SELECT | 5 | **7** — listar clientes, buscar cliente, listar medicamentos, buscar medicamento, estoque da filial, listar vendas, itens da venda |
| INSERT | 3 | **4** — cliente, medicamento, venda, item da venda |
| UPDATE | 2 | **3** — cliente, medicamento, estoque |
| DELETE | 2 | **3** — cliente, itens da venda, venda |

## Como executar

1. Crie o banco `sistema_farmacia` no PostgreSQL e execute o script DDL.
2. Instale a dependência:
   ```
   pip install -r requirements.txt
   ```
3. Abra `Conexao.py` e coloque a senha do seu PostgreSQL.
4. Execute:
   ```
   python InterfaceGrafica.py
   ```
