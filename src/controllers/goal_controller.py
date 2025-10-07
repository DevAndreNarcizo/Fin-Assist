from src.database.database import get_db_connection
from datetime import datetime

class GoalController:
    def __init__(self, user):
        self.user = user

    def add_goal(self, title, target_amount, deadline):
        """Adiciona uma nova meta financeira"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """
                INSERT INTO financial_goals (user_id, title, target_amount, deadline)
                VALUES (?, ?, ?, ?)
                """,
                (self.user.id, title, target_amount, deadline)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao adicionar meta: {e}")
            return False
        finally:
            conn.close()
    
    def get_goals(self, status=None):
        """Retorna as metas do usuário com filtro opcional de status"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM financial_goals WHERE user_id = ?"
        params = [self.user.id]
        
        if status:
            query += " AND status = ?"
            params.append(status)
        
        query += " ORDER BY deadline ASC"
        
        cursor.execute(query, params)
        goals = cursor.fetchall()
        conn.close()
        
        return goals
    
    def update_goal_progress(self, goal_id, current_amount):
        """Atualiza o progresso de uma meta"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """
                UPDATE financial_goals
                SET current_amount = ?
                WHERE id = ? AND user_id = ?
                """,
                (current_amount, goal_id, self.user.id)
            )
            
            # Verifica se a meta foi alcançada
            cursor.execute(
                """
                SELECT target_amount FROM financial_goals
                WHERE id = ? AND user_id = ?
                """,
                (goal_id, self.user.id)
            )
            
            target_amount = cursor.fetchone()[0]
            if current_amount >= target_amount:
                cursor.execute(
                    """
                    UPDATE financial_goals
                    SET status = 'completed'
                    WHERE id = ? AND user_id = ?
                    """,
                    (goal_id, self.user.id)
                )
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao atualizar meta: {e}")
            return False
        finally:
            conn.close()
    
    def delete_goal(self, goal_id):
        """Remove uma meta"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "DELETE FROM financial_goals WHERE id = ? AND user_id = ?",
                (goal_id, self.user.id)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao deletar meta: {e}")
            return False
        finally:
            conn.close()
    
    def get_goal_progress(self):
        """Retorna o progresso geral das metas"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT 
                COUNT(*) as total_goals,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_goals,
                SUM(target_amount) as total_target,
                SUM(current_amount) as total_current
            FROM financial_goals
            WHERE user_id = ?
            """,
            (self.user.id,)
        )
        
        progress = cursor.fetchone()
        conn.close()
        
        return {
            'total_goals': progress[0],
            'completed_goals': progress[1],
            'total_target': progress[2] or 0,
            'total_current': progress[3] or 0
        }
    
    def update_goal(self, goal_id, title, target_amount, deadline):
        """Atualiza uma meta existente."""
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                UPDATE financial_goals
                SET title = ?, target_amount = ?, deadline = ?
                WHERE id = ? AND user_id = ?
                """,
                (title, target_amount, deadline, goal_id, self.user.id)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao atualizar meta: {e}")
            return False
        finally:
            conn.close()