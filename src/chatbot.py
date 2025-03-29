import re
from datetime import datetime, date
import json


class ChatBot:
    def __init__(self, db):
        self.db = db
        self.context = {}

    def process_message(self, message):
        """Processa a mensagem do usuário e retorna uma resposta apropriada"""
        message = message.lower()

        # Padrões de reconhecimento
        patterns = {
            r'ajuda': self.show_help,
            r'resumo': self.show_summary,
            r'despesa': self.handle_expense,
            r'receita': self.handle_income,
            r'orçamento': self.handle_budget,
            r'meta': self.handle_goal,
            r'investimento': self.handle_investment,
            r'lembrete': self.handle_reminder,
            r'dica': self.show_tip
        }

        # Verificar padrões
        for pattern, handler in patterns.items():
            if re.search(pattern, message):
                return handler(message)

        return "Desculpe, não entendi. Digite 'ajuda' para ver as opções disponíveis."

    def show_help(self, message):
        """Mostra as opções disponíveis"""
        return """
        Olá! Sou seu assistente virtual. Como posso ajudar?
        
        Comandos disponíveis:
        - 'resumo': Mostra um resumo das suas finanças
        - 'despesa': Adiciona uma nova despesa
        - 'receita': Adiciona uma nova receita
        - 'orçamento': Gerencia seus orçamentos
        - 'meta': Gerencia suas metas financeiras
        - 'investimento': Gerencia seus investimentos
        - 'lembrete': Gerencia seus lembretes
        - 'dica': Mostra uma dica financeira
        """

    def show_summary(self, message):
        """Mostra um resumo das finanças"""
        resumo = self.db.get_resumo_financeiro()
        return f"""
        Resumo Financeiro:
        
        Saldo Total: R$ {resumo['saldo_total']:.2f}
        Receitas do Mês: R$ {resumo['receitas']:.2f}
        Despesas do Mês: R$ {resumo['despesas']:.2f}
        
        Despesas por Categoria:
        {self._format_categories(resumo['despesas_por_categoria'])}
        """

    def handle_expense(self, message):
        """Processa comandos relacionados a despesas"""
        # Extrair informações da mensagem
        try:
            # Padrão: despesa 100 alimentação
            match = re.search(r'despesa (\d+(?:\.\d+)?) (\w+)', message)
            if match:
                valor = float(match.group(1))
                categoria = match.group(2)

                # Adicionar despesa
                if self.db.add_transacao(
                    descricao=f"Despesa em {categoria}",
                    valor=valor,
                    categoria=categoria,
                    tipo="Despesa",
                    data=date.today()
                ):
                    return f"Despesa de R$ {valor:.2f} em {categoria} registrada com sucesso!"
                else:
                    return "Erro ao registrar despesa."

        except Exception as e:
            return "Desculpe, não consegui entender os detalhes da despesa. Use o formato: despesa valor categoria"

    def handle_income(self, message):
        """Processa comandos relacionados a receitas"""
        try:
            # Padrão: receita 1000 salário
            match = re.search(r'receita (\d+(?:\.\d+)?) (\w+)', message)
            if match:
                valor = float(match.group(1))
                categoria = match.group(2)

                # Adicionar receita
                if self.db.add_transacao(
                    descricao=f"Receita de {categoria}",
                    valor=valor,
                    categoria=categoria,
                    tipo="Receita",
                    data=date.today()
                ):
                    return f"Receita de R$ {valor:.2f} em {categoria} registrada com sucesso!"
                else:
                    return "Erro ao registrar receita."

        except Exception as e:
            return "Desculpe, não consegui entender os detalhes da receita. Use o formato: receita valor categoria"

    def handle_budget(self, message):
        """Processa comandos relacionados a orçamentos"""
        try:
            # Padrão: orçamento alimentação 1000
            match = re.search(r'orçamento (\w+) (\d+(?:\.\d+)?)', message)
            if match:
                categoria = match.group(1)
                valor = float(match.group(2))

                # Adicionar orçamento
                if self.db.add_orcamento(categoria, valor):
                    return f"Orçamento de R$ {valor:.2f} para {categoria} definido com sucesso!"
                else:
                    return "Erro ao definir orçamento."

        except Exception as e:
            return "Desculpe, não consegui entender os detalhes do orçamento. Use o formato: orçamento categoria valor"

    def handle_goal(self, message):
        """Processa comandos relacionados a metas"""
        try:
            # Padrão: meta viagem 5000
            match = re.search(r'meta (\w+) (\d+(?:\.\d+)?)', message)
            if match:
                nome = match.group(1)
                valor = float(match.group(2))

                # Adicionar meta
                if self.db.add_meta(nome, valor):
                    return f"Meta '{nome}' com valor de R$ {valor:.2f} definida com sucesso!"
                else:
                    return "Erro ao definir meta."

        except Exception as e:
            return "Desculpe, não consegui entender os detalhes da meta. Use o formato: meta nome valor"

    def handle_investment(self, message):
        """Processa comandos relacionados a investimentos"""
        try:
            # Padrão: investimento poupança 1000
            match = re.search(r'investimento (\w+) (\d+(?:\.\d+)?)', message)
            if match:
                tipo = match.group(1)
                valor = float(match.group(2))

                # Adicionar investimento
                if self.db.add_investimento(tipo, valor):
                    return f"Investimento de R$ {valor:.2f} em {tipo} registrado com sucesso!"
                else:
                    return "Erro ao registrar investimento."

        except Exception as e:
            return "Desculpe, não consegui entender os detalhes do investimento. Use o formato: investimento tipo valor"

    def handle_reminder(self, message):
        """Processa comandos relacionados a lembretes"""
        try:
            # Padrão: lembrete conta luz 100 15
            match = re.search(r'lembrete (\w+) (\d+(?:\.\d+)?) (\d+)', message)
            if match:
                titulo = match.group(1)
                valor = float(match.group(2))
                dia = int(match.group(3))

                # Adicionar lembrete
                if self.db.add_lembrete(titulo, valor, dia):
                    return f"Lembrete para {titulo} no valor de R$ {valor:.2f} no dia {dia} registrado com sucesso!"
                else:
                    return "Erro ao registrar lembrete."

        except Exception as e:
            return "Desculpe, não consegui entender os detalhes do lembrete. Use o formato: lembrete título valor dia"

    def show_tip(self, message):
        """Mostra uma dica financeira aleatória"""
        dicas = [
            "Mantenha um controle rigoroso das suas despesas diárias.",
            "Crie um fundo de emergência com 3 a 6 meses de despesas.",
            "Evite compras por impulso, faça um planejamento antes.",
            "Compare preços antes de fazer compras grandes.",
            "Use aplicativos de cashback para economizar.",
            "Faça um orçamento mensal e siga-o rigorosamente.",
            "Pague suas contas em dia para evitar juros.",
            "Invista em educação financeira.",
            "Diversifique seus investimentos.",
            "Evite dívidas com juros altos."
        ]

        import random
        return random.choice(dicas)

    def _format_categories(self, categories):
        """Formata as categorias para exibição"""
        if not categories:
            return "Nenhuma despesa registrada."

        return "\n".join([f"- {cat}: R$ {valor:.2f}" for cat, valor in categories.items()])
