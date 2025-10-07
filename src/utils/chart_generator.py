import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
from collections import defaultdict
import customtkinter as ctk

class ChartGenerator:
    def __init__(self):
        self.colors = {
            'income': '#43A047',      # Verde
            'expense': '#E53935',     # Vermelho
            'investment': '#FBC02D'   # Amarelo
        }
    
    def create_monthly_pie_chart(self, transactions, master_frame):
        """Cria gráfico de pizza com distribuição financeira do mês"""
        # Filtra transações do mês atual
        now = datetime.datetime.now()
        transacoes_mes = []
        
        for t in transactions:
            data_str = t[7]  # data está em t[7]
            try:
                # Tenta com hora completa
                data_dt = datetime.datetime.strptime(data_str, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                try:
                    # Tenta só com data
                    data_dt = datetime.datetime.strptime(data_str, '%Y-%m-%d')
                except Exception:
                    continue
            if data_dt.month == now.month and data_dt.year == now.year:
                transacoes_mes.append(t)
        
        # Calcula valores por tipo
        valores = []
        labels = []
        cores = []
        
        for tipo in ['income', 'expense', 'investment']:
            valor = sum(t[5] for t in transacoes_mes if t[2] == tipo)
            if valor > 0:
                valores.append(valor)
                labels.append(tipo.capitalize())
                cores.append(self.colors[tipo])
        
        if sum(valores) == 0:
            return None
            
        # Cria o gráfico
        fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
        ax.pie(valores, labels=labels, autopct='%1.1f%%', colors=cores, textprops={'color':"w"})
        ax.set_title('Distribuição Financeira do Mês', color='#fff')
        fig.patch.set_facecolor('#232323')
        
        # Cria canvas
        canvas = FigureCanvasTkAgg(fig, master=master_frame)
        canvas.draw()
        
        return canvas
    
    def create_expense_ranking(self, transactions, master_frame):
        """Cria ranking de gastos por categoria/subcategoria"""
        # Filtra transações do mês atual
        now = datetime.datetime.now()
        transacoes_mes = []
        
        for t in transactions:
            data_str = t[7]
            try:
                data_dt = datetime.datetime.strptime(data_str, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                try:
                    data_dt = datetime.datetime.strptime(data_str, '%Y-%m-%d')
                except Exception:
                    continue
            if data_dt.month == now.month and data_dt.year == now.year:
                transacoes_mes.append(t)
        
        # Agrupa despesas por categoria/subcategoria
        gastos = defaultdict(float)
        for t in transacoes_mes:
            if t[2] == 'expense':
                chave = t[3]  # Categoria
                if t[4]:  # Subcategoria
                    chave += f" / {t[4]}"
                gastos[chave] += float(t[5])
        
        # Ordena do maior para o menor
        ranking = sorted(gastos.items(), key=lambda x: x[1], reverse=True)
        
        # Cria frame para o ranking
        ranking_frame = ctk.CTkFrame(master_frame, fg_color="#232323")
        ctk.CTkLabel(ranking_frame, text="Principais Gastos do Mês", 
                    font=("Roboto", 14, "bold"), text_color="#fff").pack(anchor="w", pady=(0,8))
        
        if ranking:
            for i, (cat, val) in enumerate(ranking[:8]):
                ctk.CTkLabel(ranking_frame, text=f"{i+1}. {cat}: R$ {val:.2f}", 
                           font=("Roboto", 12), text_color="#fff").pack(anchor="w")
        else:
            ctk.CTkLabel(ranking_frame, text="Nenhuma despesa registrada.", 
                         font=("Roboto", 12), text_color="#bbb").pack(anchor="w")
        
        return ranking_frame
    
    def create_monthly_charts(self, transactions, master_frame):
        """Cria layout completo com gráfico de pizza e ranking de gastos"""
        # Layout: gráfico à esquerda, ranking à direita
        chart_content = ctk.CTkFrame(master_frame, fg_color="transparent")
        chart_content.pack(fill="both", expand=True)
        chart_content.grid_columnconfigure(0, weight=1)
        chart_content.grid_columnconfigure(1, weight=1)
        
        # Gráfico de pizza
        pie_canvas = self.create_monthly_pie_chart(transactions, chart_content)
        if pie_canvas:
            pie_canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        else:
            ctk.CTkLabel(chart_content, text="Sem dados para exibir o gráfico do mês.", 
                        font=("Roboto", 14), text_color="#fff").grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Ranking de gastos
        ranking_frame = self.create_expense_ranking(transactions, chart_content)
        ranking_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        return chart_content