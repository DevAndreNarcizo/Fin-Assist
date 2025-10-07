import customtkinter as ctk
from src.models.user import User
from src.views.main_view import MainView
from src.views.register_view import RegisterView

class LoginView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.setup_ui()
    
    def setup_ui(self):
        # Configuração do frame principal
        self.configure(fg_color="#1a1a1a")
        
        # Frame de login
        login_frame = ctk.CTkFrame(self, fg_color="#2b2b2b", corner_radius=15)
        login_frame.pack(pady=50, padx=50, fill="both", expand=True)
        
        # Título
        title_label = ctk.CTkLabel(
            login_frame,
            text="Fin-Assist",
            font=("Roboto", 32, "bold"),
            text_color="#ffffff"
        )
        title_label.pack(pady=30)
        
        # Frame para campos de entrada
        input_frame = ctk.CTkFrame(login_frame, fg_color="transparent")
        input_frame.pack(pady=20, padx=40, fill="both")
        
        # Campo de usuário
        self.username_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Usuário",
            width=300,
            height=40,
            font=("Roboto", 14)
        )
        self.username_entry.pack(pady=10)
        
        # Campo de senha
        self.password_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Senha",
            width=300,
            height=40,
            font=("Roboto", 14),
            show="*"
        )
        self.password_entry.pack(pady=10)
        
        # Botão de login
        login_button = ctk.CTkButton(
            input_frame,
            text="Entrar",
            width=300,
            height=40,
            font=("Roboto", 14, "bold"),
            command=self.login
        )
        login_button.pack(pady=20)
        
        # Link para cadastro
        register_label = ctk.CTkLabel(
            input_frame,
            text="Não tem uma conta? Cadastre-se",
            font=("Roboto", 12),
            text_color="#4a9eff",
            cursor="hand2"
        )
        register_label.pack(pady=10)
        register_label.bind("<Button-1>", lambda e: self.show_register())
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            self.show_error("Por favor, preencha todos os campos")
            return
        
        user = User.authenticate(username, password)
        if user:
            self.show_main_view(user)
        else:
            self.show_error("Usuário ou senha inválidos")
    
    def show_register(self):
        self.destroy()
        RegisterView(self.master).pack(fill="both", expand=True)
    
    def show_main_view(self, user):
        self.destroy()
        MainView(self.master, user).pack(fill="both", expand=True)
    
    def show_error(self, message):
        from src.utils.message_utils import MessageUtils
        MessageUtils.show_error(self, message) 