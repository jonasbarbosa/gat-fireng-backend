#!/usr/bin/env python3
"""
Script para testar a API de usuários
"""

import requests
import json

def test_users_api():
    """Testa a API de usuários"""
    print("Testando API de Usuarios")
    print("=" * 40)
    
    base_url = "http://localhost:5000"
    
    # Testar se o backend está rodando
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        print(f"Backend status: {response.status_code}")
        if response.status_code == 200:
            print("Backend funcionando!")
        else:
            print("Backend com problema")
            return
    except Exception as e:
        print(f"Erro ao conectar com backend: {str(e)}")
        print("Inicie o backend com: python app.py")
        return
    
    # Testar API de usuários
    try:
        print("\nTestando GET /api/users...")
        response = requests.get(f"{base_url}/api/users", timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            users = response.json()
            print(f"Usuarios encontrados: {len(users)}")
            
            if users:
                print("\nUsuarios:")
                for user in users:
                    print(f"  - ID: {user.get('id')}")
                    print(f"    Nome: {user.get('name')}")
                    print(f"    Email: {user.get('email')}")
                    print(f"    Role: {user.get('role')}")
                    print(f"    Ativo: {user.get('is_active')}")
                    print()
            else:
                print("Nenhum usuario encontrado na API")
        else:
            print(f"Erro na API: {response.text}")
            
    except Exception as e:
        print(f"Erro ao testar API de usuarios: {str(e)}")

def test_database_direct():
    """Testa o banco diretamente"""
    print("\nTestando banco diretamente...")
    
    try:
        from app import create_app
        from models import db, User
        from sqlalchemy import text
        
        app = create_app()
        
        with app.app_context():
            # Contar usuários
            user_count = User.query.count()
            print(f"Usuarios no banco: {user_count}")
            
            if user_count > 0:
                # Buscar usuários
                users = User.query.all()
                print("\nUsuarios no banco:")
                for user in users:
                    print(f"  - ID: {user.id}")
                    print(f"    Nome: {user.name}")
                    print(f"    Email: {user.email}")
                    print(f"    Role: {user.role}")
                    print(f"    Ativo: {user.is_active}")
                    print()
            else:
                print("Nenhum usuario no banco")
                
                # Verificar se a tabela existe
                result = db.session.execute(text("SHOW TABLES"))
                tables = result.fetchall()
                print(f"\nTabelas no banco: {len(tables)}")
                for table in tables:
                    print(f"  - {table[0]}")
                    
                # Verificar estrutura da tabela users
                try:
                    result = db.session.execute(text("DESCRIBE users"))
                    columns = result.fetchall()
                    print(f"\nEstrutura da tabela users:")
                    for column in columns:
                        print(f"  - {column[0]} ({column[1]})")
                except Exception as e:
                    print(f"Erro ao verificar estrutura: {str(e)}")
                    
    except Exception as e:
        print(f"Erro ao testar banco: {str(e)}")

def main():
    """Função principal"""
    print("Diagnostico da API de Usuarios")
    print("=" * 50)
    
    # Testar API
    test_users_api()
    
    # Testar banco diretamente
    test_database_direct()

if __name__ == '__main__':
    main()
