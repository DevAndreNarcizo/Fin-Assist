import csv
import json
from datetime import datetime
from tkinter import filedialog, messagebox
import customtkinter as ctk

class DataImportExport:
    def __init__(self, transaction_controller, goal_controller, user):
        self.transaction_controller = transaction_controller
        self.goal_controller = goal_controller
        self.user = user
    
    def export_transactions_csv(self, parent):
        """Exporta transações para CSV"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Salvar transações como CSV..."
        )
        
        if not filename:
            return False
            
        try:
            transactions = self.transaction_controller.get_transactions()
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['ID', 'Tipo', 'Categoria', 'Subcategoria', 'Valor', 'Descrição', 'Data'])
                
                for t in transactions:
                    # Converte data para DD-MM-YYYY para exportação
                    try:
                        data_display = datetime.strptime(t[7][:10], '%Y-%m-%d').strftime('%d-%m-%Y')
                    except:
                        data_display = t[7][:10]
                    
                    writer.writerow([
                        t[0],  # ID
                        t[2],  # Tipo
                        t[3],  # Categoria
                        t[4],  # Subcategoria
                        t[5],  # Valor
                        t[6],  # Descrição
                        data_display  # Data
                    ])
            
            messagebox.showinfo("Sucesso", f"Transações exportadas para:\n{filename}")
            return True
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar transações:\n{str(e)}")
            return False
    
    def export_goals_csv(self, parent):
        """Exporta metas para CSV"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Salvar metas como CSV..."
        )
        
        if not filename:
            return False
            
        try:
            goals = self.goal_controller.get_goals()
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['ID', 'Título', 'Valor Alvo', 'Valor Atual', 'Prazo', 'Status'])
                
                for g in goals:
                    # Converte data para DD-MM-YYYY para exportação
                    try:
                        data_display = datetime.strptime(g[5], '%Y-%m-%d').strftime('%d-%m-%Y')
                    except:
                        data_display = g[5]
                    
                    writer.writerow([
                        g[0],  # ID
                        g[2],  # Título
                        g[3],  # Valor Alvo
                        g[4],  # Valor Atual
                        data_display,  # Prazo
                        g[6]   # Status
                    ])
            
            messagebox.showinfo("Sucesso", f"Metas exportadas para:\n{filename}")
            return True
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar metas:\n{str(e)}")
            return False
    
    def import_transactions_csv(self, parent):
        """Importa transações de CSV"""
        filename = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv")],
            title="Selecionar arquivo CSV para importar..."
        )
        
        if not filename:
            return False
            
        try:
            with open(filename, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                imported_count = 0
                errors = []
                
                for row_num, row in enumerate(reader, start=2):  # Começa em 2 (linha 1 é cabeçalho)
                    try:
                        # Converte data DD-MM-YYYY para YYYY-MM-DD
                        data_iso = datetime.strptime(row['Data'], '%d-%m-%Y').strftime('%Y-%m-%d')
                        
                        # Adiciona transação
                        success = self.transaction_controller.add_transaction(
                            tipo=row['Tipo'],
                            categoria=row['Categoria'],
                            valor=float(row['Valor']),
                            descricao=row['Descrição'],
                            data=data_iso,
                            subcategoria=row['Subcategoria']
                        )
                        
                        if success:
                            imported_count += 1
                        else:
                            errors.append(f"Linha {row_num}: Erro ao adicionar transação")
                            
                    except Exception as e:
                        errors.append(f"Linha {row_num}: {str(e)}")
                
                # Mostra resultado
                if imported_count > 0:
                    message = f"Importadas {imported_count} transações com sucesso!"
                    if errors:
                        message += f"\n\nErros encontrados:\n" + "\n".join(errors[:5])
                        if len(errors) > 5:
                            message += f"\n... e mais {len(errors) - 5} erros"
                    messagebox.showinfo("Importação Concluída", message)
                else:
                    messagebox.showerror("Erro", "Nenhuma transação foi importada.\n" + "\n".join(errors[:5]))
                
                return imported_count > 0
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao importar transações:\n{str(e)}")
            return False
    
    def export_all_data_json(self, parent):
        """Exporta todos os dados para JSON"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            title="Salvar backup completo como JSON..."
        )
        
        if not filename:
            return False
            
        try:
            transactions = self.transaction_controller.get_transactions()
            goals = self.goal_controller.get_goals()
            
            data = {
                'user_id': self.user.id,
                'export_date': datetime.now().isoformat(),
                'transactions': [],
                'goals': []
            }
            
            # Adiciona transações
            for t in transactions:
                data['transactions'].append({
                    'id': t[0],
                    'type': t[2],
                    'category': t[3],
                    'subcategory': t[4],
                    'amount': t[5],
                    'description': t[6],
                    'date': t[7]
                })
            
            # Adiciona metas
            for g in goals:
                data['goals'].append({
                    'id': g[0],
                    'title': g[2],
                    'target_amount': g[3],
                    'current_amount': g[4],
                    'deadline': g[5],
                    'status': g[6]
                })
            
            with open(filename, 'w', encoding='utf-8') as jsonfile:
                json.dump(data, jsonfile, indent=2, ensure_ascii=False)
            
            messagebox.showinfo("Sucesso", f"Backup completo salvo em:\n{filename}")
            return True
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar backup:\n{str(e)}")
            return False
