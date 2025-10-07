import customtkinter as ctk
from tkinter import messagebox
import re

class MessageUtils:
    @staticmethod
    def show_error(parent, message, duration=3000):
        """Mostra mensagem de erro temporária"""
        error_label = ctk.CTkLabel(
            parent,
            text=message,
            text_color="#ff4444",
            font=("Roboto", 12)
        )
        error_label.pack(pady=10)
        parent.after(duration, error_label.destroy)
    
    @staticmethod
    def show_success(parent, message, duration=3000):
        """Mostra mensagem de sucesso temporária"""
        success_label = ctk.CTkLabel(
            parent,
            text=message,
            text_color="#4CAF50",
            font=("Roboto", 12)
        )
        success_label.pack(pady=10)
        parent.after(duration, success_label.destroy)
    
    @staticmethod
    def show_info(parent, message, duration=3000):
        """Mostra mensagem informativa temporária"""
        info_label = ctk.CTkLabel(
            parent,
            text=message,
            text_color="#2196F3",
            font=("Roboto", 12)
        )
        info_label.pack(pady=10)
        parent.after(duration, info_label.destroy)
    
    @staticmethod
    def show_error_dialog(title, message):
        """Mostra diálogo de erro modal"""
        messagebox.showerror(title, message)
    
    @staticmethod
    def show_success_dialog(title, message):
        """Mostra diálogo de sucesso modal"""
        messagebox.showinfo(title, message)
    
    @staticmethod
    def show_confirmation_dialog(title, message):
        """Mostra diálogo de confirmação"""
        return messagebox.askyesno(title, message)

class ValidationUtils:
    @staticmethod
    def validate_email(email):
        """Valida formato de email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_password(password):
        """Valida força da senha"""
        if len(password) < 8:
            return False, "A senha deve ter pelo menos 8 caracteres"
        
        if not re.search(r'[A-Z]', password):
            return False, "A senha deve conter pelo menos uma letra maiúscula"
        
        if not re.search(r'[a-z]', password):
            return False, "A senha deve conter pelo menos uma letra minúscula"
        
        if not re.search(r'\d', password):
            return False, "A senha deve conter pelo menos um número"
        
        return True, "Senha válida"
    
    @staticmethod
    def validate_date_format(date_str, format_str='%d-%m-%Y'):
        """Valida formato de data"""
        try:
            from datetime import datetime
            datetime.strptime(date_str, format_str)
            return True, "Data válida"
        except ValueError:
            return False, f"Formato de data inválido. Use {format_str.replace('%', '')}"
    
    @staticmethod
    def validate_positive_number(value):
        """Valida se é um número positivo"""
        try:
            num = float(value)
            if num <= 0:
                return False, "O valor deve ser maior que zero"
            return True, "Valor válido"
        except ValueError:
            return False, "Digite um número válido"
