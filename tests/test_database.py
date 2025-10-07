import unittest
import sys
import os
import tempfile
import sqlite3

# Adiciona o diretório raiz ao path para importar módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.database.database import init_db, get_db_connection

class TestDatabase(unittest.TestCase):
    
    def setUp(self):
        """Configuração antes de cada teste"""
        # Cria um banco temporário para testes
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        
        # Substitui temporariamente o caminho do banco
        import src.database.database as db_module
        self.original_db_path = db_module.DB_PATH
        db_module.DB_PATH = self.temp_db.name
        
        # Inicializa o banco de teste
        init_db()
    
    def tearDown(self):
        """Limpeza após cada teste"""
        # Restaura o caminho original do banco
        import src.database.database as db_module
        db_module.DB_PATH = self.original_db_path
        
        # Remove o arquivo temporário
        os.unlink(self.temp_db.name)
    
    def test_database_initialization(self):
        """Testa se o banco é inicializado corretamente"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verifica se as tabelas foram criadas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        expected_tables = ['users', 'transactions', 'financial_goals']
        for table in expected_tables:
            self.assertIn(table, tables)
        
        conn.close()
    
    def test_users_table_structure(self):
        """Testa a estrutura da tabela users"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        
        # Verifica se as colunas esperadas existem
        column_names = [col[1] for col in columns]
        expected_columns = ['id', 'username', 'password', 'email', 'created_at']
        
        for col in expected_columns:
            self.assertIn(col, column_names)
        
        conn.close()
    
    def test_transactions_table_structure(self):
        """Testa a estrutura da tabela transactions"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA table_info(transactions)")
        columns = cursor.fetchall()
        
        # Verifica se as colunas esperadas existem
        column_names = [col[1] for col in columns]
        expected_columns = ['id', 'user_id', 'type', 'category', 'subcategory', 'amount', 'description', 'date']
        
        for col in expected_columns:
            self.assertIn(col, column_names)
        
        conn.close()
    
    def test_financial_goals_table_structure(self):
        """Testa a estrutura da tabela financial_goals"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA table_info(financial_goals)")
        columns = cursor.fetchall()
        
        # Verifica se as colunas esperadas existem
        column_names = [col[1] for col in columns]
        expected_columns = ['id', 'user_id', 'title', 'target_amount', 'current_amount', 'deadline', 'status']
        
        for col in expected_columns:
            self.assertIn(col, column_names)
        
        conn.close()
    
    def test_foreign_keys_enabled(self):
        """Testa se as chaves estrangeiras estão habilitadas"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA foreign_keys")
        result = cursor.fetchone()
        
        self.assertEqual(result[0], 1)  # 1 = habilitado, 0 = desabilitado
        
        conn.close()
    
    def test_indexes_created(self):
        """Testa se os índices foram criados"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
        indexes = [row[0] for row in cursor.fetchall()]
        
        # Verifica se os índices esperados existem
        expected_indexes = [
            'idx_transactions_user_date',
            'idx_transactions_user_type',
            'idx_goals_user_status'
        ]
        
        for idx in expected_indexes:
            self.assertIn(idx, indexes)
        
        conn.close()

if __name__ == '__main__':
    unittest.main()
