from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Standard
from decorators import role_required

standards_bp = Blueprint('standards', __name__)

@standards_bp.route('', methods=['GET'])
@jwt_required()
@role_required('superadmin', 'admin', 'coord', 'tecnico')
def list_standards():
    """Lista todas as normas técnicas
    ---
    tags:
      - 📋 GAT - Normas
    security:
      - Bearer: []
    parameters:
      - in: query
        name: is_active
        type: boolean
        description: Filtrar por status ativo/inativo
    responses:
      200:
        description: Lista de normas
    """
    is_active = request.args.get('is_active', type=lambda v: v.lower() == 'true')
    
    query = Standard.query
    
    if is_active is not None:
        query = query.filter_by(is_active=is_active)
    
    standards = query.all()
    
    return jsonify({
        'standards': [standard.to_dict() for standard in standards]
    }), 200


@standards_bp.route('', methods=['POST'])
@jwt_required()
@role_required('superadmin', 'admin', 'coord')
def create_standard():
    """Cria uma nova norma técnica
    ---
    tags:
      - 📋 GAT - Normas
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
            - code
          properties:
            name:
              type: string
              example: "Extintores de incêndio"
            code:
              type: string
              example: "NBR 12962"
            description:
              type: string
    responses:
      201:
        description: Norma criada com sucesso
      400:
        description: Dados inválidos
      409:
        description: Nome ou código já existe
    """
    data = request.get_json()
    
    # Validação
    if not data.get('name') or not data.get('code'):
        return jsonify({'error': 'Nome e código são obrigatórios'}), 400
    
    # Verificar nome duplicado
    existing_name = Standard.query.filter_by(name=data['name']).first()
    if existing_name:
        return jsonify({'error': 'Nome de norma já existe'}), 409
    
    # Verificar código duplicado
    existing_code = Standard.query.filter_by(code=data['code']).first()
    if existing_code:
        return jsonify({'error': 'Código de norma já existe'}), 409
    
    standard = Standard(
        name=data['name'],
        code=data['code'],
        description=data.get('description')
    )
    
    db.session.add(standard)
    db.session.commit()
    
    return jsonify({
        'message': 'Norma criada com sucesso',
        'standard': standard.to_dict()
    }), 201


@standards_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@role_required('superadmin', 'admin', 'coord', 'tecnico')
def get_standard(id):
    """Retorna detalhes de uma norma
    ---
    tags:
      - 📋 GAT - Normas
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        type: integer
        required: true
    responses:
      200:
        description: Detalhes da norma
      404:
        description: Norma não encontrada
    """
    standard = Standard.query.get(id)
    
    if not standard:
        return jsonify({'error': 'Norma não encontrada'}), 404
    
    return jsonify(standard.to_dict()), 200


@standards_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@role_required('superadmin', 'admin', 'coord')
def update_standard(id):
    """Atualiza uma norma
    ---
    tags:
      - 📋 GAT - Normas
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
        description: Norma atualizada
      404:
        description: Norma não encontrada
    """
    standard = Standard.query.get(id)
    
    if not standard:
        return jsonify({'error': 'Norma não encontrada'}), 404
    
    data = request.get_json()
    
    # Verificar nome duplicado
    if data.get('name') and data['name'] != standard.name:
        existing = Standard.query.filter_by(name=data['name']).first()
        if existing:
            return jsonify({'error': 'Nome de norma já existe'}), 409
    
    # Verificar código duplicado
    if data.get('code') and data['code'] != standard.code:
        existing = Standard.query.filter_by(code=data['code']).first()
        if existing:
            return jsonify({'error': 'Código de norma já existe'}), 409
    
    # Atualizar campos
    if 'name' in data:
        standard.name = data['name']
    if 'code' in data:
        standard.code = data['code']
    if 'description' in data:
        standard.description = data['description']
    if 'is_active' in data:
        standard.is_active = data['is_active']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Norma atualizada com sucesso',
        'standard': standard.to_dict()
    }), 200


@standards_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required('superadmin', 'admin')
def delete_standard(id):
    """Exclui uma norma
    ---
    tags:
      - 📋 GAT - Normas
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        type: integer
        required: true
    responses:
      200:
        description: Norma excluída
      404:
        description: Norma não encontrada
    """
    standard = Standard.query.get(id)
    
    if not standard:
        return jsonify({'error': 'Norma não encontrada'}), 404
    
    db.session.delete(standard)
    db.session.commit()
    
    return jsonify({'message': 'Norma excluída com sucesso'}), 200
