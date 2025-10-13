from datetime import datetime
from .. import db

class Branch(db.Model):
    """Modelo de filial - Filiais das empresas clientes"""
    
    __tablename__ = 'branches'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(18), unique=True)
    address = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(2))
    zip_code = db.Column(db.String(10))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    is_active = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text)
    
    # Foreign Keys
    company_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Branch {self.id} - {self.name}>'
    
    def to_dict(self, include_relations=False):
        """Serializa a filial para dicionário"""
        data = {
            'id': self.id,
            'name': self.name,
            'cnpj': self.cnpj,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'phone': self.phone,
            'email': self.email,
            'is_active': self.is_active,
            'notes': self.notes,
            'company_id': self.company_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_relations:
            if self.company:
                data['company'] = {
                    'id': self.company.id,
                    'name': self.company.name
                }
        
        return data
