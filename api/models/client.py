from datetime import datetime
from .. import db

class Client(db.Model):
    """Modelo de cliente"""
    
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20))
    cpf_cnpj = db.Column(db.String(20), unique=True)
    address = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(2))
    zip_code = db.Column(db.String(10))
    is_active = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    inspections = db.relationship('Inspection', backref='client', lazy='dynamic')
    maintenances = db.relationship('Maintenance', backref='client', lazy='dynamic')
    branches = db.relationship('Branch', backref='company', lazy='dynamic')
    contracts = db.relationship('Contract', backref='company', lazy='dynamic')
    
    def __repr__(self):
        return f'<Client {self.name}>'
    
    def to_dict(self, include_relations=False):
        """Serializa o cliente para dicionário"""
        data = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'cpf_cnpj': self.cpf_cnpj,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'is_active': self.is_active,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_relations:
            data['branches_count'] = self.branches.count()
            data['contracts_count'] = self.contracts.count()
            data['inspections_count'] = self.inspections.count()
            data['maintenances_count'] = self.maintenances.count()
        
        return data

