"""
1 - Extração de Dados
Faz download do arquivo .zip do Google Drive, 
descompacta e extrai os 4 arquivos .csv,
faz a carga nas tabelas Raw correspondentes no MySQL.  
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))  # Adiciona o diretório src ao sys.path
import os
import zipfile
import csv
import requests
from config import DRIVE_FILE_ID, PASTA_DADOS, ARQUIVOS, TAMANHO_BLOCO, CSV_ENCODING, CSV_SEPARADOR
import banco

#-------------------------------------------------------------------------------

def fazer_download():
    """Baixa o arquivo .zip do Google Drive e salva na pasta data/."""

    PASTA_DADOS.mkdir(exist_ok=True)

    caminho_zip = PASTA_DADOS / "viagens.zip"

    url = f"https://drive.usercontent.google.com/download?id={DRIVE_FILE_ID}&export=download&confirm=t"

    print("Iniciando download do arquivo...")

    try:
        sessao = requests.Session()
        resposta = sessao.get(url, stream=True)
        resposta.raise_for_status()

        with open(caminho_zip, "wb") as arquivo:
            for bloco in resposta.iter_content(chunk_size=8192):
                arquivo.write(bloco)

        print(f"Download concluído. {caminho_zip}")
        return caminho_zip

    except requests.exceptions.RequestException as e:
        print(f"Erro no download: {e}")
        raise

#-------------------------------------------------------------------------------

def descompactar(caminho_zip):
    """Descompacta o .zip e retorna o caminho da pasta data/."""

    print("Descompactando arquivo...")

    try:
        with zipfile.ZipFile(caminho_zip, "r") as zip_ref:
            zip_ref.extractall(PASTA_DADOS)

        print(f"Arquivos extraídos em: {PASTA_DADOS}")
        return PASTA_DADOS

    except zipfile.BadZipFile as e:
        print(f"Erro ao descompactar: {e}")
        raise

#-------------------------------------------------------------------------------

def carregar_raw(caminho_pasta):
    """Lê cada CSV em blocos e carrega nas tabelas Raw."""

    conexao = banco.conectar()

    try:
        for chave, info in ARQUIVOS.items():
            caminho_csv = caminho_pasta / info["csv"]
            tabela = info["tabela_raw"]

            print(f"\nCarregando {info['csv']} → {tabela}")

            banco.executar(conexao, f"TRUNCATE TABLE {tabela}")

            with open(caminho_csv, encoding=CSV_ENCODING, errors="replace") as f:
                leitor = csv.DictReader(f, delimiter=CSV_SEPARADOR)

                colunas_csv = leitor.fieldnames
                placeholders = ", ".join(["%s"] * len(colunas_csv))

                cursor = conexao.cursor()
                cursor.execute(f"SHOW COLUMNS FROM {tabela}")
                colunas_tabela = [row[0] for row in cursor.fetchall()]
                cursor.close()

                colunas_sql = ", ".join(colunas_tabela)
                sql_insert = f"INSERT INTO {tabela} ({colunas_sql}) VALUES ({placeholders})"

                bloco = []

                for linha in leitor:
                    valores = tuple(linha.get(col, None) for col in colunas_csv)
                    bloco.append(valores)

                    if len(bloco) >= TAMANHO_BLOCO:
                        banco.inserir_em_lote(conexao, sql_insert, bloco)
                        print(f"  {TAMANHO_BLOCO} linhas inseridas...")
                        bloco = []

                if bloco:
                    banco.inserir_em_lote(conexao, sql_insert, bloco)

            print(f"  ✓ {tabela} carregada com sucesso.")

        conexao.commit()
        print("\nCarga Raw concluída com sucesso!")

    except Exception as e:
        conexao.rollback()
        print(f"Erro na carga: {e}")
        raise

    finally:
        conexao.close()

#-------------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== FASE 1 — EXTRAÇÃO E CARGA RAW ===\n")

    caminho_zip = fazer_download()
    caminho_pasta = descompactar(caminho_zip)
    carregar_raw(caminho_pasta)

    print("\n=== EXTRAÇÃO CONCLUÍDA ===")