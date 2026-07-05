## AUTOR: Rodrigo Maduell Fonseca
## TURMA: Análise de Dados com Python - T2 - 2026
## INSTITUIÇÃO: SCTEC/SENAI-SC 

# NOME PROJETO: Pipeline de dados - viagens a serviço 
# ORIGEM DADOS: Portal da Transparência do Governo Federal


## DESCRIÇÃO DO PROJETO:

Pipeline de dados criado do zero para extrair, limpar e analisar dados públicos de 'Viagens a Serviço' retirados do Portal da Transparência do Governo Federal.

O projeto visa transformar dados brutos em métricas claras para tomada de decisão.

### Arquitetura Medallion

Este projeto segue a Arquitetura Medallion com três camadas progressivas de qualidade: 

RAW >>> SILVER >>> GOLD

🥉 Raw: Cópia fiel dos CSVs, todas as colunas VARCHAR
Tabelas: raw_viagem, raw_pagamento, raw_passagem, raw_trecho

🥈 Silver: Dados tipados, limpos e com integridade referencial 
Tabelas: silver_viagem, silver_pagamento, silver_passagem, silver_trecho

🥇 Gold: Agregações e métricas prontas para análise
Tabelas: gold_resumo_orgaos + views analíticas


## TÉCNOLOGIAS UTILIZADAS

- **Python 3.12** — linguagem principal
- **Pandas** — manipulação e transformação de dados
- **MySQL** — banco de dados relacional
- **mysql-connector-python** — integração Python + MySQL
- **Matplotlib / Seaborn** — visualização de dados
- **Jupyter Notebook** — análise exploratória e camada Gold
- **Git / GitHub** — versionamento do projeto


## ESTRUTURA DO PROJETO

pipeline-transparencia/
├-- config.py            # Parâmetros e leitura do .env
├-- banco.py             # Conexão e funções utilitárias do MySQL
├-- .env.example         # Modelo de credenciais (copie para .env)
├-- .gitignore           # Arquivos ignorados pelo Git
├-- requirements.txt     # Dependências do projeto
|-- README.md            # Descrição do projeto / Instruções
├-- 0_criar_banco.sql    # Criação do banco e das 8 tabelas
├-- 1_extrair.py         # Download + carga na camada Raw
├-- 2_transformar.py     # Limpeza e tipagem (Raw >>> Silver)
└-- 3_analise.ipynb      # Camada Gold + perguntas de negócio + gráficos


## COMO EXECUTAR

### 1. Clonar o repositório
```bash
git clone https://github.com/rodrigomaduell/pipeline-transparencia.git
cd pipeline-transparencia
```

### 2. Criar e ativar o ambiente virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar credenciais
```bash
cp .env.example .env
# Edite o arquivo .env com suas credenciais do MySQL
```

### 5. Executar o pipeline na ordem
```bash
# Criar banco e tabelas
mysql -u root -p < 0_criar_banco.sql

# Extração e carga Raw
python 1_extrair.py

# Transformação e carga Silver
python 2_transformar.py

# Análise Gold (abrir no Jupyter)
jupyter notebook 3_analise.ipynb
```

## PERGUNTAS DE NEGÓCIO

1. Quais os 5 órgãos com maior custo total de viagens?
2. Quais os 3 destinos com maior custo médio por viagem?
3. Qual a viagem de maior duração e seu custo total?
4. Qual o tipo de pagamento com maior valor médio?
5. Qual o meio de transporte mais usado nos trechos?
6. Qual a UF de destino que aparece em mais trechos?
7. Qual órgão pagou mais no total?

> Os resultados, gráficos e insights estão detalhados no notebook '3_analise.ipynb'.


## INSIGHTS

> *Será preenchido após a execução das análises*


