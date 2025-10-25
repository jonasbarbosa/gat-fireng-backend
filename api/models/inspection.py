from datetime import datetime
from . import db

class Inspection(db.Model):
    """Modelo de inspeção"""
    
    __tablename__ = 'inspections'
    
    # Status possíveis
    STATUS_PENDING = 'pendente'
    STATUS_IN_PROGRESS = 'em_andamento'
    STATUS_COMPLETED = 'concluida'
    STATUS_CANCELLED = 'cancelada'
    
    STATUSES = [STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_COMPLETED, STATUS_CANCELLED]
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
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
    result = db.Column(db.Text)
    observations = db.Column(db.Text)
    photos = db.Column(db.Text)  # JSON string com URLs das fotos
    signature = db.Column(db.Text)  # Base64 da assinatura
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships adicionais - removidos temporariamente para resolver conflito
    # client = db.relationship('Client', foreign_keys=[client_id])
    # technician = db.relationship('User', foreign_keys=[technician_id])
    # created_by_user = db.relationship('User', foreign_keys=[created_by])
    # branch = db.relationship('Branch', foreign_keys=[branch_id])
    # equipment_obj = db.relationship('Equipment', foreign_keys=[equipment_id])
    # contract = db.relationship('Contract', foreign_keys=[contract_id])
    # team = db.relationship('Team', foreign_keys=[team_id])
    
    def __repr__(self):
        return f'<Inspection {self.id} - {self.title}>'
    
    def to_dict(self, include_relations=True):
        """Serializa a inspeção para dicionário"""
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
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
            'result': self.result,
            'observations': self.observations,
            'photos': self.photos,
            'signature': self.signature,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_relations:
            if self.client:
                data['client'] = self.client.to_dict()
            if self.technician:
                data['technician'] = self.technician.to_dict()
            if self.team:
                data['team'] = self.team.to_dict()
            if self.branch:
                data['branch'] = self.branch.to_dict()
            if self.contract:
                data['contract'] = self.contract.to_dict()
            if self.equipment_obj:
                data['equipment_obj'] = self.equipment_obj.to_dict()
        
        return data

