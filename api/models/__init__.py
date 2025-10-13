from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

# Importar modelos na ordem correta (respeitando dependências)
from .user import User
from .client import Client
from .branch import Branch
from .team import Team
from .contract import Contract
from .technician import Technician
from .standard import Standard
from .inventory import Inventory
from .equipment import Equipment, equipment_standards
from .inspection import Inspection
from .maintenance import Maintenance

__all__ = [
    'db', 
    'migrate', 
    'User', 
    'Client', 
    'Branch',
    'Team',
    'Contract',
    'Technician',
    'Standard',
    'Inventory',
    'Equipment',
    'equipment_standards',
    'Inspection', 
    'Maintenance'
]

