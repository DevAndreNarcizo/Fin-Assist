import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget
from PyQt6.QtCore import Qt
from src.analise_gastos import AnaliseGastos

class AssistenteFinanceiro(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Assistente Virtual Financeiro")
        self.setGeometry(100, 100, 1000, 700)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Título
        titulo = QLabel("Assistente Virtual Financeiro")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        layout.addWidget(titulo)
        
        # Container para os botões e conteúdo
        container = QHBoxLayout()
        
        # Botões de ação
        botoes_layout = QVBoxLayout()
        botoes_layout.setSpacing(10)
        botoes_layout.setContentsMargins(20, 0, 20, 0)
        
        self.criar_botoes(botoes_layout)
        container.addLayout(botoes_layout)
        
        # Área de conteúdo
        self.conteudo = QStackedWidget()
        self.conteudo.setStyleSheet("""
            QStackedWidget {
                background-color: #f0f0f0;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        container.addWidget(self.conteudo)
        
        layout.addLayout(container)
        
        # Inicializar páginas
        self.analise_gastos = AnaliseGastos()
        self.conteudo.addWidget(self.analise_gastos)
        
    def criar_botoes(self, layout):
        botoes = [
            ("Análise de Gastos", self.analisar_gastos),
            ("Planejamento Orçamentário", self.planejar_orcamento),
            ("Recomendações", self.ver_recomendacoes),
            ("Relatórios", self.ver_relatorios)
        ]
        
        for i, (texto, funcao) in enumerate(botoes):
            botao = QPushButton(texto)
            botao.setObjectName(f"botao_{i}")
            botao.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 15px;
                    border-radius: 5px;
                    font-size: 16px;
                    text-align: left;
                    min-width: 200px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QPushButton:checked {
                    background-color: #367c39;
                }
            """)
            botao.setCheckable(True)
            botao.clicked.connect(funcao)
            layout.addWidget(botao)
    
    def analisar_gastos(self):
        self.conteudo.setCurrentWidget(self.analise_gastos)
        self.atualizar_botoes(0)
    
    def planejar_orcamento(self):
        # TODO: Implementar planejamento orçamentário
        pass
    
    def ver_recomendacoes(self):
        # TODO: Implementar recomendações
        pass
    
    def ver_relatorios(self):
        # TODO: Implementar relatórios
        pass
    
    def atualizar_botoes(self, indice_ativo):
        for i in range(self.conteudo.count()):
            botao = self.findChild(QPushButton, f"botao_{i}")
            if botao:
                botao.setChecked(i == indice_ativo)

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Estilo moderno
    window = AssistenteFinanceiro()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 