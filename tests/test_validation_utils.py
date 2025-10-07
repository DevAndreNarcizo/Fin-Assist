import unittest
import sys
import os

# Adiciona o diretório raiz ao path para importar módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.utils.message_utils import ValidationUtils

class TestValidationUtils(unittest.TestCase):
    
    def test_validate_email_valid(self):
        """Testa validação de emails válidos"""
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "test123@test.org",
            "a@b.c"
        ]
        
        for email in valid_emails:
            with self.subTest(email=email):
                self.assertTrue(ValidationUtils.validate_email(email))
    
    def test_validate_email_invalid(self):
        """Testa validação de emails inválidos"""
        invalid_emails = [
            "invalid-email",
            "@domain.com",
            "user@",
            "user@domain",
            "user.domain.com",
            ""
        ]
        
        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertFalse(ValidationUtils.validate_email(email))
    
    def test_validate_password_valid(self):
        """Testa validação de senhas válidas"""
        valid_passwords = [
            "Password123",
            "MySecure1",
            "Test1234",
            "StrongPass1"
        ]
        
        for password in valid_passwords:
            with self.subTest(password=password):
                is_valid, message = ValidationUtils.validate_password(password)
                self.assertTrue(is_valid)
                self.assertEqual(message, "Senha válida")
    
    def test_validate_password_invalid(self):
        """Testa validação de senhas inválidas"""
        test_cases = [
            ("short", "A senha deve ter pelo menos 8 caracteres"),
            ("nouppercase123", "A senha deve conter pelo menos uma letra maiúscula"),
            ("NOLOWERCASE123", "A senha deve conter pelo menos uma letra minúscula"),
            ("NoNumbers", "A senha deve conter pelo menos um número")
        ]
        
        for password, expected_message in test_cases:
            with self.subTest(password=password):
                is_valid, message = ValidationUtils.validate_password(password)
                self.assertFalse(is_valid)
                self.assertEqual(message, expected_message)
    
    def test_validate_date_format_valid(self):
        """Testa validação de datas válidas"""
        valid_dates = [
            "01-01-2024",
            "31-12-2023",
            "15-06-2025"
        ]
        
        for date_str in valid_dates:
            with self.subTest(date=date_str):
                is_valid, message = ValidationUtils.validate_date_format(date_str)
                self.assertTrue(is_valid)
                self.assertEqual(message, "Data válida")
    
    def test_validate_date_format_invalid(self):
        """Testa validação de datas inválidas"""
        invalid_dates = [
            "2024-01-01",  # Formato errado
            "32-01-2024",  # Dia inválido
            "01-13-2024",  # Mês inválido
            "01/01/2024",  # Separador errado
            "invalid-date"
        ]
        
        for date_str in invalid_dates:
            with self.subTest(date=date_str):
                is_valid, message = ValidationUtils.validate_date_format(date_str)
                self.assertFalse(is_valid)
                self.assertIn("Formato de data inválido", message)
    
    def test_validate_positive_number_valid(self):
        """Testa validação de números positivos válidos"""
        valid_numbers = [
            "1",
            "100.50",
            "0.01",
            "999.99"
        ]
        
        for number_str in valid_numbers:
            with self.subTest(number=number_str):
                is_valid, message = ValidationUtils.validate_positive_number(number_str)
                self.assertTrue(is_valid)
                self.assertEqual(message, "Valor válido")
    
    def test_validate_positive_number_invalid(self):
        """Testa validação de números inválidos"""
        test_cases = [
            ("0", "O valor deve ser maior que zero"),
            ("-1", "O valor deve ser maior que zero"),
            ("abc", "Digite um número válido"),
            ("", "Digite um número válido")
        ]
        
        for number_str, expected_message in test_cases:
            with self.subTest(number=number_str):
                is_valid, message = ValidationUtils.validate_positive_number(number_str)
                self.assertFalse(is_valid)
                self.assertEqual(message, expected_message)

if __name__ == '__main__':
    unittest.main()
