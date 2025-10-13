from datetime import datetime
from sqlalchemy import Numeric
from models import db

class Contract(db.Model):
    """Modelo de contrato - Contratos de serviços com empresas"""
    
    __tablename__ = 'contracts'
    
    # Status possíveis
    STATUS_ACTIVE = 'ativo'
    STATUS_SUSPENDED = 'suspenso'
    STATUS_FINISHED = 'encerrado'
    STATUS_CANCELLED = 'cancelado'
    
    STATUSES = [STATUS_ACTIVE, STATUS_SUSPENDED, STATUS_FINISHED, STATUS_CANCELLED]
    
    id = db.Column(db.Integer, primary_key=True)
    contract_number = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    value = db.Column(Numeric(12, 2))
    status = db.Column(db.String(20), default=STATUS_ACTIVE, nullable=False)
    terms = db.Column(db.Text)  # Termos do contrato
    notes = db.Column(db.Text)
    
    # Foreign Keys
    company_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships (backref 'company' já definido em Client)
    # company é acessível via backref do Client
    team = db.relationship('Team', backref='team_contracts', lazy='joined')
    
    def __repr__(self):
        return f'<Contract {self.contract_number}>'
    
    def to_dict(self, include_relations=False):
        """Serializa o contrato para dicionário"""
        data = {
            'id': self.id,
            'contract_number': self.contract_number,
            'description': self.description,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'value': float(self.value) if self.value else None,
            'status': self.status,
            'terms': self.terms,
            'notes': self.notes,
            'company_id': self.company_id,
            'team_id': self.team_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_relations:
            data['company_name'] = self.company.name if self.company else None
            data['team_name'] = self.team.name if self.team else None
        
        return data
    
    @staticmethod
    def validate_status(status):
        """Valida se o status é válido"""
        return status in Contract.STATUSES
