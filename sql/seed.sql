-- =====================================================================
-- Script de Carga Inicial (Seed) - Controle de Vendas e Estoque
-- =====================================================================

BEGIN;

-- 1. Categorias
INSERT INTO categoria (descricao) VALUES
    ('Analgésicos e Antitérmicos'),
    ('Antibióticos'),
    ('Anti-inflamatórios'),
    ('Antialérgicos'),
    ('Vitaminas e Suplementos');

-- 2. Fabricantes
INSERT INTO fabricante (razao_social) VALUES
    ('EMS S/A'),
    ('Medley Farmacêutica Ltda'),
    ('Eurofarma Laboratórios S/A'),
    ('Neo Química Laboratório');

-- 3. Filiais
INSERT INTO filial (razao_social) VALUES
    ('Farmácia Central - Matriz Aldeota'),
    ('Farmácia Filial Sul - Messejana'),
    ('Farmácia Filial Norte - Bezerra de Menezes');

-- 4. Funcionários
INSERT INTO funcionario (nome, salario) VALUES
    ('Carlos Eduardo Mendes', 2850.00),
    ('Fernanda Costa Lima', 3100.00),
    ('Roberto Alves Rocha', 2700.00);

-- 5. Clientes (Cliente 3 não terá vendas para permitir teste de exclusão D1)
INSERT INTO cliente (nome) VALUES
    ('Ana Beatriz Souza'),
    ('Marcos Vinícius Oliveira'),
    ('Juliana Martins Pereira');

-- 6. Medicamentos
INSERT INTO medicamento (descricao, preco, cod_categoria, cod_fabricante) VALUES
    ('Dipirona Monoidratada 500mg (10 comp.)', 8.50, 1, 1),
    ('Paracetamol 750mg (20 comp.)', 14.90, 1, 2),
    ('Amoxicilina 500mg (21 cáps.)', 32.00, 2, 3),
    ('Ibuprofeno 600mg (20 comp.)', 21.50, 3, 2),
    ('Loratadina 10mg (12 comp.)', 16.75, 4, 4),
    ('Vitamina C 1g Efervescente (10 comp.)', 19.90, 5, 1);

-- 7. Estoque inicial nas filiais (necessário para testar S3 e U2)
INSERT INTO estoque (cod_filial, id_medicamento, quantidade) VALUES
    (1, 1, 120), (1, 2, 85), (1, 3, 40), (1, 4, 60), (1, 5, 50), (1, 6, 90),
    (2, 1, 75),  (2, 2, 60), (2, 4, 35), (2, 5, 45),
    (3, 1, 100), (3, 3, 25), (3, 6, 70);

-- 8. Vendas e Itens de Venda iniciais (para testar S4, S5, D1 e D2)
INSERT INTO venda (cod_filial, id_cliente, id_funcionario) VALUES
    (1, 1, 1),
    (2, 2, 2);

INSERT INTO item_venda (id_venda, id_medicamento, quantidade, preco_unitario) VALUES
    (1, 1, 2, 8.50),
    (1, 6, 1, 19.90),
    (2, 2, 1, 14.90),
    (2, 4, 2, 21.50);

-- 9. Telefones (4 tabelas de atributos multivalorados)
INSERT INTO telefone_cliente (id_cliente, ddd, numero) VALUES
    (1, '85', '998765432'),
    (2, '85', '987654321'),
    (3, '85', '991234567');

INSERT INTO telefone_funcionario (id_funcionario, ddd, numero) VALUES
    (1, '85', '996543210'),
    (2, '85', '995432109');

INSERT INTO telefone_filial (cod_filial, ddd, numero) VALUES
    (1, '85', '32441000'),
    (2, '85', '32742000'),
    (3, '85', '32873000');

INSERT INTO telefone_fabricante (cod_fabricante, ddd, numero) VALUES
    (1, '19', '38879800'),
    (2, '19', '21178000'),
    (3, '11', '50908600'),
    (4, '62', '33102000');

COMMIT;