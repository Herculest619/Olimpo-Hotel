-- CRIA O BANCO DE DADOS hotel

-- APAGA EM ORDEDM ESPECÍFICA AS TABELAS CASO ELAS EXISTAM
-- POIS EXISTEM CHAVES ESTRANGEIRAS ENTRE ELAS

-- APAGA A TABELA ALOCA CASO ELA EXISTA
DROP TABLE IF EXISTS ALOCA;

-- APAGA A TABELA POSSUI CASO ELA EXISTA
DROP TABLE IF EXISTS POSSUI;

-- APAGA A TABELA QUARTO CASO ELA EXISTA
DROP TABLE IF EXISTS QUARTO;

-- APAGA A TABELA RESERVA CASO ELA EXISTA
DROP TABLE IF EXISTS RESERVA;

-- APAGA A TABELA SERVICO CASO ELA EXISTA
DROP TABLE IF EXISTS SERVICO;

-- APAGA A TABELA CLIENTE CASO ELA EXISTA
DROP TABLE IF EXISTS CLIENTE;


-- cria a tabela cliente
CREATE TABLE CLIENTE 
( 
    CPF CHAR(11) NOT NULL,
    Nome_cliente VARCHAR(100) NOT NULL,  
    Telefone_cliente VARCHAR(20),  
    Endereco_cliente VARCHAR(200),
    Data_nasc_cliente DATE NOT NULL,
    CPF_TITULAR CHAR(11),

    PRIMARY KEY (CPF),
    FOREIGN KEY (CPF_TITULAR) REFERENCES CLIENTE (CPF)
        ON UPDATE CASCADE  -- ATUALIZA CPF DO ACOMPANHANTE CASO ELE MUDE
        ON DELETE SET NULL -- DELETA ACOMPANHANTE CASO CLIENTE SEJA DELETADO
); 
-- INSERE DADOS NA TABELA CLIENTE
INSERT INTO CLIENTE 
VALUES 
('12312312312', 'Carlos', '3190000001', 'Rua 7', '1990-01-01', NULL),

('12154513454', 'Ana', '1140028922', 'Rua 4', '1999-04-05', NULL),

('00000000001', 'Paula', '3190000002', 'Rua 6', '2000-04-05', NULL),
('00548431256', 'Pedro', '3198745632', 'Rua 5', '2001-01-05', '00000000001'),

('12345678966', 'João', '3138524905', 'Rua 1', '1987-07-09', NULL),
('16341414889', 'Maria', '31971681418', 'Rua 2', '2015-12-25', '12345678966'),
('06094904104', 'José', '3170707070', 'Rua 3', '1999-05-04', '12345678966');


-- CRIA A TABELA SERVICO
CREATE TABLE SERVICO 
( 
    Nome_servico VARCHAR(100) NOT NULL,
    Valor_servico FLOAT NOT NULL,

    PRIMARY KEY (Nome_servico)
);
-- INSERE DADOS NA TABELA SERVICO
INSERT INTO SERVICO
VALUES 
('Cafe da manha', 20),
('Almoco', 30),
('Jantar', 40),
('Lavanderia', 50),
('Estacionamento', 15),
('Piscina', 25),
('Academia', 35),
('Sauna', 90),
('SPA', 100);


-- CRIA A TABELA RESERVA
CREATE TABLE RESERVA 
( 
    ID_reserva INT NOT NULL AUTO_INCREMENT,
    Data_check_in_reserva DATE NOT NULL,
    Data_check_out_reserva DATE NOT NULL,
    CLIENTE CHAR(11) NOT NULL,

    PRIMARY KEY (ID_reserva),
    FOREIGN KEY (CLIENTE) REFERENCES CLIENTE (CPF)
        ON UPDATE CASCADE  -- ATUALIZA CPF DO CLIENTE CASO ELE MUDE
        ON DELETE RESTRICT -- NÃO DEIXA DELETAR CLIENTE SE ELE TIVER RESERVA
);
-- INSERE DADOS NA TABELA RESERVA
INSERT INTO RESERVA
VALUES
(1, '2023-01-02', '2020-01-03', '12312312312'),
(2, '2023-01-04', '2020-02-06', '12154513454'),
(3, '2023-01-03', '2020-01-15', '00000000001'),
(4, '2023-01-01', '2020-01-03', '12345678966');


-- CRIA A TABELA QUARTO
CREATE TABLE QUARTO 
( 
    Numero_quarto INT NOT NULL,
    Tipo_quarto VARCHAR(100) NOT NULL,
    Capacidade_quarto INT NOT NULL, 
    Valor_quarto FLOAT NOT NULL,
        
    PRIMARY KEY (Numero_quarto)
);
-- INSERE DADOS NA TABELA QUARTO
INSERT INTO QUARTO
VALUES
(101, 'Solteiro', 1, 100),
(102, 'Solteiro', 1, 100),
(103, 'Solteiro', 1, 100),
(201, 'Casal', 2, 250),
(202, 'Casal', 2, 250),
(203, 'Casal', 2, 250),
(301, 'Queen', 2, 300),
(302, 'Queen', 2, 300),
(303, 'Queen', 2, 300),
(401, 'King', 3, 500),
(402, 'King', 3, 500),
(403, 'King', 3, 500);


-- CRIA A TABELA POSSUI
CREATE TABLE POSSUI
( 
    Nome_servico VARCHAR(100) NOT NULL, 
    ID_reserva INT NOT NULL,
    Quantidade_servico INT DEFAULT 1 NOT NULL,

    PRIMARY KEY (Nome_servico, ID_reserva),
    
    FOREIGN KEY (Nome_servico) REFERENCES SERVICO (Nome_servico)
        ON UPDATE CASCADE -- ATUALIZA NOME_SERVICO CASO ELE MUDE
        ON DELETE RESTRICT, -- NÃO DEIXA DELETAR SERVICO SE ELE ESTIVER SENDO USADO

    FOREIGN KEY (ID_reserva) REFERENCES RESERVA (ID_reserva)
        ON UPDATE CASCADE -- ATUALIZA ID_RESERVA DA RESERVA CASO ELE MUDE
        ON DELETE RESTRICT -- NÃO DEIXA DELETAR RESERVA SE ELA ESTIVER SENDO USADA
);
-- INSERE DADOS NA TABELA POSSUI
INSERT INTO POSSUI
VALUES
('Almoco', 1, 1),
('Jantar', 2, 1);


-- CRIA A TABELA ALOCA
CREATE TABLE ALOCA
(
    Numero_quarto INT NOT NULL,
    ID_reserva INT NOT NULL,

    PRIMARY KEY (Numero_quarto, ID_reserva),

    FOREIGN KEY (Numero_quarto) REFERENCES QUARTO (Numero_quarto)
        ON UPDATE CASCADE -- ATUALIZA NUMERO_QUARTO DO QUARTO CASO ELE MUDE
        ON DELETE RESTRICT, -- NÃO DEIXA DELETAR QUARTO SE ELE ESTIVER SENDO USADO

    FOREIGN KEY (ID_reserva) REFERENCES RESERVA (ID_reserva)
        ON UPDATE CASCADE -- ATUALIZA ID_RESERVA DA RESERVA CASO ELE MUDE
        ON DELETE RESTRICT -- NÃO DEIXA DELETAR RESERVA SE ELA ESTIVER SENDO USADA
);
-- INSERE DADOS NA TABELA ALOCA
INSERT INTO ALOCA
VALUES
(101, 1),
(201, 2),
(301, 3),
(401, 4);