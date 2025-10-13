import os
from app import create_app
from models import db
import pymysql

def add_missing_columns():
    app = create_app()
    with app.app_context():
        print("🔧 Adicionando colunas faltantes nas tabelas...")
        
        # Configurações do banco
        DB_HOST = 'srv1198.hstgr.io'
        DB_USER = 'u811651050_gatfirenguser'
        DB_PASSWORD = '@GatFireng@2025'
        DB_NAME = 'u811651050_gatfireng'
        
        # Conectar ao MySQL
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset='utf8mb4'
        )
        
        try:
            with connection.cursor() as cursor:
                # Adicionar colunas na tabela inspections
                print("📋 Adicionando colunas na tabela inspections...")
                
                columns_to_add = [
                    "ALTER TABLE inspections ADD COLUMN branch_id INT",
                    "ALTER TABLE inspections ADD COLUMN equipment_id INT", 
                    "ALTER TABLE inspections ADD COLUMN contract_id INT",
                    "ALTER TABLE inspections ADD COLUMN team_id INT"
                ]
                
                for sql in columns_to_add:
                    try:
                        cursor.execute(sql)
                        print(f"  ✅ {sql}")
                    except pymysql.Error as e:
                        if "Duplicate column name" in str(e):
                            print(f"  ⚠️ Coluna já existe: {sql}")
                        else:
                            print(f"  ❌ Erro: {sql} - {e}")
                
                # Adicionar colunas na tabela maintenances
                print("\n🔧 Adicionando colunas na tabela maintenances...")
                
                maintenance_columns = [
                    "ALTER TABLE maintenances ADD COLUMN branch_id INT",
                    "ALTER TABLE maintenances ADD COLUMN equipment_id INT",
                    "ALTER TABLE maintenances ADD COLUMN contract_id INT", 
                    "ALTER TABLE maintenances ADD COLUMN team_id INT"
                ]
                
                for sql in maintenance_columns:
                    try:
                        cursor.execute(sql)
                        print(f"  ✅ {sql}")
                    except pymysql.Error as e:
                        if "Duplicate column name" in str(e):
                            print(f"  ⚠️ Coluna já existe: {sql}")
                        else:
                            print(f"  ❌ Erro: {sql} - {e}")
                
                # Commit das mudanças
                connection.commit()
                print("\n✅ Colunas adicionadas com sucesso!")
                
        except Exception as e:
            print(f"❌ Erro geral: {e}")
            connection.rollback()
        finally:
            connection.close()

if __name__ == '__main__':
    add_missing_columns()
