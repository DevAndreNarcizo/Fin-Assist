import unittest
import sys
import os
import tempfile
import sqlite3

# Adiciona o diretório raiz ao path para importar módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models.user import User
from src.database.database import init_db, get_db_connection

class TestUserModel(unittest.TestCase):
    
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
    
    def test_password_hashing(self):
        """Testa se a senha é hashada corretamente"""
        password = "test123"
        hashed = User.hash_password(password)
        
        # Verifica se o hash é diferente da senha original
        self.assertNotEqual(password, hashed.decode('utf-8'))
        
        # Verifica se o hash tem o tamanho esperado (bcrypt)
        self.assertEqual(len(hashed), 60)  # bcrypt hash tem 60 caracteres
    
    def test_password_verification(self):
        """Testa se a verificação de senha funciona"""
        password = "test123"
        hashed = User.hash_password(password)
        
        # Verifica se a senha correta é aceita
        self.assertTrue(User.verify_password(password, hashed))
        
        # Verifica se a senha incorreta é rejeitada
        self.assertFalse(User.verify_password("wrong_password", hashed))
    
    def test_user_creation(self):
        """Testa a criação de um usuário"""
        user = User(
            username="testuser",
            password="password123",
            email="test@example.com"
        )
        
        # Verifica se o usuário foi criado com os dados corretos
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertIsNotNone(user.password)  # Senha deve ser hashada
        self.assertIsNone(user.id)  # ID deve ser None antes de salvar
    
    def test_user_save(self):
        """Testa o salvamento de um usuário no banco"""
        user = User(
            username="testuser",
            password="password123",
            email="test@example.com"
        )
        
        # Salva o usuário
        result = user.save()
        
        # Verifica se foi salvo com sucesso
        self.assertTrue(result)
        self.assertIsNotNone(user.id)  # ID deve ser definido após salvar
        
        # Verifica se o usuário existe no banco
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user.id,))
        db_user = cursor.fetchone()
        
        self.assertIsNotNone(db_user)
        self.assertEqual(db_user[1], "testuser")  # username
        self.assertEqual(db_user[3], "test@example.com")  # email
        
        conn.close()
    
    def test_user_authenticate_success(self):
        """Testa autenticação bem-sucedida"""
        # Cria um usuário
        user = User(
            username="testuser",
            password="password123",
            email="test@example.com"
        )
        user.save()
        
        # Tenta autenticar
        authenticated_user = User.authenticate("testuser", "password123")
        
        self.assertIsNotNone(authenticated_user)
        self.assertEqual(authenticated_user.username, "testuser")
        self.assertEqual(authenticated_user.email, "test@example.com")
    
    def test_user_authenticate_failure(self):
        """Testa falha na autenticação"""
        # Cria um usuário
        user = User(
            username="testuser",
            password="password123",
            email="test@example.com"
        )
        user.save()
        
        # Tenta autenticar com credenciais incorretas
        authenticated_user = User.authenticate("testuser", "wrong_password")
        self.assertIsNone(authenticated_user)
        
        authenticated_user = User.authenticate("wrong_user", "password123")
        self.assertIsNone(authenticated_user)
    
    def test_duplicate_username(self):
        """Testa tentativa de criar usuário com username duplicado"""
        # Cria primeiro usuário
        user1 = User(
            username="testuser",
            password="password123",
            email="test1@example.com"
        )
        result1 = user1.save()
        self.assertTrue(result1)
        
        # Tenta criar segundo usuário com mesmo username
        user2 = User(
            username="testuser",
            password="password456",
            email="test2@example.com"
        )
        result2 = user2.save()
        self.assertFalse(result2)  # Deve falhar
    
    def test_duplicate_email(self):
        """Testa tentativa de criar usuário com email duplicado"""
        # Cria primeiro usuário
        user1 = User(
            username="testuser1",
            password="password123",
            email="test@example.com"
        )
        result1 = user1.save()
        self.assertTrue(result1)
        
        # Tenta criar segundo usuário com mesmo email
        user2 = User(
            username="testuser2",
            password="password456",
            email="test@example.com"
        )
        result2 = user2.save()
        self.assertFalse(result2)  # Deve falhar

if __name__ == '__main__':
    unittest.main()
