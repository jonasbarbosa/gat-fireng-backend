#!/usr/bin/env python3
"""
Script para testar importação dos modelos SQLAlchemy
"""

import sys
import os

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_models_import():
    """Testa se os modelos podem ser importados sem conflitos"""
    print("Testando importacao dos modelos...")
    
    try:
        # Tentar importar cada modelo individualmente
        print("1. Importando User...")
        from api.models.user import User
        print("   User importado com sucesso")
        
        print("2. Importando Maintenance...")
        from api.models.maintenance import Maintenance
        print("   Maintenance importado com sucesso")
        
        print("3. Importando Inspection...")
        from api.models.inspection import Inspection
        print("   Inspection importado com sucesso")
        
        print("4. Importando Technician...")
        from api.models.technician import Technician
        print("   Technician importado com sucesso")
        
        print("5. Importando todos os modelos...")
        from api.models import db, User, Maintenance, Inspection, Technician
        print("   Todos os modelos importados com sucesso")
        
        print("6. Testando criacao de sessao...")
        from flask import Flask
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        db.init_app(app)
        
        with app.app_context():
            print("   Sessao criada com sucesso")
            print("   Modelos carregados sem conflitos!")
        
        return True
        
    except Exception as e:
        print(f"ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_models_import()
    if success:
        print("\nTODOS OS MODELOS FORAM IMPORTADOS COM SUCESSO!")
    else:
        print("\nERRO NA IMPORTACAO DOS MODELOS!")
