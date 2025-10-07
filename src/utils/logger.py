import logging
import os
from pathlib import Path
from src.config.settings import LOGGING_CONFIG, BASE_DIR

class Logger:
    """Classe para gerenciar logs da aplicação"""
    
    _loggers = {}
    
    @classmethod
    def get_logger(cls, name):
        """Retorna um logger configurado"""
        if name not in cls._loggers:
            cls._loggers[name] = cls._setup_logger(name)
        return cls._loggers[name]
    
    @classmethod
    def _setup_logger(cls, name):
        """Configura um logger"""
        logger = logging.getLogger(name)
        
        # Evita duplicar handlers
        if logger.handlers:
            return logger
        
        logger.setLevel(getattr(logging, LOGGING_CONFIG['level']))
        
        # Formatter
        formatter = logging.Formatter(LOGGING_CONFIG['format'])
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File handler
        log_file = Path(LOGGING_CONFIG['file'])
        log_file.parent.mkdir(exist_ok=True)
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        return logger

def log_function_call(func):
    """Decorator para logar chamadas de função"""
    def wrapper(*args, **kwargs):
        logger = Logger.get_logger(func.__module__)
        logger.info(f"Chamando {func.__name__} com args={args}, kwargs={kwargs}")
        
        try:
            result = func(*args, **kwargs)
            logger.info(f"{func.__name__} executada com sucesso")
            return result
        except Exception as e:
            logger.error(f"Erro em {func.__name__}: {str(e)}")
            raise
    
    return wrapper

def log_database_operation(operation):
    """Decorator para logar operações de banco de dados"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger = Logger.get_logger('database')
            logger.info(f"Iniciando {operation}")
            
            try:
                result = func(*args, **kwargs)
                logger.info(f"{operation} concluída com sucesso")
                return result
            except Exception as e:
                logger.error(f"Erro em {operation}: {str(e)}")
                raise
        
        return wrapper
    return decorator

# Loggers específicos para diferentes módulos
def get_database_logger():
    return Logger.get_logger('database')

def get_controller_logger():
    return Logger.get_logger('controller')

def get_view_logger():
    return Logger.get_logger('view')

def get_utils_logger():
    return Logger.get_logger('utils')
