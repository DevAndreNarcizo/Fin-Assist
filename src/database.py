import sqlite3
import json
from datetime import datetime, date
import os


class DatabaseManager:
    def __init__(self):
        self.db_file = 'fin_assist.db'
        self.init_database()

    def init_database(self):
        """Inicializa o banco de dados com todas as tabelas necessárias"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # Tabela de usuários
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                data_criacao DATE NOT NULL
            )
        ''')

        # Tabela de transações
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descricao TEXT NOT NULL,
                valor REAL NOT NULL,
                categoria TEXT NOT NULL,
                tipo TEXT NOT NULL,
                data DATE NOT NULL,
                usuario_id INTEGER,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')

        # Tabela de orçamentos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orcamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                categoria TEXT NOT NULL,
                valor REAL NOT NULL,
                mes INTEGER NOT NULL,
                ano INTEGER NOT NULL,
                usuario_id INTEGER,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')

        # Tabela de metas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                valor_meta REAL NOT NULL,
                valor_atual REAL NOT NULL,
                data_inicio DATE NOT NULL,
                data_fim DATE NOT NULL,
                usuario_id INTEGER,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')

        # Tabela de investimentos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS investimentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL,
                valor REAL NOT NULL,
                rentabilidade REAL NOT NULL,
                data_inicio DATE NOT NULL,
                usuario_id INTEGER,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')

        # Tabela de contas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                tipo TEXT NOT NULL,
                banco TEXT NOT NULL,
                saldo REAL NOT NULL,
                usuario_id INTEGER,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')

        # Tabela de cartões
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cartoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                tipo TEXT NOT NULL,
                banco TEXT NOT NULL,
                limite REAL NOT NULL,
                dia_fechamento INTEGER NOT NULL,
                dia_vencimento INTEGER NOT NULL,
                usuario_id INTEGER,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')

        # Tabela de lembretes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lembretes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descricao TEXT,
                valor REAL NOT NULL,
                data DATE NOT NULL,
                categoria TEXT NOT NULL,
                recorrencia TEXT NOT NULL,
                usuario_id INTEGER,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')

        # Tabela de dicas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dicas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                conteudo TEXT NOT NULL,
                categoria TEXT NOT NULL,
                data_criacao DATE NOT NULL
            )
        ''')

        conn.commit()
        conn.close()

    def register_user(self, nome, email, senha):
        """Registra um novo usuário"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO usuarios (nome, email, senha, data_criacao)
                VALUES (?, ?, ?, ?)
            ''', (nome, email, senha, date.today()))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Erro ao registrar usuário: {str(e)}")
            return False

    def verify_credentials(self, email, senha):
        """Verifica as credenciais do usuário"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT id FROM usuarios
                WHERE email = ? AND senha = ?
            ''', (email, senha))

            result = cursor.fetchone()
            conn.close()

            return result is not None

        except Exception as e:
            print(f"Erro ao verificar credenciais: {str(e)}")
            return False

    def get_resumo_financeiro(self):
        """Retorna um resumo das finanças do usuário"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            # Obter saldo total
            cursor.execute('''
                SELECT SUM(saldo) FROM contas
            ''')
            saldo_total = cursor.fetchone()[0] or 0

            # Obter receitas do mês
            cursor.execute('''
                SELECT SUM(valor) FROM transacoes
                WHERE tipo = 'Receita'
                AND strftime('%Y-%m', data) = strftime('%Y-%m', 'now')
            ''')
            receitas = cursor.fetchone()[0] or 0

            # Obter despesas do mês
            cursor.execute('''
                SELECT SUM(valor) FROM transacoes
                WHERE tipo = 'Despesa'
                AND strftime('%Y-%m', data) = strftime('%Y-%m', 'now')
            ''')
            despesas = cursor.fetchone()[0] or 0

            # Obter despesas por categoria
            cursor.execute('''
                SELECT categoria, SUM(valor) FROM transacoes
                WHERE tipo = 'Despesa'
                AND strftime('%Y-%m', data) = strftime('%Y-%m', 'now')
                GROUP BY categoria
            ''')
            despesas_por_categoria = dict(cursor.fetchall())

            conn.close()

            return {
                'saldo_total': saldo_total,
                'receitas': receitas,
                'despesas': despesas,
                'despesas_por_categoria': despesas_por_categoria
            }

        except Exception as e:
            print(f"Erro ao obter resumo financeiro: {str(e)}")
            return {
                'saldo_total': 0,
                'receitas': 0,
                'despesas': 0,
                'despesas_por_categoria': {}
            }

    def add_transacao(self, descricao, valor, categoria, tipo, data):
        """Adiciona uma nova transação"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO transacoes (descricao, valor, categoria, tipo, data)
                VALUES (?, ?, ?, ?, ?)
            ''', (descricao, valor, categoria, tipo, data))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Erro ao adicionar transação: {str(e)}")
            return False

    def get_transacoes(self):
        """Retorna todas as transações"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT * FROM transacoes
                ORDER BY data DESC
            ''')

            transacoes = []
            for row in cursor.fetchall():
                transacoes.append({
                    'id': row[0],
                    'descricao': row[1],
                    'valor': row[2],
                    'categoria': row[3],
                    'tipo': row[4],
                    'data': datetime.strptime(row[5], '%Y-%m-%d').date()
                })

            conn.close()
            return transacoes

        except Exception as e:
            print(f"Erro ao obter transações: {str(e)}")
            return []

    def add_orcamento(self, categoria, valor):
        """Adiciona um novo orçamento"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            hoje = date.today()
            cursor.execute('''
                INSERT INTO orcamentos (categoria, valor, mes, ano)
                VALUES (?, ?, ?, ?)
            ''', (categoria, valor, hoje.month, hoje.year))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Erro ao adicionar orçamento: {str(e)}")
            return False

    def get_orcamentos(self):
        """Retorna todos os orçamentos"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            hoje = date.today()
            cursor.execute('''
                SELECT * FROM orcamentos
                WHERE mes = ? AND ano = ?
            ''', (hoje.month, hoje.year))

            orcamentos = []
            for row in cursor.fetchall():
                # Calcular gasto na categoria
                cursor.execute('''
                    SELECT SUM(valor) FROM transacoes
                    WHERE categoria = ? AND tipo = 'Despesa'
                    AND strftime('%Y-%m', data) = strftime('%Y-%m', 'now')
                ''', (row[1],))
                gasto = cursor.fetchone()[0] or 0

                orcamentos.append({
                    'id': row[0],
                    'categoria': row[1],
                    'valor': row[2],
                    'gasto': gasto,
                    'restante': row[2] - gasto
                })

            conn.close()
            return orcamentos

        except Exception as e:
            print(f"Erro ao obter orçamentos: {str(e)}")
            return []

    def add_meta(self, nome, valor_meta):
        """Adiciona uma nova meta"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            hoje = date.today()
            cursor.execute('''
                INSERT INTO metas (nome, valor_meta, valor_atual, data_inicio, data_fim)
                VALUES (?, ?, ?, ?, ?)
            ''', (nome, valor_meta, 0, hoje, hoje.replace(year=hoje.year + 1)))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Erro ao adicionar meta: {str(e)}")
            return False

    def get_metas(self):
        """Retorna todas as metas"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT * FROM metas
                WHERE data_fim >= date('now')
            ''')

            metas = []
            for row in cursor.fetchall():
                metas.append({
                    'id': row[0],
                    'nome': row[1],
                    'valor_meta': row[2],
                    'valor_atual': row[3],
                    'data_inicio': datetime.strptime(row[4], '%Y-%m-%d').date(),
                    'data_fim': datetime.strptime(row[5], '%Y-%m-%d').date()
                })

            conn.close()
            return metas

        except Exception as e:
            print(f"Erro ao obter metas: {str(e)}")
            return []

    def add_investimento(self, tipo, valor):
        """Adiciona um novo investimento"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            # Simular rentabilidade (em um caso real, isso viria de uma API)
            rentabilidade = 0.1  # 10% ao ano

            cursor.execute('''
                INSERT INTO investimentos (tipo, valor, rentabilidade, data_inicio)
                VALUES (?, ?, ?, ?)
            ''', (tipo, valor, rentabilidade, date.today()))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Erro ao adicionar investimento: {str(e)}")
            return False

    def get_investimentos(self):
        """Retorna todos os investimentos"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT * FROM investimentos
                ORDER BY data_inicio DESC
            ''')

            investimentos = []
            for row in cursor.fetchall():
                investimentos.append({
                    'id': row[0],
                    'tipo': row[1],
                    'valor': row[2],
                    'rentabilidade': row[3],
                    'data_inicio': datetime.strptime(row[4], '%Y-%m-%d').date()
                })

            conn.close()
            return investimentos

        except Exception as e:
            print(f"Erro ao obter investimentos: {str(e)}")
            return []

    def add_conta(self, nome, tipo, banco, saldo):
        """Adiciona uma nova conta"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO contas (nome, tipo, banco, saldo)
                VALUES (?, ?, ?, ?)
            ''', (nome, tipo, banco, saldo))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Erro ao adicionar conta: {str(e)}")
            return False

    def get_contas(self):
        """Retorna todas as contas"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT * FROM contas
                ORDER BY nome
            ''')

            contas = []
            for row in cursor.fetchall():
                contas.append({
                    'id': row[0],
                    'nome': row[1],
                    'tipo': row[2],
                    'banco': row[3],
                    'saldo': row[4]
                })

            conn.close()
            return contas

        except Exception as e:
            print(f"Erro ao obter contas: {str(e)}")
            return []

    def add_cartao(self, nome, tipo, banco, limite, dia_fechamento, dia_vencimento):
        """Adiciona um novo cartão"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO cartoes (nome, tipo, banco, limite, dia_fechamento, dia_vencimento)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nome, tipo, banco, limite, dia_fechamento, dia_vencimento))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Erro ao adicionar cartão: {str(e)}")
            return False

    def get_cartoes(self):
        """Retorna todos os cartões"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT * FROM cartoes
                ORDER BY nome
            ''')

            cartoes = []
            for row in cursor.fetchall():
                cartoes.append({
                    'id': row[0],
                    'nome': row[1],
                    'tipo': row[2],
                    'banco': row[3],
                    'limite': row[4],
                    'dia_fechamento': row[5],
                    'dia_vencimento': row[6]
                })

            conn.close()
            return cartoes

        except Exception as e:
            print(f"Erro ao obter cartões: {str(e)}")
            return []

    def add_lembrete(self, titulo, valor, dia):
        """Adiciona um novo lembrete"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            hoje = date.today()
            data_lembrete = hoje.replace(day=dia)
            if data_lembrete < hoje:
                data_lembrete = data_lembrete.replace(month=hoje.month + 1)

            cursor.execute('''
                INSERT INTO lembretes (titulo, valor, data, categoria, recorrencia)
                VALUES (?, ?, ?, ?, ?)
            ''', (titulo, valor, data_lembrete, 'Contas', 'Mensal'))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Erro ao adicionar lembrete: {str(e)}")
            return False

    def get_lembretes(self):
        """Retorna todos os lembretes"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT * FROM lembretes
                WHERE data >= date('now')
                ORDER BY data
            ''')

            lembretes = []
            for row in cursor.fetchall():
                lembretes.append({
                    'id': row[0],
                    'titulo': row[1],
                    'descricao': row[2],
                    'valor': row[3],
                    'data': datetime.strptime(row[4], '%Y-%m-%d').date(),
                    'categoria': row[5],
                    'recorrencia': row[6]
                })

            conn.close()
            return lembretes

        except Exception as e:
            print(f"Erro ao obter lembretes: {str(e)}")
            return []

    def add_tip(self, titulo, conteudo, categoria):
        """Adiciona uma nova dica"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO dicas (titulo, conteudo, categoria, data_criacao)
                VALUES (?, ?, ?, ?)
            ''', (titulo, conteudo, categoria, date.today()))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Erro ao adicionar dica: {str(e)}")
            return False

    def get_tips(self):
        """Retorna todas as dicas"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT * FROM dicas
                ORDER BY data_criacao DESC
            ''')

            dicas = []
            for row in cursor.fetchall():
                dicas.append({
                    'id': row[0],
                    'titulo': row[1],
                    'conteudo': row[2],
                    'categoria': row[3],
                    'data_criacao': datetime.strptime(row[4], '%Y-%m-%d').date()
                })

            conn.close()
            return dicas

        except Exception as e:
            print(f"Erro ao obter dicas: {str(e)}")
            return []

    def save(self):
        """Salva o estado atual do banco de dados"""
        try:
            # Em um caso real, isso seria um backup do banco de dados
            # Por enquanto, apenas retornamos True
            return True

        except Exception as e:
            print(f"Erro ao salvar banco de dados: {str(e)}")
            return False

    def restore_backup(self, backup_data):
        """Restaura um backup do banco de dados"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            # Limpar tabelas existentes
            cursor.execute('DELETE FROM transacoes')
            cursor.execute('DELETE FROM orcamentos')
            cursor.execute('DELETE FROM metas')
            cursor.execute('DELETE FROM investimentos')
            cursor.execute('DELETE FROM contas')
            cursor.execute('DELETE FROM cartoes')
            cursor.execute('DELETE FROM lembretes')

            # Restaurar dados
            for transacao in backup_data['transactions']:
                cursor.execute('''
                    INSERT INTO transacoes (descricao, valor, categoria, tipo, data)
                    VALUES (?, ?, ?, ?, ?)
                ''', (transacao['descricao'], transacao['valor'],
                      transacao['categoria'], transacao['tipo'], transacao['data']))

            for orcamento in backup_data['budgets']:
                cursor.execute('''
                    INSERT INTO orcamentos (categoria, valor, mes, ano)
                    VALUES (?, ?, ?, ?)
                ''', (orcamento['categoria'], orcamento['valor'],
                      orcamento['mes'], orcamento['ano']))

            for meta in backup_data['goals']:
                cursor.execute('''
                    INSERT INTO metas (nome, valor_meta, valor_atual, data_inicio, data_fim)
                    VALUES (?, ?, ?, ?, ?)
                ''', (meta['nome'], meta['valor_meta'], meta['valor_atual'],
                      meta['data_inicio'], meta['data_fim']))

            for investimento in backup_data['investments']:
                cursor.execute('''
                    INSERT INTO investimentos (tipo, valor, rentabilidade, data_inicio)
                    VALUES (?, ?, ?, ?)
                ''', (investimento['tipo'], investimento['valor'],
                      investimento['rentabilidade'], investimento['data_inicio']))

            for conta in backup_data['accounts']:
                cursor.execute('''
                    INSERT INTO contas (nome, tipo, banco, saldo)
                    VALUES (?, ?, ?, ?)
                ''', (conta['nome'], conta['tipo'], conta['banco'], conta['saldo']))

            for cartao in backup_data['cards']:
                cursor.execute('''
                    INSERT INTO cartoes (nome, tipo, banco, limite, dia_fechamento, dia_vencimento)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (cartao['nome'], cartao['tipo'], cartao['banco'],
                      cartao['limite'], cartao['dia_fechamento'], cartao['dia_vencimento']))

            for lembrete in backup_data['reminders']:
                cursor.execute('''
                    INSERT INTO lembretes (titulo, descricao, valor, data, categoria, recorrencia)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (lembrete['titulo'], lembrete['descricao'], lembrete['valor'],
                      lembrete['data'], lembrete['categoria'], lembrete['recorrencia']))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Erro ao restaurar backup: {str(e)}")
            return False
