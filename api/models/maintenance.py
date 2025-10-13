from datetime import datetime
from sqlalchemy import Numeric
from .. import db

class Maintenance(db.Model):
    """Modelo de manutenção"""
    
    __tablename__ = 'maintenances'
    
    # Status possíveis
    STATUS_PENDING = 'pendente'
    STATUS_IN_PROGRESS = 'em_andamento'
    STATUS_COMPLETED = 'concluida'
    STATUS_CANCELLED = 'cancelada'
    
    STATUSES = [STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_COMPLETED, STATUS_CANCELLED]
    
    # Tipos de manutenção
    TYPE_PREVENTIVE = 'preventiva'
    TYPE_CORRECTIVE = 'corretiva'
    TYPE_PREDICTIVE = 'preditiva'
    
    TYPES = [TYPE_PREVENTIVE, TYPE_CORRECTIVE, TYPE_PREDICTIVE]
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    maintenance_type = db.Column(db.String(20), default=TYPE_PREVENTIVE, nullable=False)
    scheduled_date = db.Column(db.DateTime, nullable=False)
    completed_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default=STATUS_PENDING, nullable=False)
    priority = db.Column(db.String(20), default='media')  # baixa, media, alta, urgente
    location = db.Column(db.String(255))
    equipment = db.Column(db.String(100))
    
    # Chaves estrangeiras
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    technician_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'))
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipments.id'))
    contract_id = db.Column(db.Integer, db.ForeignKey('contracts.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    
    # Campos de resultado
    work_performed = db.Column(db.Text)
    parts_used = db.Column(db.Text)  # JSON string com peças utilizadas
    observations = db.Column(db.Text)
    photos = db.Column(db.Text)  # JSON string com URLs das fotos
    signature = db.Column(db.Text)  # Base64 da assinatura
    
    # Custos
    labor_cost = db.Column(Numeric(10, 2))
    parts_cost = db.Column(Numeric(10, 2))
    total_cost = db.Column(Numeric(10, 2))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships adicionais
    branch = db.relationship('Branch', foreign_keys=[branch_id])
    equipment_obj = db.relationship('Equipment', foreign_keys=[equipment_id])
    contract = db.relationship('Contract', foreign_keys=[contract_id])
    team = db.relationship('Team', foreign_keys=[team_id])
    
    def __repr__(self):
        return f'<Maintenance {self.id} - {self.title}>'
    
    def to_dict(self, include_relations=True):
        """Serializa a manutenção para dicionário"""
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'maintenance_type': self.maintenance_type,
            'scheduled_date': self.scheduled_date.isoformat() if self.scheduled_date else None,
            'completed_date': self.completed_date.isoformat() if self.completed_date else None,
            'status': self.status,
            'priority': self.priority,
            'location': self.location,
            'equipment': self.equipment,
            'client_id': self.client_id,
            'technician_id': self.technician_id,
            'created_by': self.created_by,
            'branch_id': self.branch_id,
            'equipment_id': self.equipment_id,
            'contract_id': self.contract_id,
            'team_id': self.team_id,
            'work_performed': self.work_performed,
            'parts_used': self.parts_used,
            'observations': self.observations,
            'photos': self.photos,
            'signature': self.signature,
            'labor_cost': float(self.labor_cost) if self.labor_cost else None,
            'parts_cost': float(self.parts_cost) if self.parts_cost else None,
            'total_cost': float(self.total_cost) if self.total_cost else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_relations:
            if self.client:
                data['client'] = self.client.to_dict()
            if self.technician:
                data['technician'] = self.technician.to_dict()
        
        return data

