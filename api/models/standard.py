from datetime import datetime
from models import db

class Standard(db.Model):
    """Modelo de norma - Normas técnicas NBR, IT, NR"""
    
    __tablename__ = 'standards'
    
    # Tipos de norma
    TYPE_NBR = 'NBR'  # Norma Brasileira
    TYPE_IT = 'IT'    # Instrução Técnica
    TYPE_NR = 'NR'    # Norma Regulamentadora
    TYPE_ABNT = 'ABNT'  # Associação Brasileira de Normas Técnicas
    
    TYPES = [TYPE_NBR, TYPE_IT, TYPE_NR, TYPE_ABNT]
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)  # Ex: NBR 10897, IT 17
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    type = db.Column(db.String(20), nullable=False)
    version = db.Column(db.String(20))
    publication_date = db.Column(db.Date)
    revision_date = db.Column(db.Date)
    document_url = db.Column(db.String(500))
    summary = db.Column(db.Text)  # Resumo da norma
    scope = db.Column(db.Text)  # Escopo de aplicação
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Standard {self.code} - {self.name}>'
    
    def to_dict(self):
        """Serializa a norma para dicionário"""
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'description': self.description,
            'type': self.type,
            'version': self.version,
            'publication_date': self.publication_date.isoformat() if self.publication_date else None,
            'revision_date': self.revision_date.isoformat() if self.revision_date else None,
            'document_url': self.document_url,
            'summary': self.summary,
            'scope': self.scope,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def validate_type(type):
        """Valida se o tipo é válido"""
        return type in Standard.TYPES
