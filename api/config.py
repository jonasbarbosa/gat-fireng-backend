import os
from datetime import timedelta
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configurações base da aplicação"""
    
    # Configurações gerais
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Configurações do banco de dados - MySQL Remoto
    DB_HOST = os.getenv('DB_HOST', 'srv1198.hstgr.io')
    DB_PORT = os.getenv('DB_PORT', '3306')
    DB_USER = os.getenv('DB_USER', 'u811651050_gatfirenguser')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '@GatFireng@2025')
    DB_NAME = os.getenv('DB_NAME', 'u811651050_gatfireng')
    
    # URL do banco de dados - MySQL Remoto sempre
    USE_SQLITE = os.getenv('USE_SQLITE', 'false').lower() == 'true'
    
    if USE_SQLITE:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///fireng.db'
        SQLALCHEMY_ENGINE_OPTIONS = {}
    else:
        # URL encode da senha para lidar com caracteres especiais
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        # Configurações de pool de conexões para evitar "MySQL server has gone away"
        SQLALCHEMY_ENGINE_OPTIONS = {
            'pool_pre_ping': True,  # Verifica conexão antes de usar
            'pool_recycle': 280,    # Recicla conexões a cada 280 segundos (antes do timeout do MySQL)
            'pool_size': 10,        # Número de conexões no pool
            'max_overflow': 20,     # Conexões extras permitidas
            'connect_args': {
                'connect_timeout': 10
            }
        }
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # Configurações JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Configurações CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5173,http://localhost:5174').split(',')


class DevelopmentConfig(Config):
    """Configurações de desenvolvimento"""
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """Configurações de produção"""
    DEBUG = False
    SQLALCHEMY_ECHO = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

