# BDI — Trabalho Prático de Implementação

Aplicação em Python via terminal (CLI) para **Controle de Vendas e Estoque de Farmácia**, utilizando **PostgreSQL** e `psycopg2`.

## Sumário

- [Integrantes da Equipe](#integrantes-da-equipe)
- [Atendimento aos Requisitos Mínimos](#atendimento-aos-requisitos-mínimos)
- [Como Executar o Projeto](#como-executar-o-projeto)
- [Apêndice A — Script DDL (PostgreSQL)](#apêndice-a--script-ddl-postgresql)

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

No **Windows**:

```bash
venv\Scripts\activate
```

No **Linux/macOS**:

```bash
source venv/bin/activate
```

Em seguida, instale as dependências:

```bash
pip install -r requirements.txt
```

### 3. Configurar as Variáveis de Ambiente

Antes de executar o projeto, é necessário criar um arquivo chamado `.env` na pasta raiz do projeto.

Use o arquivo `.env.example` como modelo, copiando todo o seu conteúdo para o novo arquivo `.env`.

No **Windows**:

```bash
copy .env.example .env
```

No **Linux/macOS**:

```bash
cp .env.example .env
```

Depois de criar o arquivo `.env`, abra-o e altere a senha do banco de dados para a senha configurada no seu PostgreSQL.

> [!IMPORTANT]
> Verifique se as demais informações de conexão presentes no `.env` — como nome do banco, usuário, host e porta — correspondem à configuração do seu PostgreSQL.
>
> O arquivo `.env` deve permanecer na pasta raiz do projeto, no mesmo diretório em que o projeto será executado.

### 4. Criar o Banco de Dados

Com o PostgreSQL em execução e um banco de dados vazio criado, execute o script `schema.sql` ([Apêndice A](#apêndice-a--script-ddl-postgresql)) para criar as tabelas e carregar alguns dados iniciais de exemplo para consulta. Isso pode ser feito pelo `psql`, pgAdmin, DBeaver ou qualquer outro cliente PostgreSQL.

Exemplo via terminal:

```bash
psql -U <usuario> -d <nome_do_banco> -f schema.sql
```

### 5. Executar o Projeto

Com o ambiente virtual ativado, as dependências instaladas, o PostgreSQL em execução, o banco de dados criado e o arquivo `.env` configurado, execute no terminal:

```bash
python main.py
```

A aplicação será iniciada diretamente no terminal.

---

## Apêndice A — Script DDL (PostgreSQL)

Script de criação do banco de dados a partir do modelo lógico, já com uma carga inicial de dados de exemplo (*seed*) para consulta e testes. Pode ser executado no `psql`, pgAdmin ou DBeaver, em um banco vazio.

<details>
<summary><strong>Clique para expandir o <code>schema.sql</code></strong></summary>

```sql
-- =====================================================================
-- Controle de Vendas e Estoque de Farmácia
-- Script DDL - PostgreSQL
-- 13 tabelas | 13 chaves primárias | 13 chaves estrangeiras
-- =====================================================================

DROP TABLE IF EXISTS telefone_fabricante, telefone_filial,
    telefone_funcionario, telefone_cliente, item_venda, estoque, venda,
    medicamento, cliente, funcionario, filial, fabricante, categoria CASCADE;

-- ---------------------------------------------------------------------
-- Entidades independentes
-- ---------------------------------------------------------------------
CREATE TABLE categoria (
    cod_categoria SERIAL CONSTRAINT pk_categoria PRIMARY KEY,
    descricao     VARCHAR(80) NOT NULL
                  CONSTRAINT uq_categoria_descricao UNIQUE
);

CREATE TABLE fabricante (
    cod_fabricante SERIAL CONSTRAINT pk_fabricante PRIMARY KEY,
    razao_social   VARCHAR(120) NOT NULL
);

CREATE TABLE filial (
    cod_filial   SERIAL CONSTRAINT pk_filial PRIMARY KEY,
    razao_social VARCHAR(120) NOT NULL
);

CREATE TABLE funcionario (
    id_funcionario SERIAL CONSTRAINT pk_funcionario PRIMARY KEY,
    nome           VARCHAR(120) NOT NULL,
    salario        DECIMAL(10,2) NOT NULL
                   CONSTRAINT ck_funcionario_salario CHECK (salario >= 0)
);

CREATE TABLE cliente (
    id_cliente SERIAL CONSTRAINT pk_cliente PRIMARY KEY,
    nome       VARCHAR(120) NOT NULL
);

-- ---------------------------------------------------------------------
-- Medicamento (categoria e fabricante obrigatórios)
-- ---------------------------------------------------------------------
CREATE TABLE medicamento (
    id_medicamento SERIAL CONSTRAINT pk_medicamento PRIMARY KEY,
    descricao      VARCHAR(120) NOT NULL,
    preco          DECIMAL(10,2) NOT NULL
                   CONSTRAINT ck_medicamento_preco CHECK (preco >= 0),
    cod_categoria  INTEGER NOT NULL,
    cod_fabricante INTEGER NOT NULL,
    CONSTRAINT fk_medicamento_categoria FOREIGN KEY (cod_categoria)
        REFERENCES categoria (cod_categoria)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_medicamento_fabricante FOREIGN KEY (cod_fabricante)
        REFERENCES fabricante (cod_fabricante)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

-- ---------------------------------------------------------------------
-- Venda (filial, cliente e funcionário obrigatórios)
-- ---------------------------------------------------------------------
CREATE TABLE venda (
    id_venda       SERIAL CONSTRAINT pk_venda PRIMARY KEY,
    data_hora      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    cod_filial     INTEGER NOT NULL,
    id_cliente     INTEGER NOT NULL,
    id_funcionario INTEGER NOT NULL,
    CONSTRAINT fk_venda_filial FOREIGN KEY (cod_filial)
        REFERENCES filial (cod_filial)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_venda_cliente FOREIGN KEY (id_cliente)
        REFERENCES cliente (id_cliente)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_venda_funcionario FOREIGN KEY (id_funcionario)
        REFERENCES funcionario (id_funcionario)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

-- ---------------------------------------------------------------------
-- Associativas: ESTOQUE (Filial x Medicamento) e
--               ITEM_VENDA (Venda x Medicamento)
-- ---------------------------------------------------------------------
CREATE TABLE estoque (
    cod_filial     INTEGER NOT NULL,
    id_medicamento INTEGER NOT NULL,
    quantidade     INTEGER NOT NULL DEFAULT 0
                   CONSTRAINT ck_estoque_quantidade CHECK (quantidade >= 0),
    CONSTRAINT pk_estoque PRIMARY KEY (cod_filial, id_medicamento),
    CONSTRAINT fk_estoque_filial FOREIGN KEY (cod_filial)
        REFERENCES filial (cod_filial)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_estoque_medicamento FOREIGN KEY (id_medicamento)
        REFERENCES medicamento (id_medicamento)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE item_venda (
    id_venda       INTEGER NOT NULL,
    id_medicamento INTEGER NOT NULL,
    quantidade     INTEGER NOT NULL
                   CONSTRAINT ck_item_venda_quantidade CHECK (quantidade > 0),
    preco_unitario DECIMAL(10,2) NOT NULL
                   CONSTRAINT ck_item_venda_preco CHECK (preco_unitario >= 0),
    CONSTRAINT pk_item_venda PRIMARY KEY (id_venda, id_medicamento),
    CONSTRAINT fk_item_venda_venda FOREIGN KEY (id_venda)
        REFERENCES venda (id_venda)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_item_venda_medicamento FOREIGN KEY (id_medicamento)
        REFERENCES medicamento (id_medicamento)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

-- ---------------------------------------------------------------------
-- Telefones (atributo multivalorado -> uma tabela por dono)
-- DDD e número como texto para preservar zeros à esquerda
-- ---------------------------------------------------------------------
CREATE TABLE telefone_cliente (
    id_cliente INTEGER NOT NULL,
    ddd        VARCHAR(3) NOT NULL
               CONSTRAINT ck_tel_cliente_ddd CHECK (ddd ~ '^[0-9]{2,3}$'),
    numero     VARCHAR(9) NOT NULL
               CONSTRAINT ck_tel_cliente_numero
               CHECK (numero ~ '^[0-9]{8,9}$'),
    CONSTRAINT pk_telefone_cliente PRIMARY KEY (id_cliente, ddd, numero),
    CONSTRAINT fk_telefone_cliente FOREIGN KEY (id_cliente)
        REFERENCES cliente (id_cliente)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE telefone_funcionario (
    id_funcionario INTEGER NOT NULL,
    ddd            VARCHAR(3) NOT NULL
                   CONSTRAINT ck_tel_funcionario_ddd
                   CHECK (ddd ~ '^[0-9]{2,3}$'),
    numero         VARCHAR(9) NOT NULL
                   CONSTRAINT ck_tel_funcionario_numero
                   CHECK (numero ~ '^[0-9]{8,9}$'),
    CONSTRAINT pk_telefone_funcionario
        PRIMARY KEY (id_funcionario, ddd, numero),
    CONSTRAINT fk_telefone_funcionario FOREIGN KEY (id_funcionario)
        REFERENCES funcionario (id_funcionario)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE telefone_filial (
    cod_filial INTEGER NOT NULL,
    ddd        VARCHAR(3) NOT NULL
               CONSTRAINT ck_tel_filial_ddd CHECK (ddd ~ '^[0-9]{2,3}$'),
    numero     VARCHAR(9) NOT NULL
               CONSTRAINT ck_tel_filial_numero
               CHECK (numero ~ '^[0-9]{8,9}$'),
    CONSTRAINT pk_telefone_filial PRIMARY KEY (cod_filial, ddd, numero),
    CONSTRAINT fk_telefone_filial FOREIGN KEY (cod_filial)
        REFERENCES filial (cod_filial)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE telefone_fabricante (
    cod_fabricante INTEGER NOT NULL,
    ddd            VARCHAR(3) NOT NULL
                   CONSTRAINT ck_tel_fabricante_ddd
                   CHECK (ddd ~ '^[0-9]{2,3}$'),
    numero         VARCHAR(9) NOT NULL
                   CONSTRAINT ck_tel_fabricante_numero
                   CHECK (numero ~ '^[0-9]{8,9}$'),
    CONSTRAINT pk_telefone_fabricante
        PRIMARY KEY (cod_fabricante, ddd, numero),
    CONSTRAINT fk_telefone_fabricante FOREIGN KEY (cod_fabricante)
        REFERENCES fabricante (cod_fabricante)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- ---------------------------------------------------------------------
-- Índices de apoio às consultas (FKs que não são prefixo de PK)
-- ---------------------------------------------------------------------
CREATE INDEX ix_medicamento_categoria  ON medicamento (cod_categoria);
CREATE INDEX ix_medicamento_fabricante ON medicamento (cod_fabricante);
CREATE INDEX ix_venda_filial           ON venda (cod_filial);
CREATE INDEX ix_venda_cliente          ON venda (id_cliente);
CREATE INDEX ix_venda_funcionario      ON venda (id_funcionario);
CREATE INDEX ix_venda_data_hora        ON venda (data_hora);
CREATE INDEX ix_estoque_medicamento    ON estoque (id_medicamento);
CREATE INDEX ix_item_venda_medicamento ON item_venda (id_medicamento);

-- =====================================================================
-- Carga inicial de dados (seed) para consulta e testes
-- Observação: os IDs seriais são atribuídos automaticamente, na mesma
-- ordem dos INSERTs abaixo, portanto as referências de FK já estão
-- corretas (ex.: 1ª categoria inserida = cod_categoria 1, e assim por diante).
-- =====================================================================

-- ---------------------------------------------------------------------
-- Entidades independentes
-- ---------------------------------------------------------------------
INSERT INTO categoria (descricao) VALUES
    ('Analgésico'),
    ('Antibiótico'),
    ('Antialérgico'),
    ('Antitérmico'),
    ('Vitamina e suplemento');

INSERT INTO fabricante (razao_social) VALUES
    ('EMS S/A'),
    ('Eurofarma Laboratórios S/A'),
    ('Medley Farmacêutica Ltda'),
    ('Neo Química Indústria Farmacêutica');

INSERT INTO filial (razao_social) VALUES
    ('Farmácia Central - Matriz'),
    ('Farmácia Bairro Norte'),
    ('Farmácia Bairro Sul');

INSERT INTO funcionario (nome, salario) VALUES
    ('Carlos Eduardo Souza',   2500.00),
    ('Marina Alves Pereira',   2800.00),
    ('Rafael Lima Santos',     2200.00),
    ('Fernanda Costa Ribeiro', 3000.00);

INSERT INTO cliente (nome) VALUES
    ('João Pedro Almeida'),
    ('Ana Clara Ferreira'),
    ('Lucas Gabriel Rocha'),
    ('Beatriz Oliveira Martins'),
    ('Gustavo Henrique Barbosa');

-- ---------------------------------------------------------------------
-- Medicamento
-- (cod_categoria e cod_fabricante seguem a ordem de inserção acima:
--   1=Analgésico, 2=Antibiótico, 3=Antialérgico, 4=Antitérmico, 5=Vitamina
--   1=EMS, 2=Eurofarma, 3=Medley, 4=Neo Química)
-- ---------------------------------------------------------------------
INSERT INTO medicamento (descricao, preco, cod_categoria, cod_fabricante) VALUES
    ('Paracetamol 750mg',     12.50, 1, 1),
    ('Dipirona Sódica 500mg',  9.90, 1, 2),
    ('Amoxicilina 500mg',     24.90, 2, 3),
    ('Azitromicina 500mg',    32.00, 2, 1),
    ('Loratadina 10mg',       15.00, 3, 4),
    ('Cetirizina 10mg',       18.50, 3, 2),
    ('Ibuprofeno 400mg',      11.20, 4, 1),
    ('Vitamina C 1g',         22.00, 5, 3);

-- ---------------------------------------------------------------------
-- Venda
-- (cod_filial: 1=Central, 2=Norte, 3=Sul)
-- ---------------------------------------------------------------------
INSERT INTO venda (cod_filial, id_cliente, id_funcionario) VALUES
    (1, 1, 1),
    (1, 2, 2),
    (2, 3, 3),
    (3, 4, 4),
    (2, 5, 1);

-- ---------------------------------------------------------------------
-- Estoque (Filial x Medicamento)
-- ---------------------------------------------------------------------
INSERT INTO estoque (cod_filial, id_medicamento, quantidade) VALUES
    (1, 1, 100),
    (1, 2,  80),
    (1, 3,  50),
    (1, 4,  40),
    (1, 5,  30),
    (2, 1,  60),
    (2, 5,  70),
    (2, 6,  55),
    (3, 7,  90),
    (3, 8,  65);

-- ---------------------------------------------------------------------
-- Item_venda (Venda x Medicamento)
-- ---------------------------------------------------------------------
INSERT INTO item_venda (id_venda, id_medicamento, quantidade, preco_unitario) VALUES
    (1, 1, 2, 12.50),
    (1, 3, 1, 24.90),
    (2, 2, 3,  9.90),
    (3, 5, 2, 15.00),
    (4, 7, 1, 11.20),
    (4, 8, 2, 22.00),
    (5, 4, 1, 32.00);

-- ---------------------------------------------------------------------
-- Telefones
-- ---------------------------------------------------------------------
INSERT INTO telefone_cliente (id_cliente, ddd, numero) VALUES
    (1, '11', '987654321'),
    (2, '21', '988776655'),
    (3, '31', '998877665'),
    (4, '41', '987123456'),
    (5, '51', '996543210');

INSERT INTO telefone_funcionario (id_funcionario, ddd, numero) VALUES
    (1, '11', '991112222'),
    (2, '21', '992223333'),
    (3, '31', '993334444'),
    (4, '41', '994445555');

INSERT INTO telefone_filial (cod_filial, ddd, numero) VALUES
    (1, '11', '33221100'),
    (2, '21', '33224455'),
    (3, '31', '33556677');

INSERT INTO telefone_fabricante (cod_fabricante, ddd, numero) VALUES
    (1, '11', '40028922'),
    (2, '21', '40028933'),
    (3, '31', '40028944'),
    (4, '41', '40028955');
```

</details>
