from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime

class PDFGenerator:
    def __init__(self, user):
        self.user = user
        self.styles = getSampleStyleSheet()
        self.custom_style = ParagraphStyle(
            'Custom',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=20
        )
    
    def generate_financial_report(self, transactions, goals, output_path):
        """Gera um relatório financeiro completo em PDF"""
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        elements = []
        
        # Título
        title = Paragraph(f"Relatório Financeiro - {self.user.username}", self.styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 20))
        
        # Data do relatório
        date = Paragraph(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", self.custom_style)
        elements.append(date)
        elements.append(Spacer(1, 20))
        
        # Resumo financeiro
        elements.append(Paragraph("Resumo Financeiro", self.styles['Heading2']))
        elements.append(self._create_summary_table(transactions))
        elements.append(Spacer(1, 20))
        
        # Metas financeiras
        elements.append(Paragraph("Metas Financeiras", self.styles['Heading2']))
        elements.append(self._create_goals_table(goals))
        elements.append(Spacer(1, 20))
        
        # Transações recentes
        elements.append(Paragraph("Transações Recentes", self.styles['Heading2']))
        elements.append(self._create_transactions_table(transactions))
        
        doc.build(elements)
    
    def _create_summary_table(self, transactions):
        """Cria a tabela de resumo financeiro"""
        # transactions: (id, user_id, type, category, subcategory, amount, description, date)
        income = sum(float(t[5]) for t in transactions if t[2] == 'income')
        expenses = sum(float(t[5]) for t in transactions if t[2] == 'expense')
        balance = income - expenses
        
        data = [
            ['Categoria', 'Valor'],
            ['Receitas', f'R$ {income:.2f}'],
            ['Despesas', f'R$ {expenses:.2f}'],
            ['Saldo', f'R$ {balance:.2f}']
        ]
        
        table = Table(data, colWidths=[2*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        return table
    
    def _create_goals_table(self, goals):
        """Cria a tabela de metas financeiras"""
        data = [['Meta', 'Valor Alvo', 'Valor Atual', 'Progresso', 'Status']]
        
        for goal in goals:
            progress = (goal[4] / goal[3]) * 100 if goal[3] > 0 else 0
            data.append([
                goal[2],
                f'R$ {goal[3]:.2f}',
                f'R$ {goal[4]:.2f}',
                f'{progress:.1f}%',
                goal[6]
            ])
        
        table = Table(data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        return table
    
    def _create_transactions_table(self, transactions):
        """Cria a tabela de transações recentes"""
        data = [['Data', 'Tipo', 'Categoria', 'Valor', 'Descrição']]
        
        for transaction in transactions[:10]:  # Mostra apenas as 10 transações mais recentes
            # Data pode estar em 'YYYY-MM-DD HH:MM:SS' ou 'YYYY-MM-DD'
            try:
                dt = datetime.strptime(transaction[7], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                try:
                    dt = datetime.strptime(transaction[7], '%Y-%m-%d')
                except Exception:
                    dt = None
            data.append([
                dt.strftime('%d/%m/%Y') if dt else (transaction[7] or ''),
                transaction[2].capitalize(),
                transaction[3],
                f'R$ {float(transaction[5]):.2f}',
                transaction[6] or ''
            ])
        
        table = Table(data, colWidths=[1*inch, 1*inch, 1.5*inch, 1*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        return table 