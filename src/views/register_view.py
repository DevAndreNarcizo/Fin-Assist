import customtkinter as ctk
from src.models.user import User

class RegisterView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.setup_ui()
    
    def setup_ui(self):
        # Configuração do frame principal
        self.configure(fg_color="#1a1a1a")
        
        # Frame de cadastro
        register_frame = ctk.CTkFrame(self, fg_color="#2b2b2b", corner_radius=15)
        register_frame.pack(pady=50, padx=50, fill="both", expand=True)
        
        # Título
        title_label = ctk.CTkLabel(
            register_frame,
            text="Criar Conta",
            font=("Roboto", 32, "bold"),
            text_color="#ffffff"
        )
        title_label.pack(pady=30)
        
        # Frame para campos de entrada
        input_frame = ctk.CTkFrame(register_frame, fg_color="transparent")
        input_frame.pack(pady=20, padx=40, fill="both")
        
        # Campo de nome de usuário
        self.username_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Nome de usuário",
            width=300,
            height=40,
            font=("Roboto", 14)
        )
        self.username_entry.pack(pady=10)
        
        # Campo de email
        self.email_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Email",
            width=300,
            height=40,
            font=("Roboto", 14)
        )
        self.email_entry.pack(pady=10)
        
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
        
        # Campo de confirmação de senha
        self.confirm_password_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Confirmar senha",
            width=300,
            height=40,
            font=("Roboto", 14),
            show="*"
        )
        self.confirm_password_entry.pack(pady=10)
        
        # Botão de cadastro
        register_button = ctk.CTkButton(
            input_frame,
            text="Cadastrar",
            width=300,
            height=40,
            font=("Roboto", 14, "bold"),
            command=self.register
        )
        register_button.pack(pady=20)
        
        # Link para voltar ao login
        back_label = ctk.CTkLabel(
            input_frame,
            text="Voltar para o login",
            font=("Roboto", 12),
            text_color="#4a9eff",
            cursor="hand2"
        )
        back_label.pack(pady=10)
        back_label.bind("<Button-1>", lambda e: self.show_login())
    
    def register(self):
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        # Validação dos campos usando ValidationUtils
        from src.utils.message_utils import ValidationUtils
        
        if not all([username, email, password, confirm_password]):
            self.show_error("Por favor, preencha todos os campos")
            return
        
        if password != confirm_password:
            self.show_error("As senhas não coincidem")
            return
        
        # Validação de email
        if not ValidationUtils.validate_email(email):
            self.show_error("Formato de email inválido")
            return
        
        # Validação de senha
        is_valid, message = ValidationUtils.validate_password(password)
        if not is_valid:
            self.show_error(message)
            return
        
        # Cria o usuário
        user = User(
            username=username,
            password=User.hash_password(password).decode('utf-8'),
            email=email
        )
        
        # Tenta salvar o usuário
        if user.save():
            self.show_success("Cadastro realizado com sucesso!")
            self.after(2000, self.show_login)
        else:
            self.show_error("Nome de usuário ou email já cadastrado")
    
    def show_login(self):
        self.destroy()
        from src.views.login_view import LoginView
        LoginView(self.master).pack(fill="both", expand=True)
    
    def show_error(self, message):
        from src.utils.message_utils import MessageUtils
        MessageUtils.show_error(self, message)
    
    def show_success(self, message):
        from src.utils.message_utils import MessageUtils
        MessageUtils.show_success(self, message) 