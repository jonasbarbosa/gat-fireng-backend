from datetime import datetime
from models import db

class Inventory(db.Model):
    """Modelo de inventário - Controle de inventário por filial"""
    
    __tablename__ = 'inventories'
    
    # Status
    STATUS_UPDATED = 'atualizado'
    STATUS_PENDING = 'pendente'
    STATUS_AUDITING = 'auditando'
    STATUS_OUTDATED = 'desatualizado'
    
    STATUSES = [STATUS_UPDATED, STATUS_PENDING, STATUS_AUDITING, STATUS_OUTDATED]
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Keys
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=False, unique=True)
    
    # Dados do inventário
    total_equipments = db.Column(db.Integer, default=0)
    last_audit_date = db.Column(db.Date)
    next_audit_date = db.Column(db.Date)
    status = db.Column(db.String(20), default=STATUS_UPDATED)
    notes = db.Column(db.Text)
    
    # Contadores por tipo de equipamento
    extinguishers_count = db.Column(db.Integer, default=0)
    hydrants_count = db.Column(db.Integer, default=0)
    sprinklers_count = db.Column(db.Integer, default=0)
    alarms_count = db.Column(db.Integer, default=0)
    emergency_lights_count = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    branch = db.relationship('Branch', backref=db.backref('inventory', uselist=False))
    
    def __repr__(self):
        return f'<Inventory {self.id} - Branch {self.branch_id}>'
    
    def to_dict(self, include_relations=False):
        """Serializa o inventário para dicionário"""
        data = {
            'id': self.id,
            'branch_id': self.branch_id,
            'total_equipments': self.total_equipments,
            'last_audit_date': self.last_audit_date.isoformat() if self.last_audit_date else None,
            'next_audit_date': self.next_audit_date.isoformat() if self.next_audit_date else None,
            'status': self.status,
            'notes': self.notes,
            'extinguishers_count': self.extinguishers_count,
            'hydrants_count': self.hydrants_count,
            'sprinklers_count': self.sprinklers_count,
            'alarms_count': self.alarms_count,
            'emergency_lights_count': self.emergency_lights_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_relations:
            if self.branch:
                data['branch'] = {
                    'id': self.branch.id,
                    'name': self.branch.name,
                    'company_id': self.branch.company_id
                }
            if hasattr(self, 'equipments'):
                data['equipments_count'] = len(self.equipments)
        
        return data
    
    def update_counts(self):
        """Atualiza os contadores de equipamentos"""
        if hasattr(self, 'equipments'):
            self.total_equipments = len(self.equipments)
            self.extinguishers_count = sum(1 for e in self.equipments if e.type == 'extintor')
            self.hydrants_count = sum(1 for e in self.equipments if e.type == 'hidrante')
            self.sprinklers_count = sum(1 for e in self.equipments if e.type == 'sprinkler')
            self.alarms_count = sum(1 for e in self.equipments if e.type == 'alarme')
            self.emergency_lights_count = sum(1 for e in self.equipments if e.type == 'iluminacao_emergencia')
    
    @staticmethod
    def validate_status(status):
        """Valida se o status é válido"""
        return status in Inventory.STATUSES
