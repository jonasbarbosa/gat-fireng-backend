from datetime import datetime
from . import db

class Team(db.Model):
    """Modelo de equipe - Equipes técnicas"""
    
    __tablename__ = 'teams'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    specialization = db.Column(db.String(100))  # sprinklers, alarme, extintores, hidrantes, etc
    is_active = db.Column(db.Boolean, default=True)
    
    # Foreign Keys
    coordinator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    coordinator = db.relationship('User', foreign_keys=[coordinator_id], backref='coordinated_teams')
    
    def __repr__(self):
        return f'<Team {self.id} - {self.name}>'
    
    def to_dict(self, include_relations=False):
        """Serializa a equipe para dicionário"""
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'specialization': self.specialization,
            'is_active': self.is_active,
            'coordinator_id': self.coordinator_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_relations:
            # Informações do coordenador
            if self.coordinator:
                data['coordinator_name'] = self.coordinator.name
                data['coordinator_email'] = self.coordinator.email
                data['coordinator_phone'] = self.coordinator.phone
                data['coordinator'] = {
                    'id': self.coordinator.id,
                    'name': self.coordinator.name,
                    'email': self.coordinator.email,
                    'phone': self.coordinator.phone
                }
            
            # Informações dos técnicos
            if hasattr(self, 'technicians'):
                data['members_count'] = len(self.technicians)
                data['technicians'] = [
                    {
                        'id': tech.id,
                        'user_id': tech.user_id,
                        'registration_number': tech.registration_number,
                        'specializations': tech.specializations if isinstance(tech.specializations, list) else [],
                        'experience_years': tech.experience_years,
                        'notes': tech.notes,
                        'user': {
                            'id': tech.user.id if tech.user else None,
                            'name': tech.user.name if tech.user else None,
                            'email': tech.user.email if tech.user else None,
                            'phone': tech.user.phone if tech.user else None,
                            'is_active': tech.user.is_active if tech.user else None
                        }
                    }
                    for tech in self.technicians
                ]
            
            # Contagem de contratos
            if hasattr(self, 'contracts'):
                data['contracts_count'] = len(self.contracts)
        
        return data
