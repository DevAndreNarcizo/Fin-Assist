# Fin-Assist 💰

Sistema completo de gestão financeira pessoal com **IA integrada** desenvolvido em Python. Interface moderna, chatbot inteligente e funcionalidades avançadas para controle total das suas finanças.

## 🌟 **Destaques Principais**

### 🤖 **Chatbot FinBot com IA**

- **Google Gemini AI** integrado para conselhos financeiros personalizados
- **Sistema inteligente** de reconhecimento de frases similares e sinônimos
- **Respostas humanas e naturais** como um consultor financeiro experiente
- **Modo degradado** funciona mesmo sem API key
- **Cálculos financeiros automáticos** (juros compostos, financiamentos, metas)

### 🎨 **Interface Moderna e Intuitiva**

- **CustomTkinter** com tema dark profissional
- **Layout responsivo** com sidebar e área principal
- **Feedback visual** com loading states e mensagens temporárias
- **Design clean** e fácil de usar

### 🔐 **Sistema de Autenticação Seguro**

- **Criptografia bcrypt** para senhas
- **Validação robusta** de email e senha forte
- **Cadastro e login** com verificação de dados

## 🚀 **Funcionalidades Completas**

### 💰 **Gestão Financeira Completa**

- **Transações**: Cadastro, edição e exclusão de receitas, despesas e investimentos
- **Categorias Personalizáveis**: Crie suas próprias categorias para melhor organização
- **Filtros Avançados**: Busque transações por período, tipo e categoria
- **Validação de Dados**: Verificação automática de formatos e valores

### 🎯 **Metas Financeiras Inteligentes**

- **Definição de Objetivos**: Estabeleça metas com prazo e valor alvo
- **Acompanhamento Visual**: Progresso em tempo real com barras de progresso
- **Status Inteligente**: Metas concluídas, em andamento e vencidas
- **Cálculos Automáticos**: Quanto poupar por mês para atingir suas metas

### 📊 **Dashboard Interativo**

- **Resumo Financeiro**: Cards com totais de receitas, despesas e saldo
- **Gráficos Dinâmicos**: Distribuição financeira do mês com gráfico de pizza
- **Ranking de Gastos**: Principais categorias de despesas
- **Atualização em Tempo Real**: Dados sempre atualizados

### 📄 **Relatórios Profissionais**

- **PDF Personalizado**: Relatórios com seleção de período
- **Dados Completos**: Transações e metas em um único documento
- **Interface Intuitiva**: Seleção fácil de datas e local de salvamento
- **Loading States**: Feedback visual durante geração

### 🤖 **Chatbot FinBot - Assistente Financeiro IA**

#### **Capacidades Avançadas:**

- **Análise Financeira**: Analisa receitas, despesas e padrões de gastos
- **Dicas de Economia**: Estratégias práticas para reduzir gastos
- **Orientação de Investimentos**: Conselhos sobre renda fixa e variável
- **Gestão de Dívidas**: Planos para sair do negativo
- **Planejamento de Metas**: Como definir e alcançar objetivos financeiros
- **Educação Financeira**: Conceitos básicos e avançados
- **Cálculos Financeiros**: Juros compostos, financiamentos, aposentadoria

#### **Sistema de Reconhecimento Inteligente:**

- **Palavras Similares**: Reconhece variações (economizar/economizar, poupar/guardar)
- **Frases Completas**: Entende expressões naturais ("como gastar menos dinheiro")
- **Sinônimos**: Compreende linguagem informal e regional
- **Contexto Semântico**: Interpreta intenção mesmo com palavras diferentes

#### **Exemplos de Interação:**

```
Usuário: "Como fazer sobrar dinheiro no final do mês?"
FinBot: "Olha, economizar dinheiro não é um bicho de sete cabeças! Vou te dar umas dicas que realmente funcionam..."

Usuário: "Sair do vermelho do cartão"
FinBot: "Relaxa, sair do negativo é possível sim! Já ajudei muita gente nessa situação..."

Usuário: "Quanto preciso poupar por mês para ter R$ 50.000 em 2 anos?"
FinBot: "Perfeito! Deixa eu calcular pra você: Você precisa guardar R$ 1.042 por mês..."
```

### 📁 **Import/Export de Dados**

- **Exportação CSV**: Transações e metas em formato tabular
- **Importação CSV**: Carregue dados de outros sistemas
- **Backup JSON**: Backup completo de todos os dados
- **Validação de Dados**: Verificação automática de formatos

### ✅ **Validações e UX Avançadas**

- **Validações Robustas**: Email, senha forte, datas e valores
- **Feedback Visual**: Mensagens de sucesso, erro e informação
- **Confirmações**: Diálogos de confirmação para exclusões
- **Loading States**: Indicadores de progresso para operações longas

## 🛠️ **Tecnologias Utilizadas**

- **Python 3.8+**: Linguagem principal
- **CustomTkinter 5.2.1**: Interface gráfica moderna e responsiva
- **SQLite**: Banco de dados local com índices otimizados
- **Google Gemini AI**: Chatbot inteligente com IA
- **Matplotlib 3.8.2**: Geração de gráficos interativos
- **ReportLab 4.1.0**: Criação de relatórios PDF profissionais
- **bcrypt 4.1.2**: Criptografia segura de senhas
- **python-dotenv 1.0.1**: Gerenciamento de variáveis de ambiente
- **Pillow 10.2.0**: Manipulação de imagens

## 📦 **Instalação Rápida**

### **Pré-requisitos**

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### **Passo a Passo**

1. **Clone o repositório:**

```bash
git clone <url-do-repositorio>
cd fin-assist
```

2. **Crie um ambiente virtual:**

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

4. **Configure a API do Gemini (opcional para chatbot):**

```bash
# Crie um arquivo .env na raiz do projeto
echo "GEMINI_API_KEY=sua_chave_aqui" > .env
```

## 🚀 **Execução**

```bash
python main.py
```

## 🧪 **Testes**

Execute todos os testes do projeto:

```bash
python run_tests.py
```

### **Cobertura de Testes**

- ✅ Validações de dados (email, senha, datas, números)
- ✅ Modelo de usuário (criação, autenticação, hash de senha)
- ✅ Banco de dados (estrutura, índices, chaves estrangeiras)
- ✅ Funcionalidades de import/export
- ✅ Sistema de reconhecimento de frases similares

## 📁 **Estrutura do Projeto**

```
fin-assist/
├── main.py                           # Arquivo principal
├── run_tests.py                      # Executor de testes
├── test_similar_phrases.py          # Teste do sistema de IA
├── requirements.txt                  # Dependências
├── README.md                         # Documentação
├── .env                             # Variáveis de ambiente (criar)
├── src/
│   ├── config/                      # Configurações centralizadas
│   │   ├── __init__.py
│   │   └── settings.py              # Configurações do sistema
│   ├── controllers/                 # Lógica de negócio
│   │   ├── chatbot_controller.py    # 🤖 Chatbot IA com Gemini
│   │   ├── goal_controller.py       # Metas financeiras
│   │   ├── transaction_controller.py # Transações
│   │   └── category_controller.py   # Categorias
│   ├── models/                      # Modelos de dados
│   │   └── user.py                  # Modelo de usuário
│   ├── views/                       # Interfaces gráficas
│   │   ├── login_view.py            # Tela de login
│   │   ├── main_view.py             # Interface principal
│   │   └── register_view.py         # Tela de cadastro
│   ├── database/                    # Configuração do banco
│   │   └── database.py              # SQLite setup
│   └── utils/                       # Utilitários
│       ├── chart_generator.py       # Gráficos matplotlib
│       ├── pdf_generator.py         # Relatórios PDF
│       ├── message_utils.py         # Mensagens e validações
│       ├── loading_utils.py         # Loading states
│       ├── data_import_export.py    # Import/Export
│       └── logger.py                # Sistema de logs
├── tests/                           # Testes automatizados
│   ├── __init__.py
│   ├── test_validation_utils.py
│   ├── test_database.py
│   └── test_user_model.py
├── database/                        # Banco de dados SQLite
│   └── fin_assist.db
└── assets/                          # Recursos estáticos
```

## 🎯 **Como Usar o Fin-Assist**

### **1. Primeiro Acesso**

1. Execute `python main.py`
2. Clique em "Cadastre-se" na tela de login
3. Preencha os dados (email, usuário, senha forte)
4. Faça login com suas credenciais

### **2. Interface Principal**

- **Sidebar**: Navegação entre funcionalidades
- **Dashboard**: Visão geral das suas finanças
- **Transações**: Gerencie receitas, despesas e investimentos
- **Metas**: Defina e acompanhe objetivos financeiros
- **Relatórios**: Gere PDFs com seus dados
- **Chatbot**: Converse com o FinBot para conselhos

### **3. Chatbot FinBot**

- **Perguntas Naturais**: "Como economizar mais?", "Sair do vermelho"
- **Cálculos**: "Quanto preciso poupar para ter R$ 30.000 em 2 anos?"
- **Conselhos**: Dicas personalizadas baseadas nos seus dados
- **Respostas Humanas**: Linguagem natural e prática

### **4. Gestão de Transações**

- **Adicionar**: Clique no botão "+" para nova transação
- **Categorias**: Use as existentes ou crie personalizadas
- **Filtros**: Busque por período, tipo ou categoria
- **Editar/Excluir**: Clique na transação para opções

### **5. Metas Financeiras**

- **Criar Meta**: Defina valor, prazo e descrição
- **Acompanhar**: Veja progresso em tempo real
- **Cálculos**: FinBot ajuda a calcular valores mensais

## 🔧 **Configurações Avançadas**

### **Personalização de Categorias**

- Adicione categorias personalizadas clicando no botão "+" ao lado do campo categoria
- Categorias são salvas automaticamente no banco de dados
- Disponível para receitas, despesas e investimentos

### **Chatbot Personalizado**

- Configure `GEMINI_API_KEY` no arquivo `.env` para IA completa
- Sem API key, o chatbot funciona em modo degradado com respostas pré-definidas
- Sistema de reconhecimento de frases similares funciona sempre

### **Importação de Dados**

- Suporte a arquivos CSV com validação automática
- Formato esperado: ID, Tipo, Categoria, Subcategoria, Valor, Descrição, Data
- Relatório detalhado de importação com contagem de sucessos e erros

### **Exportação de Dados**

- **CSV**: Formato tabular para análise em Excel/Google Sheets
- **JSON**: Backup completo com metadados
- **PDF**: Relatórios profissionais com gráficos

## 🐛 **Solução de Problemas**

### **Problemas Comuns**

1. **Erro de instalação do Pillow:**

```bash
pip install --upgrade pip setuptools wheel
pip install Pillow
```

2. **API do Gemini não funciona:**

- Verifique se a chave está no arquivo `.env`
- O chatbot funciona em modo degradado sem API
- Teste com: `python test_similar_phrases.py`

3. **Banco de dados corrompido:**

- Delete o arquivo `database/fin_assist.db`
- Execute novamente para recriar o banco

4. **Interface não carrega:**

- Verifique se todas as dependências foram instaladas
- Execute: `pip install -r requirements.txt`

## 🎉 **Funcionalidades Únicas**

### **🤖 Sistema de IA Avançado**

- **Reconhecimento de 200+ variações** de frases financeiras
- **Respostas contextuais** baseadas nos dados do usuário
- **Cálculos automáticos** de juros, financiamentos e metas
- **Linguagem natural** como um consultor financeiro real

### **🎨 Interface Moderna**

- **Tema dark** profissional
- **Loading states** para melhor UX
- **Feedback visual** em todas as operações
- **Layout responsivo** e intuitivo

### **🔐 Segurança Avançada**

- **Criptografia bcrypt** para senhas
- **Validação robusta** de todos os dados
- **Banco SQLite** local e seguro

## 🤝 **Contribuição**

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### **Padrões de Código**

- Use type hints quando possível
- Documente funções complexas
- Adicione testes para novas funcionalidades
- Siga o padrão de nomenclatura do projeto

## 📄 **Licença**

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 **Suporte**

Para dúvidas ou sugestões, abra uma issue no repositório ou entre em contato através do email: [dev.andrenarcizo@gmail.com]

---

**Desenvolvido com ❤️ por Dev. André Narcizo**

_Transformando gestão financeira pessoal com IA e tecnologia moderna_ 🚀
