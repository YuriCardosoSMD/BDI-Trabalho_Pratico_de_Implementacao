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
               CONSTRAINT ck_tel_cliente_numero CHECK (numero ~ '^[0-9]{8,9}$'),
    CONSTRAINT pk_telefone_cliente PRIMARY KEY (id_cliente, ddd, numero),
    CONSTRAINT fk_telefone_cliente FOREIGN KEY (id_cliente)
        REFERENCES cliente (id_cliente)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE telefone_funcionario (
    id_funcionario INTEGER NOT NULL,
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
    cod_filial INTEGER NOT NULL,
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
    cod_fabricante INTEGER NOT NULL,
    ddd            VARCHAR(3) NOT NULL
                   CONSTRAINT ck_tel_fabricante_ddd CHECK (ddd ~ '^[0-9]{2,3}$'),
    numero         VARCHAR(9) NOT NULL
                   CONSTRAINT ck_tel_fabricante_numero CHECK (numero ~ '^[0-9]{8,9}$'),
    CONSTRAINT pk_telefone_fabricante PRIMARY KEY (cod_fabricante, ddd, numero),
    CONSTRAINT fk_telefone_fabricante FOREIGN KEY (cod_fabricante)
        REFERENCES fabricante (cod_fabricante)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- =====================================================================
-- Carga inicial de dados fictícios
-- Os IDs (SERIAL) são gerados na ordem dos INSERTs abaixo
-- =====================================================================

INSERT INTO categoria (descricao) VALUES
    ('Analgésico'),             -- 1
    ('Antibiótico'),            -- 2
    ('Antialérgico'),           -- 3
    ('Anti-inflamatório'),      -- 4
    ('Vitamina e suplemento');  -- 5

INSERT INTO fabricante (razao_social) VALUES
    ('Mariano Farmacêutica Ltda'),    -- 1
    ('Lobão Laboratórios S/A'),       -- 2
    ('Serafim Medicamentos Ltda'),    -- 3
    ('Cardoso Pharma S/A');           -- 4

INSERT INTO filial (razao_social) VALUES
    ('Farmácia DITY - Matriz Benfica'),  -- 1
    ('Farmácia DITY - Aldeota'),         -- 2
    ('Farmácia DITY - Messejana');       -- 3

INSERT INTO funcionario (nome, salario) VALUES
    ('Dália Mariano',    3200.00),  -- 1
    ('Isabele Lobão',    2800.00),  -- 2
    ('Thaíssa Serafim',  2800.00),  -- 3
    ('Yuri Cardoso',     2500.00);  -- 4

INSERT INTO cliente (nome) VALUES
    ('Dália Freitas da Silva Mariano'),      -- 1
    ('Isabele Alessandra Fernandes Lobão'),  -- 2
    ('Thaíssa Victória Nunes Serafim'),      -- 3
    ('Yuri da Silva Cardoso');               -- 4

INSERT INTO medicamento (descricao, preco, cod_categoria, cod_fabricante) VALUES
    ('Paracetamol 750mg',      12.50, 1, 1),  -- 1
    ('Dipirona Sódica 500mg',   9.90, 1, 2),  -- 2
    ('Amoxicilina 500mg',      24.90, 2, 3),  -- 3
    ('Azitromicina 500mg',     32.00, 2, 4),  -- 4
    ('Loratadina 10mg',        15.00, 3, 1),  -- 5
    ('Cetirizina 10mg',        18.50, 3, 2),  -- 6
    ('Ibuprofeno 400mg',       11.20, 4, 3),  -- 7
    ('Vitamina C 1g',          22.00, 5, 4);  -- 8

INSERT INTO estoque (cod_filial, id_medicamento, quantidade) VALUES
    (1, 1, 100), (1, 2, 80), (1, 3, 50), (1, 4, 40),
    (1, 5,  30), (1, 6, 25), (1, 7, 60), (1, 8, 45),
    (2, 1,  60), (2, 2, 40), (2, 5, 70), (2, 6, 55),
    (3, 3,  20), (3, 7, 90), (3, 8, 65);

INSERT INTO venda (cod_filial, id_cliente, id_funcionario) VALUES
    (1, 1, 4),  -- 1: Dália comprou na Matriz, atendida por Yuri
    (1, 2, 3),  -- 2: Isabele comprou na Matriz, atendida por Thaíssa
    (2, 3, 2),  -- 3: Thaíssa comprou na Aldeota, atendida por Isabele
    (3, 4, 1),  -- 4: Yuri comprou em Messejana, atendido por Dália
    (2, 1, 2);  -- 5: Dália comprou na Aldeota, atendida por Isabele

INSERT INTO item_venda (id_venda, id_medicamento, quantidade, preco_unitario) VALUES
    (1, 1, 2, 12.50),
    (1, 8, 1, 22.00),
    (2, 2, 3,  9.90),
    (3, 5, 1, 15.00),
    (3, 6, 1, 18.50),
    (4, 7, 2, 11.20),
    (4, 3, 1, 24.90),
    (5, 2, 1,  9.90);

INSERT INTO telefone_cliente (id_cliente, ddd, numero) VALUES
    (1, '85', '988110001'),
    (2, '85', '988220002'),
    (3, '85', '988330003'),
    (4, '85', '988440004'),
    (4, '85', '32440004');

INSERT INTO telefone_funcionario (id_funcionario, ddd, numero) VALUES
    (1, '85', '997110001'),
    (2, '85', '997220002'),
    (3, '85', '997330003'),
    (4, '85', '997440004');

INSERT INTO telefone_filial (cod_filial, ddd, numero) VALUES
    (1, '85', '33110000'),
    (2, '85', '33220000'),
    (3, '85', '33330000');

INSERT INTO telefone_fabricante (cod_fabricante, ddd, numero) VALUES
    (1, '85', '40041001'),
    (2, '85', '40041002'),
    (3, '85', '40041003'),
    (4, '85', '40041004');
