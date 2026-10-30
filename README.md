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

Crie e ative um ambiente virtual:

```bash
python -m venv venv
```

No Windows:

```bash
venv\Scripts\activate
```

No Linux/macOS:

```bash
source venv/bin/activate
```

Em seguida, instale as dependências:

```bash
pip install -r requirements.txt
```

### 3. Configurar as Variáveis de Ambiente

Antes de executar o projeto, é **necessário criar um arquivo chamado `.env` na pasta raiz do projeto**.

Use o arquivo `.env.example` como modelo. Copie todo o seu conteúdo para o novo arquivo `.env`.

Por exemplo, no Windows:

```bash
copy .env.example .env
```

No Linux/macOS:

```bash
cp .env.example .env
```

Depois de criar o arquivo `.env`, abra-o e **altere a senha do banco de dados** para a senha configurada no seu PostgreSQL.

> **Importante:** verifique se as demais informações de conexão presentes no `.env`, como nome do banco, usuário, host e porta, correspondem à configuração do seu PostgreSQL.

O arquivo `.env` deve permanecer dentro da pasta raiz do projeto, no mesmo diretório em que o projeto será executado.

### 4. Executar o Projeto

Com o ambiente virtual ativado, as dependências instaladas, o PostgreSQL em execução e o arquivo `.env` configurado, execute no terminal:

```bash
python main.py
```

A aplicação será iniciada diretamente no terminal.
