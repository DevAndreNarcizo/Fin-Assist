import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
from datetime import datetime, timedelta

class ChatbotController:
    def __init__(self, user=None, transaction_controller=None, goal_controller=None):
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = None
        self.chat = None
        self.user = user
        self.transaction_controller = transaction_controller
        self.goal_controller = goal_controller
        self.setup_gemini()
    
    def setup_gemini(self):
        """Configura a API do Gemini com prompt especializado"""
        if not self.api_key:
            return
        
        try:
            genai.configure(api_key=self.api_key)
            
            # Prompt especializado para assistente financeiro
            system_prompt = self._get_financial_assistant_prompt()
            
            self.model = genai.GenerativeModel('gemini-pro')
            self.chat = self.model.start_chat(history=[])
            
            # Envia o prompt inicial
            self.chat.send_message(system_prompt)
            
        except Exception as e:
            print(f"Erro ao configurar Gemini: {e}")
    
    def _get_financial_assistant_prompt(self):
        """Retorna o prompt especializado do assistente financeiro"""
        user_data = self._get_user_financial_data()
        
        return f"""
Você é um assistente financeiro especializado e experiente chamado "FinBot". Sua missão é ajudar o usuário a melhorar sua saúde financeira com conselhos práticos e personalizados.

CONTEXTO DO USUÁRIO:
{user_data}

SUAS ESPECIALIDADES:
1. **Análise Financeira**: Analise receitas, despesas e padrões de gastos
2. **Dicas de Economia**: Estratégias práticas para reduzir gastos
3. **Investimentos**: Orientações sobre onde e como investir
4. **Sair do Negativo**: Planos para eliminar dívidas e melhorar saldo
5. **Metas Financeiras**: Ajuda a definir e alcançar objetivos
6. **Educação Financeira**: Explicações claras sobre conceitos financeiros

DIRETRIZES DE RESPOSTA:
- Seja sempre positivo e encorajador
- Use linguagem simples e acessível
- Dê conselhos práticos e acionáveis
- Personalize as respostas baseado nos dados do usuário
- Sugira valores específicos quando apropriado
- Sempre motive o usuário a tomar ação
- Se não tiver dados suficientes, peça mais informações

FORMATO DAS RESPOSTAS:
- Comece com uma saudação amigável
- Identifique o problema ou pergunta
- Dê conselhos específicos e práticos
- Termine com uma pergunta para engajar o usuário

EXEMPLOS DE RESPOSTAS:
- "Olá! Vejo que você tem R$ 2.000 em despesas mensais. Vou te ajudar a economizar..."
- "Excelente pergunta sobre investimentos! Baseado no seu perfil, recomendo..."
- "Para sair do negativo, sugiro este plano em 3 etapas..."

Responda sempre em português brasileiro e seja um verdadeiro mentor financeiro!
"""
    
    def _get_user_financial_data(self):
        """Coleta dados financeiros do usuário para personalizar as respostas"""
        if not self.transaction_controller or not self.goal_controller:
            return "Dados financeiros não disponíveis."
        
        try:
            # Busca transações dos últimos 3 meses
            three_months_ago = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
            transactions = self.transaction_controller.get_transactions(start_date=three_months_ago)
            
            # Calcula totais
            total_income = sum(t[5] for t in transactions if t[2] == 'income')
            total_expenses = sum(t[5] for t in transactions if t[2] == 'expense')
            total_investments = sum(t[5] for t in transactions if t[2] == 'investment')
            balance = total_income - total_expenses
            
            # Busca metas
            goals = self.goal_controller.get_goals()
            active_goals = [g for g in goals if g[6] == 'active']
            
            # Categorias de gastos mais frequentes
            expense_categories = {}
            for t in transactions:
                if t[2] == 'expense':
                    cat = t[3]
                    expense_categories[cat] = expense_categories.get(cat, 0) + t[5]
            
            top_expenses = sorted(expense_categories.items(), key=lambda x: x[1], reverse=True)[:5]
            
            return f"""
DADOS FINANCEIROS ATUAIS (últimos 3 meses):
- Receitas: R$ {total_income:.2f}
- Despesas: R$ {total_expenses:.2f}
- Investimentos: R$ {total_investments:.2f}
- Saldo: R$ {balance:.2f}
- Principais gastos: {', '.join([f"{cat} (R$ {val:.2f})" for cat, val in top_expenses])}
- Metas ativas: {len(active_goals)} metas
- Status: {'Positivo' if balance > 0 else 'Negativo'}
"""
        except Exception as e:
            return f"Erro ao obter dados: {str(e)}"
    
    def get_response(self, message):
        """Obtém resposta personalizada do assistente financeiro"""
        # Verifica se é um cálculo financeiro
        calculation_response = self.parse_financial_calculation(message)
        if calculation_response and "Para calcular" not in calculation_response:
            return calculation_response
        
        # Se não é cálculo, usa resposta normal
        if not self.chat:
            return self._get_fallback_response(message)
        
        try:
            # Adiciona contexto atual se disponível
            context_message = f"""
Dados atuais: {self._get_user_financial_data()}

Pergunta do usuário: {message}

Responda como um assistente financeiro especializado, dando conselhos práticos e personalizados.
"""
            
            response = self.chat.send_message(context_message)
            return response.text
        except Exception as e:
            return self._get_fallback_response(message)
    
    def _detect_similar_phrases(self, message_lower):
        """Detecta frases similares e sinônimos"""
        # Frases sobre economia
        economy_phrases = [
            'como gastar menos', 'reduzir despesas', 'diminuir gastos', 'cortar custos',
            'economizar dinheiro', 'poupar mais', 'guardar dinheiro', 'juntar dinheiro',
            'fazer sobrar', 'ter sobra', 'sobra no final do mês', 'sobra no fim do mês',
            'dinheiro sobrando', 'renda sobrando', 'salário sobrando', 'salario sobrando'
        ]
        
        # Frases sobre investimentos
        investment_phrases = [
            'onde colocar dinheiro', 'onde aplicar dinheiro', 'melhor investimento',
            'investimento seguro', 'investimento que rende', 'aplicação que rende',
            'onde investir melhor', 'melhor lugar para investir', 'aplicação segura',
            'rendimento melhor', 'maior retorno', 'mais lucrativo'
        ]
        
        # Frases sobre dívidas
        debt_phrases = [
            'sair do vermelho', 'sair do buraco', 'sair do sufoco', 'sair da dívida',
            'pagar cartão', 'quitar cartão', 'zerar cartão', 'limpar nome',
            'limpar spc', 'limpar serasa', 'nome limpo', 'nome sujo',
            'protestado', 'protesto', 'cheque especial', 'limite estourado'
        ]
        
        # Frases sobre metas
        goals_phrases = [
            'conseguir comprar', 'ter dinheiro para', 'juntar para comprar',
            'economizar para', 'poupar para', 'guardar para',
            'realizar sonho', 'concretizar sonho', 'materializar sonho',
            'fazer acontecer', 'conseguir realizar', 'alcançar objetivo'
        ]
        
        # Frases sobre orçamento
        budget_phrases = [
            'controlar dinheiro', 'organizar finanças', 'organizar dinheiro',
            'administrar gastos', 'gerenciar dinheiro', 'planejar gastos',
            'fazer orçamento', 'criar orçamento', 'montar orçamento',
            'acompanhar gastos', 'monitorar gastos', 'acompanhar despesas'
        ]
        
        # Verifica se alguma frase similar está presente
        all_phrases = {
            'economy': economy_phrases,
            'investment': investment_phrases,
            'debt': debt_phrases,
            'goals': goals_phrases,
            'budget': budget_phrases
        }
        
        for category, phrases in all_phrases.items():
            for phrase in phrases:
                if phrase in message_lower:
                    return category
        
        return None

    def _get_economy_response(self):
        """Resposta sobre economia"""
        return """Olha, economizar dinheiro não é um bicho de sete cabeças! Vou te dar umas dicas que realmente funcionam:

**Primeiro, vamos organizar sua renda:**
- 50% para o essencial (aluguel, comida, transporte)
- 30% para seus desejos (lazer, roupas)
- 20% para guardar (essa é a parte mais importante!)

**Dicas práticas que funcionam:**
1. Faça lista de compras - sério, isso evita compras desnecessárias
2. Compare preços no Zoom ou Mercado Livre antes de comprar
3. Espere 1 dia antes de comprar algo que não estava planejado
4. Ligue para suas operadoras (internet, celular) e peça desconto - funciona!
5. Cozinhe mais em casa, delivery é caro demais
6. Use cupons e promoções, não é vergonha nenhuma

**A meta é simples:** tenta guardar pelo menos 20% do que ganha por mês.

Quer que eu veja seus gastos e te ajude a identificar onde dá pra cortar?"""

    def _get_investment_response(self):
        """Resposta sobre investimentos"""
        return """Cara, investir não precisa ser complicado! Deixa eu te explicar de um jeito simples:

**Se você está começando (e tem medo de perder dinheiro):**
- Tesouro Selic: 100% seguro, você pode tirar a qualquer hora
- CDB de banco grande: também seguro, rende mais que poupança
- Poupança: só pra emergência mesmo, rende pouco

**Se você já tem uma grana guardada e quer crescer mais:**
- Ações de empresas grandes (Petrobras, Vale, etc.)
- Fundos que espelham a Bolsa
- LCI/LCA: rende bem e não paga imposto

**Se você é mais arrojado e tem estômago forte:**
- Ações individuais
- Fundos Imobiliários (renda mensal)
- Criptomoedas (só um pouquinho, hein!)

**A regra de ouro:** comece devagar, sempre com dinheiro que você pode perder. E invista todo mês, mesmo que seja pouco.

Me conta: você já investe alguma coisa ou está começando do zero?"""

    def _get_debt_response(self):
        """Resposta sobre dívidas"""
        return """Relaxa, sair do negativo é possível sim! Já ajudei muita gente nessa situação. Vamos por partes:

**Primeiro, vamos fazer um diagnóstico:**
- Anota todas as suas dívidas (cartão, empréstimo, cheque especial)
- Olha qual tem o juros mais alto - essa vai ser a prioridade
- Calcula quanto você consegue pagar por mês (seja realista)

**Agora vamos cortar gastos:**
- Cancela assinaturas que não usa (Netflix, Spotify, etc.)
- Para com delivery, cozinha em casa
- Liga pra operadora e pede desconto
- Vende coisas que não usa mais no OLX

**Terceiro passo - aumentar a renda:**
- Faz uns bicos, freelances
- Vende suas habilidades (se sabe Excel, ensina alguém)
- Pede aumento no trabalho (não custa tentar!)

**Estratégia de pagamento:**
Tem dois jeitos: pagar a dívida com maior juros primeiro (economiza mais) ou a menor dívida primeiro (te motiva mais).

**Meta realista:** em 2 anos você pode estar livre!

Me fala quanto você deve e qual sua renda mensal que eu te ajudo a fazer um plano específico."""

    def _get_goals_response(self):
        """Resposta sobre metas"""
        return """Olha, ter metas financeiras é o que separa quem consegue do que fica no "quero mas não consigo". Vou te ensinar como fazer isso direito:

**Primeiro, defina sua meta de um jeito claro:**
- Não fale "quero um carro", fale "quero um carro de R$ 25.000 em 2 anos"
- Seja realista com o prazo baseado na sua renda
- Escolha algo que realmente importa pra você

**Tipos de metas que fazem sentido:**
- **Curto prazo (até 1 ano):** viagem, móveis, emergência
- **Médio prazo (1-5 anos):** carro, entrada de casa, curso
- **Longo prazo (5+ anos):** casa própria, aposentadoria

**Como alcançar:**
1. Quebra em pedaços menores: R$ 25.000 em 2 anos = R$ 1.042 por mês
2. Coloca débito automático todo dia 5 (não vai esquecer)
3. Acompanha todo mês se tá no caminho certo
4. Celebra quando alcança 25%, 50%, 75%
5. Se der ruim, ajusta o prazo (não desiste!)

**Dica importante:** sempre tenha uma meta de emergência primeiro (6 meses de gastos guardados).

Qual seu sonho? Me conta que eu te ajudo a calcular quanto você precisa guardar por mês!"""

    def _get_budget_response(self):
        """Resposta sobre orçamento"""
        return """Cara, controlar o dinheiro é mais simples do que parece! Deixa eu te explicar como fazer:

**Vamos organizar sua grana assim:**
- 50% pra necessidades (aluguel, comida, transporte)
- 30% pra seus desejos (lazer, roupas, sair)
- 20% pra guardar (essa é a parte mais importante!)

**Ferramentas que funcionam:**
- Planilha do Excel (grátis e simples)
- App Mobills (bem completo)
- App Guiabolso (conecta com seu banco)
- Ou até um caderninho mesmo!

**Como controlar todo mês:**
1. Anota quanto entra (salário, freelances)
2. Lista o que sai fixo (aluguel, contas)
3. Controla o que varia (comida, gasolina, lazer)
4. O que sobrar vai pra poupança

**Dicas que funcionam:**
- Anota TUDO que gasta, até aquele cafezinho de R$ 5
- Revise todo domingo como tá indo
- Separa por categorias (comida, transporte, lazer)
- Coloca limite por categoria
- Se estourar o limite, para de gastar!

**Sinais de alerta:**
- Cartão de crédito virou 30% da renda
- Não sobra nada no final do mês
- Tá pegando empréstimo pra pagar conta básica

Quer que eu te ajude a montar um orçamento que funciona pra você?"""

    def _get_fallback_response(self, message):
        """Respostas quando o Gemini não está disponível"""
        message_lower = message.lower()
        
        # Primeiro tenta detectar frases similares
        similar_category = self._detect_similar_phrases(message_lower)
        if similar_category:
            if similar_category == 'economy':
                return self._get_economy_response()
            elif similar_category == 'investment':
                return self._get_investment_response()
            elif similar_category == 'debt':
                return self._get_debt_response()
            elif similar_category == 'goals':
                return self._get_goals_response()
            elif similar_category == 'budget':
                return self._get_budget_response()
        
        # Dicas de economia e poupança
        if any(word in message_lower for word in [
            'economizar', 'economia', 'economico', 'economico', 'economico', 'economico',
            'gastar menos', 'gastar menos', 'gastos', 'gasto', 'gastar', 'gastos',
            'poupar', 'poupança', 'poupanca', 'poupando', 'poupar dinheiro', 'guardar dinheiro',
            'cortar gastos', 'reduzir gastos', 'diminuir gastos', 'menos gastos',
            'como economizar', 'dicas para economizar', 'economizar dinheiro',
            'onde economizar', 'como poupar', 'como guardar', 'como cortar gastos',
            'listra de compras', 'compras', 'supermercado', 'mercado',
            'preço', 'preços', 'barato', 'barata', 'desconto', 'descontos',
            'cupom', 'cupons', 'promoção', 'promoções', 'oferta', 'ofertas'
        ]):
            return """💰 **Dicas para Economizar:**

1. **Regra 50/30/20**: 50% para necessidades, 30% para desejos, 20% para poupança
2. **Lista de compras**: Sempre faça lista antes de ir ao mercado
3. **Compare preços**: Use apps como Zoom, Buscapé, Mercado Livre
4. **Evite compras por impulso**: Espere 24h antes de comprar
5. **Negocie contas**: Ligue para operadoras e negocie valores
6. **Use cupons**: Aproveite descontos e promoções
7. **Cozinhe em casa**: Reduza delivery e restaurantes
8. **Aproveite promoções**: Compre produtos não perecíveis em promoção

**Meta:** Tente economizar pelo menos 20% da sua renda mensal!

Quer que eu analise seus gastos para dar dicas mais específicas?"""

        # Dicas de investimentos
        elif any(word in message_lower for word in [
            'investir', 'investimento', 'investimentos', 'investindo', 'investidor', 'investir dinheiro',
            'renda fixa', 'renda variavel', 'renda variável', 'renda-fixa', 'renda-variavel',
            'ações', 'acao', 'acoes', 'bolsa', 'bolsa de valores', 'mercado de ações',
            'fundo', 'fundos', 'fundo de investimento', 'fdi', 'fii', 'fundo imobiliario',
            'tesouro', 'tesouro direto', 'tesouro selic', 'tesouro ipca', 'tdi', 'tselic',
            'cdb', 'lci', 'lca', 'debentures', 'debenture',
            'criptomoeda', 'criptomoedas', 'bitcoin', 'btc', 'ethereum', 'eth',
            'poupança', 'poupanca', 'caderneta de poupança', 'poupança tradicional',
            'onde investir', 'como investir', 'melhor investimento', 'investir melhor',
            'aplicar dinheiro', 'aplicação', 'aplicações', 'onde aplicar', 'como aplicar',
            'rendimento', 'rendimentos', 'rentabilidade', 'lucro', 'lucros', 'ganho', 'ganhos',
            'portfólio', 'portfolio', 'carteira', 'carteira de investimentos',
            'diversificação', 'diversificar', 'diversificar investimentos',
            'perfil', 'perfil de investidor', 'conservador', 'moderado', 'agressivo',
            'risco', 'riscos', 'baixo risco', 'alto risco', 'médio risco'
        ]):
            return """📈 **Guia Completo de Investimentos:**

**🥉 Iniciante (Conservador):**
- Tesouro Selic (100% seguro, liquidez diária)
- CDB de bancos sólidos (até R$ 250k protegido pelo FGC)
- Fundos DI (baixo risco)
- Poupança (só para emergência)

**🥈 Intermediário (Moderado):**
- Ações de empresas sólidas (Blue Chips)
- Fundos de investimento diversificados
- ETFs (Fundos de Índice)
- LCI/LCA (isento de IR)

**🥇 Avançado (Agressivo):**
- Ações individuais de crescimento
- Fundos imobiliários (FIIs)
- Criptomoedas (máximo 5% do patrimônio)
- Fundos multimercado

**💡 Dicas Importantes:**
- Comece sempre com renda fixa
- Diversifique seus investimentos
- Invista regularmente (DCA)
- Nunca invista dinheiro que não pode perder

Qual seu perfil de risco? Conservador, moderado ou agressivo?"""

        # Sair do negativo e dívidas
        elif any(word in message_lower for word in [
            'dívida', 'divida', 'dívidas', 'dividas', 'devendo', 'deve', 'devem', 'dever',
            'negativo', 'negativos', 'saldo negativo', 'conta negativa', 'no vermelho', 'vermelho',
            'sair', 'sair do negativo', 'sair do vermelho', 'sair das dívidas', 'sair das dividas',
            'endividado', 'endividada', 'endividados', 'endividadas', 'endividamento',
            'cartão', 'cartao', 'cartão de crédito', 'cartao de credito', 'limite do cartão',
            'cheque especial', 'cheque especial', 'limite', 'limites',
            'empréstimo', 'emprestimo', 'empréstimos', 'emprestimos', 'financiamento',
            'parcela', 'parcelas', 'parcelado', 'parcelamento', 'dividir em parcelas',
            'juros', 'juros altos', 'taxa alta', 'taxas altas', 'juros do cartão',
            'pagamento', 'pagar', 'pagar dívidas', 'pagar cartão', 'quitar', 'quitar dívidas',
            'renegociar', 'renegociação', 'negociar dívida', 'refinanciar',
            'consolidar', 'consolidação', 'juntar dívidas', 'unificar dívidas',
            'como sair', 'sair do buraco', 'sair do sufoco', 'resolver dívidas',
            'problema financeiro', 'problemas financeiros', 'dificuldade financeira',
            'nome sujo', 'spc', 'serasa', 'protesto', 'protestado'
        ]):
            return """🚨 **Plano Completo para Sair do Negativo:**

**📋 Passo 1 - Organize (Auditoria):**
- Liste TODAS as dívidas com valores e juros
- Priorize pelas taxas de juros (mais altas primeiro)
- Calcule quanto pode pagar por mês

**✂️ Passo 2 - Corte Gastos (Austeridade):**
- Elimine gastos desnecessários (assinaturas, delivery)
- Renegocie todas as dívidas (taxas menores, prazos maiores)
- Use a regra 50/30/20: 50% necessidades, 30% dívidas, 20% emergência

**💪 Passo 3 - Aumente Renda:**
- Venda itens não usados (OLX, Marketplace)
- Faça freelances ou trabalhos extras
- Peça aumento ou promoção no trabalho
- Considere mudança de emprego se necessário

**⚡ Passo 4 - Estratégias de Pagamento:**
- **Método Avalanche**: Pague a dívida com maior juros primeiro
- **Método Bola de Neve**: Pague a menor dívida primeiro (motivação)
- **Consolidação**: Junte dívidas em uma só com juros menor

**🎯 Meta:** Fique livre de dívidas em até 24 meses!

Quer que eu ajude a criar um plano específico baseado nas suas dívidas?"""

        # Metas financeiras
        elif any(word in message_lower for word in [
            'meta', 'metas', 'objetivo', 'objetivos', 'sonho', 'sonhos', 'sonhar',
            'conseguir', 'alcançar', 'alcançar', 'atingir', 'atingir metas',
            'comprar', 'compra', 'adquirir', 'adquirir', 'ter', 'possuir',
            'realizar', 'realização', 'concretizar', 'materializar',
            'plano', 'planos', 'planejamento', 'planejar', 'organizar',
            'projeto', 'projetos', 'projetar', 'futuro', 'futuros',
            'carro', 'casa', 'apartamento', 'imóvel', 'casa própria',
            'viagem', 'viagens', 'viajar', 'férias', 'ferias',
            'curso', 'cursos', 'estudar', 'estudos', 'educação', 'educacao',
            'casar', 'casamento', 'casamentos', 'noivado', 'noivos',
            'filho', 'filhos', 'família', 'familia', 'criança', 'crianças',
            'aposentadoria', 'aposentar', 'aposentado', 'aposentados',
            'independência', 'independencia', 'independência financeira',
            'liberdade', 'liberdade financeira', 'vida tranquila',
            'reserva', 'reservas', 'fundo de emergência', 'fundo de emergencia',
            'segurança', 'seguranca', 'segurança financeira', 'tranquilidade'
        ]):
            return """🎯 **Como Definir e Alcançar Metas Financeiras:**

**🎯 Método SMART:**
- **S**pecífica: "Comprar um carro usado"
- **M**ensurável: "R$ 30.000"
- **A**tingível: Baseado na sua renda atual
- **R**elevante: Importante para sua qualidade de vida
- **T**emporal: "Em 18 meses"

**💰 Tipos de Metas:**
- **Curto prazo** (até 1 ano): Emergência, viagem, móveis
- **Médio prazo** (1-5 anos): Carro, casa, educação
- **Longo prazo** (5+ anos): Aposentadoria, casa própria

**📈 Estratégias de Alcance:**
1. **Quebre em metas menores**: R$ 30k em 18 meses = R$ 1.667/mês
2. **Automatize a poupança**: Débito automático todo dia 5
3. **Acompanhe o progresso**: Revise mensalmente
4. **Celebre vitórias**: Cada 25% conquistado
5. **Ajuste quando necessário**: Seja flexível mas disciplinado

**🏆 Dicas Extras:**
- Tenha sempre uma meta de emergência (6 meses de gastos)
- Use apps de controle para acompanhar
- Mantenha a motivação visualizando o objetivo

Qual sua meta financeira principal? Vou te ajudar a calcular quanto poupar por mês!"""

        # Orçamento e controle financeiro
        elif any(word in message_lower for word in [
            'orçamento', 'orcamento', 'orçamentos', 'orcamentos', 'budget',
            'controle', 'controlar', 'controles', 'controle financeiro',
            'planejamento', 'planejar', 'planejamentos', 'planificar',
            'organizar', 'organização', 'organizacao', 'organizar finanças',
            'gerenciar', 'gerenciamento', 'gerenciar dinheiro', 'administrar',
            'administração', 'administracao', 'administrar finanças',
            'controle de gastos', 'controlar gastos', 'gastos', 'gasto',
            'receitas', 'receita', 'renda', 'rendas', 'salário', 'salario',
            'despesas', 'despesa', 'gastos mensais', 'gastos do mês',
            'balanço', 'balanco', 'balanço financeiro', 'saldo', 'saldos',
            'planilha', 'planilhas', 'planilha de gastos', 'planilha financeira',
            'app', 'aplicativo', 'aplicativos', 'app de controle',
            'mobills', 'guiabolso', 'organizze', 'minhas economias',
            'categoria', 'categorias', 'categorizar', 'separar gastos',
            'limite', 'limites', 'limite de gastos', 'limite mensal',
            'fundo de emergência', 'fundo de emergencia', 'reserva', 'reservas'
        ]):
            return """📊 **Controle Financeiro Completo:**

**📋 Orçamento 50/30/20:**
- **50% Necessidades**: Aluguel, comida, transporte, saúde
- **30% Desejos**: Lazer, hobbies, entretenimento
- **20% Poupança**: Emergência, investimentos, metas

**📱 Ferramentas Essenciais:**
- **Planilha Excel/Google Sheets** (gratuita)
- **App Mobills** (controle completo)
- **App Guiabolso** (conecta contas bancárias)
- **Planilha própria** (mais controle)

**📈 Controle Mensal:**
1. **Receitas**: Salário, freelances, rendimentos
2. **Despesas Fixas**: Aluguel, contas, parcelas
3. **Despesas Variáveis**: Alimentação, transporte, lazer
4. **Saldo**: Receitas - Despesas = Poupança

**🎯 Dicas de Organização:**
- Anote TODOS os gastos (mesmo R$ 5)
- Revise semanalmente seu orçamento
- Use categorias claras (Alimentação, Transporte, Lazer)
- Estabeleça limites por categoria
- Use envelope virtual para cada categoria

**📉 Red Flags (Sinais de Alerta):**
- Gastando mais de 30% em cartão de crédito
- Não sobra nada no final do mês
- Dependendo de empréstimo para necessidades básicas

Quer que eu te ajude a criar um orçamento personalizado?"""

        # Aposentadoria e planejamento de longo prazo
        elif any(word in message_lower for word in [
            'aposentadoria', 'aposentar', 'aposentado', 'aposentados', 'aposentadas',
            'futuro', 'futuros', 'futuro financeiro', 'futuro da aposentadoria',
            'longo prazo', 'longo-prazo', 'investimento longo prazo', 'planejamento longo prazo',
            'pensão', 'pensoes', 'pensao', 'pensoes', 'aposentadoria pública',
            'inss', 'previdência', 'previdencia', 'previdência social', 'previdencia social',
            'previdência privada', 'previdencia privada', 'pgbl', 'vgbl',
            'regra dos 25x', 'regra 25x', '25 vezes', '25x', 'regra dos 4%',
            'independência financeira', 'independencia financeira', 'fi', 'fire',
            'renda passiva', 'rendas passivas', 'viver de renda', 'viver de dividendos',
            'patrimônio', 'patrimonio', 'patrimônio para aposentadoria',
            'reserva para aposentadoria', 'dinheiro para aposentadoria',
            'quanto preciso para aposentar', 'quanto preciso aposentar',
            'plano de aposentadoria', 'planejamento aposentadoria'
        ]):
            return """👴 **Planejamento para Aposentadoria:**

**⏰ Comece AGORA!** Quanto mais cedo, melhor o resultado.

**💰 Quanto Preciso?**
- **Regra dos 25x**: 25 vezes seu gasto anual
- **Exemplo**: Gasta R$ 50k/ano → precisa de R$ 1,25 milhão
- **Regra dos 4%**: Pode sacar 4% ao ano sem comprometer o capital

**📈 Estratégias por Idade:**
- **20-30 anos**: 15-20% da renda em investimentos agressivos
- **30-40 anos**: 20-25% da renda, equilíbrio risco/retorno
- **40-50 anos**: 25-30% da renda, mais conservador
- **50+ anos**: Foco em preservação de capital

**🏦 Onde Investir para Aposentadoria:**
- **Tesouro IPCA+** (proteção inflação)
- **Fundos de Previdência** (PGBL/VGBL)
- **Ações de dividendos** (renda passiva)
- **Fundos Imobiliários** (FIIs)
- **Fundos de Investimento** (diversificados)

**🎯 Plano de Ação:**
1. Calcule quanto precisa (regra dos 25x)
2. Defina quanto pode investir por mês
3. Use investimentos automáticos (DCA)
4. Revise anualmente e ajuste
5. Não retire antes do tempo (juros compostos)

**💡 Dica Ouro**: Comece com R$ 500/mês aos 25 anos = R$ 1,5 milhão aos 65!

Quer que eu calcule quanto você precisa para sua aposentadoria?"""

        # Educação financeira
        elif any(word in message_lower for word in ['educação', 'aprender', 'curso', 'estudar', 'conhecimento']):
            return """📚 **Educação Financeira - Por Onde Começar:**

**📖 Livros Essenciais:**
- "Pai Rico, Pai Pobre" - Robert Kiyosaki
- "Os Segredos da Mente Milionária" - T. Harv Eker
- "Investimentos Inteligentes" - Gustavo Cerbasi
- "Casais Inteligentes Enriquecem Juntos" - Gustavo Cerbasi

**🎥 Canais YouTube (Gratuitos):**
- **Primo Rico** (Thiago Nigro)
- **Me Poupe!** (Nathalia Arcuri)
- **O Primo Rico** (Thiago Nigro)
- **Nath Finanças** (Nathalia Rodrigues)

**📱 Apps Educativos:**
- **Nubank** (conteúdo educativo)
- **XP Educação** (cursos gratuitos)
- **B3 Educação** (mercado financeiro)
- **Anbima** (conceitos financeiros)

**🎓 Cursos Online:**
- **XP Educação** (gratuitos e pagos)
- **CVM Educação** (regulador do mercado)
- **Anbima** (certificações)
- **Coursera/edX** (universidades internacionais)

**📊 Conceitos Básicos para Dominar:**
1. **Juros compostos** (o maior aliado)
2. **Inflação** (inimigo silencioso)
3. **Diversificação** (não coloque ovos na mesma cesta)
4. **Liquidez** (acesso ao dinheiro)
5. **Risco vs Retorno** (quanto mais risco, mais retorno)

**🎯 Plano de Estudos (30 dias):**
- Semana 1: Orçamento e controle de gastos
- Semana 2: Fundo de emergência e poupança
- Semana 3: Investimentos básicos (renda fixa)
- Semana 4: Investimentos avançados (renda variável)

Quer que eu crie um plano de estudos personalizado para você?"""

        # Impostos e tributação
        elif any(word in message_lower for word in [
            'imposto', 'impostos', 'ir', 'imposto de renda', 'imposto de renda',
            'tributo', 'tributos', 'tributação', 'tributacao', 'tributario',
            'receita federal', 'receita', 'declaração', 'declaracao', 'declarar ir',
            'dedução', 'deducao', 'deduções', 'deducoes', 'deduzir',
            'isenção', 'isencao', 'isento', 'isenta', 'isentos',
            'alíquota', 'aliquota', 'alíquotas', 'aliquotas', 'faixa',
            'restituição', 'restituicao', 'restituir', 'devolução', 'devolucao',
            'carnê-leão', 'carne leao', 'carnê leão', 'carnê leao',
            'informe', 'informes', 'informe de rendimentos',
            'cpf', 'pis', 'pis/pasep', 'inss', 'contribuição', 'contribuicao',
            'dar', 'dar imposto', 'dar ir', 'declarar', 'declaracao',
            'imposto sobre investimentos', 'imposto investimentos',
            'iof', 'iof', 'cpmf', 'cide', 'cofins', 'pis', 'pasep'
        ]):
            return """🧾 **Impostos e Tributação - Guia Completo:**

**📋 Imposto de Renda (IR):**
- **Isento**: Renda até R$ 2.112/mês (2024)
- **7,5%**: R$ 2.112 a R$ 2.826
- **15%**: R$ 2.826 a R$ 3.751
- **22,5%**: R$ 3.751 a R$ 4.664
- **27,5%**: Acima de R$ 4.664

**💰 Deduções Importantes:**
- **Educação**: Até R$ 3.561/ano por dependente
- **Saúde**: Sem limite (comprovado)
- **Previdência Privada**: Até 12% da renda bruta
- **Dependentes**: R$ 2.275 por dependente

**📈 Impostos sobre Investimentos:**
- **Ações**: 15% sobre lucro (acima de R$ 20k/mês)
- **Fundos**: 15% sobre resgate (acima de R$ 20k/mês)
- **Tesouro**: 15% sobre resgate
- **CDB/LCI/LCA**: 15% sobre resgate (LCI/LCA isentos)

**💡 Estratégias Legais de Redução:**
1. **Previdência Privada**: Reduz IR e investe
2. **LCI/LCA**: Isentos de IR
3. **Fundos Imobiliários**: Dividendos isentos
4. **Planejamento**: Distribua vendas ao longo do ano

**📅 Cronograma Anual:**
- **Janeiro**: Receba informes de rendimentos
- **Março**: Declare IR (prazo limite)
- **Dezembro**: Planeje para o próximo ano

**⚠️ Cuidados:**
- Mantenha todos os comprovantes
- Use software oficial da Receita
- Consulte contador para casos complexos
- Não tente "burlar" o sistema

Quer ajuda para otimizar sua declaração de IR?"""

        # Empreendedorismo e renda extra
        elif any(word in message_lower for word in ['empreendedor', 'negócio', 'empresa', 'renda extra', 'freelance']):
            return """🚀 **Empreendedorismo e Renda Extra:**

**💼 Ideias de Renda Extra (Baixo Investimento):**
- **Freelance**: Design, programação, redação, tradução
- **E-commerce**: Revenda produtos online
- **Serviços**: Aulas particulares, consultoria
- **Conteúdo**: YouTube, blog, podcast
- **Afiliados**: Indique produtos e ganhe comissão

**📊 Planejamento Financeiro Empresarial:**
- **Separe contas**: Pessoal vs empresarial
- **Reserve impostos**: 15-30% para IR e contribuições
- **Fundo de emergência**: 6 meses de despesas
- **Reinvista lucros**: Cresça o negócio primeiro

**📈 Escala de Negócios:**
1. **Início**: Trabalhe sozinho, baixo investimento
2. **Crescimento**: Contrate freelancers, automação
3. **Expansão**: Equipe fixa, múltiplos produtos
4. **Escala**: Franquias, licenciamento, venda

**💰 Gestão Financeira Empresarial:**
- **Fluxo de caixa**: Controle entradas e saídas
- **Margem de lucro**: Mínimo 30%
- **Capital de giro**: 3-6 meses de despesas
- **Reserva para crescimento**: 20% dos lucros

**🎯 Dicas de Ouro:**
- Comece pequeno, pense grande
- Valide a ideia antes de investir muito
- Foque no cliente, não no produto
- Aprenda vendas (essencial!)
- Networking é fundamental

**⚠️ Armadilhas a Evitar:**
- Misturar dinheiro pessoal com empresarial
- Não reservar para impostos
- Gastar lucros antes de consolidar
- Não ter plano B

Qual área te interessa mais? Vou te dar dicas específicas!"""

        # Imóveis e patrimônio
        elif any(word in message_lower for word in ['casa', 'imóvel', 'comprar casa', 'financiamento', 'patrimônio']):
            return """🏠 **Imóveis e Patrimônio - Guia Completo:**

**💰 Financiamento vs Aluguel:**
- **Financiamento**: Construção de patrimônio, valorização
- **Aluguel**: Flexibilidade, dinheiro livre para investir
- **Regra**: Aluguel < 30% da renda + tenha entrada de 20%

**📊 Análise de Compra:**
- **Entrada**: Mínimo 20% do valor
- **Prestação**: Máximo 30% da renda bruta
- **Taxa**: Compare CET (Custo Efetivo Total)
- **Prazo**: Máximo 30 anos (ideal 20-25)

**🏦 Tipos de Financiamento:**
- **SBPE**: Taxa fixa, juros mais baixos
- **SFH**: Taxa variável, juros mais altos
- **Financiamento Direto**: Bancos privados
- **Leasing Imobiliário**: Para empresas

**📈 Estratégias de Investimento Imobiliário:**
1. **Casa própria**: Primeiro imóvel, estabilidade
2. **Aluguel**: Segunda propriedade, renda passiva
3. **Fundos Imobiliários**: Liquidez, diversificação
4. **Terrenos**: Alto risco, alto retorno

**🎯 Plano de Ação:**
1. **Junte a entrada**: 20% do valor do imóvel
2. **Melhore o score**: Pagamentos em dia, cartões
3. **Compare ofertas**: Pelo menos 3 bancos
4. **Negocie**: Taxa, prazo, seguro
5. **Documente tudo**: Contratos, escrituras

**💡 Dicas Importantes:**
- **Localização**: Mais importante que o imóvel
- **Documentação**: Verifique se está regular
- **Avaliação**: Contrate avaliação independente
- **Seguro**: Proteja seu investimento
- **Manutenção**: Reserve 1% do valor/ano

**⚠️ Cuidados:**
- Não comprometa mais de 30% da renda
- Tenha fundo de emergência antes de comprar
- Considere custos extras (IPTU, condomínio, manutenção)
- Avalie se realmente precisa comprar agora

Quer ajuda para calcular se vale mais financiar ou continuar alugando?"""

        # Cálculos financeiros
        elif any(word in message_lower for word in [
            'calcular', 'calculo', 'calcular', 'conta', 'contas', 'contar',
            'quanto', 'quantos', 'quanto custa', 'quanto preciso', 'quanto vale',
            'valor', 'valores', 'preço', 'preços', 'custo', 'custos',
            'prestação', 'prestacoes', 'prestação', 'parcela', 'parcelas',
            'juros', 'taxa', 'taxas', 'taxa de juros', 'juros compostos',
            'financiamento', 'financiamentos', 'emprestimo', 'empréstimo',
            'investimento', 'investir', 'aplicação', 'aplicar',
            'poupança', 'poupanca', 'guardar', 'economizar',
            'meta', 'metas', 'objetivo', 'objetivos',
            'aposentadoria', 'aposentar', 'futuro',
            'simulação', 'simulacao', 'simular', 'projeção', 'projecao',
            'cálculo', 'calculo', 'matemática', 'matematica',
            'formula', 'fórmula', 'equação', 'equacao'
        ]):
            return """🧮 **Calculadora Financeira FinBot:**

Posso calcular para você:

**💰 Cálculos Básicos:**
• Juros compostos e simples
• Valor futuro de investimentos
• Parcelas de financiamento
• Valor presente líquido

**🏠 Financiamento Imobiliário:**
• Prestação mensal
• Custo efetivo total (CET)
• Comparação de taxas
• Valor da entrada necessária

**📈 Investimentos:**
• Retorno de investimentos
• Meta de poupança mensal
• Tempo para atingir meta
• Aposentadoria necessária

**🎯 Metas Financeiras:**
• Quanto poupar por mês
• Tempo para atingir objetivo
• Valor necessário para meta
• Progresso atual vs meta

**💳 Cartão de Crédito:**
• Juros rotativos
• Parcelamento vs à vista
• Taxa efetiva anual
• Tempo para quitar dívida

**📊 Orçamento:**
• Percentual da renda por categoria
• Valor máximo por categoria
• Economia mensal necessária
• Projeção de gastos anuais

**🔢 Exemplos de Perguntas:**
• "Quanto preciso poupar por mês para ter R$ 50.000 em 2 anos?"
• "Qual a prestação de um financiamento de R$ 300.000 em 30 anos?"
• "Quanto vou ter se investir R$ 500/mês por 20 anos?"
• "Qual o juros real de um investimento que rende 12% ao ano?"

**Para calcular, me diga:**
• Tipo de cálculo que precisa
• Valores envolvidos
• Período de tempo
• Taxa de juros (se aplicável)

Que cálculo posso fazer para você?"""

        # Resposta padrão expandida
        else:
            return """👋 **Olá! Sou seu assistente financeiro FinBot!**

Posso te ajudar com uma ampla variedade de tópicos:

**💰 Gestão Financeira:**
• Orçamento e controle de gastos
• Dicas para economizar e poupar
• Planejamento financeiro pessoal

**📈 Investimentos:**
• Renda fixa e variável
• Perfil de investidor
• Estratégias de diversificação

**🚨 Dívidas e Crédito:**
• Planos para sair do negativo
• Renegociação de dívidas
• Uso inteligente do cartão

**🎯 Metas e Sonhos:**
• Como definir metas SMART
• Estratégias para alcançar objetivos
• Planejamento de aposentadoria

**🏠 Patrimônio:**
• Financiamento de imóveis
• Análise compra vs aluguel
• Investimentos imobiliários

**🧾 Impostos:**
• Otimização do IR
• Tributação de investimentos
• Deduções e isenções

**🚀 Empreendedorismo:**
• Ideias de renda extra
• Planejamento empresarial
• Gestão financeira de negócios

**📚 Educação:**
• Conceitos financeiros básicos
• Livros e cursos recomendados
• Ferramentas de controle

**🧮 Cálculos Financeiros:**
• Juros compostos e parcelas
• Meta de poupança mensal
• Financiamentos e investimentos
• Projeções financeiras

**💡 Dicas Personalizadas:**
• Análise da sua situação atual
• Cálculos específicos
• Planos de ação customizados

O que você gostaria de saber? Seja específico na sua pergunta para receber a melhor orientação!"""
    
    def get_financial_advice(self, user_context):
        """Obtém conselhos financeiros personalizados"""
        if not self.chat:
            return self._get_fallback_response("conselho financeiro")
        
        prompt = f"""
        Você é um assistente financeiro especializado. 
        Com base no seguinte contexto do usuário, forneça conselhos financeiros relevantes:
        
        {user_context}
        
        Por favor, forneça:
        1. Análise da situação atual
        2. Sugestões de melhorias
        3. Recomendações de investimentos
        4. Dicas para economizar
        """
        
        try:
            response = self.chat.send_message(prompt)
            return response.text
        except Exception as e:
            return f"Desculpe, ocorreu um erro ao processar sua solicitação: {str(e)}"
    
    def get_investment_suggestions(self, user_profile):
        """Obtém sugestões de investimento baseadas no perfil do usuário"""
        if not self.chat:
            return self._get_fallback_response("investimentos")
        
        prompt = f"""
        Você é um consultor de investimentos. 
        Analise o seguinte perfil do usuário e sugira opções de investimento adequadas:
        
        {user_profile}
        
        Por favor, considere:
        1. Perfil de risco
        2. Objetivos financeiros
        3. Horizonte de tempo
        4. Conhecimento em investimentos
        
        Forneça sugestões detalhadas e explique os riscos envolvidos.
        """
        
        try:
            response = self.chat.send_message(prompt)
            return response.text
        except Exception as e:
            return f"Desculpe, ocorreu um erro ao processar sua solicitação: {str(e)}"
    
    def get_budgeting_tips(self, spending_patterns):
        """Obtém dicas de orçamento baseadas nos padrões de gastos"""
        if not self.chat:
            return self._get_fallback_response("orçamento")
        
        prompt = f"""
        Você é um especialista em orçamento pessoal.
        Analise os seguintes padrões de gastos e forneça dicas para melhorar o orçamento:
        
        {spending_patterns}
        
        Por favor, sugira:
        1. Áreas para redução de gastos
        2. Estratégias de economia
        3. Prioridades de gastos
        4. Metas realistas de economia
        """
        
        try:
            response = self.chat.send_message(prompt)
            return response.text
        except Exception as e:
            return f"Desculpe, ocorreu um erro ao processar sua solicitação: {str(e)}"
    
    def get_debt_management_advice(self, debt_info):
        """Obtém conselhos para gerenciamento de dívidas"""
        if not self.chat:
            return self._get_fallback_response("dívidas")
        
        prompt = f"""
        Você é um especialista em gerenciamento de dívidas.
        Analise a seguinte situação de dívidas e forneça um plano de ação:
        
        {debt_info}
        
        Por favor, inclua:
        1. Estratégia de pagamento
        2. Priorização de dívidas
        3. Dicas para negociação
        4. Prevenção de novas dívidas
        """
        
        try:
            response = self.chat.send_message(prompt)
            return response.text
        except Exception as e:
            return f"Desculpe, ocorreu um erro ao processar sua solicitação: {str(e)}"
    
    def calculate_compound_interest(self, principal, rate, time, monthly_contribution=0):
        """Calcula juros compostos"""
        try:
            # Converte taxa anual para mensal
            monthly_rate = rate / 12 / 100
            
            # Calcula valor futuro
            future_value = principal * ((1 + monthly_rate) ** (time * 12))
            
            # Adiciona contribuições mensais
            if monthly_contribution > 0:
                future_value += monthly_contribution * (((1 + monthly_rate) ** (time * 12) - 1) / monthly_rate)
            
            return future_value
        except Exception as e:
            return None
    
    def calculate_loan_payment(self, principal, rate, time):
        """Calcula prestação de financiamento"""
        try:
            # Converte taxa anual para mensal
            monthly_rate = rate / 12 / 100
            
            # Fórmula da prestação
            payment = principal * (monthly_rate * (1 + monthly_rate) ** (time * 12)) / ((1 + monthly_rate) ** (time * 12) - 1)
            
            return payment
        except Exception as e:
            return None
    
    def calculate_retirement_needed(self, annual_expenses, years_to_retirement):
        """Calcula quanto precisa para aposentadoria"""
        try:
            # Regra dos 25x + crescimento
            needed_amount = annual_expenses * 25
            
            # Ajusta pela inflação (assumindo 4% ao ano)
            inflation_rate = 0.04
            adjusted_amount = needed_amount * ((1 + inflation_rate) ** years_to_retirement)
            
            return adjusted_amount
        except Exception as e:
            return None
    
    def calculate_monthly_savings_needed(self, goal_amount, current_amount, years, annual_return=0.08):
        """Calcula quanto precisa poupar por mês para atingir uma meta"""
        try:
            monthly_return = annual_return / 12
            
            # Se já tem valor inicial
            if current_amount > 0:
                future_current = current_amount * ((1 + monthly_return) ** (years * 12))
                remaining_needed = goal_amount - future_current
            else:
                remaining_needed = goal_amount
            
            # Calcula contribuição mensal necessária
            if remaining_needed > 0:
                monthly_savings = remaining_needed / (((1 + monthly_return) ** (years * 12) - 1) / monthly_return)
            else:
                monthly_savings = 0
            
            return max(0, monthly_savings)
        except Exception as e:
            return None
    
    def parse_financial_calculation(self, message):
        """Analisa a mensagem e executa cálculos financeiros"""
        message_lower = message.lower()
        
        # Extrai números da mensagem
        import re
        numbers = re.findall(r'\d+(?:\.\d+)?', message)
        
        if not numbers:
            return "Para calcular, preciso dos valores! Exemplo: 'Quanto preciso poupar por mês para ter R$ 50000 em 2 anos?'"
        
        try:
            # Meta de poupança
            if any(word in message_lower for word in ['poupar', 'economizar', 'juntar']):
                if len(numbers) >= 2:
                    goal = float(numbers[0]) * 1000 if len(numbers[0]) == 2 else float(numbers[0])
                    years = float(numbers[1]) if len(numbers) > 1 else 1
                    
                    monthly_needed = self.calculate_monthly_savings_needed(goal, 0, years)
                    
                    if monthly_needed:
                        return f"""💰 **Cálculo de Poupança:**

**Meta:** R$ {goal:,.2f}
**Tempo:** {years:.0f} anos
**Investimento mensal necessário:** R$ {monthly_needed:,.2f}

**💡 Dicas:**
• Automatize o investimento mensal
• Use investimentos com rendimento de 8-12% ao ano
• Revise anualmente e ajuste conforme necessário

**Alternativas:**
• Aumentar o prazo reduz o valor mensal
• Começar com menos e aumentar gradualmente
• Buscar renda extra para acelerar o processo"""
            
            # Financiamento
            elif any(word in message_lower for word in ['financiamento', 'prestação', 'parcela']):
                if len(numbers) >= 3:
                    principal = float(numbers[0]) * 1000 if len(numbers[0]) <= 3 else float(numbers[0])
                    rate = float(numbers[1])
                    years = float(numbers[2])
                    
                    payment = self.calculate_loan_payment(principal, rate, years)
                    
                    if payment:
                        total_paid = payment * years * 12
                        total_interest = total_paid - principal
                        
                        return f"""🏠 **Cálculo de Financiamento:**

**Valor financiado:** R$ {principal:,.2f}
**Taxa de juros:** {rate:.2f}% ao ano
**Prazo:** {years:.0f} anos

**📊 Resultado:**
• **Prestação mensal:** R$ {payment:,.2f}
• **Total a pagar:** R$ {total_paid:,.2f}
• **Total de juros:** R$ {total_interest:,.2f}
• **CET aproximado:** {rate:.2f}% ao ano

**💡 Dicas:**
• Compare ofertas de pelo menos 3 bancos
• Negocie a taxa de juros
• Considere antecipar parcelas para economizar juros
• Avalie se a prestação não compromete mais de 30% da renda"""
            
            # Investimento com juros compostos
            elif any(word in message_lower for word in ['investir', 'investimento', 'juros compostos']):
                if len(numbers) >= 3:
                    principal = float(numbers[0]) * 1000 if len(numbers[0]) <= 3 else float(numbers[0])
                    rate = float(numbers[1])
                    years = float(numbers[2])
                    monthly = float(numbers[3]) if len(numbers) > 3 else 0
                    
                    future_value = self.calculate_compound_interest(principal, rate, years, monthly)
                    
                    if future_value:
                        total_invested = principal + (monthly * years * 12)
                        profit = future_value - total_invested
                        
                        return f"""📈 **Cálculo de Investimento:**

**Investimento inicial:** R$ {principal:,.2f}
**Contribuição mensal:** R$ {monthly:,.2f}
**Taxa de retorno:** {rate:.2f}% ao ano
**Tempo:** {years:.0f} anos

**💰 Resultado:**
• **Valor final:** R$ {future_value:,.2f}
• **Total investido:** R$ {total_invested:,.2f}
• **Lucro obtido:** R$ {profit:,.2f}
• **Rendimento total:** {(profit/total_invested)*100:.1f}%

**💡 O poder dos juros compostos:**
• Quanto mais tempo, maior o crescimento
• Contribuições regulares aceleram o crescimento
• Começar cedo é a chave do sucesso!"""
            
            # Aposentadoria
            elif any(word in message_lower for word in ['aposentadoria', 'aposentar']):
                if len(numbers) >= 2:
                    annual_expenses = float(numbers[0]) * 1000 if len(numbers[0]) <= 3 else float(numbers[0])
                    years = float(numbers[1])
                    
                    needed = self.calculate_retirement_needed(annual_expenses, years)
                    monthly_needed = self.calculate_monthly_savings_needed(needed, 0, years)
                    
                    if needed and monthly_needed:
                        return f"""👴 **Cálculo de Aposentadoria:**

**Gastos anuais atuais:** R$ {annual_expenses:,.2f}
**Anos para aposentadoria:** {years:.0f} anos

**🎯 Necessário para aposentadoria:**
• **Valor total necessário:** R$ {needed:,.2f}
• **Poupança mensal necessária:** R$ {monthly_needed:,.2f}
• **Regra dos 25x:** 25 vezes seus gastos anuais

**💡 Estratégias:**
• Comece com menos e aumente gradualmente
• Use investimentos de longo prazo (ações, FIIs)
• Considere previdência privada (PGBL/VGBL)
• Revise anualmente e ajuste conforme necessário

**🏆 Meta:** Comece hoje, mesmo que com pouco!"""
            
            return "Consegui identificar os números, mas preciso entender melhor o tipo de cálculo. Pode ser mais específico?"
            
        except Exception as e:
            return f"Desculpe, houve um erro no cálculo. Verifique se os valores estão corretos."