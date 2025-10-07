import customtkinter as ctk
from src.views.login_view import LoginView
from src.database.database import init_db
import os
from dotenv import load_dotenv

def main():
    # Carrega variáveis de ambiente
    load_dotenv()
    
    # Configuração do tema
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # Inicializa o banco de dados
    init_db()
    
    # Cria a janela principal
    root = ctk.CTk()
    root.title("Fin-Assist")
    root.geometry("1200x800")
                
    # Inicia com a tela de login
    login_view = LoginView(root)
    login_view.pack(fill="both", expand=True)
    
    root.mainloop()

if __name__ == "__main__":
    main() 