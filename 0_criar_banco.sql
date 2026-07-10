-- =======================================================
-- Pipeline de dados - Viagens a Serviço
-- Portal da Transparência do Governo Fedeeral
-- Autor: Rodrigo Maduell
-- =======================================================


CREATE DATABASE IF NOT EXISTS transparencia;
USE transparencia;

-- =======================================================
-- CAMADA RAW - Tabelas para armazenar os dados brutos
-- =======================================================

DROP TABLE IF EXISTS silver_trecho;
DROP TABLE IF EXISTS silver_passagem;
DROP TABLE IF EXISTS silver_pagamento;
DROP TABLE IF EXISTS silver_viagem;

DROP TABLE IF EXISTS raw_trecho;
DROP TABLE IF EXISTS raw_passagem;
DROP TABLE IF EXISTS raw_pagamento;
DROP TABLE IF EXISTS raw_viagem;


CREATE TABLE raw_viagem (
    id_viagem                          VARCHAR(20),
    num_proposta                       VARCHAR(20),
    situacao                           VARCHAR(50),
    viagem_urgente                     VARCHAR(20),
    justificativa_urgencia             VARCHAR(1000),
    cod_orgao_superior                 VARCHAR(20),
    nome_orgao_superior                VARCHAR(100),
    cod_orgao_solicitante              VARCHAR(20),
    nome_orgao_solicitante             VARCHAR(100),
    cpf_viajante                       VARCHAR(20),
    nome_viajante                      VARCHAR(255),
    cargo                              VARCHAR(255),
    funcao                             VARCHAR(255),
    descricao_funcao                   VARCHAR(255),
    data_inicio                        VARCHAR(20),
    data_fim                           VARCHAR(20),
    destinos                           VARCHAR(4000),
    motivo                             VARCHAR(4000),
    valor_diarias                      VARCHAR(20),
    valor_passagens                    VARCHAR(20),
    valor_devolucao                    VARCHAR(20),
    valor_outros_gastos                VARCHAR(20)
)

ENGINE=InnoDB ROW_FORMAT=DYNAMIC 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_general_ci; 


CREATE TABLE raw_pagamento (
    id_viagem                         VARCHAR(20),
    num_proposta                      VARCHAR(40),
    cod_orgao_superior                VARCHAR(40),
    nome_orgao_superior               VARCHAR(100),
    cod_orgao_pagador                 VARCHAR(40),
    nome_orgao_pagador                VARCHAR(100),
    cod_ug_pagadora                   VARCHAR(40),
    nome_ug_pagadora                  VARCHAR(100),
    tipo_pagamento                    VARCHAR(100),
    valor                             VARCHAR(20)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_general_ci;

CREATE TABLE raw_passagem (
    id_viagem               VARCHAR(20),
    num_proposta            VARCHAR(20),
    meio_transporte         VARCHAR(50),
    pais_origem_ida         VARCHAR(60),
    uf_origem_ida           VARCHAR(40),
    cidade_origem_ida       VARCHAR(80),
    pais_destino_ida        VARCHAR(60),
    uf_destino_ida          VARCHAR(40),
    cidade_destino_ida      VARCHAR(80),
    pais_origem_volta       VARCHAR(60),
    uf_origem_volta         VARCHAR(40),
    cidade_origem_volta     VARCHAR(80),
    pais_destino_volta      VARCHAR(60),
    uf_destino_volta        VARCHAR(40),
    cidade_destino_volta    VARCHAR(80),
    valor_passagem          VARCHAR(20),
    taxa_servico            VARCHAR(20),
    data_emissao            VARCHAR(20),
    hora_emissao            VARCHAR(20)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_general_ci;

CREATE TABLE raw_trecho (
    id_viagem               VARCHAR(20),
    num_proposta            VARCHAR(40),
    sequencia_trecho        VARCHAR(60),
    origem_data             VARCHAR(20),
    origem_pais             VARCHAR(60),
    origem_uf               VARCHAR(40),
    origem_cidade           VARCHAR(80),
    destino_data            VARCHAR(20),
    destino_pais            VARCHAR(60),
    destino_uf              VARCHAR(40),
    destino_cidade          VARCHAR(80),
    meio_transporte         VARCHAR(50),
    numero_diarias          VARCHAR(20),
    missao                  VARCHAR(4000)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_general_ci;


-- =======================================================
-- CAMADA SILVER - Dados tratados com PK, FK e constraints
-- =======================================================

-- TABELA PAI - silver_viagem
CREATE TABLE silver_viagem (
    id_viagem                       VARCHAR(20) PRIMARY KEY,
    num_proposta                    VARCHAR(40),
    situacao                        VARCHAR(50),
    viagem_urgente                  VARCHAR(40),
    cod_orgao_superior                  VARCHAR(20),
    nome_orgao_superior                 VARCHAR(100) NOT NULL,
    nome_viajante                    VARCHAR(255),
    cargo                            VARCHAR(255),
    data_inicio                       DATE,
    data_fim                          DATE,
    destinos                         VARCHAR(4000),
    motivo                           VARCHAR(4000),
    valor_diarias                    DECIMAL(10,2), CHECK (valor_diarias >= 0),
    valor_passagens                  DECIMAL(10,2),
    valor_devolucao                  DECIMAL(10,2),
    valor_outros_gastos              DECIMAL(10,2),
    valor_total                      DECIMAL(10,2),
    duracao_dias                     INT
    )
    ENGINE=InnoDB ROW_FORMAT=DYNAMIC
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_general_ci;

-- TABELAS FILHAS - silver_pagamento, silver_passagem, silver_trecho
    CREATE TABLE silver_pagamento (
        id_pagamento                   INT               PRIMARY KEY AUTO_INCREMENT,
        id_viagem                      VARCHAR(20)       NOT NULL,
        num_proposta                   VARCHAR(40),
        nome_orgao_pagador             VARCHAR(255),
        nome_ug_pagadora               VARCHAR(255),
        tipo_pagamento                 VARCHAR(100),
        valor                          DECIMAL(10,2)     CHECK (valor >= 0),
        FOREIGN KEY (id_viagem) REFERENCES silver_viagem(id_viagem)
    )
    ENGINE=InnoDB
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_general_ci;


    CREATE TABLE silver_passagem (
        id_passagem                    INT               PRIMARY KEY AUTO_INCREMENT,
        id_viagem                      VARCHAR(20)       NOT NULL,
        meio_transporte                 VARCHAR(50),
        pais_origem_ida                 VARCHAR(60),
        uf_origem_ida                   VARCHAR(40),
        cidade_origem_ida               VARCHAR(80),
        pais_destino_ida                VARCHAR(60),
        uf_destino_ida                  VARCHAR(40),
        cidade_destino_ida              VARCHAR(80),
        valor_passagem                  DECIMAL(10,2)     CHECK (valor_passagem >= 0),
        taxa_servico                    DECIMAL(10,2)     CHECK (taxa_servico >=0),
        data_emissao                    DATE,
        FOREIGN KEY (id_viagem) REFERENCES silver_viagem(id_viagem)
    )
    ENGINE=InnoDB
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_general_ci;


    CREATE TABLE silver_trecho (
        id_trecho                      INT               PRIMARY KEY AUTO_INCREMENT,
        id_viagem                      VARCHAR(20)       NOT NULL,
        sequencia_trecho               VARCHAR(60)       NOT NULL,
        origem_data                    DATE,
        origem_uf                      VARCHAR(40),
        origem_cidade                  VARCHAR(80),
        destino_data                   DATE,
        destino_uf                     VARCHAR(40),
        destino_cidade                 VARCHAR(80),
        meio_transporte                VARCHAR(50),
        numero_diarias                 DECIMAL(10,2)     CHECK (numero_diarias >= 0),
        FOREIGN KEY (id_viagem) REFERENCES silver_viagem(id_viagem),
        UNIQUE (id_viagem, sequencia_trecho)
    )
    ENGINE=InnoDB
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_general_ci;