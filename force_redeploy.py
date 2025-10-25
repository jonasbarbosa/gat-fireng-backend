#!/usr/bin/env python3
"""
Script para forçar redeploy e limpar cache
"""

import os
import subprocess
import sys

def force_redeploy():
    """Força um redeploy completo"""
    print("Forcando redeploy do backend...")
    
    try:
        # 1. Limpar cache Python
        print("1. Limpando cache Python...")
        if os.path.exists('__pycache__'):
            subprocess.run(['rm', '-rf', '__pycache__'], shell=True)
        if os.path.exists('api/__pycache__'):
            subprocess.run(['rm', '-rf', 'api/__pycache__'], shell=True)
        if os.path.exists('api/models/__pycache__'):
            subprocess.run(['rm', '-rf', 'api/models/__pycache__'], shell=True)
        print("   Cache limpo")
        
        # 2. Verificar se há arquivos .pyc
        print("2. Removendo arquivos .pyc...")
        subprocess.run(['find', '.', '-name', '*.pyc', '-delete'], shell=True)
        print("   Arquivos .pyc removidos")
        
        # 3. Commit das mudanças
        print("3. Fazendo commit das correcoes...")
        subprocess.run(['git', 'add', '.'], shell=True)
        subprocess.run(['git', 'commit', '-m', 'fix: corrigir relacionamentos SQLAlchemy - remover back_populates'], shell=True)
        print("   Commit realizado")
        
        # 4. Push para forçar redeploy
        print("4. Fazendo push para forcar redeploy...")
        subprocess.run(['git', 'push', 'origin', 'main'], shell=True)
        print("   Push realizado")
        
        print("\nREDEPLOY FORCADO COM SUCESSO!")
        print("Aguarde alguns minutos para o Vercel processar o deploy...")
        
        return True
        
    except Exception as e:
        print(f"ERRO no redeploy: {e}")
        return False

if __name__ == "__main__":
    success = force_redeploy()
    if not success:
        print("\nERRO NO REDEPLOY!")
        sys.exit(1)
