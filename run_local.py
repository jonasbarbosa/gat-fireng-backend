#!/usr/bin/env python3
"""
Script para executar a aplicação Flask localmente
Sistema Fireng - GAT & DAT Backend
"""
import os
import sys
import subprocess

def check_dependencies():
    """Verifica se todas as dependências estão instaladas"""
    try:
        import flask
        import flask_sqlalchemy
        import flask_migrate
        import flask_jwt_extended
        import flasgger
        import flask_cors
        import bcrypt
        import pymysql
        print("✅ Todas as dependências estão instaladas")
        return True
    except ImportError as e:
        print(f"❌ Dependência faltando: {e}")
        print("Execute: pip3 install -r requirements.txt")
        return False

def setup_environment():
    """Configura o ambiente de desenvolvimento"""
    # Adicionar o diretório raiz ao Python path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # Configurar variáveis de ambiente
    os.environ['FLASK_ENV'] = 'development'
    os.environ['USE_SQLITE'] = 'true'
    
    print("🔧 Ambiente configurado para desenvolvimento")

def create_database_if_needed():
    """Cria o banco de dados SQLite se não existir"""
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'fireng.db')
    if not os.path.exists(db_path):
        print("📁 Criando diretório instance...")
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        print("✅ Banco de dados SQLite será criado automaticamente")

def main():
    """Função principal"""
    print("🚀 Fireng Backend - Sistema GAT & DAT")
    print("=" * 50)
    
    # Verificar dependências
    if not check_dependencies():
        return
    
    # Configurar ambiente
    setup_environment()
    
    # Verificar banco de dados
    create_database_if_needed()
    
    # Importar e executar a aplicação
    try:
        from api.app import create_app
        
        app = create_app('development')
        
        print("\n🎯 Servidor iniciado com sucesso!")
        print("📱 API disponível em: http://localhost:5001")
        print("📚 Documentação Swagger: http://localhost:5001/api/docs")
        print("🔍 Health Check: http://localhost:5001/api/health")
        print("🛑 Para parar o servidor: Ctrl+C")
        print("=" * 50)
        
        app.run(
            host='0.0.0.0',
            port=5001,
            debug=True,
            use_reloader=True
        )
        
    except Exception as e:
        print(f"❌ Erro ao iniciar o servidor: {e}")
        print("Verifique se todas as dependências estão instaladas")
        return 1

if __name__ == '__main__':
    main()