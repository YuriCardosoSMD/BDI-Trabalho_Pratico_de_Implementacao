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
    cod_categoria SERIAL      CONSTRAINT pk_categoria PRIMARY KEY,
    descricao     VARCHAR(80) NOT NULL
                  CONSTRAINT uq_categoria_descricao UNIQUE
);

CREATE TABLE fabricante (
    cod_fabricante SERIAL       CONSTRAINT pk_fabricante PRIMARY KEY,
    razao_social   VARCHAR(120) NOT NULL
);

CREATE TABLE filial (
    cod_filial   SERIAL       CONSTRAINT pk_filial PRIMARY KEY,
    razao_social VARCHAR(120) NOT NULL
);

CREATE TABLE funcionario (
    id_funcionario SERIAL        CONSTRAINT pk_funcionario PRIMARY KEY,
    nome           VARCHAR(120)  NOT NULL,
    salario        DECIMAL(10,2) NOT NULL
                   CONSTRAINT ck_funcionario_salario CHECK (salario >= 0)
);

CREATE TABLE cliente (
    id_cliente SERIAL       CONSTRAINT pk_cliente PRIMARY KEY,
    nome       VARCHAR(120) NOT NULL
);

-- ---------------------------------------------------------------------
-- Medicamento (categoria e fabricante obrigatórios)
-- ---------------------------------------------------------------------
CREATE TABLE medicamento (
    id_medicamento SERIAL        CONSTRAINT pk_medicamento PRIMARY KEY,
    descricao      VARCHAR(120)  NOT NULL,
    preco          DECIMAL(10,2) NOT NULL
                   CONSTRAINT ck_medicamento_preco CHECK (preco >= 0),
    cod_categoria  INTEGER       NOT NULL,
    cod_fabricante INTEGER       NOT NULL,
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
    id_venda       SERIAL    CONSTRAINT pk_venda PRIMARY KEY,
    data_hora      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    cod_filial     INTEGER   NOT NULL,
    id_cliente     INTEGER   NOT NULL,
    id_funcionario INTEGER   NOT NULL,
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
    id_venda       INTEGER       NOT NULL,
    id_medicamento INTEGER       NOT NULL,
    quantidade     INTEGER       NOT NULL
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
    id_cliente INTEGER    NOT NULL,
    ddd        VARCHAR(3) NOT NULL
               CONSTRAINT ck_tel_cliente_ddd CHECK (ddd ~ '^[0-9]{2,3}$'),
    numero     VARCHAR(9) NOT NULL
               CONSTRAINT ck_tel_cliente_numero CHECK (numero ~ '^[0-9]{8,9}$'),
    CONSTRAINT pk_telefone_cliente PRIMARY KEY (id_cliente, ddd, numero),
    CONSTRAINT fk_telefone_cliente FOREIGN KEY (id_cliente)
        REFERENCES cliente (id_cliente)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE telefone_funcionario (
    id_funcionario INTEGER    NOT NULL,
    ddd            VARCHAR(3) NOT NULL
                   CONSTRAINT ck_tel_funcionario_ddd CHECK (ddd ~ '^[0-9]{2,3}$'),
    numero         VARCHAR(9) NOT NULL
                   CONSTRAINT ck_tel_funcionario_numero CHECK (numero ~ '^[0-9]{8,9}$'),
    CONSTRAINT pk_telefone_funcionario PRIMARY KEY (id_funcionario, ddd, numero),
    CONSTRAINT fk_telefone_funcionario FOREIGN KEY (id_funcionario)
        REFERENCES funcionario (id_funcionario)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE telefone_filial (
    cod_filial INTEGER    NOT NULL,
    ddd        VARCHAR(3) NOT NULL
               CONSTRAINT ck_tel_filial_ddd CHECK (ddd ~ '^[0-9]{2,3}$'),
    numero     VARCHAR(9) NOT NULL
               CONSTRAINT ck_tel_filial_numero CHECK (numero ~ '^[0-9]{8,9}$'),
    CONSTRAINT pk_telefone_filial PRIMARY KEY (cod_filial, ddd, numero),
    CONSTRAINT fk_telefone_filial FOREIGN KEY (cod_filial)
        REFERENCES filial (cod_filial)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE telefone_fabricante (
    cod_fabricante INTEGER    NOT NULL,
    ddd            VARCHAR(3) NOT NULL
                   CONSTRAINT ck_tel_fabricante_ddd CHECK (ddd ~ '^[0-9]{2,3}$'),
    numero         VARCHAR(9) NOT NULL
                   CONSTRAINT ck_tel_fabricante_numero CHECK (numero ~ '^[0-9]{8,9}$'),
    CONSTRAINT pk_telefone_fabricante PRIMARY KEY (cod_fabricante, ddd, numero),
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