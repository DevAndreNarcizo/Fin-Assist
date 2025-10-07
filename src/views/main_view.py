import customtkinter as ctk
from src.controllers.transaction_controller import TransactionController
from src.controllers.goal_controller import GoalController
from src.controllers.chatbot_controller import ChatbotController
from datetime import datetime

from src.utils.message_utils import MessageUtils

# Funções utilitárias para conversão de tipo
TIPO_PT_EN = {
    "receita": "income",
    "despesa": "expense",
    "investimento": "investment"
}
TIPO_EN_PT = {v: k.capitalize() for k, v in TIPO_PT_EN.items()}

def tipo_para_en(tipo):
    return TIPO_PT_EN.get(tipo.lower(), tipo)

def tipo_para_pt(tipo):
    return TIPO_EN_PT.get(tipo, tipo.capitalize())

class MainView(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master)
        self.master = master
        self.user = user
        self.closed = False  # Flag para indicar se a janela foi fechada
        self.transaction_controller = TransactionController(user)
        self.goal_controller = GoalController(user)
        self.chatbot_controller = ChatbotController(user, self.transaction_controller, self.goal_controller)
        
        self.setup_ui()
    
    def setup_ui(self):
        # Configuração do frame principal
        self.configure(fg_color="#1a1a1a")
        
        # Barra lateral
        self.sidebar = ctk.CTkFrame(self, width=200, fg_color="#2b2b2b")
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)
        
        # Botões da barra lateral
        self.create_sidebar_buttons()
        
        # Área principal
        self.main_area = ctk.CTkFrame(self, fg_color="#2b2b2b")
        self.main_area.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Exibe o dashboard inicialmente
        self.show_dashboard()
    
    def create_sidebar_buttons(self):
        # Logo
        logo_label = ctk.CTkLabel(
            self.sidebar,
            text="Fin-Assist",
            font=("Roboto", 20, "bold"),
            text_color="#ffffff"
        )
        logo_label.pack(pady=20)
        
        # Botões
        buttons = [
            ("Dashboard", self.show_dashboard),
            ("Transações", self.show_transactions),
            ("Metas", self.show_goals),
            ("Relatórios", self.show_reports),
            ("Chatbot", self.show_chatbot),
            ("Sair", self.logout)
        ]
        
        for text, command in buttons:
            button = ctk.CTkButton(
                self.sidebar,
                text=text,
                width=180,
                height=40,
                font=("Roboto", 14),
                command=command
            )
            button.pack(pady=5)
    
    def show_dashboard(self):
        self.clear_main_area()
        
        # Título
        title_label = ctk.CTkLabel(
            self.main_area,
            text="Dashboard",
            font=("Roboto", 24, "bold"),
            text_color="#ffffff"
        )
        title_label.pack(pady=20)
        
        # Cards de resumo
        self.create_summary_cards()
        
        # Gráficos
        self.create_charts()
    
    def show_transactions(self):
        self.clear_main_area()
        
        # Título
        title_label = ctk.CTkLabel(
            self.main_area,
            text="Transações",
            font=("Roboto", 24, "bold"),
            text_color="#ffffff"
        )
        title_label.pack(pady=20)
        
        # Categorias por tipo
        self.categorias_receita = [
            "Salário", "Freelance", "Rendimentos", "Prêmios", "Reembolso", "Outros"
        ]
        self.categorias_despesa = [
            "Alimentação", "Transporte", "Moradia", "Educação", "Lazer", "Saúde", "Compras", "Contas", "Viagem", "Impostos", "Doações", "Outros"
        ]
        self.categorias_investimento = [
            "Ações", "Fundos Imobiliários", "Tesouro Direto", "CDB", "Criptomoedas", "Poupança", "Outros"
        ]

        # Frame principal da tela de transações
        trans_frame = ctk.CTkFrame(self.main_area, fg_color="#232323")
        trans_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # --- Formulário de nova transação centralizado ---
        form_center = ctk.CTkFrame(trans_frame, fg_color="transparent")
        form_center.pack(pady=10, fill="x")
        form_center.grid_columnconfigure((0,1,2,3,4,5,6,7), weight=1)

        ctk.CTkLabel(form_center, text="Adicionar Transação", font=("Roboto", 16, "bold"), text_color="#fff").grid(row=0, column=0, columnspan=8, pady=(0, 10), sticky="n")

        # Tipo
        ctk.CTkLabel(form_center, text="Tipo:", font=("Roboto", 12), text_color="#fff").grid(row=1, column=0, sticky="e")
        self.tipo_var = ctk.StringVar(value="receita")
        tipo_combo = ctk.CTkComboBox(form_center, values=["receita", "despesa", "investimento"], variable=self.tipo_var, width=120, command=self.update_categoria_options)
        tipo_combo.grid(row=1, column=1, padx=5, sticky="w")

        # Categoria
        categoria_frame = ctk.CTkFrame(form_center, fg_color="transparent")
        categoria_frame.grid(row=1, column=2, columnspan=2, padx=5, sticky="w")
        
        ctk.CTkLabel(categoria_frame, text="Categoria:", font=("Roboto", 12), text_color="#fff").pack(side="left")
        self.categoria_var = ctk.StringVar()
        self.categoria_combo = ctk.CTkComboBox(categoria_frame, values=self.categorias_receita, variable=self.categoria_var, width=100)
        self.categoria_combo.pack(side="left", padx=(10, 5))
        
        # Botão para adicionar categoria personalizada
        add_cat_btn = ctk.CTkButton(categoria_frame, text="+", command=self.add_custom_category, width=30, height=30)
        add_cat_btn.pack(side="left", padx=5)

        # Subcategoria
        ctk.CTkLabel(form_center, text="Subcategoria:", font=("Roboto", 12), text_color="#fff").grid(row=1, column=4, sticky="e")
        self.subcategoria_entry = ctk.CTkEntry(form_center, width=120)
        self.subcategoria_entry.grid(row=1, column=5, padx=5, sticky="w")

        # Valor
        ctk.CTkLabel(form_center, text="Valor:", font=("Roboto", 12), text_color="#fff").grid(row=1, column=6, sticky="e")
        self.valor_entry = ctk.CTkEntry(form_center, width=100)
        self.valor_entry.grid(row=1, column=7, padx=5, sticky="w")

        # Descrição
        ctk.CTkLabel(form_center, text="Descrição:", font=("Roboto", 12), text_color="#fff").grid(row=2, column=0, sticky="e")
        self.desc_entry = ctk.CTkEntry(form_center, width=300)
        self.desc_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="we")

        # Data
        ctk.CTkLabel(form_center, text="Data (DD-MM-YYYY):", font=("Roboto", 12), text_color="#fff").grid(row=2, column=4, sticky="e")
        self.data_entry = ctk.CTkEntry(form_center, width=100)
        self.data_entry.insert(0, datetime.now().strftime('%d-%m-%Y'))
        self.data_entry.grid(row=2, column=5, padx=5, pady=5, sticky="w")

        # Botão de adicionar
        add_btn = ctk.CTkButton(form_center, text="Adicionar", command=self.add_transaction, width=120)
        add_btn.grid(row=2, column=6, columnspan=2, pady=10, sticky="we")

        # --- Filtros ---
        filtros_frame = ctk.CTkFrame(trans_frame, fg_color="#232323")
        filtros_frame.pack(padx=10, pady=5, fill="x")
        filtros_frame.grid_columnconfigure((0,1,2,3,4,5,6), weight=1)
        ctk.CTkLabel(filtros_frame, text="Filtros:", font=("Roboto", 12, "bold"), text_color="#fff").grid(row=0, column=0, padx=5, sticky="e")
        self.filtro_tipo_var = ctk.StringVar(value="todos")
        filtro_tipo_combo = ctk.CTkComboBox(filtros_frame, values=["todos", "receita", "despesa", "investimento"], variable=self.filtro_tipo_var, width=120)
        filtro_tipo_combo.grid(row=0, column=1, padx=5, sticky="w")
        ctk.CTkLabel(filtros_frame, text="De (DD-MM-YYYY):", font=("Roboto", 12), text_color="#fff").grid(row=0, column=2, padx=5, sticky="e")
        self.filtro_data_ini = ctk.CTkEntry(filtros_frame, width=100)
        self.filtro_data_ini.grid(row=0, column=3, padx=5, sticky="w")
        ctk.CTkLabel(filtros_frame, text="Até (DD-MM-YYYY):", font=("Roboto", 12), text_color="#fff").grid(row=0, column=4, padx=5, sticky="e")
        self.filtro_data_fim = ctk.CTkEntry(filtros_frame, width=100)
        self.filtro_data_fim.grid(row=0, column=5, padx=5, sticky="w")
        filtro_btn = ctk.CTkButton(filtros_frame, text="Filtrar", command=self.update_transaction_list, width=100)
        filtro_btn.grid(row=0, column=6, padx=10, sticky="we")
        
        # --- Lista de transações ---
        self.trans_list_frame = ctk.CTkFrame(trans_frame, fg_color="#232323")
        self.trans_list_frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.update_transaction_list()
    
    def show_goals(self):
        self.clear_main_area()
        
        # Título
        title_label = ctk.CTkLabel(
            self.main_area,
            text="Metas Financeiras",
            font=("Roboto", 24, "bold"),
            text_color="#ffffff"
        )
        title_label.pack(pady=20)
        
        # Formulário de nova meta
        self.create_goal_form()
        
        # Lista de metas
        self.create_goal_list()
    
    def show_reports(self):
        self.clear_main_area()
        
        # Título
        title_label = ctk.CTkLabel(
            self.main_area,
            text="Relatórios",
            font=("Roboto", 24, "bold"),
            text_color="#ffffff"
        )
        title_label.pack(pady=20)
        
        # Opções de relatório
        self.create_report_options()
    
    def show_chatbot(self):
        self.clear_main_area()
        
        # Título
        title_label = ctk.CTkLabel(
            self.main_area,
            text="Assistente Financeiro",
            font=("Roboto", 24, "bold"),
            text_color="#ffffff"
        )
        title_label.pack(pady=20)
        
        # Área de chat
        self.create_chat_area()
    
    def is_number(self, val):
        try:
            float(val)
            return True
        except Exception:
            return False

    def create_summary_cards(self):
        # Limpa área de cards se já existir
        if hasattr(self, 'cards_frame'):
            self.cards_frame.destroy()
        self.cards_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.cards_frame.pack(pady=10, padx=10, fill="x")

        # Obtém dados
        saldo = self.transaction_controller.get_balance()
        transacoes = self.transaction_controller.get_transactions()
        receitas = sum(float(t[5]) for t in transacoes if tipo_para_en(t[2]) == 'income' and self.is_number(t[5]))
        despesas = sum(float(t[5]) for t in transacoes if tipo_para_en(t[2]) == 'expense' and self.is_number(t[5]))
        investimentos = sum(float(t[5]) for t in transacoes if tipo_para_en(t[2]) == 'investment' and self.is_number(t[5]))

        # Cores
        cores = {
            'saldo': '#1976D2',        # Azul
            'receitas': '#43A047',     # Verde
            'despesas': '#E53935',     # Vermelho
            'investimentos': '#FBC02D' # Amarelo
        }

        # Cards
        card_data = [
            ("Saldo Total", f"R$ {saldo:.2f}", cores['saldo']),
            ("Receitas", f"R$ {receitas:.2f}", cores['receitas']),
            ("Despesas", f"R$ {despesas:.2f}", cores['despesas']),
            ("Investido", f"R$ {investimentos:.2f}", cores['investimentos'])
        ]

        # Frame para centralizar os cards
        cards_center = ctk.CTkFrame(self.cards_frame, fg_color="transparent")
        cards_center.pack(anchor="center")

        card_width = int(200 * 1.9 * 1.35 * 0.8 * 0.9)
        card_height = int(100 * 1.9 * 1.35 * 0.8 * 0.9)

        for i, (titulo, valor, cor) in enumerate(card_data):
            card = ctk.CTkFrame(cards_center, fg_color=cor, corner_radius=18, width=card_width, height=card_height)
            card.grid(row=0, column=i, padx=28, pady=5)
            card.grid_propagate(False)
            # Frame interno para centralizar o texto
            inner_frame = ctk.CTkFrame(card, fg_color="transparent", width=card_width, height=card_height)
            inner_frame.pack(expand=True, fill="both")
            inner_frame.pack_propagate(False)
            # Centraliza os labels no centro do quadrado
            label_titulo = ctk.CTkLabel(inner_frame, text=titulo, font=("Roboto", 18, "bold"), text_color="#fff")
            label_titulo.pack(expand=True, anchor="center")
            label_valor = ctk.CTkLabel(inner_frame, text=valor, font=("Roboto", 28, "bold"), text_color="#fff")
            label_valor.pack(expand=True, anchor="center")

        # Tabela de metas
        if hasattr(self, 'goals_frame'):
            self.goals_frame.destroy()
        self.goals_frame = ctk.CTkFrame(self.main_area, fg_color="#232323", height=int(120*1.25))
        self.goals_frame.pack(pady=20, padx=10, fill="x")
        self.goals_frame.pack_propagate(False)
        metas = self.goal_controller.get_goals()
        ctk.CTkLabel(self.goals_frame, text="Progresso das Metas", font=("Roboto", 16, "bold"), text_color="#fff").pack(anchor="w", padx=10, pady=(10, 0))
        if metas:
            table_frame = ctk.CTkFrame(self.goals_frame, fg_color="transparent")
            table_frame.pack(fill="x", padx=10, pady=10)
            headers = ["Meta", "Valor Alvo", "Valor Atual", "% Progresso", "Status"]
            for j, h in enumerate(headers):
                ctk.CTkLabel(table_frame, text=h, font=("Roboto", 12, "bold"), text_color="#90caf9").grid(row=0, column=j, padx=8, pady=2)
            for i, meta in enumerate(metas):
                progresso = (float(meta[4])/float(meta[3])*100) if (meta[3] or 0) > 0 else 0
                row = [meta[2], f'R$ {float(meta[3]):.2f}', f'R$ {float(meta[4]):.2f}', f'{progresso:.1f}%', meta[6]]
                for j, val in enumerate(row):
                    ctk.CTkLabel(table_frame, text=val, font=("Roboto", 12), text_color="#fff").grid(row=i+1, column=j, padx=8, pady=2)
        else:
            ctk.CTkLabel(self.goals_frame, text="Nenhuma meta cadastrada.", font=("Roboto", 12), text_color="#bbb").pack(pady=10)

    def create_charts(self):
        # Limpa área de gráficos se já existir
        if hasattr(self, 'chart_frame'):
            self.chart_frame.destroy()
        self.chart_frame = ctk.CTkFrame(self.main_area, fg_color="#232323")
        self.chart_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Usa o ChartGenerator para criar os gráficos
        from src.utils.chart_generator import ChartGenerator
        transacoes = self.transaction_controller.get_transactions()
        chart_gen = ChartGenerator()
        chart_gen.create_monthly_charts(transacoes, self.chart_frame)
    
    def create_transaction_form(self):
        # TODO: Implementar formulário de transação
        pass
    
    def update_transaction_list(self):
        for widget in self.trans_list_frame.winfo_children():
            widget.destroy()

        # Filtros
        tipo = self.filtro_tipo_var.get()
        tipo_en = tipo_para_en(tipo) if tipo != "todos" else None
        
        # Converte datas DD-MM-YYYY para YYYY-MM-DD para o BD
        data_ini = None
        data_fim = None
        try:
            if self.filtro_data_ini.get():
                data_ini = datetime.strptime(self.filtro_data_ini.get(), '%d-%m-%Y').strftime('%Y-%m-%d')
            if self.filtro_data_fim.get():
                data_fim = datetime.strptime(self.filtro_data_fim.get(), '%d-%m-%Y').strftime('%Y-%m-%d')
        except ValueError:
            self.show_trans_error("Formato de data inválido nos filtros! Use DD-MM-YYYY.")
            return
            
        transacoes = self.transaction_controller.get_transactions(
            start_date=data_ini,
            end_date=data_fim,
            type=tipo_en
        )

        # Cabeçalho da tabela estilo Excel
        headers = ["Data", "Tipo", "Categoria", "Subcategoria", "Valor", "Descrição", "Editar", "Excluir"]
        for j, h in enumerate(headers):
            header = ctk.CTkLabel(self.trans_list_frame, text=h, font=("Roboto", 12, "bold"), text_color="#90caf9", fg_color="#1a1a1a", width=14)
            header.grid(row=0, column=j, padx=1, pady=1, sticky="nsew")
            self.trans_list_frame.grid_columnconfigure(j, weight=1)

        if not transacoes:
            ctk.CTkLabel(self.trans_list_frame, text="Nenhuma transação encontrada.", font=("Roboto", 12), text_color="#bbb").grid(row=1, column=0, columnspan=8, pady=10, sticky="nsew")
            return

        for i, t in enumerate(transacoes):
            bg = "#232323" if i % 2 == 0 else "#1a1a1a"
            # Converte data para DD-MM-YYYY para exibição
            try:
                data_display = datetime.strptime(t[7][:10], '%Y-%m-%d').strftime('%d-%m-%Y')
            except:
                data_display = t[7][:10]
            ctk.CTkLabel(self.trans_list_frame, text=data_display, font=("Roboto", 12), text_color="#fff", fg_color=bg).grid(row=i+1, column=0, padx=1, pady=1, sticky="nsew")  # Data
            ctk.CTkLabel(self.trans_list_frame, text=tipo_para_pt(t[2]), font=("Roboto", 12), text_color="#fff", fg_color=bg).grid(row=i+1, column=1, padx=1, pady=1, sticky="nsew")  # Tipo
            ctk.CTkLabel(self.trans_list_frame, text=t[3], font=("Roboto", 12), text_color="#fff", fg_color=bg).grid(row=i+1, column=2, padx=1, pady=1, sticky="nsew")  # Categoria
            ctk.CTkLabel(self.trans_list_frame, text=t[4], font=("Roboto", 12), text_color="#fff", fg_color=bg).grid(row=i+1, column=3, padx=1, pady=1, sticky="nsew")  # Subcategoria
            ctk.CTkLabel(self.trans_list_frame, text=f'R$ {t[5]:.2f}', font=("Roboto", 12), text_color="#fff", fg_color=bg).grid(row=i+1, column=4, padx=1, pady=1, sticky="nsew")  # Valor
            ctk.CTkLabel(self.trans_list_frame, text=t[6] or "", font=("Roboto", 12), text_color="#fff", fg_color=bg).grid(row=i+1, column=5, padx=1, pady=1, sticky="nsew")  # Descrição
            edit_btn = ctk.CTkButton(self.trans_list_frame, text="Editar", width=60, command=lambda tid=t[0]: self.edit_transaction(tid))
            edit_btn.grid(row=i+1, column=6, padx=1, pady=1, sticky="nsew")
            del_btn = ctk.CTkButton(self.trans_list_frame, text="Excluir", width=60, fg_color="#E53935", hover_color="#b71c1c", command=lambda tid=t[0]: self.delete_transaction(tid))
            del_btn.grid(row=i+1, column=7, padx=1, pady=1, sticky="nsew")

    def create_goal_form(self):
        # Formulário para adicionar metas
        form_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        form_frame.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(form_frame, text="Adicionar Meta", font=("Roboto", 16, "bold"), text_color="#fff").pack(anchor="w", pady=(0, 10))

        # Campos do formulário
        ctk.CTkLabel(form_frame, text="Nome da Meta:", font=("Roboto", 12), text_color="#fff").pack(anchor="w")
        self.meta_nome_entry = ctk.CTkEntry(form_frame, width=300)
        self.meta_nome_entry.pack(anchor="w", pady=5)

        ctk.CTkLabel(form_frame, text="Valor Alvo:", font=("Roboto", 12), text_color="#fff").pack(anchor="w")
        self.meta_valor_entry = ctk.CTkEntry(form_frame, width=300)
        self.meta_valor_entry.pack(anchor="w", pady=5)

        ctk.CTkLabel(form_frame, text="Prazo (DD-MM-YYYY):", font=("Roboto", 12), text_color="#fff").pack(anchor="w")
        self.meta_deadline_entry = ctk.CTkEntry(form_frame, width=300)
        self.meta_deadline_entry.pack(anchor="w", pady=5)

        ctk.CTkButton(form_frame, text="Adicionar Meta", command=self.add_goal, width=150).pack(anchor="w", pady=10)

    def create_goal_list(self):
        # Cria um frame separado para a lista de metas
        metas_frame = ctk.CTkFrame(self.main_area, fg_color="#232323")
        metas_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Cabeçalho da tabela
        headers = ["Meta", "Valor Alvo", "Valor Atual", "Prazo", "Progresso", "Editar", "Excluir"]
        for j, h in enumerate(headers):
            header = ctk.CTkLabel(metas_frame, text=h, font=("Roboto", 12, "bold"), text_color="#90caf9", fg_color="#1a1a1a", width=14)
            header.grid(row=0, column=j, padx=1, pady=1, sticky="nsew")
            metas_frame.grid_columnconfigure(j, weight=1)

        # Obtém as metas do controlador
        metas = self.goal_controller.get_goals()

        if not metas:
            ctk.CTkLabel(metas_frame, text="Nenhuma meta cadastrada.", font=("Roboto", 12), text_color="#bbb").grid(row=1, column=0, columnspan=len(headers), pady=10, sticky="nsew")
            return

        for i, meta in enumerate(metas):
            bg = "#232323" if i % 2 == 0 else "#1a1a1a"
            title = meta[2]
            valor_alvo = float(meta[3]) if meta[3] is not None else 0.0
            valor_atual = float(meta[4]) if meta[4] is not None else 0.0
            # Exibir prazo no formato DD-MM-YYYY
            try:
                from datetime import datetime as _dt
                deadline = _dt.strptime(meta[5], '%Y-%m-%d').strftime('%d-%m-%Y') if meta[5] else ''
            except Exception:
                deadline = meta[5]
            progresso = (valor_atual / valor_alvo) * 100 if valor_alvo > 0 else 0

            ctk.CTkLabel(metas_frame, text=title, font=("Roboto", 12), text_color="#fff", fg_color=bg).grid(row=i+1, column=0, padx=1, pady=1, sticky="nsew")
            ctk.CTkLabel(metas_frame, text=f"R$ {valor_alvo:.2f}", font=("Roboto", 12), text_color="#fff", fg_color=bg).grid(row=i+1, column=1, padx=1, pady=1, sticky="nsew")
            ctk.CTkLabel(metas_frame, text=f"R$ {valor_atual:.2f}", font=("Roboto", 12), text_color="#fff", fg_color=bg).grid(row=i+1, column=2, padx=1, pady=1, sticky="nsew")
            ctk.CTkLabel(metas_frame, text=deadline, font=("Roboto", 12), text_color="#fff", fg_color=bg).grid(row=i+1, column=3, padx=1, pady=1, sticky="nsew")
            ctk.CTkLabel(metas_frame, text=f"{progresso:.1f}%", font=("Roboto", 12), text_color="#fff", fg_color=bg).grid(row=i+1, column=4, padx=1, pady=1, sticky="nsew")

            edit_btn = ctk.CTkButton(metas_frame, text="Editar", width=60, command=lambda m=meta: self.edit_goal(m))
            edit_btn.grid(row=i+1, column=5, padx=1, pady=1, sticky="nsew")

            del_btn = ctk.CTkButton(metas_frame, text="Excluir", width=60, fg_color="#E53935", hover_color="#b71c1c", command=lambda m=meta: self.delete_goal(m))
            del_btn.grid(row=i+1, column=6, padx=1, pady=1, sticky="nsew")

    def create_report_options(self):
        # Opções de relatório
        report_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        report_frame.pack(pady=10, padx=10, fill="both", expand=True)

        ctk.CTkLabel(report_frame, text="Relatórios Financeiros", font=("Roboto", 16, "bold"), text_color="#fff").pack(anchor="w", pady=(0, 10))

        ctk.CTkButton(report_frame, text="Gerar Relatório de Transações", command=self.generate_transaction_report, width=200).pack(anchor="w", pady=10)
        ctk.CTkButton(report_frame, text="Gerar Relatório de Metas", command=self.generate_goal_report, width=200).pack(anchor="w", pady=10)
        
        # Separador
        ctk.CTkLabel(report_frame, text="Importar/Exportar Dados", font=("Roboto", 14, "bold"), text_color="#fff").pack(anchor="w", pady=(20, 10))
        
        ctk.CTkButton(report_frame, text="Exportar Transações (CSV)", command=self.export_transactions_csv, width=200).pack(anchor="w", pady=5)
        ctk.CTkButton(report_frame, text="Importar Transações (CSV)", command=self.import_transactions_csv, width=200).pack(anchor="w", pady=5)
        ctk.CTkButton(report_frame, text="Backup Completo (JSON)", command=self.export_all_data_json, width=200).pack(anchor="w", pady=5)

    def create_chat_area(self):
        # Área de chat
        chat_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        chat_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Título e descrição
        title_frame = ctk.CTkFrame(chat_frame, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(title_frame, text="🤖 Assistente Financeiro FinBot", font=("Roboto", 18, "bold"), text_color="#4CAF50").pack(anchor="w")
        ctk.CTkLabel(title_frame, text="Seu mentor financeiro pessoal - pergunte sobre economia, investimentos e metas!", 
                    font=("Roboto", 12), text_color="#bbb").pack(anchor="w", pady=(5, 0))

        # Sugestões de perguntas
        suggestions_frame = ctk.CTkFrame(chat_frame, fg_color="#2b2b2b")
        suggestions_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(suggestions_frame, text="💡 Perguntas Sugeridas:", font=("Roboto", 14, "bold"), text_color="#fff").pack(anchor="w", padx=10, pady=(10, 5))
        
        # Botões de sugestões
        suggestions_buttons = ctk.CTkFrame(suggestions_frame, fg_color="transparent")
        suggestions_buttons.pack(fill="x", padx=10, pady=(0, 10))
        
        suggestions = [
            "Como economizar dinheiro?",
            "Onde investir meu dinheiro?",
            "Como sair do negativo?",
            "Dicas para orçamento",
            "Análise dos meus gastos"
        ]
        
        for i, suggestion in enumerate(suggestions):
            btn = ctk.CTkButton(suggestions_buttons, text=suggestion, 
                               command=lambda s=suggestion: self._ask_suggestion(s),
                               width=150, height=30, font=("Roboto", 10))
            btn.grid(row=i//3, column=i%3, padx=5, pady=2, sticky="w")

        # Área de entrada
        input_frame = ctk.CTkFrame(chat_frame, fg_color="transparent")
        input_frame.pack(fill="x", pady=(0, 10))
        input_frame.grid_columnconfigure(0, weight=1)  # Faz o campo de entrada expandir
        
        self.chat_input = ctk.CTkEntry(input_frame, placeholder_text="Digite sua pergunta sobre finanças...", 
                                      height=40, font=("Roboto", 12))
        self.chat_input.grid(row=0, column=0, sticky="ew", padx=(0, 10))  # sticky="ew" para expandir horizontalmente
        self.chat_input.bind("<Return>", lambda e: self.send_chat_message())

        ctk.CTkButton(input_frame, text="Enviar", command=self.send_chat_message, 
                     width=100, height=40, font=("Roboto", 12, "bold")).grid(row=0, column=1, sticky="w")

        # Área de saída do chat
        self.chat_output = ctk.CTkScrollableFrame(chat_frame, fg_color="#232323")
        self.chat_output.pack(fill="both", expand=True, pady=(0, 10))
        
        # Mensagem de boas-vindas
        self._add_chat_message("FinBot", "👋 Olá! Sou seu assistente financeiro pessoal. Como posso te ajudar hoje?", "bot")

    def add_transaction(self):
        tipo = tipo_para_en(self.tipo_var.get())
        categoria = self.categoria_var.get()
        subcategoria = self.subcategoria_entry.get()
        valor = self.valor_entry.get()
        descricao = self.desc_entry.get()
        data = self.data_entry.get()

        # Validação simples
        if not categoria or not valor or not data:
            self.show_trans_error("Preencha todos os campos obrigatórios!")
            return
        try:
            valor = float(valor)
        except ValueError:
            self.show_trans_error("Valor inválido!")
            return

        # Validação do valor usando ValidationUtils
        from src.utils.message_utils import ValidationUtils
        is_valid, message = ValidationUtils.validate_positive_number(valor)
        if not is_valid:
            self.show_trans_error(message)
            return

        # Converte data DD-MM-YYYY para YYYY-MM-DD para o BD
        try:
            data_iso = datetime.strptime(data, '%d-%m-%Y').strftime('%Y-%m-%d')
        except ValueError:
            self.show_trans_error("Formato de data inválido! Use DD-MM-YYYY.")
            return

        # Adiciona transação
        if self.transaction_controller.add_transaction(tipo, categoria, valor, descricao, data_iso, subcategoria):
            from src.utils.message_utils import MessageUtils
            MessageUtils.show_success(self.main_area, "Transação adicionada com sucesso!")
            self.categoria_var.set(self.categorias_receita[0])
            self.subcategoria_entry.delete(0, 'end')
            self.valor_entry.delete(0, 'end')
            self.desc_entry.delete(0, 'end')
            self.data_entry.delete(0, 'end')
            self.data_entry.insert(0, datetime.now().strftime('%d-%m-%Y'))
            self.update_transaction_list()
            # Atualiza dashboard se visível
            if hasattr(self, 'cards_frame') and self.cards_frame.winfo_exists():
                self.create_summary_cards()
            if hasattr(self, 'chart_frame') and self.chart_frame.winfo_exists():
                self.create_charts()
        else:
            self.show_trans_error("Erro ao adicionar transação!")

    def show_trans_error(self, msg):
        # Mensagem de erro na tabela de transações usando grid
        if self.closed:
            return
        error_label = ctk.CTkLabel(self.trans_list_frame, text=msg, text_color="#ff4444", font=("Roboto", 12))
        # row=999 para garantir que fique no final da tabela
        error_label.grid(row=999, column=0, columnspan=8, pady=5)
        def safe_destroy():
            if not self.closed:
                error_label.destroy()
        self.trans_list_frame.after(3000, safe_destroy)

    def edit_transaction(self, trans_id):
        trans = self.transaction_controller.get_transaction_by_id(trans_id)
        if not trans:
            self.show_trans_error("Transação não encontrada!")
            return
        # Cria popup de edição
        edit_win = ctk.CTkToplevel(self)
        edit_win.title("Editar Transação")
        edit_win.geometry("600x350")
        edit_win.grab_set()

        # Campos
        ctk.CTkLabel(edit_win, text="Tipo:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        tipo_var = ctk.StringVar(value=tipo_para_pt(trans[2]).lower())
        tipo_combo = ctk.CTkComboBox(edit_win, values=["receita", "despesa", "investimento"], variable=tipo_var, width=120)
        tipo_combo.grid(row=0, column=1, padx=5, pady=10, sticky="w")

        ctk.CTkLabel(edit_win, text="Categoria:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        categoria_var = ctk.StringVar(value=trans[3])
        categoria_combo = ctk.CTkComboBox(edit_win, values=self.categorias_receita+self.categorias_despesa+self.categorias_investimento, variable=categoria_var, width=120)
        categoria_combo.grid(row=1, column=1, padx=5, pady=10, sticky="w")

        ctk.CTkLabel(edit_win, text="Subcategoria:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        subcategoria_entry = ctk.CTkEntry(edit_win, width=120)
        subcategoria_entry.insert(0, trans[4] or "")
        subcategoria_entry.grid(row=2, column=1, padx=5, pady=10, sticky="w")

        ctk.CTkLabel(edit_win, text="Valor:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        valor_entry = ctk.CTkEntry(edit_win, width=120)
        valor_entry.insert(0, str(trans[5]))
        valor_entry.grid(row=3, column=1, padx=5, pady=10, sticky="w")

        ctk.CTkLabel(edit_win, text="Descrição:").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        desc_entry = ctk.CTkEntry(edit_win, width=250)
        desc_entry.insert(0, trans[6] or "")
        desc_entry.grid(row=4, column=1, padx=5, pady=10, sticky="w")

        ctk.CTkLabel(edit_win, text="Data (DD-MM-YYYY):").grid(row=5, column=0, padx=10, pady=10, sticky="e")
        data_entry = ctk.CTkEntry(edit_win, width=120)
        # Converte data para DD-MM-YYYY para exibição
        try:
            data_display = datetime.strptime(trans[7][:10], '%Y-%m-%d').strftime('%d-%m-%Y')
        except:
            data_display = trans[7][:10]
        data_entry.insert(0, data_display)
        data_entry.grid(row=5, column=1, padx=5, pady=10, sticky="w")

        def salvar_edicao():
            tipo_db = tipo_para_en(tipo_var.get())
            try:
                valor = float(valor_entry.get())
            except ValueError:
                self.show_trans_error("Valor inválido!")
                return
            
            # Validação do valor usando ValidationUtils
            from src.utils.message_utils import ValidationUtils
            is_valid, message = ValidationUtils.validate_positive_number(valor)
            if not is_valid:
                self.show_trans_error(message)
                return
            
            # Converte data DD-MM-YYYY para YYYY-MM-DD
            try:
                data_iso = datetime.strptime(data_entry.get(), '%d-%m-%Y').strftime('%Y-%m-%d')
            except ValueError:
                self.show_trans_error("Formato de data inválido! Use DD-MM-YYYY.")
                return
                
            ok = self.transaction_controller.update_transaction(
                trans[0], tipo_db, categoria_var.get(), subcategoria_entry.get(), valor, desc_entry.get(), data_iso
            )
            if ok:
                from src.utils.message_utils import MessageUtils
                MessageUtils.show_success(self.main_area, "Transação atualizada com sucesso!")
                edit_win.destroy()
                self.update_transaction_list()
                # Atualiza dashboard se visível
                if hasattr(self, 'cards_frame') and self.cards_frame.winfo_exists():
                    self.create_summary_cards()
                if hasattr(self, 'chart_frame') and self.chart_frame.winfo_exists():
                    self.create_charts()
            else:
                self.show_trans_error("Erro ao atualizar transação!")

        salvar_btn = ctk.CTkButton(edit_win, text="Salvar", command=salvar_edicao, width=100)
        salvar_btn.grid(row=6, column=0, columnspan=2, pady=20)

    def delete_transaction(self, trans_id):
        from src.utils.message_utils import MessageUtils
        from src.utils.loading_utils import ConfirmationDialog
        
        # Busca dados da transação para mostrar na confirmação
        transactions = self.transaction_controller.get_transactions()
        trans = next((t for t in transactions if t[0] == trans_id), None)
        
        if not trans:
            MessageUtils.show_error(self.main_area, "Transação não encontrada!")
            return
        
        # Confirmação antes de excluir
        trans_desc = f"{trans[3]} - R$ {trans[5]:.2f}" if trans[6] else f"{trans[3]} - R$ {trans[5]:.2f}"
        if not ConfirmationDialog.show(self, "Confirmar Exclusão", 
                                     f"Tem certeza que deseja excluir a transação '{trans_desc}'?"):
            return
        
        # Excluir transação
        if self.transaction_controller.delete_transaction(trans_id):
            MessageUtils.show_success(self.main_area, "Transação excluída com sucesso!")
            self.update_transaction_list()
            # Atualiza dashboard se visível
            if hasattr(self, 'cards_frame') and self.cards_frame.winfo_exists():
                self.create_summary_cards()
            if hasattr(self, 'chart_frame') and self.chart_frame.winfo_exists():
                self.create_charts()
        else:
            self.show_trans_error("Erro ao excluir transação!")

    def update_categoria_options(self, *args):
        from src.controllers.category_controller import CategoryController
        
        tipo = self.tipo_var.get()
        tipo_en = tipo_para_en(tipo)
        
        # Busca categorias do banco de dados
        category_controller = CategoryController(self.user)
        categories = category_controller.get_categories(tipo_en)
        
        self.categoria_combo.configure(values=categories)
        if categories:
            self.categoria_var.set(categories[0])
    
    def add_custom_category(self):
        """Adiciona uma nova categoria personalizada"""
        from src.controllers.category_controller import CategoryController
        from src.utils.message_utils import MessageUtils
        
        # Janela para adicionar categoria
        cat_win = ctk.CTkToplevel(self)
        cat_win.title("Nova Categoria")
        cat_win.geometry("400x200")
        cat_win.grab_set()
        
        ctk.CTkLabel(cat_win, text="Adicionar Nova Categoria", font=("Roboto", 16, "bold")).pack(pady=20)
        
        # Campo de nome da categoria
        ctk.CTkLabel(cat_win, text="Nome da categoria:").pack(pady=10)
        cat_entry = ctk.CTkEntry(cat_win, width=200)
        cat_entry.pack(pady=5)
        
        def salvar_categoria():
            nome = cat_entry.get().strip()
            if not nome:
                MessageUtils.show_error(cat_win, "Digite um nome para a categoria!")
                return
            
            tipo = self.tipo_var.get()
            tipo_en = tipo_para_en(tipo)
            
            category_controller = CategoryController(self.user)
            if category_controller.add_custom_category(tipo_en, nome):
                MessageUtils.show_success(cat_win, "Categoria adicionada com sucesso!")
                # Atualiza lista de categorias
                self.update_categoria_options()
                cat_win.destroy()
            else:
                MessageUtils.show_error(cat_win, "Categoria já existe!")
        
        ctk.CTkButton(cat_win, text="Salvar", command=salvar_categoria, width=100).pack(pady=20)

    def add_goal(self):
        from src.utils.message_utils import MessageUtils, ValidationUtils
        
        nome = self.meta_nome_entry.get()
        valor_alvo = self.meta_valor_entry.get()
        deadline = self.meta_deadline_entry.get()

        if not nome or not valor_alvo or not deadline:
            MessageUtils.show_error(self.main_area, "Preencha todos os campos!")
            return

        # Validação do valor
        is_valid, message = ValidationUtils.validate_positive_number(valor_alvo)
        if not is_valid:
            MessageUtils.show_error(self.main_area, message)
            return
        
        valor_alvo = float(valor_alvo)

        # Validação do formato de data (DD-MM-YYYY) e conversão para ISO
        import datetime
        try:
            prazo_convertido = datetime.datetime.strptime(deadline, '%d-%m-%Y').strftime('%Y-%m-%d')
        except ValueError:
            MessageUtils.show_error(self.main_area, "Prazo inválido! Use o formato DD-MM-YYYY.")
            return

        # Adiciona a meta (usa assinatura do controller: title, target_amount, deadline)
        if self.goal_controller.add_goal(nome, valor_alvo, prazo_convertido):
            MessageUtils.show_success(self.main_area, "Meta adicionada com sucesso!")
            # Limpa os campos
            self.meta_nome_entry.delete(0, 'end')
            self.meta_valor_entry.delete(0, 'end')
            self.meta_deadline_entry.delete(0, 'end')
            self.show_goals()
        else:
            MessageUtils.show_error(self.main_area, "Erro ao adicionar meta!")

    def delete_goal(self, meta):
        """Exclui uma meta."""
        from src.utils.message_utils import MessageUtils
        from src.utils.loading_utils import ConfirmationDialog
        
        # Confirmação antes de excluir
        if not ConfirmationDialog.show(self, "Confirmar Exclusão", 
                                     f"Tem certeza que deseja excluir a meta '{meta[2]}'?"):
            return
        
        meta_id = meta[0]  # Supondo que o ID da meta seja o primeiro elemento da tupla
        if self.goal_controller.delete_goal(meta_id):
            MessageUtils.show_success(self.main_area, "Meta excluída com sucesso!")
            self.show_goals()  # Atualiza a lista de metas após a exclusão
        else:
            MessageUtils.show_error(self.main_area, "Erro ao excluir meta!")

    def edit_goal(self, meta):
        """Abre um layout para editar uma meta."""
        edit_win = ctk.CTkToplevel(self) 
        edit_win.title("Editar Meta")
        edit_win.geometry("400x300")
        edit_win.grab_set()

        # Campos
        ctk.CTkLabel(edit_win, text="Nome da Meta:", font=("Roboto", 12)).pack(pady=5)
        nome_entry = ctk.CTkEntry(edit_win, width=300)
        nome_entry.insert(0, meta[2])
        nome_entry.pack(pady=5)

        ctk.CTkLabel(edit_win, text="Valor Alvo:", font=("Roboto", 12)).pack(pady=5)
        valor_entry = ctk.CTkEntry(edit_win, width=300)
        valor_entry.insert(0, str(meta[3]))
        valor_entry.pack(pady=5)

        ctk.CTkLabel(edit_win, text="Prazo (DD-MM-YYYY):", font=("Roboto", 12)).pack(pady=5)
        prazo_entry = ctk.CTkEntry(edit_win, width=300)
        # Converte o prazo para o formato DD-MM-YYYY
        prazo_formatado = datetime.strptime(meta[5], '%Y-%m-%d').strftime('%d-%m-%Y')
        prazo_entry.insert(0, prazo_formatado)  # Supondo que o prazo seja o quarto elemento da tupla
        prazo_entry.pack(pady=5)

        def salvar_edicao():
            nome = nome_entry.get()
            valor_alvo = valor_entry.get()
            prazo = prazo_entry.get()

            if not nome or not valor_alvo or not prazo:
                print("Preencha todos os campos!")
                return

            try:
                valor_alvo = float(valor_alvo)
            except ValueError:
                print("Valor inválido! Insira um número válido.")
                return

            # Converte o prazo para o formato YYYY-MM-DD antes de salvar
            try:
                prazo_convertido = datetime.strptime(prazo, '%d-%m-%Y').strftime('%Y-%m-%d')
            except ValueError:
                MessageUtils.show_error(edit_win, "Prazo inválido! Use o formato DD-MM-YYYY.")
                return

            meta_id = meta[0]
            if self.goal_controller.update_goal(meta_id, nome, valor_alvo, prazo_convertido):
                MessageUtils.show_success(self.main_area, "Meta atualizada com sucesso!")
                edit_win.destroy()
                self.show_goals()
            else:
                MessageUtils.show_error(self.main_area, "Erro ao atualizar meta!")

        salvar_btn = ctk.CTkButton(edit_win, text="Salvar", command=salvar_edicao, width=100)
        salvar_btn.pack(pady=20)

    def generate_transaction_report(self):
        """Gera relatório PDF de transações com seleção de período"""
        from tkinter import filedialog, messagebox
        from src.utils.pdf_generator import PDFGenerator
        import os
        
        # Janela de seleção de período
        period_win = ctk.CTkToplevel(self)
        period_win.title("Período do Relatório")
        period_win.geometry("400x200")
        period_win.grab_set()
        
        ctk.CTkLabel(period_win, text="Selecione o período:", font=("Roboto", 14, "bold")).pack(pady=10)
        
        # Frame para datas
        date_frame = ctk.CTkFrame(period_win, fg_color="transparent")
        date_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(date_frame, text="Data inicial (DD-MM-YYYY):").pack(anchor="w")
        start_date_entry = ctk.CTkEntry(date_frame, width=200)
        start_date_entry.pack(pady=5, anchor="w")
        
        ctk.CTkLabel(date_frame, text="Data final (DD-MM-YYYY):").pack(anchor="w")
        end_date_entry = ctk.CTkEntry(date_frame, width=200)
        end_date_entry.pack(pady=5, anchor="w")
        
        def generate_report():
            start_date = start_date_entry.get()
            end_date = end_date_entry.get()
            
            if not start_date or not end_date:
                messagebox.showerror("Erro", "Preencha ambas as datas!")
                return
                
            # Converte datas para formato do BD
            try:
                from datetime import datetime
                start_iso = datetime.strptime(start_date, '%d-%m-%Y').strftime('%Y-%m-%d')
                end_iso = datetime.strptime(end_date, '%d-%m-%Y').strftime('%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Erro", "Formato de data inválido! Use DD-MM-YYYY.")
                return
            
            # Seleciona local de salvamento
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                title="Salvar relatório como..."
            )
            
            if not filename:
                return
                
            try:
                from src.utils.loading_utils import LoadingManager
                
                # Mostra loading
                loading_manager = LoadingManager(period_win)
                loading_manager.show_loading("Gerando relatório...")
                
                # Busca transações do período
                transactions = self.transaction_controller.get_transactions(
                    start_date=start_iso,
                    end_date=end_iso
                )
                
                # Gera PDF
                pdf_gen = PDFGenerator(self.user)
                pdf_gen.generate_financial_report(transactions, [], filename)
                
                # Esconde loading e mostra sucesso
                loading_manager.hide_loading()
                messagebox.showinfo("Sucesso", f"Relatório salvo em:\n{filename}")
                period_win.destroy()
                
            except Exception as e:
                if 'loading_manager' in locals():
                    loading_manager.hide_loading()
                messagebox.showerror("Erro", f"Erro ao gerar relatório:\n{str(e)}")
        
        ctk.CTkButton(period_win, text="Gerar Relatório", command=generate_report, width=150).pack(pady=20)

    def generate_goal_report(self):
        """Gera relatório PDF de metas"""
        from tkinter import filedialog, messagebox
        from src.utils.pdf_generator import PDFGenerator
        import os
        
        # Seleciona local de salvamento
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Salvar relatório de metas como..."
        )
        
        if not filename:
            return
            
        try:
            from src.utils.loading_utils import LoadingManager
            
            # Mostra loading
            loading_manager = LoadingManager(self)
            loading_manager.show_loading("Gerando relatório de metas...")
            
            # Busca todas as metas
            goals = self.goal_controller.get_goals()
            
            # Gera PDF (sem transações, só metas)
            pdf_gen = PDFGenerator(self.user)
            pdf_gen.generate_financial_report([], goals, filename)
            
            # Esconde loading e mostra sucesso
            loading_manager.hide_loading()
            messagebox.showinfo("Sucesso", f"Relatório de metas salvo em:\n{filename}")
            
        except Exception as e:
            if 'loading_manager' in locals():
                loading_manager.hide_loading()
            messagebox.showerror("Erro", f"Erro ao gerar relatório:\n{str(e)}")

    def export_transactions_csv(self):
        """Exporta transações para CSV"""
        from src.utils.data_import_export import DataImportExport
        
        data_export = DataImportExport(self.transaction_controller, self.goal_controller, self.user)
        if data_export.export_transactions_csv(self):
            # Atualiza lista se visível
            if hasattr(self, 'trans_list_frame') and self.trans_list_frame.winfo_exists():
                self.update_transaction_list()

    def import_transactions_csv(self):
        """Importa transações de CSV"""
        from src.utils.data_import_export import DataImportExport
        
        data_import = DataImportExport(self.transaction_controller, self.goal_controller, self.user)
        if data_import.import_transactions_csv(self):
            # Atualiza lista e dashboard se visível
            if hasattr(self, 'trans_list_frame') and self.trans_list_frame.winfo_exists():
                self.update_transaction_list()
            if hasattr(self, 'cards_frame') and self.cards_frame.winfo_exists():
                self.create_summary_cards()
            if hasattr(self, 'chart_frame') and self.chart_frame.winfo_exists():
                self.create_charts()

    def export_all_data_json(self):
        """Exporta todos os dados para JSON"""
        from src.utils.data_import_export import DataImportExport
        
        data_export = DataImportExport(self.transaction_controller, self.goal_controller, self.user)
        data_export.export_all_data_json(self)

    def send_chat_message(self):
        from src.utils.message_utils import MessageUtils
        
        mensagem = self.chat_input.get().strip()
        if not mensagem:
            MessageUtils.show_error(self.chat_output, "Digite uma mensagem!")
            return

        # Adiciona mensagem do usuário
        self._add_chat_message("Você", mensagem, "user")
        
        # Limpa o campo de entrada
        self.chat_input.delete(0, 'end')
        
        # Mostra indicador de carregamento
        loading_label = ctk.CTkLabel(self.chat_output, text="FinBot está pensando...", 
                                   font=("Roboto", 12, "italic"), text_color="#bbb")
        loading_label.pack(anchor="w", pady=5)
        self.update()
        
        # Obtém resposta do chatbot
        try:
            resposta = self.chatbot_controller.get_response(mensagem)
            loading_label.destroy()  # Remove indicador de carregamento
            self._add_chat_message("FinBot", resposta, "bot")
        except Exception as e:
            loading_label.destroy()
            self._add_chat_message("FinBot", f"Desculpe, ocorreu um erro: {str(e)}", "error")
    
    def _ask_suggestion(self, suggestion):
        """Faz uma pergunta sugerida"""
        self.chat_input.delete(0, 'end')
        self.chat_input.insert(0, suggestion)
        self.send_chat_message()
    
    def _add_chat_message(self, sender, message, message_type="bot"):
        """Adiciona uma mensagem ao chat com formatação"""
        # Frame da mensagem
        msg_frame = ctk.CTkFrame(self.chat_output, fg_color="transparent")
        msg_frame.pack(fill="both", expand=True, padx=5, pady=5)
        msg_frame.grid_columnconfigure(0, weight=1)
        
        # Cabeçalho da mensagem
        if message_type == "user":
            header_color = "#4CAF50"
            bg_color = "#2b2b2b"
        elif message_type == "error":
            header_color = "#ff4444"
            bg_color = "#3b1a1a"
        else:  # bot
            header_color = "#2196F3"
            bg_color = "#1a2b3b"
        
        # Nome do remetente
        sender_label = ctk.CTkLabel(msg_frame, text=f"{sender}:", 
                                  font=("Roboto", 12, "bold"), text_color=header_color)
        sender_label.grid(row=0, column=0, sticky="w", padx=5, pady=(5, 0))
        
        # Conteúdo da mensagem
        content_frame = ctk.CTkFrame(msg_frame, fg_color=bg_color, corner_radius=10)
        content_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=(2, 5))
        
        # Configura o frame para usar todo o espaço disponível
        content_frame.grid_columnconfigure(0, weight=1)
        
        # Usa um único label para o texto completo com justificação adequada
        text_color = "#fff" if message_type != "error" else "#ffcccc"
        message_label = ctk.CTkLabel(
            content_frame, 
            text=message, 
            font=("Roboto", 12), 
            text_color=text_color, 
            justify="left",
            anchor="w"  # Alinha à esquerda
        )
        message_label.grid(row=0, column=0, sticky="ew", padx=15, pady=15)
        
        # Scroll para a última mensagem
        self.chat_output.update()
        self.chat_output._parent_canvas.yview_moveto(1.0)
    

    def logout(self):
        # Fecha a janela principal e retorna à tela de login
        self.master.destroy()
        print("Usuário desconectado.")  # Mensagem de logout (opcional)

    def clear_main_area(self):
        # Remove todos os widgets da área principal
        for widget in self.main_area.winfo_children():
            widget.destroy()

    def get_goals(self):
        # Exemplo de retorno esperado
        return [
            {"nome": "Meta 1", "valor_alvo": 1000, "valor_atual": 500, "deadline": "2025-12-31"},
            {"nome": "Meta 2", "valor_alvo": 2000, "valor_atual": 1500, "deadline": "2025-11-30"}
        ]
