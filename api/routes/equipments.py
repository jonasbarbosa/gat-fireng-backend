from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime
from models import db, Equipment, Inventory, Standard
from decorators import role_required

equipments_bp = Blueprint('equipments', __name__)

@equipments_bp.route('', methods=['GET'])
@jwt_required()
@role_required('superadmin', 'admin', 'coord', 'tecnico')
def list_equipments():
    """Lista todos os equipamentos
    ---
    tags:
      - 🧯 GAT - Equipamentos
    security:
      - Bearer: []
    parameters:
      - in: query
        name: inventory_id
        type: integer
        description: Filtrar por inventário
      - in: query
        name: is_active
        type: boolean
        description: Filtrar por status ativo/inativo
    responses:
      200:
        description: Lista de equipamentos
    """
    inventory_id = request.args.get('inventory_id', type=int)
    is_active = request.args.get('is_active', type=lambda v: v.lower() == 'true')
    
    query = Equipment.query
    
    if inventory_id:
        query = query.filter_by(inventory_id=inventory_id)
    if is_active is not None:
        query = query.filter_by(is_active=is_active)
    
    equipments = query.all()
    
    return jsonify({
        'equipments': [equip.to_dict(include_relations=True) for equip in equipments]
    }), 200


@equipments_bp.route('', methods=['POST'])
@jwt_required()
@role_required('superadmin', 'admin', 'coord')
def create_equipment():
    """Cria um novo equipamento
    ---
    tags:
      - 🧯 GAT - Equipamentos
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - serial_number
            - inventory_id
          properties:
            name:
              type: string
            serial_number:
              type: string
            model:
              type: string
            manufacturer:
              type: string
            installation_date:
              type: string
              format: date-time
            last_inspection_date:
              type: string
              format: date
            next_inspection_date:
              type: string
              format: date
            location_description:
              type: string
            inventory_id:
              type: integer
            standard_ids:
              type: array
              items:
                type: integer
            notes:
              type: string
    responses:
      201:
        description: Equipamento criado com sucesso
      400:
        description: Dados inválidos
      404:
        description: Inventário não encontrado
      409:
        description: Número de série já existe
    """
    data = request.get_json()
    
    # Validação
    required_fields = ['name', 'serial_number', 'inventory_id']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} é obrigatório'}), 400
    
    # Verificar se o inventário existe
    inventory = Inventory.query.get(data['inventory_id'])
    if not inventory:
        return jsonify({'error': 'Inventário não encontrado'}), 404
    
    # Verificar número de série duplicado
    existing = Equipment.query.filter_by(serial_number=data['serial_number']).first()
    if existing:
        return jsonify({'error': 'Número de série já existe'}), 409
    
    equipment = Equipment(
        name=data['name'],
        type=data.get('type', 'extintor'),
        serial_number=data['serial_number'],
        model=data.get('model'),
        manufacturer=data.get('manufacturer'),
        installation_date=datetime.fromisoformat(data['installation_date'].replace('Z', '+00:00')) if data.get('installation_date') else None,
        last_inspection_date=datetime.fromisoformat(data['last_inspection_date'].replace('Z', '+00:00')).date() if data.get('last_inspection_date') else None,
        next_inspection_date=datetime.fromisoformat(data['next_inspection_date'].replace('Z', '+00:00')).date() if data.get('next_inspection_date') else None,
        location=data.get('location'),
        inventory_id=data['inventory_id'],
        notes=data.get('notes')
    )
    
    # Adicionar normas se fornecidas
    if data.get('standard_ids'):
        for standard_id in data['standard_ids']:
            standard = Standard.query.get(standard_id)
            if standard:
                equipment.standards.append(standard)
    
    db.session.add(equipment)
    db.session.commit()
    
    return jsonify({
        'message': 'Equipamento criado com sucesso',
        'equipment': equipment.to_dict(include_relations=True)
    }), 201


@equipments_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@role_required('superadmin', 'admin', 'coord', 'tecnico')
def get_equipment(id):
    """Retorna detalhes de um equipamento
    ---
    tags:
      - 🧯 GAT - Equipamentos
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        type: integer
        required: true
    responses:
      200:
        description: Detalhes do equipamento
      404:
        description: Equipamento não encontrado
    """
    equipment = Equipment.query.get(id)
    
    if not equipment:
        return jsonify({'error': 'Equipamento não encontrado'}), 404
    
    return jsonify(equipment.to_dict(include_relations=True)), 200


@equipments_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@role_required('superadmin', 'admin', 'coord')
def update_equipment(id):
    """Atualiza um equipamento
    ---
    tags:
      - 🧯 GAT - Equipamentos
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        type: integer
        required: true
      - in: body
        name: body
        schema:
          type: object
    responses:
      200:
        description: Equipamento atualizado
      404:
        description: Equipamento não encontrado
    """
    equipment = Equipment.query.get(id)
    
    if not equipment:
        return jsonify({'error': 'Equipamento não encontrado'}), 404
    
    data = request.get_json()
    
    # Verificar número de série duplicado
    if data.get('serial_number') and data['serial_number'] != equipment.serial_number:
        existing = Equipment.query.filter_by(serial_number=data['serial_number']).first()
        if existing:
            return jsonify({'error': 'Número de série já existe'}), 409
    
    # Atualizar campos
    if 'name' in data:
        equipment.name = data['name']
    if 'serial_number' in data:
        equipment.serial_number = data['serial_number']
    if 'model' in data:
        equipment.model = data['model']
    if 'manufacturer' in data:
        equipment.manufacturer = data['manufacturer']
    if 'installation_date' in data:
        equipment.installation_date = datetime.fromisoformat(data['installation_date'].replace('Z', '+00:00')) if data['installation_date'] else None
    if 'last_inspection_date' in data:
        equipment.last_inspection_date = datetime.fromisoformat(data['last_inspection_date'].replace('Z', '+00:00')).date() if data['last_inspection_date'] else None
    if 'next_inspection_date' in data:
        equipment.next_inspection_date = datetime.fromisoformat(data['next_inspection_date'].replace('Z', '+00:00')).date() if data['next_inspection_date'] else None
    if 'location' in data:
        equipment.location = data['location']
    if 'is_active' in data:
        equipment.is_active = data['is_active']
    if 'notes' in data:
        equipment.notes = data['notes']
    
    # Atualizar normas se fornecidas
    if 'standard_ids' in data:
        equipment.standards.clear()
        for standard_id in data['standard_ids']:
            standard = Standard.query.get(standard_id)
            if standard:
                equipment.standards.append(standard)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Equipamento atualizado com sucesso',
        'equipment': equipment.to_dict(include_relations=True)
    }), 200


@equipments_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required('superadmin', 'admin')
def delete_equipment(id):
    """Exclui um equipamento
    ---
    tags:
      - 🧯 GAT - Equipamentos
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        type: integer
        required: true
    responses:
      200:
        description: Equipamento excluído
      404:
        description: Equipamento não encontrado
    """
    equipment = Equipment.query.get(id)
    
    if not equipment:
        return jsonify({'error': 'Equipamento não encontrado'}), 404
    
    db.session.delete(equipment)
    db.session.commit()
    
    return jsonify({'message': 'Equipamento excluído com sucesso'}), 200
