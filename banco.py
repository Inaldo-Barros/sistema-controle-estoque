import sqlite3

NOME_BANCO = "estoque.db"

def conectar():
    """
    Cria conexão com o banco SQLite
    """
    return sqlite3.connect(NOME_BANCO)

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    # TABELA PRODUTOS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            estoque_minimo INTEGER NOT NULL,
            preco_venda REAL NOT NULL DEFAULT 0
        )
    """)

    # TABELA MOVIMENTAÇÕES
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(produto_id) REFERENCES produtos(id)
        )
    """)

    conn.commit()
    conn.close()

# OPERAÇÕES DE PRODUTOS

def inserir_produto(nome, quantidade, estoque_minimo, preco_venda):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO produtos (nome, quantidade, estoque_minimo, preco_venda)
        VALUES (?, ?, ?, ?)
    """, (nome, quantidade, estoque_minimo, preco_venda))
    conn.commit()
    conn.close()

def listar_produtos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nome, quantidade, estoque_minimo, preco_venda
        FROM produtos
        ORDER BY nome
    """)
    produtos = cursor.fetchall()
    conn.close()
    return produtos

def buscar_produto_por_id(produto_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nome, quantidade, estoque_minimo, preco_venda
        FROM produtos
        WHERE id = ?
    """, (produto_id,))
    produto = cursor.fetchone()
    conn.close()
    return produto

def atualizar_estoque(produto_id, nova_quantidade):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE produtos
        SET quantidade = ?
        WHERE id = ?
    """, (nova_quantidade, produto_id))
    conn.commit()
    conn.close()

def excluir_produto(produto_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM produtos
        WHERE id = ?
    """, (produto_id,))
    conn.commit()
    conn.close()

def buscar_produtos_por_nome(nome):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nome, quantidade, estoque_minimo, preco_venda
        FROM produtos
        WHERE nome LIKE ?
        ORDER BY nome
    """, (f"%{nome}%",))
    produtos = cursor.fetchall()
    conn.close()
    return produtos

def atualizar_produto(produto_id, nome, quantidade, estoque_minimo, preco_venda):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE produtos
        SET nome = ?, quantidade = ?, estoque_minimo = ?, preco_venda = ?
        WHERE id = ?
    """, (nome, quantidade, estoque_minimo, preco_venda, produto_id))
    conn.commit()
    conn.close()

# OPERAÇÕES DE MOVIMENTAÇÕES

def registrar_movimentacao(produto_id, tipo, quantidade):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO movimentacoes (produto_id, tipo, quantidade)
        VALUES (?, ?, ?)
    """, (produto_id, tipo, quantidade))
    conn.commit()
    conn.close()

def listar_movimentacoes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, produto_id, tipo, quantidade, data
        FROM movimentacoes
        ORDER BY data DESC
    """)
    movimentacoes = cursor.fetchall()
    conn.close()
    return movimentacoes

def entrada_estoque(produto_id, quantidade):
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT quantidade FROM produtos WHERE id = ?
    """, (produto_id,))
    produto = cursor.fetchone()

    if produto is None:
        conn.close()
        return False

    estoque_atual = produto[0]
    novo_estoque = estoque_atual + quantidade

    cursor.execute("""
        UPDATE produtos SET quantidade = ? WHERE id = ?
    """, (novo_estoque, produto_id))

    cursor.execute("""
        INSERT INTO movimentacoes (produto_id, tipo, quantidade)
        VALUES (?, 'ENTRADA', ?)
    """, (produto_id, quantidade))

    conn.commit()
    conn.close()
    return True

def listar_movimentacoes_completas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.id, p.nome, m.tipo, m.quantidade, m.data
        FROM movimentacoes m
        INNER JOIN produtos p ON p.id = m.produto_id
        ORDER BY m.data DESC
    """)
    movimentacoes = cursor.fetchall()
    conn.close()
    return movimentacoes

def ultima_movimentacao():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.nome, m.tipo, m.quantidade, m.data
        FROM movimentacoes m
        INNER JOIN produtos p ON p.id = m.produto_id
        ORDER BY m.id DESC
        LIMIT 1
    """)
    resultado = cursor.fetchone()
    conn.close()
    return resultado

# MÉTRICAS DO DASHBOARD

def total_produtos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM produtos")
    total = cursor.fetchone()[0]
    conn.close()
    return total

def produtos_estoque_baixo():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM produtos WHERE quantidade <= estoque_minimo")
    total = cursor.fetchone()[0]
    conn.close()
    return total

def quantidade_total_estoque():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(quantidade) FROM produtos")
    resultado = cursor.fetchone()[0]
    conn.close()
    return resultado if resultado else 0

def obter_quantidade_produto(produto_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT quantidade FROM produtos WHERE id = ?
    """, (produto_id,))
    resultado = cursor.fetchone()
    conn.close()
    
    if resultado:
        return resultado[0]
    return None

if __name__ == "__main__":
    criar_tabelas()
    print("Banco criado com sucesso!")