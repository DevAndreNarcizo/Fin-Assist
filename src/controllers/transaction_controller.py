from src.database.database import get_db_connection
from datetime import datetime

class TransactionController:
    def __init__(self, user):
        self.user = user
    
    def add_transaction(self, type, category, amount, description=None, date=None, subcategory=None):
        """Adiciona uma nova transação"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """
                INSERT INTO transactions (user_id, type, category, subcategory, amount, description, date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (self.user.id, type, category, subcategory, amount, description, date)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao adicionar transação: {e}")
            return False
        finally:
            conn.close()
    
    def get_transactions(self, start_date=None, end_date=None, type=None):
        """Retorna as transações do usuário com filtros opcionais"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "SELECT id, user_id, type, category, subcategory, amount, description, date FROM transactions WHERE user_id = ?"
        params = [self.user.id]
        
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        
        if type:
            query += " AND type = ?"
            params.append(type)
        
        query += " ORDER BY date DESC"
        
        cursor.execute(query, params)
        transactions = cursor.fetchall()
        conn.close()
        
        return transactions
    
    def get_balance(self):
        """Calcula o saldo atual do usuário"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT 
                SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) -
                SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END)
            FROM transactions
            WHERE user_id = ?
            """,
            (self.user.id,)
        )
        
        balance = cursor.fetchone()[0] or 0
        conn.close()
        
        return balance
    
    def get_monthly_summary(self, year, month):
        """Retorna um resumo das transações do mês"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        start_date = f"{year}-{month:02d}-01"
        end_date = f"{year}-{month:02d}-31"
        
        cursor.execute(
            """
            SELECT 
                type,
                SUM(amount) as total,
                COUNT(*) as count
            FROM transactions
            WHERE user_id = ? AND date BETWEEN ? AND ?
            GROUP BY type
            """,
            (self.user.id, start_date, end_date)
        )
        
        summary = cursor.fetchall()
        conn.close()
        
        return summary
    
    def get_category_summary(self, start_date=None, end_date=None):
        """Retorna um resumo das transações por categoria"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT 
                category,
                type,
                SUM(amount) as total,
                COUNT(*) as count
            FROM transactions
            WHERE user_id = ?
        """
        params = [self.user.id]
        
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        
        query += " GROUP BY category, type"
        
        cursor.execute(query, params)
        summary = cursor.fetchall()
        conn.close()
        
        return summary
    
    def delete_transaction(self, trans_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM transactions WHERE id = ? AND user_id = ?", (trans_id, self.user.id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao deletar transação: {e}")
            return False
        finally:
            conn.close()
    
    def update_transaction(self, trans_id, type, category, subcategory, amount, description, date):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                UPDATE transactions
                SET type = ?, category = ?, subcategory = ?, amount = ?, description = ?, date = ?
                WHERE id = ? AND user_id = ?
                """,
                (type, category, subcategory, amount, description, date, trans_id, self.user.id)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao atualizar transação: {e}")
            return False
        finally:
            conn.close()
    
    def get_transaction_by_id(self, trans_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, user_id, type, category, subcategory, amount, description, date FROM transactions WHERE id = ? AND user_id = ?", (trans_id, self.user.id))
        trans = cursor.fetchone()
        conn.close()
        return trans 