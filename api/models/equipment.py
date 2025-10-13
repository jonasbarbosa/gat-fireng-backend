from datetime import datetime
from models import db

# Tabela de relacionamento N:N entre Equipment e Standard
equipment_standards = db.Table('equipment_standards',
    db.Column('equipment_id', db.Integer, db.ForeignKey('equipments.id'), primary_key=True),
    db.Column('standard_id', db.Integer, db.ForeignKey('standards.id'), primary_key=True),
    db.Column('created_at', db.DateTime, default=datetime.utcnow)
)

class Equipment(db.Model):
    """Modelo de equipamento - Equipamentos de combate a incêndio"""
    
    __tablename__ = 'equipments'
    
    # Tipos de equipamento
    TYPE_EXTINGUISHER = 'extintor'
    TYPE_HYDRANT = 'hidrante'
    TYPE_SPRINKLER = 'sprinkler'
    TYPE_ALARM = 'alarme'
    TYPE_EMERGENCY_LIGHT = 'iluminacao_emergencia'
    TYPE_FIRE_DOOR = 'porta_corta_fogo'
    TYPE_HOSE = 'mangueira'
    TYPE_PUMP = 'bomba'
    
    TYPES = [TYPE_EXTINGUISHER, TYPE_HYDRANT, TYPE_SPRINKLER, TYPE_ALARM, 
             TYPE_EMERGENCY_LIGHT, TYPE_FIRE_DOOR, TYPE_HOSE, TYPE_PUMP]
    
    # Status
    STATUS_ACTIVE = 'ativo'
    STATUS_INACTIVE = 'inativo'
    STATUS_MAINTENANCE = 'manutencao'
    STATUS_EXPIRED = 'vencido'
    
    STATUSES = [STATUS_ACTIVE, STATUS_INACTIVE, STATUS_MAINTENANCE, STATUS_EXPIRED]
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    manufacturer = db.Column(db.String(100))
    model = db.Column(db.String(100))
    serial_number = db.Column(db.String(100))
    tag_number = db.Column(db.String(50))  # Número de identificação/plaqueta
    manufacturing_date = db.Column(db.Date)
    installation_date = db.Column(db.Date)
    last_inspection_date = db.Column(db.Date)
    next_inspection_date = db.Column(db.Date)
    expiry_date = db.Column(db.Date)  # Data de validade (para extintores, etc)
    status = db.Column(db.String(20), default=STATUS_ACTIVE)
    location = db.Column(db.String(255))  # Localização física
    capacity = db.Column(db.String(50))  # Capacidade (ex: 6kg, 10L)
    notes = db.Column(db.Text)
    
    # Foreign Keys
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventories.id'))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    inventory = db.relationship('Inventory', backref='equipments')
    standards = db.relationship('Standard', secondary=equipment_standards, backref='equipments')
    
    def __repr__(self):
        return f'<Equipment {self.id} - {self.name}>'
    
    def to_dict(self, include_relations=False):
        """Serializa o equipamento para dicionário"""
        data = {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'manufacturer': self.manufacturer,
            'model': self.model,
            'serial_number': self.serial_number,
            'tag_number': self.tag_number,
            'manufacturing_date': self.manufacturing_date.isoformat() if self.manufacturing_date else None,
            'installation_date': self.installation_date.isoformat() if self.installation_date else None,
            'last_inspection_date': self.last_inspection_date.isoformat() if self.last_inspection_date else None,
            'next_inspection_date': self.next_inspection_date.isoformat() if self.next_inspection_date else None,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'status': self.status,
            'location': self.location,
            'capacity': self.capacity,
            'notes': self.notes,
            'inventory_id': self.inventory_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_relations:
            if self.inventory:
                data['inventory'] = {
                    'id': self.inventory.id,
                    'branch_id': self.inventory.branch_id
                }
            if self.standards:
                data['standards'] = [
                    {
                        'id': std.id,
                        'code': std.code,
                        'name': std.name
                    }
                    for std in self.standards
                ]
        
        return data
    
    @staticmethod
    def validate_type(type):
        """Valida se o tipo é válido"""
        return type in Equipment.TYPES
    
    @staticmethod
    def validate_status(status):
        """Valida se o status é válido"""
        return status in Equipment.STATUSES
