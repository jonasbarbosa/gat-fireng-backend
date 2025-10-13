from .auth import auth_bp
from .users import users_bp
from .clients import clients_bp
from .inspections import inspections_bp
from .maintenances import maintenances_bp
from .branches import branches_bp
from .contracts import contracts_bp
from .teams import teams_bp
from .technicians import technicians_bp
from .standards import standards_bp
from .inventories import inventories_bp
from .equipments import equipments_bp
from .auto_inspections import auto_inspections_bp

def register_routes(app):
    """Registra todas as rotas da aplicação"""
    # Rotas compartilhadas
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    # Rotas GAT (Gestão)
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(clients_bp, url_prefix='/api/clients')
    app.register_blueprint(branches_bp, url_prefix='/api/branches')
    app.register_blueprint(contracts_bp, url_prefix='/api/contracts')
    app.register_blueprint(teams_bp, url_prefix='/api/teams')
    app.register_blueprint(technicians_bp, url_prefix='/api/technicians')
    app.register_blueprint(standards_bp, url_prefix='/api/standards')
    app.register_blueprint(inventories_bp, url_prefix='/api/inventories')
    app.register_blueprint(equipments_bp, url_prefix='/api/equipments')
    
    # Rotas DAT (Diário de campo)
    app.register_blueprint(inspections_bp, url_prefix='/api/inspections')
    app.register_blueprint(maintenances_bp, url_prefix='/api/maintenances')
    
    # Rotas de automação
    app.register_blueprint(auto_inspections_bp, url_prefix='/api/auto-inspections')

