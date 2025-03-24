from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QTableWidget, QTableWidgetItem, QLineEdit,
                             QComboBox, QMessageBox)
from PyQt6.QtCore import Qt
import pandas as pd
from datetime import datetime
import os

class AnaliseGastos(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.dados = pd.DataFrame(columns=['Data', 'Categoria', 'Descrição', 'Valor'])
        self.carregar_dados()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Título
        titulo = QLabel("Análise de Gastos")
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px;")
        layout.addWidget(titulo)
        
        # Formulário de entrada
        form_layout = QHBoxLayout()
        
        # Data
        self.data_input = QLineEdit()
        self.data_input.setPlaceholderText("Data (DD/MM/AAAA)")
        form_layout.addWidget(self.data_input)
        
        # Categoria
        self.categoria_input = QComboBox()
        self.categoria_input.addItems([
            "Alimentação", "Transporte", "Moradia", "Saúde",
            "Educação", "Lazer", "Outros"
        ])
        form_layout.addWidget(self.categoria_input)
        
        # Descrição
        self.descricao_input = QLineEdit()
        self.descricao_input.setPlaceholderText("Descrição")
        form_layout.addWidget(self.descricao_input)
        
        # Valor
        self.valor_input = QLineEdit()
        self.valor_input.setPlaceholderText("Valor")
        form_layout.addWidget(self.valor_input)
        
        # Botão de adicionar
        btn_adicionar = QPushButton("Adicionar Gasto")
        btn_adicionar.clicked.connect(self.adicionar_gasto)
        form_layout.addWidget(btn_adicionar)
        
        layout.addLayout(form_layout)
        
        # Tabela de gastos
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(4)
        self.tabela.setHorizontalHeaderLabels(["Data", "Categoria", "Descrição", "Valor"])
        self.tabela.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.tabela)
        
        # Botões de ação
        botoes_layout = QHBoxLayout()
        
        btn_remover = QPushButton("Remover Selecionado")
        btn_remover.clicked.connect(self.remover_gasto)
        botoes_layout.addWidget(btn_remover)
        
        btn_limpar = QPushButton("Limpar Todos")
        btn_limpar.clicked.connect(self.limpar_gastos)
        botoes_layout.addWidget(btn_limpar)
        
        layout.addLayout(botoes_layout)
        
        # Resumo
        self.resumo_label = QLabel()
        layout.addWidget(self.resumo_label)
        
        self.setLayout(layout)
        self.atualizar_tabela()
        
    def adicionar_gasto(self):
        try:
            data = datetime.strptime(self.data_input.text(), "%d/%m/%Y")
            categoria = self.categoria_input.currentText()
            descricao = self.descricao_input.text()
            valor = float(self.valor_input.text().replace(",", "."))
            
            novo_gasto = pd.DataFrame({
                'Data': [data],
                'Categoria': [categoria],
                'Descrição': [descricao],
                'Valor': [valor]
            })
            
            self.dados = pd.concat([self.dados, novo_gasto], ignore_index=True)
            self.salvar_dados()
            self.atualizar_tabela()
            
            # Limpar campos
            self.data_input.clear()
            self.descricao_input.clear()
            self.valor_input.clear()
            
            QMessageBox.information(self, "Sucesso", "Gasto adicionado com sucesso!")
            
        except ValueError as e:
            QMessageBox.warning(self, "Erro", "Por favor, verifique os dados inseridos.")
            
    def remover_gasto(self):
        linha_selecionada = self.tabela.currentRow()
        if linha_selecionada >= 0:
            self.dados = self.dados.drop(linha_selecionada)
            self.salvar_dados()
            self.atualizar_tabela()
            
    def limpar_gastos(self):
        reply = QMessageBox.question(self, "Confirmar", 
                                   "Tem certeza que deseja remover todos os gastos?",
                                   QMessageBox.StandardButton.Yes | 
                                   QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            self.dados = pd.DataFrame(columns=['Data', 'Categoria', 'Descrição', 'Valor'])
            self.salvar_dados()
            self.atualizar_tabela()
            
    def atualizar_tabela(self):
        self.tabela.setRowCount(len(self.dados))
        
        for i, row in self.dados.iterrows():
            self.tabela.setItem(i, 0, QTableWidgetItem(row['Data'].strftime("%d/%m/%Y")))
            self.tabela.setItem(i, 1, QTableWidgetItem(row['Categoria']))
            self.tabela.setItem(i, 2, QTableWidgetItem(row['Descrição']))
            self.tabela.setItem(i, 3, QTableWidgetItem(f"R$ {row['Valor']:.2f}"))
            
        self.atualizar_resumo()
        
    def atualizar_resumo(self):
        if len(self.dados) > 0:
            total = self.dados['Valor'].sum()
            media = self.dados['Valor'].mean()
            max_gasto = self.dados['Valor'].max()
            categoria_mais_cara = self.dados.groupby('Categoria')['Valor'].sum().idxmax()
            
            resumo = f"""
            Resumo dos Gastos:
            Total: R$ {total:.2f}
            Média por Gasto: R$ {media:.2f}
            Maior Gasto: R$ {max_gasto:.2f}
            Categoria com Mais Gastos: {categoria_mais_cara}
            """
            self.resumo_label.setText(resumo)
        else:
            self.resumo_label.setText("Nenhum gasto registrado.")
            
    def carregar_dados(self):
        arquivo = "data/gastos.csv"
        if os.path.exists(arquivo):
            self.dados = pd.read_csv(arquivo)
            self.dados['Data'] = pd.to_datetime(self.dados['Data'])
            
    def salvar_dados(self):
        os.makedirs("data", exist_ok=True)
        self.dados.to_csv("data/gastos.csv", index=False) 