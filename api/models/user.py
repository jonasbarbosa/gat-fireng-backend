from datetime import datetime
import bcrypt
from . import db

class User(db.Model):
    """Modelo de usuário com controle de roles"""
    
    __tablename__ = 'users'
    
    # Roles disponíveis no sistema
    ROLES = ['superadmin', 'admin', 'coord', 'tecnico', 'cliente']
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='tecnico')
    phone = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos - removidos temporariamente para resolver conflito
    # inspections = db.relationship('Inspection', backref='technician_user', lazy='dynamic', 
    #                              foreign_keys='Inspection.technician_id')
    # maintenances = db.relationship('Maintenance', backref='technician_user', lazy='dynamic',
    #                               foreign_keys='Maintenance.technician_id')
    
    def __repr__(self):
        return f'<User {self.email} - {self.role}>'
    
    def set_password(self, password):
        """Gera hash da senha usando bcrypt"""
        # Gera salt e hash com bcrypt (12 rounds)
        salt = bcrypt.gensalt(rounds=12)
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, password):
        """Verifica se a senha está correta"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def has_role(self, *roles):
        """Verifica se o usuário possui uma das roles especificadas"""
        return self.role in roles
    
    def to_dict(self, include_sensitive=False):
        """Serializa o usuário para dicionário"""
        data = {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'role': self.role,
            'phone': self.phone,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        return data
    
    @staticmethod
    def validate_role(role):
        """Valida se a role é válida"""
        return role in User.ROLES

