#!/usr/bin/env python3
"""
Script para criar o arquivo .env
"""

import os

def create_env_file():
    """Cria o arquivo .env com as configurações corretas"""
    
    env_content = """# Configuracoes do Banco de Dados Remoto
USE_SQLITE=false

# Configuracoes do MySQL Remoto (Credenciais da Arquitetura)
DB_HOST=srv1198.hstgr.io
DB_PORT=3306
DB_USER=u811651050_gatfirenguser
DB_PASSWORD=@GatFireng@2025
DB_NAME=u811651050_gatfireng

# Configuracoes de Seguranca
SECRET_KEY=dev-secret-key-change-in-production
JWT_SECRET_KEY=jwt-secret-key-change-in-production

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Ambiente
FLASK_ENV=production
"""
    
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("Arquivo .env criado com sucesso!")
    print(f"Local: {env_path}")
    
    # Verificar se foi criado
    if os.path.exists(env_path):
        print("Arquivo .env existe e está acessível")
        return True
    else:
        print("Erro: Arquivo .env não foi criado")
        return False

if __name__ == '__main__':
    create_env_file()
