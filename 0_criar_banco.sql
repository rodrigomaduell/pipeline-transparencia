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
    viagem_urgente                     VARCHAR(5),
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
    num_proposta                      VARCHAR(20),
    cod_orgao_superior                VARCHAR(20),
    nome_orgao_superior               VARCHAR(100),
    cod_orgao_pagador                 VARCHAR(20),
    nome_orgao_pagador                VARCHAR(100),
    cod_ug_pagadora                   VARCHAR(20),
    nome_ug_pagadora                  VARCHAR(100),
    tipo_pagamento                    VARCHAR(20),
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
    hora_emissao            VARCHAR(10)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_general_ci;

CREATE TABLE raw_trecho (
    id_viagem               VARCHAR(20),
    num_proposta            VARCHAR(20),
    sequencia_trecho        VARCHAR(10),
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

