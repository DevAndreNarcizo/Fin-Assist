import os
from pathlib import Path

# Caminhos do projeto
BASE_DIR = Path(__file__).parent.parent.parent
SRC_DIR = BASE_DIR / "src"
DATABASE_DIR = BASE_DIR / "database"
ASSETS_DIR = BASE_DIR / "assets"

# Configurações do banco de dados
DATABASE_PATH = DATABASE_DIR / "fin_assist.db"

# Configurações da aplicação
APP_NAME = "Fin-Assist"
APP_VERSION = "1.0.0"
APP_AUTHOR = "André"

# Configurações de UI
THEME_COLORS = {
    'primary': '#1a1a1a',
    'secondary': '#2b2b2b',
    'accent': '#4a9eff',
    'success': '#4CAF50',
    'error': '#ff4444',
    'warning': '#FBC02D',
    'info': '#2196F3',
    'text': '#ffffff',
    'text_secondary': '#bbb'
}

# Configurações de validação
MIN_PASSWORD_LENGTH = 8
MAX_USERNAME_LENGTH = 50
MAX_EMAIL_LENGTH = 100
MAX_TRANSACTION_DESCRIPTION_LENGTH = 200
MAX_GOAL_TITLE_LENGTH = 100

# Configurações de categorias padrão
DEFAULT_CATEGORIES = {
    'income': ['Salário', 'Freelance', 'Investimentos', 'Vendas', 'Outros'],
    'expense': ['Alimentação', 'Transporte', 'Moradia', 'Saúde', 'Educação', 'Lazer', 'Outros'],
    'investment': ['Ações', 'Fundos', 'Tesouro Direto', 'CDB', 'Outros']
}

# Configurações de relatórios
REPORT_SETTINGS = {
    'default_filename': 'relatorio_financeiro',
    'max_transactions_per_report': 1000,
    'date_format_display': '%d-%m-%Y',
    'date_format_storage': '%Y-%m-%d'
}

# Configurações de import/export
IMPORT_EXPORT_SETTINGS = {
    'max_file_size_mb': 10,
    'supported_formats': ['csv', 'json'],
    'encoding': 'utf-8'
}

# Configurações de logging
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': BASE_DIR / 'logs' / 'app.log'
}

# Configurações de API (se aplicável)
API_SETTINGS = {
    'timeout': 30,
    'max_retries': 3,
    'rate_limit': 100  # requests per minute
}

def ensure_directories():
    """Garante que todos os diretórios necessários existam"""
    directories = [
        DATABASE_DIR,
        ASSETS_DIR,
        BASE_DIR / 'logs',
        BASE_DIR / 'exports',
        BASE_DIR / 'backups'
    ]
    
    for directory in directories:
        directory.mkdir(exist_ok=True)

def get_database_path():
    """Retorna o caminho do banco de dados"""
    ensure_directories()
    return str(DATABASE_PATH)

def get_export_path():
    """Retorna o caminho para exportações"""
    ensure_directories()
    return str(BASE_DIR / 'exports')

def get_backup_path():
    """Retorna o caminho para backups"""
    ensure_directories()
    return str(BASE_DIR / 'backups')
