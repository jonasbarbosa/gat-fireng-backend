#!/usr/bin/env python3
"""
Script para criar/atualizar as tabelas do banco de dados
com a nova modelagem UML completa
"""

from app import create_app
from models import db

def migrate_database():
    """Cria todas as tabelas no banco de dados"""
    app = create_app()
    
    with app.app_context():
        print("🔄 Criando/atualizando tabelas no banco de dados...")
        print("=" * 60)
        
        try:
            # Criar todas as tabelas
            db.create_all()
            
            print("✅ Tabelas criadas/atualizadas com sucesso!")
            print("\n📋 Tabelas disponíveis:")
            print("=" * 60)
            
            tables = [
                "users - Usuários do sistema",
                "clients - Empresas clientes",
                "branches - Filiais das empresas",
                "contracts - Contratos de serviços",
                "teams - Equipes técnicas",
                "technicians - Perfil de técnicos",
                "standards - Normas técnicas (NBR, IT, NR)",
                "inventories - Inventários por filial",
                "equipments - Equipamentos de combate a incêndio",
                "equipment_standards - Relacionamento equipamentos-normas",
                "inspections - Inspeções",
                "maintenances - Manutenções"
            ]
            
            for table in tables:
                print(f"  ✓ {table}")
            
            print("\n" + "=" * 60)
            print("🎉 Migração concluída com sucesso!")
            print("\n💡 Próximos passos:")
            print("  1. Verifique as tabelas no banco de dados")
            print("  2. Execute: python create_admin.py (se necessário)")
            print("  3. Inicie o servidor: python app.py")
            print("  4. Acesse o Swagger: http://localhost:5000/api/docs")
            
        except Exception as e:
            print(f"❌ Erro ao criar tabelas: {str(e)}")
            print("\n💡 Dica: Verifique se:")
            print("  - O MySQL está rodando")
            print("  - As credenciais no .env estão corretas")
            print("  - O banco de dados existe")
            return False
    
    return True

if __name__ == '__main__':
    migrate_database()
