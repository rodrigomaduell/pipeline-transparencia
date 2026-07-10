"""Transformar:
Limpeza e Tipagem dos dados(Raw >>> Silver)
Converte tipos, calcula colunas e respeita a integridade referêncial"""

import csv
from datetime import datetime
import banco
from config import MYSQL_CONFIG, ARQUIVOS, CSV_SEPARADOR, CSV_ENCODING, TAMANHO_BLOCO

#-------------------------------------------------------------------------------

def converter_data(valor):
    """Converte string DD/MM/AAAA para objeto date. Retorna None se inválido."""
    if not valor or valor.strip() == "":
        return None
    try:
        return datetime.strptime(valor.strip(), "%d/%m/%Y").date()
    except ValueError:
        return None


def converter_decimal(valor):
    """Converte string com vírgula para float. Retorna None se inválido."""
    if not valor or valor.strip() == "":
        return None
    try:
        return float(valor.strip().replace(".", "").replace(",", "."))
    except ValueError:
        return None
    
#-------------------------------------------------------------------------------

def transformar_viagem(conexao):
    """Copia raw_viagem para silver_viagem com tipagem e colunas calculadas."""

    print("\nTransformando raw_viagem → silver_viagem...")

    banco.executar(conexao, "TRUNCATE TABLE silver_viagem")

    cursor_leitura = conexao.cursor(dictionary=True, buffered=True)
    cursor_leitura.execute("SELECT * FROM raw_viagem")

    bloco = []
    total = 0

    sql_insert = """
        INSERT INTO silver_viagem (
            id_viagem, num_proposta, situacao, viagem_urgente,
            cod_orgao_superior, nome_orgao_superior, nome_viajante, cargo,
            data_inicio, data_fim, destinos, motivo,
            valor_diarias, valor_passagens, valor_devolucao, valor_outros_gastos,
            valor_total, duracao_dias
        ) VALUES (
            %s, %s, %s, %s,
            %s, %s, %s, %s,
            %s, %s, %s, %s,
            %s, %s, %s, %s,
            %s, %s
        )
    """

    for linha in cursor_leitura:

        data_inicio = converter_data(linha.get("data_inicio"))
        data_fim    = converter_data(linha.get("data_fim"))

        val_diarias      = converter_decimal(linha.get("valor_diarias"))
        val_passagens    = converter_decimal(linha.get("valor_passagens"))
        val_devolucao    = converter_decimal(linha.get("valor_devolucao"))
        val_outros       = converter_decimal(linha.get("valor_outros_gastos"))

        # Colunas calculadas
        valor_total = None
        if all(v is not None for v in [val_diarias, val_passagens, val_devolucao, val_outros]):
            valor_total = val_diarias + val_passagens + val_outros - val_devolucao

        duracao_dias = None
        if data_inicio and data_fim:
            duracao_dias = (data_fim - data_inicio).days

        bloco.append((
            linha.get("id_viagem"),
            linha.get("num_proposta"),
            linha.get("situacao"),
            linha.get("viagem_urgente"),
            linha.get("cod_orgao_superior"),
            linha.get("nome_orgao_superior"),
            linha.get("nome_viajante"),
            linha.get("cargo"),
            data_inicio,
            data_fim,
            linha.get("destinos"),
            linha.get("motivo"),
            val_diarias,
            val_passagens,
            val_devolucao,
            val_outros,
            valor_total,
            duracao_dias,
        ))

        if len(bloco) >= TAMANHO_BLOCO:
            banco.inserir_em_lote(conexao, sql_insert, bloco)
            total += len(bloco)
            print(f"  {total} linhas inseridas...")
            bloco = []

    if bloco:
        banco.inserir_em_lote(conexao, sql_insert, bloco)
        total += len(bloco)

    cursor_leitura.close()
    print(f"  ✓ silver_viagem: {total} registros inseridos.")

#-------------------------------------------------------------------------------

def transformar_pagamento(conexao):
    """Copia raw_pagamento para silver_pagamento com tipagem."""

    print("\nTransformando raw_pagamento → silver_pagamento...")

    banco.executar(conexao, "TRUNCATE TABLE silver_pagamento")

    cursor_leitura = conexao.cursor(dictionary=True, buffered=True)
    cursor_leitura.execute("SELECT * FROM raw_pagamento")

    bloco = []
    total = 0

    sql_insert = """
        INSERT INTO silver_pagamento (
            id_viagem, num_proposta, nome_orgao_pagador,
            nome_ug_pagadora, tipo_pagamento, valor
        ) VALUES (%s, %s, %s, %s, %s, %s)
    """

    for linha in cursor_leitura:
        bloco.append((
            linha.get("id_viagem"),
            linha.get("num_proposta"),
            linha.get("nome_orgao_pagador"),
            linha.get("nome_ug_pagadora"),
            linha.get("tipo_pagamento"),
            converter_decimal(linha.get("valor")),
        ))

        if len(bloco) >= TAMANHO_BLOCO:
            banco.inserir_em_lote(conexao, sql_insert, bloco)
            total += len(bloco)
            print(f"  {total} linhas inseridas...")
            bloco = []

    if bloco:
        banco.inserir_em_lote(conexao, sql_insert, bloco)
        total += len(bloco)

    cursor_leitura.close()
    print(f"  ✓ silver_pagamento: {total} registros inseridos.")


def transformar_passagem(conexao):
    """Copia raw_passagem para silver_passagem com tipagem."""

    print("\nTransformando raw_passagem → silver_passagem...")

    banco.executar(conexao, "TRUNCATE TABLE silver_passagem")

    cursor_leitura = conexao.cursor(dictionary=True, buffered=True)
    cursor_leitura.execute("SELECT * FROM raw_passagem")

    bloco = []
    total = 0

    sql_insert = """
        INSERT INTO silver_passagem (
            id_viagem, meio_transporte,
            pais_origem_ida, uf_origem_ida, cidade_origem_ida,
            pais_destino_ida, uf_destino_ida, cidade_destino_ida,
            valor_passagem, taxa_servico, data_emissao
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    for linha in cursor_leitura:
        bloco.append((
            linha.get("id_viagem"),
            linha.get("meio_transporte"),
            linha.get("pais_origem_ida"),
            linha.get("uf_origem_ida"),
            linha.get("cidade_origem_ida"),
            linha.get("pais_destino_ida"),
            linha.get("uf_destino_ida"),
            linha.get("cidade_destino_ida"),
            converter_decimal(linha.get("valor_passagem")),
            converter_decimal(linha.get("taxa_servico")),
            converter_data(linha.get("data_emissao")),
        ))

        if len(bloco) >= TAMANHO_BLOCO:
            banco.inserir_em_lote(conexao, sql_insert, bloco)
            total += len(bloco)
            print(f"  {total} linhas inseridas...")
            bloco = []

    if bloco:
        banco.inserir_em_lote(conexao, sql_insert, bloco)
        total += len(bloco)

    cursor_leitura.close()
    print(f"  ✓ silver_passagem: {total} registros inseridos.")


def transformar_trecho(conexao):
    """Copia raw_trecho para silver_trecho com tipagem."""

    print("\nTransformando raw_trecho → silver_trecho...")

    banco.executar(conexao, "TRUNCATE TABLE silver_trecho")

    cursor_leitura = conexao.cursor(dictionary=True, buffered=True)
    cursor_leitura.execute("SELECT * FROM raw_trecho")

    bloco = []
    total = 0

    sql_insert = """
        INSERT INTO silver_trecho (
            id_viagem, sequencia_trecho,
            origem_data, origem_uf, origem_cidade,
            destino_data, destino_uf, destino_cidade,
            meio_transporte, numero_diarias
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    for linha in cursor_leitura:
        bloco.append((
            linha.get("id_viagem"),
            linha.get("sequencia_trecho"),
            converter_data(linha.get("origem_data")),
            linha.get("origem_uf"),
            linha.get("origem_cidade"),
            converter_data(linha.get("destino_data")),
            linha.get("destino_uf"),
            linha.get("destino_cidade"),
            linha.get("meio_transporte"),
            converter_decimal(linha.get("numero_diarias")),
        ))

        if len(bloco) >= TAMANHO_BLOCO:
            banco.inserir_em_lote(conexao, sql_insert, bloco)
            total += len(bloco)
            print(f"  {total} linhas inseridas...")
            bloco = []

    if bloco:
        banco.inserir_em_lote(conexao, sql_insert, bloco)
        total += len(bloco)

    cursor_leitura.close()
    print(f"  ✓ silver_trecho: {total} registros inseridos.")

#-------------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== FASE 2 — TRANSFORMAÇÃO RAW >>> SILVER ===\n")

    conexao = banco.conectar()

    try:
        # Desabilita FK para permitir TRUNCATE (O MYSQL não permite truncar tabelas com FK ativas)
        banco.executar(conexao, "SET FOREIGN_KEY_CHECKS = 0")

        transformar_viagem(conexao)
        transformar_pagamento(conexao)
        transformar_passagem(conexao)
        transformar_trecho(conexao)

        # Reabilita FK
        banco.executar(conexao, "SET FOREIGN_KEY_CHECKS = 1")

        conexao.commit()
        print("\n=== TRANSFORMAÇÃO CONCLUÍDA ===")

    except Exception as e:
        banco.executar(conexao, "SET FOREIGN_KEY_CHECKS = 1") # Reabilita FK mesmo em caso de erro
        conexao.rollback()
        print(f"\nErro na transformação: {e}")
        raise

    finally:
        conexao.close()    