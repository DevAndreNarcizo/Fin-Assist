import sqlite3
import os
from pathlib import Path

DB_PATH = Path(__file__).parent.parent.parent / "database" / "fin_assist.db"

def init_db():
    """Inicializa o banco de dados e cria as tabelas necessárias"""
    # Cria o diretório do banco de dados se não existir
    os.makedirs(DB_PATH.parent, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Garante chaves estrangeiras ativas
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # Tabela de usuários
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Tabela de transações
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        type TEXT NOT NULL,  -- 'income', 'expense', 'investment'
        category TEXT NOT NULL,
        subcategory TEXT,
        amount REAL NOT NULL,
        description TEXT,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')

    # Migração leve: adiciona coluna subcategory se a tabela existir sem ela
    try:
        cursor.execute("PRAGMA table_info(transactions);")
        cols = [row[1] for row in cursor.fetchall()]
        if 'subcategory' not in cols:
            cursor.execute("ALTER TABLE transactions ADD COLUMN subcategory TEXT;")
    except Exception:
        # Evita quebrar inicialização caso PRAGMA falhe em algum ambiente
        pass

    # Índices para performance nas consultas mais comuns
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_transactions_user_date ON transactions(user_id, date);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_transactions_user_type ON transactions(user_id, type);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_goals_user_status ON financial_goals(user_id, status);")
    
    # Tabela de metas financeiras
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS financial_goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        target_amount REAL NOT NULL,
        current_amount REAL DEFAULT 0,
        deadline DATE,
        status TEXT DEFAULT 'active',
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    """Retorna uma conexão com o banco de dados com chaves estrangeiras ativas"""
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("PRAGMA foreign_keys = ON;")
    except Exception:
        pass
    return conn