import sys
import os
from datetime import datetime, date
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QPushButton, QLineEdit,
                             QTextEdit, QDialog, QMessageBox, QComboBox,
                             QCalendarWidget, QScrollArea, QFrame, QGridLayout,
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QStackedWidget, QListWidget, QListWidgetItem,
                             QFileDialog, QGroupBox, QCheckBox, QAction, QSpinBox,
                             QMenu)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QIcon, QColor, QPalette, QLinearGradient
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from src.chatbot import ChatBot
from src.database import DatabaseManager
import csv
import json

# Configuração do matplotlib para usar o backend Qt5Agg
matplotlib.use('Qt5Agg')

# Estilo global do aplicativo
GLOBAL_STYLE = """
    QMainWindow, QDialog {
        background-color: #f0f8ff;
    }
    QLabel {
        color: #1a1a1a;
        font-size: 14px;
    }
    QLineEdit, QComboBox, QTextEdit {
        padding: 10px;
        border: 2px solid #00bcd4;
        border-radius: 8px;
        background-color: white;
        color: #1a1a1a;
        font-size: 14px;
    }
    QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
        border: 2px solid #00838f;
    }
    QPushButton {
        padding: 12px 24px;
        background-color: #00bcd4;
        color: white;
        border: none;
        border-radius: 8px;
        font-size: 14px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #00838f;
    }
    QPushButton:pressed {
        background-color: #006064;
    }
    QTableWidget {
        border: 2px solid #00bcd4;
        border-radius: 8px;
        background-color: white;
    }
    QTableWidget::item {
        padding: 12px;
        border-bottom: 1px solid #e0e0e0;
    }
    QHeaderView::section {
        background-color: #00bcd4;
        padding: 12px;
        border: none;
        border-bottom: 2px solid #00838f;
        font-weight: bold;
        color: white;
    }
    QListWidget {
        border: 2px solid #00bcd4;
        border-radius: 8px;
        background-color: white;
    }
    QListWidget::item {
        padding: 12px;
        border-bottom: 1px solid #e0e0e0;
    }
    QListWidget::item:selected {
        background-color: #00bcd4;
        color: white;
    }
    QFrame {
        border: 2px solid #00bcd4;
        border-radius: 8px;
        background-color: white;
    }
"""

# Estilo escuro
DARK_STYLE = """
    QMainWindow, QDialog {
        background-color: #1a1a1a;
    }
    QLabel {
        color: #ffffff;
    }
    QLineEdit, QComboBox, QTextEdit {
        background-color: #2d2d2d;
        color: #ffffff;
        border: 1px solid #00bcd4;
        border-radius: 4px;
        padding: 5px;
    }
    QPushButton {
        background-color: #00bcd4;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #00838f;
    }
    QPushButton:pressed {
        background-color: #006064;
    }
    QTableWidget {
        background-color: #2d2d2d;
        color: #ffffff;
        border: 1px solid #00bcd4;
        border-radius: 4px;
        gridline-color: #404040;
    }
    QTableWidget::item {
        padding: 5px;
    }
    QTableWidget::item:selected {
        background-color: #00bcd4;
        color: white;
    }
    QHeaderView::section {
        background-color: #1a1a1a;
        color: #ffffff;
        padding: 5px;
        border: 1px solid #00bcd4;
    }
    QListWidget {
        background-color: #2d2d2d;
        color: #ffffff;
        border: 1px solid #00bcd4;
        border-radius: 4px;
    }
    QListWidget::item {
        padding: 5px;
    }
    QListWidget::item:selected {
        background-color: #00bcd4;
        color: white;
    }
    QGroupBox {
        color: #ffffff;
        border: 1px solid #00bcd4;
        border-radius: 4px;
        margin-top: 10px;
        padding-top: 10px;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 3px;
    }
    QCheckBox {
        color: #ffffff;
    }
    QCheckBox::indicator {
        width: 18px;
        height: 18px;
    }
    QCheckBox::indicator:unchecked {
        border: 1px solid #404040;
        background-color: #2d2d2d;
    }
    QCheckBox::indicator:checked {
        border: 1px solid #00bcd4;
        background-color: #00bcd4;
        image: url(check.png);
    }
    QScrollArea {
        background-color: #1a1a1a;
        border: none;
    }
    QScrollBar:vertical {
        background-color: #1a1a1a;
        width: 12px;
        margin: 0px;
    }
    QScrollBar::handle:vertical {
        background-color: #404040;
        min-height: 20px;
        border-radius: 6px;
    }
    QScrollBar::handle:vertical:hover {
        background-color: #505050;
    }
    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical {
        height: 0px;
    }
"""


class ModernFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                border: 2px solid #e0e0e0;
            }
        """)


class DashboardCard(ModernFrame):
    def __init__(self, title, value, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        title_label = QLabel(title)
        title_label.setStyleSheet("color: #7f8c8d; font-size: 14px;")

        value_label = QLabel(value)
        value_label.setStyleSheet(
            "color: #2c3e50; font-size: 24px; font-weight: bold;")

        layout.addWidget(title_label)
        layout.addWidget(value_label)


class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Fin-Assist - Login")
        self.setFixedSize(400, 300)
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
            }
            QLabel {
                color: #333;
                font-size: 14px;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
                color: black;
            }
            QPushButton {
                padding: 10px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        layout = QVBoxLayout()

        # Logo e título
        title = QLabel("Fin-Assist")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        layout.addWidget(title)

        # Campos de login
        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)

        email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Digite seu email")

        password_label = QLabel("Senha:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Digite sua senha")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        form_layout.addWidget(email_label)
        form_layout.addWidget(self.email_input)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)

        layout.addLayout(form_layout)

        # Botões
        button_layout = QHBoxLayout()

        login_button = QPushButton("Entrar")
        login_button.clicked.connect(self.handle_login)

        register_button = QPushButton("Cadastrar")
        register_button.clicked.connect(self.show_register_dialog)

        button_layout.addWidget(login_button)
        button_layout.addWidget(register_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def handle_login(self):
        email = self.email_input.text()
        password = self.password_input.text()

        if self.db.verify_credentials(email, password):
            self.accept()
        else:
            QMessageBox.warning(self, "Erro", "Email ou senha inválidos!")

    def show_register_dialog(self):
        dialog = RegisterDialog(self.db, self)
        if dialog.exec():
            QMessageBox.information(
                self, "Sucesso", "Cadastro realizado com sucesso!")


class RegisterDialog(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Cadastro")
        self.setFixedSize(400, 400)
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
            }
            QLabel {
                color: #333;
                font-size: 14px;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
                color: black;
            }
            QPushButton {
                padding: 10px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        layout = QVBoxLayout()

        # Campos de cadastro
        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)

        name_label = QLabel("Nome:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Digite seu nome")

        email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Digite seu email")

        password_label = QLabel("Senha:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Digite sua senha")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        confirm_password_label = QLabel("Confirmar Senha:")
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirme sua senha")
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)

        form_layout.addWidget(name_label)
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(email_label)
        form_layout.addWidget(self.email_input)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(confirm_password_label)
        form_layout.addWidget(self.confirm_password_input)

        layout.addLayout(form_layout)

        # Botão de cadastro
        register_button = QPushButton("Cadastrar")
        register_button.clicked.connect(self.handle_register)

        layout.addWidget(register_button)

        self.setLayout(layout)

    def handle_register(self):
        name = self.name_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not all([name, email, password, confirm_password]):
            QMessageBox.warning(
                self, "Erro", "Todos os campos são obrigatórios!")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Erro", "As senhas não coincidem!")
            return

        if self.db.register_user(name, email, password):
            self.accept()
        else:
            QMessageBox.warning(self, "Erro", "Erro ao cadastrar usuário!")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.chatbot = ChatBot(self.db)
        self.setup_ui()

        # Configurar timer para atualização automática
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_all)
        self.update_timer.start(60000)  # Atualizar a cada 1 minuto

        # Carregar dados iniciais
        self.update_all()

        # Carregar configurações
        self.load_settings()

    def setup_ui(self):
        self.setWindowTitle("Fin-Assist - Gestão Financeira")
        self.setMinimumSize(1200, 800)
        self.setStyleSheet(GLOBAL_STYLE)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Menu lateral
        menu_frame = ModernFrame()
        menu_layout = QVBoxLayout(menu_frame)
        menu_layout.setContentsMargins(10, 10, 10, 10)

        # Logo
        logo_label = QLabel("Fin-Assist")
        logo_label.setStyleSheet(
            "font-size: 24px; font-weight: bold; color: #2c3e50;")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        menu_layout.addWidget(logo_label)

        # Menu items
        self.menu_list = QListWidget()
        self.menu_list.addItems([
            "Dashboard",
            "Transações",
            "Orçamentos",
            "Metas",
            "Investimentos",
            "Contas",
            "Cartões",
            "Lembretes",
            "Dicas"
        ])
        self.menu_list.currentRowChanged.connect(self.change_page)
        menu_layout.addWidget(self.menu_list)

        # Área de conteúdo
        self.content_stack = QStackedWidget()

        # Adicionar páginas
        self.content_stack.addWidget(self.create_dashboard_page())
        self.content_stack.addWidget(self.create_transactions_page())
        self.content_stack.addWidget(self.create_budgets_page())
        self.content_stack.addWidget(self.create_goals_page())
        self.content_stack.addWidget(self.create_investments_page())
        self.content_stack.addWidget(self.create_accounts_page())
        self.content_stack.addWidget(self.create_cards_page())
        self.content_stack.addWidget(self.create_reminders_page())
        self.content_stack.addWidget(self.create_tips_page())

        # Adicionar widgets ao layout principal
        main_layout.addWidget(menu_frame, 1)
        main_layout.addWidget(self.content_stack, 4)

        # Configurar conexões das tabelas
        self.setup_table_connections()

        # Conectar filtros de transações
        self.period_combo.currentTextChanged.connect(self.filter_transactions)
        self.category_combo.currentTextChanged.connect(
            self.filter_transactions)
        self.type_combo.currentTextChanged.connect(self.filter_transactions)

        # Adicionar botões de exportação e relatório
        export_button = QPushButton("Exportar Dados")
        export_button.clicked.connect(self.export_data)

        report_button = QPushButton("Gerar Relatório")
        report_button.clicked.connect(self.generate_report)

        # Adicionar botões ao layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(export_button)
        button_layout.addWidget(report_button)
        button_layout.addStretch()

        # Adicionar ao layout principal
        main_layout.addLayout(button_layout)

        # Criar menu principal
        menubar = self.menuBar()

        # Menu Arquivo
        file_menu = menubar.addMenu("Arquivo")

        export_action = QAction("Exportar Dados", self)
        export_action.triggered.connect(self.export_data)
        file_menu.addAction(export_action)

        backup_action = QAction("Fazer Backup", self)
        backup_action.triggered.connect(self.create_backup)
        file_menu.addAction(backup_action)

        restore_action = QAction("Restaurar Backup", self)
        restore_action.triggered.connect(self.restore_backup)
        file_menu.addAction(restore_action)

        file_menu.addSeparator()

        exit_action = QAction("Sair", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Menu Editar
        edit_menu = menubar.addMenu("Editar")

        settings_action = QAction("Configurações", self)
        settings_action.triggered.connect(self.show_settings)
        edit_menu.addAction(settings_action)

        # Menu Ajuda
        help_menu = menubar.addMenu("Ajuda")

        about_action = QAction("Sobre", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_dashboard_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(20)

        # Cards de resumo
        cards_layout = QHBoxLayout()

        self.balance_card = DashboardCard("Saldo Total", "R$ 0,00")
        self.revenue_card = DashboardCard("Receitas", "R$ 0,00")
        self.expense_card = DashboardCard("Despesas", "R$ 0,00")

        cards_layout.addWidget(self.balance_card)
        cards_layout.addWidget(self.revenue_card)
        cards_layout.addWidget(self.expense_card)

        layout.addLayout(cards_layout)

        # Gráficos
        charts_layout = QHBoxLayout()

        # Gráfico de despesas
        expense_chart_frame = ModernFrame()
        expense_chart_layout = QVBoxLayout(expense_chart_frame)
        expense_chart_layout.addWidget(QLabel("Despesas por Categoria"))
        self.expense_chart = QWidget()
        expense_chart_layout.addWidget(self.expense_chart)

        # Gráfico de evolução
        evolution_chart_frame = ModernFrame()
        evolution_chart_layout = QVBoxLayout(evolution_chart_frame)
        evolution_chart_layout.addWidget(QLabel("Evolução do Saldo"))
        self.evolution_chart = QWidget()
        evolution_chart_layout.addWidget(self.evolution_chart)

        charts_layout.addWidget(expense_chart_frame)
        charts_layout.addWidget(evolution_chart_frame)

        layout.addLayout(charts_layout)

        # Tabela de últimas transações
        transactions_frame = ModernFrame()
        transactions_layout = QVBoxLayout(transactions_frame)
        transactions_layout.addWidget(QLabel("Últimas Transações"))

        self.transaction_table = QTableWidget()
        self.transaction_table.setColumnCount(4)
        self.transaction_table.setHorizontalHeaderLabels(
            ["Data", "Descrição", "Categoria", "Valor"])
        self.transaction_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)

        transactions_layout.addWidget(self.transaction_table)
        layout.addWidget(transactions_frame)

        return page

    def create_transactions_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(20)

        # Cabeçalho
        header_layout = QHBoxLayout()

        title = QLabel("Transações")
        title.setStyleSheet(
            "font-size: 24px; font-weight: bold; color: #2c3e50;")

        add_button = QPushButton("Nova Transação")
        add_button.clicked.connect(self.show_add_transaction_dialog)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(add_button)

        layout.addLayout(header_layout)

        # Filtros
        filters_frame = ModernFrame()
        filters_layout = QHBoxLayout(filters_frame)

        # Período
        period_label = QLabel("Período:")
        self.period_combo = QComboBox()
        self.period_combo.addItems(
            ["Último mês", "Últimos 3 meses", "Último ano", "Personalizado"])

        # Categoria
        category_label = QLabel("Categoria:")
        self.category_combo = QComboBox()
        self.category_combo.addItems(self.db.get_categorias())

        # Tipo
        type_label = QLabel("Tipo:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Todos", "Receitas", "Despesas"])

        filters_layout.addWidget(period_label)
        filters_layout.addWidget(self.period_combo)
        filters_layout.addWidget(category_label)
        filters_layout.addWidget(self.category_combo)
        filters_layout.addWidget(type_label)
        filters_layout.addWidget(self.type_combo)

        layout.addWidget(filters_frame)

        # Tabela de transações
        self.transactions_table = QTableWidget()
        self.transactions_table.setColumnCount(5)
        self.transactions_table.setHorizontalHeaderLabels(
            ["Data", "Descrição", "Categoria", "Tipo", "Valor"])
        self.transactions_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)

        layout.addWidget(self.transactions_table)

        return page

    def create_budgets_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(20)

        # Cabeçalho
        header_layout = QHBoxLayout()

        title = QLabel("Orçamentos")
        title.setStyleSheet(
            "font-size: 24px; font-weight: bold; color: #2c3e50;")

        add_button = QPushButton("Novo Orçamento")
        add_button.clicked.connect(self.show_add_budget_dialog)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(add_button)

        layout.addLayout(header_layout)

        # Cards de orçamento
        budgets_layout = QHBoxLayout()

        # Adicionar cards de orçamento aqui
        # TODO: Implementar cards de orçamento

        layout.addLayout(budgets_layout)

        # Tabela de orçamentos
        self.budgets_table = QTableWidget()
        self.budgets_table.setColumnCount(4)
        self.budgets_table.setHorizontalHeaderLabels(
            ["Categoria", "Valor", "Gasto", "Restante"])
        self.budgets_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)

        layout.addWidget(self.budgets_table)

        return page

    def create_goals_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(20)

        # Cabeçalho
        header_layout = QHBoxLayout()

        title = QLabel("Metas Financeiras")
        title.setStyleSheet(
            "font-size: 24px; font-weight: bold; color: #2c3e50;")

        add_button = QPushButton("Nova Meta")
        add_button.clicked.connect(self.show_add_goal_dialog)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(add_button)

        layout.addLayout(header_layout)

        # Cards de metas
        goals_layout = QHBoxLayout()

        # Adicionar cards de metas aqui
        # TODO: Implementar cards de metas

        layout.addLayout(goals_layout)

        # Tabela de metas
        self.goals_table = QTableWidget()
        self.goals_table.setColumnCount(4)
        self.goals_table.setHorizontalHeaderLabels(
            ["Meta", "Valor Alvo", "Valor Atual", "Progresso"])
        self.goals_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)

        layout.addWidget(self.goals_table)

        return page

    def create_investments_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(20)

        # Cabeçalho
        header_layout = QHBoxLayout()

        title = QLabel("Investimentos")
        title.setStyleSheet(
            "font-size: 24px; font-weight: bold; color: #2c3e50;")

        add_button = QPushButton("Novo Investimento")
        add_button.clicked.connect(self.show_add_investment_dialog)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(add_button)

        layout.addLayout(header_layout)

        # Resumo de investimentos
        summary_frame = ModernFrame()
        summary_layout = QHBoxLayout(summary_frame)

        self.total_invested_card = DashboardCard("Total Investido", "R$ 0,00")
        self.total_profit_card = DashboardCard("Lucro Total", "R$ 0,00")
        self.profit_rate_card = DashboardCard("Taxa de Retorno", "0%")

        summary_layout.addWidget(self.total_invested_card)
        summary_layout.addWidget(self.total_profit_card)
        summary_layout.addWidget(self.profit_rate_card)

        layout.addWidget(summary_frame)

        # Tabela de investimentos
        self.investments_table = QTableWidget()
        self.investments_table.setColumnCount(5)
        self.investments_table.setHorizontalHeaderLabels(
            ["Nome", "Tipo", "Valor", "Rentabilidade", "Data"])
        self.investments_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)

        layout.addWidget(self.investments_table)

        return page

    def create_accounts_page(self):
        """Cria a página de contas"""
        try:
            page = QWidget()
            layout = QVBoxLayout()

            # Título
            title = QLabel("Contas")
            title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
            layout.addWidget(title)

            # Tabela de contas
            self.accounts_table = QTableWidget()
            self.accounts_table.setColumnCount(4)
            self.accounts_table.setHorizontalHeaderLabels(
                ["Nome", "Tipo", "Banco", "Saldo"])
            self.accounts_table.horizontalHeader().setSectionResizeMode(
                QHeaderView.ResizeMode.Stretch)
            self.accounts_table.setMinimumHeight(400)
            self.accounts_table.setContextMenuPolicy(
                Qt.ContextMenuPolicy.CustomContextMenu)
            self.accounts_table.customContextMenuRequested.connect(
                self.show_account_context_menu)
            layout.addWidget(self.accounts_table)

            # Botão para adicionar conta
            add_button = QPushButton("Adicionar Conta")
            add_button.clicked.connect(self.show_add_account_dialog)
            layout.addWidget(add_button)

            # Atualizar tabela
            self.update_accounts_table()

            page.setLayout(layout)
            return page

        except Exception as e:
            print(f"Erro ao criar página de contas: {str(e)}")
            return QWidget()

    def show_account_context_menu(self, position):
        """Mostra o menu de contexto da tabela de contas"""
        try:
            menu = QMenu()

            edit_action = QAction("Editar", self)
            delete_action = QAction("Excluir", self)

            menu.addAction(edit_action)
            menu.addAction(delete_action)

            # Obter o item selecionado
            item = self.accounts_table.itemAt(position)
            if item:
                row = item.row()
                account_id = self.accounts_table.item(
                    row, 0).data(Qt.ItemDataRole.UserRole)

                edit_action.triggered.connect(
                    lambda: self.edit_account(account_id))
                delete_action.triggered.connect(
                    lambda: self.delete_account(account_id))

                menu.exec(self.accounts_table.viewport().mapToGlobal(position))

        except Exception as e:
            print(f"Erro ao mostrar menu de contexto: {str(e)}")

    def create_cards_page(self):
        """Cria a página de cartões"""
        try:
            page = QWidget()
            layout = QVBoxLayout()

            # Título
            title = QLabel("Cartões")
            title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
            layout.addWidget(title)

            # Tabela de cartões
            self.cards_table = QTableWidget()
            self.cards_table.setColumnCount(4)
            self.cards_table.setHorizontalHeaderLabels(
                ["Nome", "Tipo", "Banco", "Limite"])
            self.cards_table.horizontalHeader().setSectionResizeMode(
                QHeaderView.ResizeMode.Stretch)
            self.cards_table.setMinimumHeight(400)
            self.cards_table.setContextMenuPolicy(
                Qt.ContextMenuPolicy.CustomContextMenu)
            self.cards_table.customContextMenuRequested.connect(
                self.show_card_context_menu)
            layout.addWidget(self.cards_table)

            # Botão para adicionar cartão
            add_button = QPushButton("Adicionar Cartão")
            add_button.clicked.connect(self.show_add_card_dialog)
            layout.addWidget(add_button)

            # Atualizar tabela
            self.update_cards_table()

            page.setLayout(layout)
            return page

        except Exception as e:
            print(f"Erro ao criar página de cartões: {str(e)}")
            return QWidget()

    def show_card_context_menu(self, position):
        """Mostra o menu de contexto da tabela de cartões"""
        try:
            menu = QMenu()

            edit_action = QAction("Editar", self)
            delete_action = QAction("Excluir", self)

            menu.addAction(edit_action)
            menu.addAction(delete_action)

            # Obter o item selecionado
            item = self.cards_table.itemAt(position)
            if item:
                row = item.row()
                card_id = self.cards_table.item(
                    row, 0).data(Qt.ItemDataRole.UserRole)

                edit_action.triggered.connect(lambda: self.edit_card(card_id))
                delete_action.triggered.connect(
                    lambda: self.delete_card(card_id))

                menu.exec(self.cards_table.viewport().mapToGlobal(position))

        except Exception as e:
            print(f"Erro ao mostrar menu de contexto: {str(e)}")

    def update_accounts_table(self):
        """Atualiza a tabela de contas"""
        try:
            self.accounts_table.setRowCount(0)
            accounts = self.db.get_accounts()

            for account in accounts:
                row = self.accounts_table.rowCount()
                self.accounts_table.insertRow(row)

                name_item = QTableWidgetItem(account['nome'])
                name_item.setData(Qt.ItemDataRole.UserRole, account['id'])

                self.accounts_table.setItem(row, 0, name_item)
                self.accounts_table.setItem(
                    row, 1, QTableWidgetItem(account['tipo']))
                self.accounts_table.setItem(
                    row, 2, QTableWidgetItem(account['banco']))
                self.accounts_table.setItem(
                    row, 3, QTableWidgetItem(f"R$ {account['saldo']:.2f}"))

        except Exception as e:
            print(f"Erro ao atualizar tabela de contas: {str(e)}")
            QMessageBox.warning(
                self, "Erro", "Erro ao atualizar tabela de contas!")

    def update_cards_table(self):
        """Atualiza a tabela de cartões"""
        try:
            self.cards_table.setRowCount(0)
            cards = self.db.get_cards()

            for card in cards:
                row = self.cards_table.rowCount()
                self.cards_table.insertRow(row)

                name_item = QTableWidgetItem(card['nome'])
                name_item.setData(Qt.ItemDataRole.UserRole, card['id'])

                self.cards_table.setItem(row, 0, name_item)
                self.cards_table.setItem(
                    row, 1, QTableWidgetItem(card['tipo']))
                self.cards_table.setItem(
                    row, 2, QTableWidgetItem(card['banco']))
                self.cards_table.setItem(
                    row, 3, QTableWidgetItem(f"R$ {card['limite']:.2f}"))

        except Exception as e:
            print(f"Erro ao atualizar tabela de cartões: {str(e)}")
            QMessageBox.warning(
                self, "Erro", "Erro ao atualizar tabela de cartões!")

    def create_reminders_page(self):
        """Cria a página de lembretes"""
        try:
            page = QWidget()
            layout = QVBoxLayout()

            # Título
            title = QLabel("Lembretes")
            title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
            layout.addWidget(title)

            # Lista de lembretes
            self.reminders_list = QListWidget()
            self.reminders_list.setMinimumHeight(400)
            self.reminders_list.itemClicked.connect(self.show_reminder_details)
            layout.addWidget(self.reminders_list)

            # Botão para adicionar lembrete
            add_button = QPushButton("Adicionar Lembrete")
            add_button.clicked.connect(self.show_add_reminder_dialog)
            layout.addWidget(add_button)

            # Atualizar lista
            self.update_reminders_list()

            page.setLayout(layout)
            return page

        except Exception as e:
            print(f"Erro ao criar página de lembretes: {str(e)}")
            return QWidget()

    def show_add_reminder_dialog(self):
        """Mostra o diálogo para adicionar um novo lembrete"""
        try:
            dialog = QDialog(self)
            dialog.setWindowTitle("Adicionar Lembrete")
            dialog.setMinimumWidth(400)

            layout = QVBoxLayout()

            # Campos
            title_label = QLabel("Título:")
            title_edit = QLineEdit()

            description_label = QLabel("Descrição:")
            description_edit = QTextEdit()
            description_edit.setMinimumHeight(100)

            date_label = QLabel("Data:")
            date_edit = QCalendarWidget()

            category_label = QLabel("Categoria:")
            category_combo = QComboBox()
            category_combo.addItems([
                "Contas",
                "Investimentos",
                "Metas",
                "Outros"
            ])

            value_label = QLabel("Valor:")
            value_edit = QLineEdit()

            recurrence_label = QLabel("Recorrência:")
            recurrence_combo = QComboBox()
            recurrence_combo.addItems([
                "Nenhuma",
                "Diária",
                "Semanal",
                "Mensal",
                "Anual"
            ])

            # Adicionar campos ao layout
            layout.addWidget(title_label)
            layout.addWidget(title_edit)
            layout.addWidget(description_label)
            layout.addWidget(description_edit)
            layout.addWidget(date_label)
            layout.addWidget(date_edit)
            layout.addWidget(category_label)
            layout.addWidget(category_combo)
            layout.addWidget(value_label)
            layout.addWidget(value_edit)
            layout.addWidget(recurrence_label)
            layout.addWidget(recurrence_combo)

            # Botões
            button_layout = QHBoxLayout()

            save_button = QPushButton("Salvar")
            save_button.clicked.connect(lambda: self.handle_save_reminder(
                dialog,
                title_edit.text(),
                description_edit.toPlainText(),
                date_edit.selectedDate().toPyDate(),
                category_combo.currentText(),
                value_edit.text(),
                recurrence_combo.currentText()
            ))

            cancel_button = QPushButton("Cancelar")
            cancel_button.clicked.connect(dialog.reject)

            button_layout.addWidget(save_button)
            button_layout.addWidget(cancel_button)

            layout.addLayout(button_layout)
            dialog.setLayout(layout)

            dialog.exec()

        except Exception as e:
            print(f"Erro ao mostrar diálogo de lembrete: {str(e)}")
            QMessageBox.warning(
                self, "Erro", "Erro ao mostrar diálogo de lembrete!")

    def handle_save_reminder(self, dialog, title, description, date, category, value, recurrence):
        """Salva um novo lembrete"""
        try:
            if not title or not description:
                QMessageBox.warning(
                    self, "Erro", "Preencha todos os campos obrigatórios!")
                return

            try:
                value = float(value) if value else 0.0
            except ValueError:
                QMessageBox.warning(self, "Erro", "Valor inválido!")
                return

            if self.db.add_reminder(title, description, date, category, value, recurrence):
                self.update_reminders_list()
                dialog.accept()
                QMessageBox.information(
                    self, "Sucesso", "Lembrete adicionado com sucesso!")
            else:
                QMessageBox.warning(
                    self, "Erro", "Erro ao adicionar lembrete!")

        except Exception as e:
            print(f"Erro ao salvar lembrete: {str(e)}")
            QMessageBox.warning(self, "Erro", "Erro ao salvar lembrete!")

    def show_reminder_details(self, item):
        """Mostra os detalhes de um lembrete"""
        try:
            reminder = item.data(Qt.ItemDataRole.UserRole)

            dialog = QDialog(self)
            dialog.setWindowTitle(reminder['titulo'])
            dialog.setMinimumWidth(500)
            dialog.setMinimumHeight(400)

            layout = QVBoxLayout()

            # Título
            title_label = QLabel(reminder['titulo'])
            title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
            layout.addWidget(title_label)

            # Descrição
            description_label = QLabel(reminder['descricao'])
            description_label.setWordWrap(True)
            layout.addWidget(description_label)

            # Data
            date_label = QLabel(
                f"Data: {reminder['data'].strftime('%d/%m/%Y')}")
            layout.addWidget(date_label)

            # Categoria
            category_label = QLabel(f"Categoria: {reminder['categoria']}")
            layout.addWidget(category_label)

            # Valor
            value_label = QLabel(f"Valor: R$ {reminder['valor']:.2f}")
            layout.addWidget(value_label)

            # Recorrência
            recurrence_label = QLabel(
                f"Recorrência: {reminder['recorrencia']}")
            layout.addWidget(recurrence_label)

            # Botões
            button_layout = QHBoxLayout()

            edit_button = QPushButton("Editar")
            edit_button.clicked.connect(
                lambda: self.edit_reminder(reminder['id']))

            delete_button = QPushButton("Excluir")
            delete_button.clicked.connect(
                lambda: self.delete_reminder(reminder['id']))

            close_button = QPushButton("Fechar")
            close_button.clicked.connect(dialog.accept)

            button_layout.addWidget(edit_button)
            button_layout.addWidget(delete_button)
            button_layout.addWidget(close_button)

            layout.addLayout(button_layout)
            dialog.setLayout(layout)

            dialog.exec()

        except Exception as e:
            print(f"Erro ao mostrar detalhes do lembrete: {str(e)}")
            QMessageBox.warning(
                self, "Erro", "Erro ao mostrar detalhes do lembrete!")

    def edit_reminder(self, reminder_id):
        """Edita um lembrete existente"""
        try:
            reminder = self.db.get_reminder(reminder_id)
            if not reminder:
                return

            dialog = QDialog(self)
            dialog.setWindowTitle("Editar Lembrete")
            dialog.setMinimumWidth(400)

            layout = QVBoxLayout()

            # Campos
            title_label = QLabel("Título:")
            title_edit = QLineEdit(reminder['titulo'])

            description_label = QLabel("Descrição:")
            description_edit = QTextEdit(reminder['descricao'])
            description_edit.setMinimumHeight(100)

            date_label = QLabel("Data:")
            date_edit = QCalendarWidget()
            date_edit.setSelectedDate(reminder['data'])

            category_label = QLabel("Categoria:")
            category_combo = QComboBox()
            category_combo.addItems([
                "Contas",
                "Investimentos",
                "Metas",
                "Outros"
            ])
            category_combo.setCurrentText(reminder['categoria'])

            value_label = QLabel("Valor:")
            value_edit = QLineEdit(str(reminder['valor']))

            recurrence_label = QLabel("Recorrência:")
            recurrence_combo = QComboBox()
            recurrence_combo.addItems([
                "Nenhuma",
                "Diária",
                "Semanal",
                "Mensal",
                "Anual"
            ])
            recurrence_combo.setCurrentText(reminder['recorrencia'])

            # Adicionar campos ao layout
            layout.addWidget(title_label)
            layout.addWidget(title_edit)
            layout.addWidget(description_label)
            layout.addWidget(description_edit)
            layout.addWidget(date_label)
            layout.addWidget(date_edit)
            layout.addWidget(category_label)
            layout.addWidget(category_combo)
            layout.addWidget(value_label)
            layout.addWidget(value_edit)
            layout.addWidget(recurrence_label)
            layout.addWidget(recurrence_combo)

            # Botões
            button_layout = QHBoxLayout()

            save_button = QPushButton("Salvar")
            save_button.clicked.connect(lambda: self.handle_save_reminder_edit(
                dialog,
                reminder_id,
                title_edit.text(),
                description_edit.toPlainText(),
                date_edit.selectedDate().toPyDate(),
                category_combo.currentText(),
                value_edit.text(),
                recurrence_combo.currentText()
            ))

            cancel_button = QPushButton("Cancelar")
            cancel_button.clicked.connect(dialog.reject)

            button_layout.addWidget(save_button)
            button_layout.addWidget(cancel_button)

            layout.addLayout(button_layout)
            dialog.setLayout(layout)

            dialog.exec()

        except Exception as e:
            print(f"Erro ao editar lembrete: {str(e)}")
            QMessageBox.warning(self, "Erro", "Erro ao editar lembrete!")

    def handle_save_reminder_edit(self, dialog, reminder_id, title, description, date, category, value, recurrence):
        """Salva as alterações de um lembrete"""
        try:
            if not title or not description:
                QMessageBox.warning(
                    self, "Erro", "Preencha todos os campos obrigatórios!")
                return

            try:
                value = float(value) if value else 0.0
            except ValueError:
                QMessageBox.warning(self, "Erro", "Valor inválido!")
                return

            if self.db.update_reminder(reminder_id, title, description, date, category, value, recurrence):
                self.update_reminders_list()
                dialog.accept()
                QMessageBox.information(
                    self, "Sucesso", "Lembrete atualizado com sucesso!")
            else:
                QMessageBox.warning(
                    self, "Erro", "Erro ao atualizar lembrete!")

        except Exception as e:
            print(f"Erro ao salvar edição do lembrete: {str(e)}")
            QMessageBox.warning(
                self, "Erro", "Erro ao salvar edição do lembrete!")

    def delete_reminder(self, reminder_id):
        """Exclui um lembrete"""
        try:
            reply = QMessageBox.question(
                self,
                "Confirmar Exclusão",
                "Tem certeza que deseja excluir este lembrete?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                if self.db.delete_reminder(reminder_id):
                    self.update_reminders_list()
                    QMessageBox.information(
                        self, "Sucesso", "Lembrete excluído com sucesso!")
                else:
                    QMessageBox.warning(
                        self, "Erro", "Erro ao excluir lembrete!")

        except Exception as e:
            print(f"Erro ao excluir lembrete: {str(e)}")
            QMessageBox.warning(self, "Erro", "Erro ao excluir lembrete!")

    def create_tips_page(self):
        """Cria a página de dicas financeiras"""
        try:
            page = QWidget()
            layout = QVBoxLayout()

            # Título
            title = QLabel("Dicas Financeiras")
            title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
            layout.addWidget(title)

            # Lista de dicas
            self.tips_list = QListWidget()
            self.tips_list.setMinimumHeight(400)
            layout.addWidget(self.tips_list)

            # Botão para adicionar dica
            add_button = QPushButton("Adicionar Dica")
            add_button.clicked.connect(self.show_add_tip_dialog)
            layout.addWidget(add_button)

            # Atualizar lista
            self.update_tips_list()

            page.setLayout(layout)
            return page

        except Exception as e:
            print(f"Erro ao criar página de dicas: {str(e)}")
            return QWidget()

    def show_add_tip_dialog(self):
        """Mostra o diálogo para adicionar uma nova dica"""
        try:
            dialog = QDialog(self)
            dialog.setWindowTitle("Adicionar Dica")
            dialog.setMinimumWidth(400)

            layout = QVBoxLayout()

            # Campos
            title_label = QLabel("Título:")
            title_edit = QLineEdit()

            content_label = QLabel("Conteúdo:")
            content_edit = QTextEdit()
            content_edit.setMinimumHeight(200)

            category_label = QLabel("Categoria:")
            category_combo = QComboBox()
            category_combo.addItems([
                "Economia",
                "Investimentos",
                "Orçamento",
                "Dívidas",
                "Poupança",
                "Outros"
            ])

            # Adicionar campos ao layout
            layout.addWidget(title_label)
            layout.addWidget(title_edit)
            layout.addWidget(content_label)
            layout.addWidget(content_edit)
            layout.addWidget(category_label)
            layout.addWidget(category_combo)

            # Botões
            button_layout = QHBoxLayout()

            save_button = QPushButton("Salvar")
            save_button.clicked.connect(lambda: self.handle_save_tip(
                dialog,
                title_edit.text(),
                content_edit.toPlainText(),
                category_combo.currentText()
            ))

            cancel_button = QPushButton("Cancelar")
            cancel_button.clicked.connect(dialog.reject)

            button_layout.addWidget(save_button)
            button_layout.addWidget(cancel_button)

            layout.addLayout(button_layout)
            dialog.setLayout(layout)

            dialog.exec()

        except Exception as e:
            print(f"Erro ao mostrar diálogo de dica: {str(e)}")
            QMessageBox.warning(
                self, "Erro", "Erro ao mostrar diálogo de dica!")

    def handle_save_tip(self, dialog, title, content, category):
        """Salva uma nova dica"""
        try:
            if not title or not content:
                QMessageBox.warning(self, "Erro", "Preencha todos os campos!")
                return

            if self.db.add_tip(title, content, category):
                self.update_tips_list()
                dialog.accept()
                QMessageBox.information(
                    self, "Sucesso", "Dica adicionada com sucesso!")
            else:
                QMessageBox.warning(self, "Erro", "Erro ao adicionar dica!")

        except Exception as e:
            print(f"Erro ao salvar dica: {str(e)}")
            QMessageBox.warning(self, "Erro", "Erro ao salvar dica!")

    def update_tips_list(self):
        """Atualiza a lista de dicas"""
        try:
            self.tips_list.clear()
            tips = self.db.get_tips()

            for tip in tips:
                item = QListWidgetItem(f"{tip['titulo']} - {tip['categoria']}")
                item.setData(Qt.ItemDataRole.UserRole, tip)
                self.tips_list.addItem(item)

        except Exception as e:
            print(f"Erro ao atualizar lista de dicas: {str(e)}")

    def show_tip_details(self, item):
        """Mostra os detalhes de uma dica"""
        try:
            tip = item.data(Qt.ItemDataRole.UserRole)

            dialog = QDialog(self)
            dialog.setWindowTitle(tip['titulo'])
            dialog.setMinimumWidth(500)
            dialog.setMinimumHeight(400)

            layout = QVBoxLayout()

            # Título
            title_label = QLabel(tip['titulo'])
            title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
            layout.addWidget(title_label)

            # Categoria
            category_label = QLabel(f"Categoria: {tip['categoria']}")
            layout.addWidget(category_label)

            # Conteúdo
            content_label = QLabel(tip['conteudo'])
            content_label.setWordWrap(True)
            layout.addWidget(content_label)

            # Botões
            button_layout = QHBoxLayout()

            edit_button = QPushButton("Editar")
            edit_button.clicked.connect(lambda: self.edit_tip(tip['id']))

            delete_button = QPushButton("Excluir")
            delete_button.clicked.connect(lambda: self.delete_tip(tip['id']))

            close_button = QPushButton("Fechar")
            close_button.clicked.connect(dialog.accept)

            button_layout.addWidget(edit_button)
            button_layout.addWidget(delete_button)
            button_layout.addWidget(close_button)

            layout.addLayout(button_layout)
            dialog.setLayout(layout)

            dialog.exec()

        except Exception as e:
            print(f"Erro ao mostrar detalhes da dica: {str(e)}")
            QMessageBox.warning(
                self, "Erro", "Erro ao mostrar detalhes da dica!")

    def edit_tip(self, tip_id):
        """Edita uma dica existente"""
        try:
            tip = self.db.get_tip(tip_id)
            if not tip:
                return

            dialog = QDialog(self)
            dialog.setWindowTitle("Editar Dica")
            dialog.setMinimumWidth(400)

            layout = QVBoxLayout()

            # Campos
            title_label = QLabel("Título:")
            title_edit = QLineEdit(tip['titulo'])

            content_label = QLabel("Conteúdo:")
            content_edit = QTextEdit(tip['conteudo'])
            content_edit.setMinimumHeight(200)

            category_label = QLabel("Categoria:")
            category_combo = QComboBox()
            category_combo.addItems([
                "Economia",
                "Investimentos",
                "Orçamento",
                "Dívidas",
                "Poupança",
                "Outros"
            ])
            category_combo.setCurrentText(tip['categoria'])

            # Adicionar campos ao layout
            layout.addWidget(title_label)
            layout.addWidget(title_edit)
            layout.addWidget(content_label)
            layout.addWidget(content_edit)
            layout.addWidget(category_label)
            layout.addWidget(category_combo)

            # Botões
            button_layout = QHBoxLayout()

            save_button = QPushButton("Salvar")
            save_button.clicked.connect(lambda: self.handle_save_tip_edit(
                dialog,
                tip_id,
                title_edit.text(),
                content_edit.toPlainText(),
                category_combo.currentText()
            ))

            cancel_button = QPushButton("Cancelar")
            cancel_button.clicked.connect(dialog.reject)

            button_layout.addWidget(save_button)
            button_layout.addWidget(cancel_button)

            layout.addLayout(button_layout)
            dialog.setLayout(layout)

            dialog.exec()

        except Exception as e:
            print(f"Erro ao editar dica: {str(e)}")
            QMessageBox.warning(self, "Erro", "Erro ao editar dica!")

    def handle_save_tip_edit(self, dialog, tip_id, title, content, category):
        """Salva as alterações de uma dica"""
        try:
            if not title or not content:
                QMessageBox.warning(self, "Erro", "Preencha todos os campos!")
                return

            if self.db.update_tip(tip_id, title, content, category):
                self.update_tips_list()
                dialog.accept()
                QMessageBox.information(
                    self, "Sucesso", "Dica atualizada com sucesso!")
            else:
                QMessageBox.warning(self, "Erro", "Erro ao atualizar dica!")

        except Exception as e:
            print(f"Erro ao salvar edição da dica: {str(e)}")
            QMessageBox.warning(self, "Erro", "Erro ao salvar edição da dica!")

    def delete_tip(self, tip_id):
        """Exclui uma dica"""
        try:
            reply = QMessageBox.question(
                self,
                "Confirmar Exclusão",
                "Tem certeza que deseja excluir esta dica?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                if self.db.delete_tip(tip_id):
                    self.update_tips_list()
                    QMessageBox.information(
                        self, "Sucesso", "Dica excluída com sucesso!")
                else:
                    QMessageBox.warning(self, "Erro", "Erro ao excluir dica!")

        except Exception as e:
            print(f"Erro ao excluir dica: {str(e)}")
            QMessageBox.warning(self, "Erro", "Erro ao excluir dica!")

    def change_page(self, index):
        self.content_stack.setCurrentIndex(index)

        # Atualizar dados da página atual
        if index == 0:  # Dashboard
            self.update_dashboard()
        elif index == 1:  # Transações
            self.update_transactions_table()
        elif index == 2:  # Orçamentos
            self.update_budgets_table()
        elif index == 3:  # Metas
            self.update_goals_table()
        elif index == 4:  # Investimentos
            self.update_investments_table()
        elif index == 5:  # Contas
            self.update_accounts_table()
        elif index == 6:  # Cartões
            self.update_cards_table()
        elif index == 7:  # Lembretes
            self.update_reminders_list()
        elif index == 8:  # Dicas
            self.update_tips_list()

    def update_dashboard(self):
        try:
            resumo = self.db.get_resumo_financeiro()

            # Atualizar cards
            self.balance_card.findChild(QLabel, "", Qt.FindChildOption.FindChildrenRecursively)[
                1].setText(f"R$ {resumo['saldo_total']:.2f}")
            self.revenue_card.findChild(QLabel, "", Qt.FindChildOption.FindChildrenRecursively)[
                1].setText(f"R$ {resumo['receitas']:.2f}")
            self.expense_card.findChild(QLabel, "", Qt.FindChildOption.FindChildrenRecursively)[
                1].setText(f"R$ {resumo['despesas']:.2f}")

            # Atualizar gráfico de despesas
            if resumo['despesas_por_categoria']:
                fig = Figure(figsize=(6, 4))
                ax = fig.add_subplot(111)

                labels = list(resumo['despesas_por_categoria'].keys())
                sizes = list(resumo['despesas_por_categoria'].values())
                colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))

                ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
                ax.set_title('Despesas por Categoria')

                canvas = FigureCanvas(fig)
                self.expense_chart.layout().addWidget(canvas)
            else:
                no_data_label = QLabel("Nenhuma despesa registrada")
                no_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.expense_chart.layout().addWidget(no_data_label)

        except Exception as e:
            print(f"Erro ao atualizar dashboard: {str(e)}")
            QMessageBox.warning(self, "Erro", "Erro ao atualizar dashboard!")

    def update_transactions_table(self):
        try:
            transacoes = self.db.get_transacoes()

            self.transactions_table.setRowCount(len(transacoes))

            for i, transacao in enumerate(transacoes):
                self.transactions_table.setItem(i, 0, QTableWidgetItem(
                    transacao['data'].strftime('%d/%m/%Y')))
                self.transactions_table.setItem(
                    i, 1, QTableWidgetItem(transacao['descricao']))
                self.transactions_table.setItem(
                    i, 2, QTableWidgetItem(transacao['categoria']))
                self.transactions_table.setItem(
                    i, 3, QTableWidgetItem(transacao['tipo']))
                self.transactions_table.setItem(
                    i, 4, QTableWidgetItem(f"R$ {transacao['valor']:.2f}"))

        except Exception as e:
            print(f"Erro ao atualizar tabela de transações: {str(e)}")
            QMessageBox.warning(
                self, "Erro", "Erro ao atualizar tabela de transações!")

    def update_budgets_table(self):
        try:
            orcamentos = self.db.get_orcamentos()

            self.budgets_table.setRowCount(len(orcamentos))

            for i, orcamento in enumerate(orcamentos):
                self.budgets_table.setItem(
                    i, 0, QTableWidgetItem(orcamento['categoria']))
                self.budgets_table.setItem(
                    i, 1, QTableWidgetItem(f"R$ {orcamento['valor']:.2f}"))
                self.budgets_table.setItem(
                    i, 2, QTableWidgetItem(f"R$ {orcamento['gasto']:.2f}"))
                self.budgets_table.setItem(i, 3, QTableWidgetItem(
                    f"R$ {orcamento['restante']:.2f}"))

        except Exception as e:
            print(f"Erro ao atualizar tabela de orçamentos: {str(e)}")
            QMessageBox.warning(
                self, "Erro", "Erro ao atualizar tabela de orçamentos!")

    def update_goals_table(self):
        try:
            metas = self.db.get_metas()

            self.goals_table.setRowCount(len(metas))

            for i, meta in enumerate(metas):
                self.goals_table.setItem(i, 0, QTableWidgetItem(meta['nome']))
                self.goals_table.setItem(i, 1, QTableWidgetItem(
                    f"R$ {meta['valor_alvo']:.2f}"))
                self.goals_table.setItem(i, 2, QTableWidgetItem(
                    f"R$ {meta['valor_atual']:.2f}"))

                progresso = (meta['valor_atual'] / meta['valor_meta']) * 100
                self.goals_table.setItem(
                    i, 3, QTableWidgetItem(f"{progresso:.1f}%"))

        except Exception as e:
            print(f"Erro ao atualizar tabela de metas: {str(e)}")
            QMessageBox.warning(
                self, "Erro", "Erro ao atualizar tabela de metas!")

    def update_investments_table(self):
        try:
            investimentos = self.db.get_investimentos()

            self.investments_table.setRowCount(len(investimentos))

            for i, investimento in enumerate(investimentos):
                self.investments_table.setItem(
                    i, 0, QTableWidgetItem(investimento['nome']))
                self.investments_table.setItem(
                    i, 1, QTableWidgetItem(investimento['tipo']))
                self.investments_table.setItem(
                    i, 2, QTableWidgetItem(f"R$ {investimento['valor']:.2f}"))
                self.investments_table.setItem(i, 3, QTableWidgetItem(
                    f"{investimento['rentabilidade']:.1f}%"))
                self.investments_table.setItem(i, 4, QTableWidgetItem(
                    investimento['data'].strftime('%d/%m/%Y')))

        except Exception as e:
            print(f"Erro ao atualizar tabela de investimentos: {str(e)}")
            QMessageBox.warning(
                self, "Erro", "Erro ao atualizar tabela de investimentos!")

    def update_accounts_table(self):
        try:
            contas = self.db.get_contas()

            self.accounts_table.setRowCount(len(contas))

            for i, conta in enumerate(contas):
                self.accounts_table.setItem(
                    i, 0, QTableWidgetItem(conta['nome']))
                self.accounts_table.setItem(
                    i, 1, QTableWidgetItem(conta['tipo']))
                self.accounts_table.setItem(
                    i, 2, QTableWidgetItem(f"R$ {conta['saldo']:.2f}"))
                self.accounts_table.setItem(
                    i, 3, QTableWidgetItem(conta['status']))

        except Exception as e:
            print(f"Erro ao atualizar tabela de contas: {str(e)}")
            QMessageBox.warning(
                self, "Erro", "Erro ao atualizar tabela de contas!")

    def update_reminders_list(self):
        try:
            lembretes = self.db.get_lembretes()

            self.reminders_list.clear()

            for lembrete in lembretes:
                item = QListWidgetItem()
                item.setText(
                    f"{lembrete['titulo']} - {lembrete['data'].strftime('%d/%m/%Y')}")
                item.setData(Qt.ItemDataRole.UserRole, lembrete)
                self.reminders_list.addItem(item)

        except Exception as e:
            print(f"Erro ao atualizar lista de lembretes: {str(e)}")
            QMessageBox.warning(
                self, "Erro", "Erro ao atualizar lista de lembretes!")

    def update_all(self):
        """Atualiza todos os dados da interface"""
        try:
            # Atualizar dashboard
            self.update_dashboard()

            # Atualizar tabelas e listas
            self.update_transactions_table()
            self.update_budgets_table()
            self.update_goals_table()
            self.update_investments_table()
            self.update_accounts_table()
            self.update_cards_table()
            self.update_reminders_list()
            self.update_tips_list()

            # Verificar lembretes
            self.check_reminders()

        except Exception as e:
            print(f"Erro ao atualizar dados: {str(e)}")

    def check_reminders(self):
        """Verifica se há lembretes para o dia atual"""
        try:
            lembretes = self.db.get_lembretes()
            hoje = date.today()

            for lembrete in lembretes:
                if lembrete['data'] == hoje:
                    QMessageBox.information(
                        self,
                        'Lembrete',
                        f"{lembrete['titulo']}\n\n{lembrete['descricao']}\n\nValor: R$ {lembrete['valor']:.2f}"
                    )

        except Exception as e:
            print(f"Erro ao verificar lembretes: {str(e)}")

    def closeEvent(self, event):
        """Evento chamado quando a janela é fechada"""
        try:
            # Parar o timer de atualização
            if hasattr(self, 'update_timer'):
                self.update_timer.stop()

            # Salvar dados
            self.db.save()

        except Exception as e:
            print(f"Erro ao fechar aplicação: {str(e)}")

        event.accept()

    def filter_transactions(self):
        """Filtra as transações com base nos critérios selecionados"""
        try:
            periodo = self.period_combo.currentText()
            categoria = self.category_combo.currentText()
            tipo = self.type_combo.currentText()

            # Obter data inicial baseada no período selecionado
            hoje = date.today()
            if periodo == "Último mês":
                data_inicial = hoje.replace(day=1)
            elif periodo == "Últimos 3 meses":
                data_inicial = hoje.replace(month=hoje.month-3, day=1)
            elif periodo == "Último ano":
                data_inicial = hoje.replace(year=hoje.year-1, day=1)
            else:  # Personalizado
                # TODO: Implementar seleção de data personalizada
                data_inicial = hoje.replace(day=1)

            # Filtrar transações
            transacoes = self.db.get_transacoes()
            transacoes_filtradas = []

            for transacao in transacoes:
                if (transacao['data'] >= data_inicial and
                    (categoria == "Todas" or transacao['categoria'] == categoria) and
                        (tipo == "Todos" or transacao['tipo'] == tipo)):
                    transacoes_filtradas.append(transacao)

            # Atualizar tabela
            self.transactions_table.setRowCount(len(transacoes_filtradas))

            for i, transacao in enumerate(transacoes_filtradas):
                self.transactions_table.setItem(i, 0, QTableWidgetItem(
                    transacao['data'].strftime('%d/%m/%Y')))
                self.transactions_table.setItem(
                    i, 1, QTableWidgetItem(transacao['descricao']))
                self.transactions_table.setItem(
                    i, 2, QTableWidgetItem(transacao['categoria']))
                self.transactions_table.setItem(
                    i, 3, QTableWidgetItem(transacao['tipo']))
                self.transactions_table.setItem(
                    i, 4, QTableWidgetItem(f"R$ {transacao['valor']:.2f}"))

        except Exception as e:
            print(f"Erro ao filtrar transações: {str(e)}")
            QMessageBox.warning(self, "Erro", "Erro ao filtrar transações!")

    def sort_table(self, table, column):
        """Ordena uma tabela com base na coluna selecionada"""
        try:
            # Obter todos os itens da tabela
            items = []
            for row in range(table.rowCount()):
                item = table.item(row, column)
                if item:
                    items.append((row, item.text()))

            # Ordenar itens
            items.sort(key=lambda x: x[1])

            # Reordenar linhas da tabela
            for i, (row, _) in enumerate(items):
                table.moveRow(row, i)

        except Exception as e:
            print(f"Erro ao ordenar tabela: {str(e)}")

    def setup_table_connections(self):
        """Configura as conexões para ordenação das tabelas"""
        # Transações
        self.transactions_table.horizontalHeader().sectionClicked.connect(
            lambda col: self.sort_table(self.transactions_table, col)
        )

        # Orçamentos
        self.budgets_table.horizontalHeader().sectionClicked.connect(
            lambda col: self.sort_table(self.budgets_table, col)
        )

        # Metas
        self.goals_table.horizontalHeader().sectionClicked.connect(
            lambda col: self.sort_table(self.goals_table, col)
        )

        # Investimentos
        self.investments_table.horizontalHeader().sectionClicked.connect(
            lambda col: self.sort_table(self.investments_table, col)
        )

        # Contas
        self.accounts_table.horizontalHeader().sectionClicked.connect(
            lambda col: self.sort_table(self.accounts_table, col)
        )

        # Cartões
        self.cards_table.horizontalHeader().sectionClicked.connect(
            lambda col: self.sort_table(self.cards_table, col)
        )

    def export_data(self):
        """Exporta os dados para um arquivo CSV"""
        try:
            # Obter diretório para salvar o arquivo
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Exportar Dados",
                "",
                "CSV Files (*.csv)"
            )

            if not file_path:
                return

            # Criar arquivo CSV
            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)

                # Cabeçalho
                writer.writerow(
                    ['Data', 'Descrição', 'Categoria', 'Tipo', 'Valor'])

                # Dados
                for row in range(self.transactions_table.rowCount()):
                    row_data = []
                    for col in range(self.transactions_table.columnCount()):
                        item = self.transactions_table.item(row, col)
                        row_data.append(item.text() if item else '')
                    writer.writerow(row_data)

            QMessageBox.information(
                self, "Sucesso", "Dados exportados com sucesso!")

        except Exception as e:
            print(f"Erro ao exportar dados: {str(e)}")
            QMessageBox.warning(self, "Erro", "Erro ao exportar dados!")

    def generate_report(self):
        """Gera um relatório financeiro"""
        try:
            # Obter período do relatório
            periodo = self.period_combo.currentText()
            hoje = date.today()

            if periodo == "Último mês":
                data_inicial = hoje.replace(day=1)
            elif periodo == "Últimos 3 meses":
                data_inicial = hoje.replace(month=hoje.month-3, day=1)
            elif periodo == "Último ano":
                data_inicial = hoje.replace(year=hoje.year-1, day=1)
            else:  # Personalizado
                # TODO: Implementar seleção de data personalizada
                data_inicial = hoje.replace(day=1)

            # Obter dados
            transacoes = self.db.get_transacoes()
            orcamentos = self.db.get_orcamentos()
            metas = self.db.get_metas()

            # Calcular totais
            total_receitas = sum(t['valor'] for t in transacoes if t['tipo']
                                 == 'Receita' and t['data'] >= data_inicial)
            total_despesas = sum(t['valor'] for t in transacoes if t['tipo']
                                 == 'Despesa' and t['data'] >= data_inicial)
            saldo = total_receitas - total_despesas

            # Criar relatório
            report = f"""
            RELATÓRIO FINANCEIRO
            Período: {data_inicial.strftime('%d/%m/%Y')} a {hoje.strftime('%d/%m/%Y')}
            
            RESUMO
            Total de Receitas: R$ {total_receitas:.2f}
            Total de Despesas: R$ {total_despesas:.2f}
            Saldo: R$ {saldo:.2f}
            
            ORÇAMENTOS
            """

            for orcamento in orcamentos:
                report += f"\n{orcamento['categoria']}: R$ {orcamento['valor']:.2f}"

            report += "\n\nMETAS"
            for meta in metas:
                progresso = (meta['valor_atual'] / meta['valor_meta']) * 100
                report += f"\n{meta['nome']}: R$ {meta['valor_atual']:.2f} / R$ {meta['valor_meta']:.2f} ({progresso:.1f}%)"

            # Salvar relatório
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Salvar Relatório",
                "",
                "Text Files (*.txt)"
            )

            if file_path:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(report)
                QMessageBox.information(
                    self, "Sucesso", "Relatório gerado com sucesso!")

        except Exception as e:
            print(f"Erro ao gerar relatório: {str(e)}")
            QMessageBox.warning(self, "Erro", "Erro ao gerar relatório!")

    def show_settings(self):
        """Mostra a janela de configurações"""
        try:
            dialog = QDialog(self)
            dialog.setWindowTitle("Configurações")
            dialog.setMinimumWidth(400)

            layout = QVBoxLayout()

            # Tema
            theme_group = QGroupBox("Tema")
            theme_layout = QVBoxLayout()

            self.theme_combo = QComboBox()
            self.theme_combo.addItems(["Claro", "Escuro"])
            self.theme_combo.setCurrentText(self.current_theme)
            self.theme_combo.currentTextChanged.connect(self.change_theme)

            theme_layout.addWidget(self.theme_combo)
            theme_group.setLayout(theme_layout)
            layout.addWidget(theme_group)

            # Notificações
            notification_group = QGroupBox("Notificações")
            notification_layout = QVBoxLayout()

            self.notification_check = QCheckBox("Ativar notificações")
            self.notification_check.setChecked(self.notifications_enabled)
            self.notification_check.stateChanged.connect(
                self.toggle_notifications)

            notification_layout.addWidget(self.notification_check)
            notification_group.setLayout(notification_layout)
            layout.addWidget(notification_group)

            # Backup
            backup_group = QGroupBox("Backup")
            backup_layout = QVBoxLayout()

            backup_button = QPushButton("Fazer Backup")
            backup_button.clicked.connect(self.create_backup)

            restore_button = QPushButton("Restaurar Backup")
            restore_button.clicked.connect(self.restore_backup)

            backup_layout.addWidget(backup_button)
            backup_layout.addWidget(restore_button)
            backup_group.setLayout(backup_layout)
            layout.addWidget(backup_group)

            # Botões
            button_layout = QHBoxLayout()

            save_button = QPushButton("Salvar")
            save_button.clicked.connect(dialog.accept)

            cancel_button = QPushButton("Cancelar")
            cancel_button.clicked.connect(dialog.reject)

            button_layout.addWidget(save_button)
            button_layout.addWidget(cancel_button)

            layout.addLayout(button_layout)
            dialog.setLayout(layout)

            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.save_settings()

        except Exception as e:
            print(f"Erro ao mostrar configurações: {str(e)}")
            QMessageBox.warning(self, "Erro", "Erro ao mostrar configurações!")

    def change_theme(self, theme):
        """Altera o tema da aplicação"""
        try:
            if theme == "Claro":
                self.setStyleSheet(GLOBAL_STYLE)
            else:
                self.setStyleSheet(DARK_STYLE)

            self.current_theme = theme

        except Exception as e:
            print(f"Erro ao mudar tema: {str(e)}")

    def toggle_notifications(self, state):
        """Ativa/desativa as notificações"""
        try:
            self.notifications_enabled = state == Qt.CheckState.Checked.value

        except Exception as e:
            print(f"Erro ao alterar notificações: {str(e)}")

    def create_backup(self):
        """Cria um backup dos dados"""
        try:
            # Obter diretório para salvar o backup
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Criar Backup",
                "",
                "Backup Files (*.backup)"
            )

            if not file_path:
                return

            # Criar backup
            backup_data = {
                'transactions': self.db.get_transacoes(),
                'budgets': self.db.get_orcamentos(),
                'goals': self.db.get_metas(),
                'investments': self.db.get_investimentos(),
                'accounts': self.db.get_contas(),
                'cards': self.db.get_cartoes(),
                'reminders': self.db.get_lembretes()
            }

            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(backup_data, file, indent=4, default=str)

            QMessageBox.information(
                self, "Sucesso", "Backup criado com sucesso!")

        except Exception as e:
            print(f"Erro ao criar backup: {str(e)}")
            QMessageBox.warning(self, "Erro", "Erro ao criar backup!")

    def restore_backup(self):
        """Restaura um backup dos dados"""
        try:
            # Obter arquivo de backup
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Restaurar Backup",
                "",
                "Backup Files (*.backup)"
            )

            if not file_path:
                return

            # Confirmar restauração
            reply = QMessageBox.question(
                self,
                "Confirmar Restauração",
                "Tem certeza que deseja restaurar este backup? Todos os dados atuais serão substituídos.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                # Ler backup
                with open(file_path, 'r', encoding='utf-8') as file:
                    backup_data = json.load(file)

                # Restaurar dados
                self.db.restore_backup(backup_data)

                # Atualizar interface
                self.update_all()

                QMessageBox.information(
                    self, "Sucesso", "Backup restaurado com sucesso!")

        except Exception as e:
            print(f"Erro ao restaurar backup: {str(e)}")
            QMessageBox.warning(self, "Erro", "Erro ao restaurar backup!")

    def save_settings(self):
        """Salva as configurações do usuário"""
        try:
            settings = {
                'theme': self.current_theme,
                'notifications_enabled': self.notifications_enabled
            }

            with open('settings.json', 'w', encoding='utf-8') as file:
                json.dump(settings, file, indent=4)

        except Exception as e:
            print(f"Erro ao salvar configurações: {str(e)}")

    def load_settings(self):
        """Carrega as configurações do usuário"""
        try:
            if os.path.exists('settings.json'):
                with open('settings.json', 'r', encoding='utf-8') as file:
                    settings = json.load(file)

                self.current_theme = settings.get('theme', 'Claro')
                self.notifications_enabled = settings.get(
                    'notifications_enabled', True)

            else:
                self.current_theme = 'Claro'
                self.notifications_enabled = True

        except Exception as e:
            print(f"Erro ao carregar configurações: {str(e)}")
            self.current_theme = 'Claro'
            self.notifications_enabled = True

    def show_about(self):
        """Mostra a janela Sobre"""
        try:
            QMessageBox.about(
                self,
                "Sobre",
                "Fin-Assist v1.0\n\n"
                "Um assistente virtual para gestão financeira pessoal.\n\n"
                "Desenvolvido com ❤️ usando Python e PyQt6."
            )
        except Exception as e:
            print(f"Erro ao mostrar janela Sobre: {str(e)}")

    def show_add_account_dialog(self):
        """Mostra o diálogo para adicionar uma nova conta"""
        try:
            dialog = QDialog(self)
            dialog.setWindowTitle("Adicionar Conta")
            dialog.setMinimumWidth(400)

            layout = QVBoxLayout()

            # Campos
            name_label = QLabel("Nome:")
            name_edit = QLineEdit()

            type_label = QLabel("Tipo:")
            type_combo = QComboBox()
            type_combo.addItems([
                "Conta Corrente",
                "Conta Poupança",
                "Conta Salário",
                "Outros"
            ])

            bank_label = QLabel("Banco:")
            bank_edit = QLineEdit()

            balance_label = QLabel("Saldo Inicial:")
            balance_edit = QLineEdit()

            # Adicionar campos ao layout
            layout.addWidget(name_label)
            layout.addWidget(name_edit)
            layout.addWidget(type_label)
            layout.addWidget(type_combo)
            layout.addWidget(bank_label)
            layout.addWidget(bank_edit)
            layout.addWidget(balance_label)
            layout.addWidget(balance_edit)

            # Botões
            button_layout = QHBoxLayout()

            save_button = QPushButton("Salvar")
            save_button.clicked.connect(lambda: self.handle_save_account(
                dialog,
                name_edit.text(),
                type_combo.currentText(),
                bank_edit.text(),
                balance_edit.text()
            ))

            cancel_button = QPushButton("Cancelar")
            cancel_button.clicked.connect(dialog.reject)

            button_layout.addWidget(save_button)
            button_layout.addWidget(cancel_button)

            layout.addLayout(button_layout)
            dialog.setLayout(layout)

            dialog.exec()

        except Exception as e:
            print(f"Erro ao mostrar diálogo de conta: {str(e)}")
            QMessageBox.warning(
                self, "Erro", "Erro ao mostrar diálogo de conta!")

    def handle_save_account(self, dialog, name, type, bank, balance):
        """Salva uma nova conta"""
        try:
            if not name or not bank:
                QMessageBox.warning(
                    self, "Erro", "Preencha todos os campos obrigatórios!")
                return

            try:
                balance = float(balance) if balance else 0.0
            except ValueError:
                QMessageBox.warning(self, "Erro", "Saldo inválido!")
                return

            if self.db.add_account(name, type, bank, balance):
                self.update_accounts_table()
                dialog.accept()
                QMessageBox.information(
                    self, "Sucesso", "Conta adicionada com sucesso!")
            else:
                QMessageBox.warning(self, "Erro", "Erro ao adicionar conta!")

        except Exception as e:
            print(f"Erro ao salvar conta: {str(e)}")
            QMessageBox.warning(self, "Erro", "Erro ao salvar conta!")

    def update_accounts_table(self):
        """Atualiza a tabela de contas"""
        try:
            self.accounts_table.setRowCount(0)
            accounts = self.db.get_accounts()

            for account in accounts:
                row = self.accounts_table.rowCount()
                self.accounts_table.insertRow(row)

                self.accounts_table.setItem(
                    row, 0, QTableWidgetItem(account['nome']))
                self.accounts_table.setItem(
                    row, 1, QTableWidgetItem(account['tipo']))
                self.accounts_table.setItem(
                    row, 2, QTableWidgetItem(account['banco']))
                self.accounts_table.setItem(
                    row, 3, QTableWidgetItem(f"R$ {account['saldo']:.2f}"))

        except Exception as e:
            print(f"Erro ao atualizar tabela de contas: {str(e)}")
            QMessageBox.warning(
                self, "Erro", "Erro ao atualizar tabela de contas!")

    def edit_account(self, account_id):
        """Edita uma conta existente"""
        try:
            account = self.db.get_account(account_id)
            if not account:
                return

            dialog = QDialog(self)
            dialog.setWindowTitle("Editar Conta")
            dialog.setMinimumWidth(400)

            layout = QVBoxLayout()

            # Campos
            name_label = QLabel("Nome:")
            name_edit = QLineEdit(account['nome'])

            type_label = QLabel("Tipo:")
            type_combo = QComboBox()
            type_combo.addItems([
                "Conta Corrente",
                "Conta Poupança",
                "Conta Investimento",
                "Carteira",
                "Outros"
            ])
            type_combo.setCurrentText(account['tipo'])

            bank_label = QLabel("Banco:")
            bank_edit = QLineEdit(account['banco'])

            balance_label = QLabel("Saldo:")
            balance_edit = QLineEdit(str(account['saldo']))

            # Adicionar campos ao layout
            layout.addWidget(name_label)
            layout.addWidget(name_edit)
            layout.addWidget(type_label)
            layout.addWidget(type_combo)
            layout.addWidget(bank_label)
            layout.addWidget(bank_edit)
            layout.addWidget(balance_label)
            layout.addWidget(balance_edit)

            # Botões
            button_layout = QHBoxLayout()

            save_button = QPushButton("Salvar")
            save_button.clicked.connect(lambda: self.handle_save_account_edit(
                dialog,
                account_id,
                name_edit.text(),
                type_combo.currentText(),
                bank_edit.text(),
                balance_edit.text()
            ))

            cancel_button = QPushButton("Cancelar")
            cancel_button.clicked.connect(dialog.reject)

            button_layout.addWidget(save_button)
            button_layout.addWidget(cancel_button)

            layout.addLayout(button_layout)
            dialog.setLayout(layout)

            dialog.exec()

        except Exception as e:
            print(f"Erro ao editar conta: {str(e)}")
            QMessageBox.warning(self, "Erro", "Erro ao editar conta!")

    def handle_save_account_edit(self, dialog, account_id, name, type, bank, balance):
        """Salva as alterações de uma conta"""
        try:
            if not name or not bank:
                QMessageBox.warning(
                    self, "Erro", "Preencha todos os campos obrigatórios!")
                return

            try:
                balance = float(balance) if balance else 0.0
            except ValueError:
                QMessageBox.warning(self, "Erro", "Saldo inválido!")
                return

            if self.db.update_account(account_id, name, type, bank, balance):
                self.update_accounts_table()
                dialog.accept()
                QMessageBox.information(
                    self, "Sucesso", "Conta atualizada com sucesso!")
            else:
                QMessageBox.warning(self, "Erro", "Erro ao atualizar conta!")

        except Exception as e:
            print(f"Erro ao salvar edição da conta: {str(e)}")
            QMessageBox.warning(
                self, "Erro", "Erro ao salvar edição da conta!")

    def delete_account(self, account_id):
        """Exclui uma conta"""
        try:
            reply = QMessageBox.question(
                self,
                "Confirmar Exclusão",
                "Tem certeza que deseja excluir esta conta?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                if self.db.delete_account(account_id):
                    self.update_accounts_table()
                    QMessageBox.information(
                        self, "Sucesso", "Conta excluída com sucesso!")
                else:
                    QMessageBox.warning(self, "Erro", "Erro ao excluir conta!")

        except Exception as e:
            print(f"Erro ao excluir conta: {str(e)}")
            QMessageBox.warning(self, "Erro", "Erro ao excluir conta!")

    def edit_card(self, card_id):
        """Edita um cartão existente"""
        try:
            card = self.db.get_card(card_id)
            if not card:
                return

            dialog = QDialog(self)
            dialog.setWindowTitle("Editar Cartão")
            dialog.setMinimumWidth(400)

            layout = QVBoxLayout()

            # Campos
            name_label = QLabel("Nome:")
            name_edit = QLineEdit(card['nome'])

            type_label = QLabel("Tipo:")
            type_combo = QComboBox()
            type_combo.addItems([
                "Débito",
                "Crédito",
                "Débito/Crédito",
                "Outros"
            ])
            type_combo.setCurrentText(card['tipo'])

            bank_label = QLabel("Banco:")
            bank_edit = QLineEdit(card['banco'])

            limit_label = QLabel("Limite:")
            limit_edit = QLineEdit(str(card['limite']))

            closing_day_label = QLabel("Dia de Fechamento:")
            closing_day_edit = QSpinBox()
            closing_day_edit.setRange(1, 31)
            closing_day_edit.setValue(card['dia_fechamento'])

            due_day_label = QLabel("Dia de Vencimento:")
            due_day_edit = QSpinBox()
            due_day_edit.setRange(1, 31)
            due_day_edit.setValue(card['dia_vencimento'])

            # Adicionar campos ao layout
            layout.addWidget(name_label)
            layout.addWidget(name_edit)
            layout.addWidget(type_label)
            layout.addWidget(type_combo)
            layout.addWidget(bank_label)
            layout.addWidget(bank_edit)
            layout.addWidget(limit_label)
            layout.addWidget(limit_edit)
            layout.addWidget(closing_day_label)
            layout.addWidget(closing_day_edit)
            layout.addWidget(due_day_label)
            layout.addWidget(due_day_edit)

            # Botões
            button_layout = QHBoxLayout()

            save_button = QPushButton("Salvar")
            save_button.clicked.connect(lambda: self.handle_save_card_edit(
                dialog,
                card_id,
                name_edit.text(),
                type_combo.currentText(),
                bank_edit.text(),
                limit_edit.text(),
                closing_day_edit.value(),
                due_day_edit.value()
            ))

            cancel_button = QPushButton("Cancelar")
            cancel_button.clicked.connect(dialog.reject)

            button_layout.addWidget(save_button)
            button_layout.addWidget(cancel_button)

            layout.addLayout(button_layout)
            dialog.setLayout(layout)

            dialog.exec()

        except Exception as e:
            print(f"Erro ao editar cartão: {str(e)}")
            QMessageBox.warning(self, "Erro", "Erro ao editar cartão!")

    def handle_save_card_edit(self, dialog, card_id, name, type, bank, limit, closing_day, due_day):
        """Salva as alterações de um cartão"""
        try:
            if not name or not bank:
                QMessageBox.warning(
                    self, "Erro", "Preencha todos os campos obrigatórios!")
                return

            try:
                limit = float(limit) if limit else 0.0
            except ValueError:
                QMessageBox.warning(self, "Erro", "Limite inválido!")
                return

            if self.db.update_card(card_id, name, type, bank, limit, closing_day, due_day):
                self.update_cards_table()
                dialog.accept()
                QMessageBox.information(
                    self, "Sucesso", "Cartão atualizado com sucesso!")
            else:
                QMessageBox.warning(self, "Erro", "Erro ao atualizar cartão!")

        except Exception as e:
            print(f"Erro ao salvar edição do cartão: {str(e)}")
            QMessageBox.warning(
                self, "Erro", "Erro ao salvar edição do cartão!")

    def delete_card(self, card_id):
        """Exclui um cartão"""
        try:
            reply = QMessageBox.question(
                self,
                "Confirmar Exclusão",
                "Tem certeza que deseja excluir este cartão?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                if self.db.delete_card(card_id):
                    self.update_cards_table()
                    QMessageBox.information(
                        self, "Sucesso", "Cartão excluído com sucesso!")
                else:
                    QMessageBox.warning(
                        self, "Erro", "Erro ao excluir cartão!")

        except Exception as e:
            print(f"Erro ao excluir cartão: {str(e)}")
            QMessageBox.warning(self, "Erro", "Erro ao excluir cartão!")

    def show_add_card_dialog(self):
        """Mostra o diálogo para adicionar um novo cartão"""
        try:
            dialog = QDialog(self)
            dialog.setWindowTitle("Adicionar Cartão")
            dialog.setMinimumWidth(400)

            layout = QVBoxLayout()

            # Campos
            name_label = QLabel("Nome:")
            name_edit = QLineEdit()

            type_label = QLabel("Tipo:")
            type_combo = QComboBox()
            type_combo.addItems([
                "Débito",
                "Crédito",
                "Débito/Crédito",
                "Outros"
            ])

            bank_label = QLabel("Banco:")
            bank_edit = QLineEdit()

            limit_label = QLabel("Limite:")
            limit_edit = QLineEdit()

            closing_day_label = QLabel("Dia de Fechamento:")
            closing_day_edit = QSpinBox()
            closing_day_edit.setRange(1, 31)

            due_day_label = QLabel("Dia de Vencimento:")
            due_day_edit = QSpinBox()
            due_day_edit.setRange(1, 31)

            # Adicionar campos ao layout
            layout.addWidget(name_label)
            layout.addWidget(name_edit)
            layout.addWidget(type_label)
            layout.addWidget(type_combo)
            layout.addWidget(bank_label)
            layout.addWidget(bank_edit)
            layout.addWidget(limit_label)
            layout.addWidget(limit_edit)
            layout.addWidget(closing_day_label)
            layout.addWidget(closing_day_edit)
            layout.addWidget(due_day_label)
            layout.addWidget(due_day_edit)

            # Botões
            button_layout = QHBoxLayout()

            save_button = QPushButton("Salvar")
            save_button.clicked.connect(lambda: self.handle_save_card(
                dialog,
                name_edit.text(),
                type_combo.currentText(),
                bank_edit.text(),
                limit_edit.text(),
                closing_day_edit.value(),
                due_day_edit.value()
            ))

            cancel_button = QPushButton("Cancelar")
            cancel_button.clicked.connect(dialog.reject)

            button_layout.addWidget(save_button)
            button_layout.addWidget(cancel_button)

            layout.addLayout(button_layout)
            dialog.setLayout(layout)

            dialog.exec()

        except Exception as e:
            print(f"Erro ao mostrar diálogo de cartão: {str(e)}")
            QMessageBox.warning(
                self, "Erro", "Erro ao mostrar diálogo de cartão!")

    def handle_save_card(self, dialog, name, type, bank, limit, closing_day, due_day):
        """Salva um novo cartão"""
        try:
            if not name or not bank:
                QMessageBox.warning(
                    self, "Erro", "Preencha todos os campos obrigatórios!")
                return

            try:
                limit = float(limit) if limit else 0.0
            except ValueError:
                QMessageBox.warning(self, "Erro", "Limite inválido!")
                return

            if self.db.add_card(name, type, bank, limit, closing_day, due_day):
                self.update_cards_table()
                dialog.accept()
                QMessageBox.information(
                    self, "Sucesso", "Cartão adicionado com sucesso!")
            else:
                QMessageBox.warning(self, "Erro", "Erro ao adicionar cartão!")

        except Exception as e:
            print(f"Erro ao salvar cartão: {str(e)}")
            QMessageBox.warning(self, "Erro", "Erro ao salvar cartão!")


def main():
    app = QApplication(sys.argv)

    # Verificar se o banco de dados está inicializado
    db = DatabaseManager()
    db.init_database()

    # Mostrar janela de login
    login_window = LoginWindow()
    if login_window.exec():
        main_window = MainWindow()
        main_window.show()
        sys.exit(app.exec())
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
