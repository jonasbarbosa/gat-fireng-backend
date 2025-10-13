from datetime import datetime
from models import db

class Technician(db.Model):
    """Modelo de técnico - Perfil especializado de usuários técnicos"""
    
    __tablename__ = 'technicians'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    
    # Dados específicos do técnico
    registration_number = db.Column(db.String(50), unique=True)
    specializations = db.Column(db.Text)  # JSON: ["sprinklers", "alarme", "extintores"]
    certifications = db.Column(db.Text)  # JSON: [{"name": "NR10", "date": "2024-01-01", "expiry": "2025-01-01"}]
    experience_years = db.Column(db.Integer)
    notes = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='technician_profile')
    team = db.relationship('Team', backref='technicians')
    
    def __repr__(self):
        return f'<Technician {self.id} - User {self.user_id}>'
    
    def to_dict(self, include_relations=False):
        """Serializa o técnico para dicionário"""
        import json
        
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'team_id': self.team_id,
            'registration_number': self.registration_number,
            'specializations': json.loads(self.specializations) if self.specializations else [],
            'certifications': json.loads(self.certifications) if self.certifications else [],
            'experience_years': self.experience_years,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_relations:
            if self.user:
                data['user'] = {
                    'id': self.user.id,
                    'name': self.user.name,
                    'email': self.user.email,
                    'phone': self.user.phone,
                    'role': self.user.role
                }
            if self.team:
                data['team'] = {
                    'id': self.team.id,
                    'name': self.team.name,
                    'specialization': self.team.specialization
                }
        
        return data
