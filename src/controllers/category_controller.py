from src.database.database import get_db_connection

class CategoryController:
    def __init__(self, user):
        self.user = user
    
    def get_categories(self, transaction_type):
        """Retorna categorias para um tipo de transação"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT DISTINCT category FROM transactions 
            WHERE user_id = ? AND type = ?
            ORDER BY category
        ''', (self.user.id, transaction_type))
        
        categories = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        # Adiciona categorias padrão se não existirem
        default_categories = self._get_default_categories(transaction_type)
        for cat in default_categories:
            if cat not in categories:
                categories.append(cat)
        
        return categories
    
    def add_custom_category(self, transaction_type, category_name):
        """Adiciona uma nova categoria personalizada"""
        if not category_name or not category_name.strip():
            return False
            
        category_name = category_name.strip()
        
        # Verifica se já existe
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id FROM transactions 
            WHERE user_id = ? AND type = ? AND category = ?
            LIMIT 1
        ''', (self.user.id, transaction_type, category_name))
        
        if cursor.fetchone():
            conn.close()
            return False  # Já existe
        
        # Adiciona uma transação temporária para "registrar" a categoria
        cursor.execute('''
            INSERT INTO transactions (user_id, type, category, subcategory, amount, description, date)
            VALUES (?, ?, ?, '', 0.01, 'Categoria personalizada', datetime('now'))
        ''', (self.user.id, transaction_type, category_name))
        
        conn.commit()
        conn.close()
        return True
    
    def delete_custom_category(self, transaction_type, category_name):
        """Remove uma categoria personalizada (apenas se não tiver transações)"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verifica se tem transações reais
        cursor.execute('''
            SELECT COUNT(*) FROM transactions 
            WHERE user_id = ? AND type = ? AND category = ? AND amount > 0.01
        ''', (self.user.id, transaction_type, category_name))
        
        count = cursor.fetchone()[0]
        
        if count > 0:
            conn.close()
            return False  # Tem transações reais, não pode deletar
        
        # Remove transações da categoria (incluindo a temporária)
        cursor.execute('''
            DELETE FROM transactions 
            WHERE user_id = ? AND type = ? AND category = ?
        ''', (self.user.id, transaction_type, category_name))
        
        conn.commit()
        conn.close()
        return True
    
    def _get_default_categories(self, transaction_type):
        """Retorna categorias padrão por tipo"""
        if transaction_type == 'income':
            return ['Salário', 'Freelance', 'Investimentos', 'Vendas', 'Outros']
        elif transaction_type == 'expense':
            return ['Alimentação', 'Transporte', 'Moradia', 'Saúde', 'Educação', 'Lazer', 'Outros']
        elif transaction_type == 'investment':
            return ['Ações', 'Fundos', 'Tesouro Direto', 'CDB', 'Outros']
        else:
            return []
    
    def get_category_stats(self, transaction_type):
        """Retorna estatísticas das categorias"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT category, COUNT(*) as count, SUM(amount) as total
            FROM transactions 
            WHERE user_id = ? AND type = ? AND amount > 0.01
            GROUP BY category
            ORDER BY total DESC
        ''', (self.user.id, transaction_type))
        
        stats = []
        for row in cursor.fetchall():
            stats.append({
                'category': row[0],
                'count': row[1],
                'total': row[2]
            })
        
        conn.close()
        return stats
