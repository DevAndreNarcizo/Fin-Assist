import bcrypt
import sqlite3
from src.database.database import get_db_connection

class User:
    def __init__(self, username=None, password=None, email=None):
        self.username = username
        self.password = password
        self.email = email
        self.id = None
    
    @staticmethod
    def hash_password(password):
        """Criptografa a senha usando bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)
    
    def verify_password(self, password):
        """Verifica se a senha fornecida corresponde à senha armazenada"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
    def save(self):
        """Salva o usuário no banco de dados"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                (self.username, self.password, self.email)
            )
            self.id = cursor.lastrowid
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    @staticmethod
    def get_by_username(username):
        """Retorna um usuário pelo nome de usuário"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data:
            user = User()
            user.id = user_data[0]
            user.username = user_data[1]
            user.password = user_data[2]
            user.email = user_data[3]
            return user
        return None
    
    @staticmethod
    def authenticate(username, password):
        """Autentica um usuário"""
        user = User.get_by_username(username)
        if user and user.verify_password(password):
            return user
        return None 