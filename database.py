import sqlite3 as sq3
import pandas as pd


# =========================================================
# CONFIGURAÇÃO DO BANCO DE DADOS
# =========================================================

db_name = "vendas.db"


# =========================================================
# CONEXÃO COM O BANCO
# =========================================================

def conectar():
    """
    Cria e retorna uma conexão com o banco SQLite.
    """

    conexao = sq3.connect(db_name)

    return conexao


# =========================================================
# CRIAÇÃO DA TABELA
# =========================================================

def criar_tabela():
    """
    Cria a tabela vendas caso ela ainda não exista.
    """

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            semana INTEGER,
            data_entrega TEXT NOT NULL,
            comprador TEXT NOT NULL,
            valor REAL NOT NULL,
            status_pagamento TEXT NOT NULL,
            sabor TEXT,
            pagador TEXT
        )
    """)

    conexao.commit()
    conexao.close()


# =========================================================
# CREATE - INSERIR VENDA
# =========================================================

def inserir_venda(
    semana,
    data_entrega,
    comprador,
    valor,
    status_pagamento,
    sabor,
    pagador
):
    """
    Insere uma nova venda no banco de dados.
    """

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO vendas (
            semana,
            data_entrega,
            comprador,
            valor,
            status_pagamento,
            sabor,
            pagador
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        semana,
        data_entrega,
        comprador,
        valor,
        status_pagamento,
        sabor,
        pagador
    ))

    conexao.commit()
    conexao.close()


# =========================================================
# READ - LISTAR VENDAS
# =========================================================

def listar_vendas():
    """
    Retorna todas as vendas cadastradas em um DataFrame.
    """

    conexao = conectar()

    df = pd.read_sql_query("""
        SELECT *
        FROM vendas
        ORDER BY id DESC
    """, conexao)

    conexao.close()

    return df


# =========================================================
# UPDATE - ALTERAR VENDA
# =========================================================

def alterar_venda(
    id_venda,
    semana,
    data_entrega,
    comprador,
    valor,
    status_pagamento,
    sabor,
    pagador
):
    """
    Altera os dados de uma venda existente.
    """

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE vendas
        SET
            semana = ?,
            data_entrega = ?,
            comprador = ?,
            valor = ?,
            status_pagamento = ?,
            sabor = ?,
            pagador = ?
        WHERE id = ?
    """, (
        semana,
        data_entrega,
        comprador,
        valor,
        status_pagamento,
        sabor,
        pagador,
        id_venda
    ))

    conexao.commit()
    conexao.close()


# =========================================================
# DELETE - EXCLUIR VENDA
# =========================================================

def excluir_venda(id_venda):
    """
    Exclui uma venda através do seu ID.
    """

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        DELETE FROM vendas
        WHERE id = ?
        """,
        (id_venda,)
    )

    conexao.commit()
    conexao.close()


# =========================================================
# FUNÇÃO DE MANUTENÇÃO - APAGAR TABELA
# =========================================================

def apagar_tabela_vendas():
    """
    Apaga completamente a tabela vendas.

    ATENÇÃO:
    Todos os registros serão excluídos.
    """

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        DROP TABLE IF EXISTS vendas
    """)

    conexao.commit()
    conexao.close()

    print("Tabela 'vendas' apagada com sucesso.")