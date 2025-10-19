import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager

# Tornar imports resilientes para rodar tanto localmente (pacote api) quanto no Vercel (executando api/index.py)
try:
    from .config import config
    from .models import db, migrate
    from .routes import register_routes
except ImportError:
    from config import config
    from models import db, migrate
    from routes import register_routes

from flasgger import Swagger

def create_app(config_name='default'):
    """Factory para criar a aplicação Flask"""
    
    app = Flask(__name__)
    # Seleciona config baseada em FLASK_ENV (production/development)
    env = os.getenv('FLASK_ENV', 'production')
    selected = 'production' if env == 'production' else 'development'
    config_name = config_name or selected
    app.config.from_object(config[config_name])
    
    # Configuração do Swagger
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/api/docs"
    }
    
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Fireng API - GAT & DAT",
            "description": """
API unificada para os sistemas Fireng:

**GAT (Gestão de Atendimento Técnico)**: Sistema web administrativo
- Gerenciamento de usuários, clientes e equipes
- Planejamento e agendamento de serviços
- Relatórios e dashboards gerenciais
- Acesso: Admin, Coordenadores

**DAT (Diário de Atendimento Técnico)**: Aplicativo mobile para técnicos
- Registro de inspeções e manutenções em campo
- Captura de fotos e assinaturas
- Sincronização offline
- Acesso: Técnicos, Clientes

**Compartilhado**: Recursos comuns entre GAT e DAT
- Autenticação e autorização (JWT)
- Perfis de usuário
- Notificações
            """,
            "version": "1.0.0",
            "contact": {
                "name": "Fireng",
                "url": "https://github.com/seu-usuario/fireng"
            }
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Authorization header usando o esquema Bearer. Exemplo: 'Bearer {token}'"
            }
        },
        "security": [{"Bearer": []}]
    }
    
    # Inicializar extensões
    db.init_app(app)
    migrate.init_app(app, db)
    
    # CORS simplificado para aceitar qualquer origem
    CORS(app, 
         origins=['*'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
         allow_headers=['Content-Type', 'Authorization', 'X-Requested-With'],
         supports_credentials=False)
    
    # Configurar JWT
    jwt = JWTManager(app)
    
    # Handlers de erro JWT
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            'error': 'Token inválido',
            'message': str(error)
        }), 401
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'error': 'Token expirado',
            'message': 'O token de acesso expirou'
        }), 401
    
    @jwt.unauthorized_loader
    def unauthorized_callback(error):
        return jsonify({
            'error': 'Token não fornecido',
            'message': 'Authorization header não encontrado ou inválido'
        }), 401
    
    # Swagger removido temporariamente devido a incompatibilidade
    # Swagger(app, config=swagger_config, template=swagger_template)
    Swagger(app, config=swagger_config, template=swagger_template)
    
    # Adicionar headers CORS manualmente para garantir funcionamento
    @app.after_request
    def after_request(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        response.headers['Access-Control-Max-Age'] = '86400'
        return response
    
    # Endpoint de health check simples
    @app.route('/api/health')
    def health_check():
        return jsonify({
            'status': 'ok',
            'message': 'API funcionando',
            'version': '1.0.0'
        })
    
    # Registrar rotas
    register_routes(app)
    
    # Criar tabelas do banco de dados (apenas se explicitamente habilitado em dev)
    if app.config.get('DEBUG') and os.getenv('RUN_DB_CREATE', 'false').lower() == 'true':
        with app.app_context():
            db.create_all()

    return app

# Criar a aplicação para Vercel
app = create_app()