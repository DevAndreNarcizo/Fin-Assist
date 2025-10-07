import customtkinter as ctk
import threading
import time

class LoadingDialog:
    def __init__(self, parent, message="Carregando..."):
        self.parent = parent
        self.message = message
        self.dialog = None
        self.is_running = False
        
    def show(self):
        """Mostra o diálogo de loading"""
        self.dialog = ctk.CTkToplevel(self.parent)
        self.dialog.title("Carregando")
        self.dialog.geometry("300x150")
        self.dialog.grab_set()
        
        # Centraliza na tela
        self.dialog.transient(self.parent)
        self.dialog.geometry("+%d+%d" % (
            self.parent.winfo_rootx() + 50,
            self.parent.winfo_rooty() + 50
        ))
        
        # Frame principal
        main_frame = ctk.CTkFrame(self.dialog, fg_color="#2b2b2b")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Label de mensagem
        self.message_label = ctk.CTkLabel(
            main_frame,
            text=self.message,
            font=("Roboto", 14),
            text_color="#ffffff"
        )
        self.message_label.pack(pady=20)
        
        # Barra de progresso animada
        self.progress_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.progress_frame.pack(pady=10)
        
        self.progress_bar = ctk.CTkProgressBar(
            self.progress_frame,
            width=200,
            height=20,
            progress_color="#4CAF50"
        )
        self.progress_bar.pack()
        self.progress_bar.set(0)
        
        # Inicia animação
        self.is_running = True
        self._animate_progress()
        
    def _animate_progress(self):
        """Anima a barra de progresso"""
        if not self.is_running:
            return
            
        # Simula progresso indeterminado
        current = self.progress_bar.get()
        if current >= 1.0:
            self.progress_bar.set(0)
        else:
            self.progress_bar.set(current + 0.1)
            
        self.dialog.after(100, self._animate_progress)
    
    def hide(self):
        """Esconde o diálogo de loading"""
        self.is_running = False
        if self.dialog:
            self.dialog.destroy()
            self.dialog = None

class ConfirmationDialog:
    @staticmethod
    def show(parent, title, message):
        """Mostra diálogo de confirmação"""
        from src.utils.message_utils import MessageUtils
        return MessageUtils.show_confirmation_dialog(title, message)

class LoadingManager:
    """Gerencia estados de loading para operações longas"""
    
    def __init__(self, parent):
        self.parent = parent
        self.loading_dialog = None
        
    def show_loading(self, message="Carregando..."):
        """Mostra loading"""
        self.loading_dialog = LoadingDialog(self.parent, message)
        self.loading_dialog.show()
        
    def hide_loading(self):
        """Esconde loading"""
        if self.loading_dialog:
            self.loading_dialog.hide()
            self.loading_dialog = None
    
    def execute_with_loading(self, func, *args, **kwargs):
        """Executa função com loading"""
        def run():
            try:
                result = func(*args, **kwargs)
                self.parent.after(0, self.hide_loading)
                return result
            except Exception as e:
                self.parent.after(0, self.hide_loading)
                raise e
        
        self.show_loading()
        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()
        return thread
