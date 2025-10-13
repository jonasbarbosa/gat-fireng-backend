from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Technician, User, Team
from decorators import role_required

technicians_bp = Blueprint('technicians', __name__)

@technicians_bp.route('', methods=['GET'])
@jwt_required()
@role_required('superadmin', 'admin', 'coord')
def list_technicians():
    """Lista todos os técnicos
    ---
    tags:
      - 🔧 GAT - Técnicos
    security:
      - Bearer: []
    parameters:
      - in: query
        name: team_id
        type: integer
        description: Filtrar por equipe
      - in: query
        name: is_available
        type: boolean
        description: Filtrar por disponibilidade
    responses:
      200:
        description: Lista de técnicos
    """
    team_id = request.args.get('team_id', type=int)
    is_available = request.args.get('is_available', type=lambda v: v.lower() == 'true')
    
    query = Technician.query
    
    if team_id:
        query = query.filter_by(team_id=team_id)
    if is_available is not None:
        query = query.filter_by(is_available=is_available)
    
    technicians = query.all()
    
    return jsonify({
        'technicians': [tech.to_dict(include_relations=True) for tech in technicians]
    }), 200


@technicians_bp.route('', methods=['POST'])
@jwt_required()
@role_required('superadmin', 'admin', 'coord')
def create_technician():
    """Cria um novo perfil de técnico
    ---
    tags:
      - 🔧 GAT - Técnicos
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - user_id
          properties:
            user_id:
              type: integer
            registration_number:
              type: string
            specialty:
              type: string
            team_id:
              type: integer
    responses:
      201:
        description: Técnico criado com sucesso
      400:
        description: Dados inválidos
      404:
        description: Usuário não encontrado
      409:
        description: Usuário já possui perfil de técnico
    """
    data = request.get_json()
    
    # Validação
    if not data.get('user_id'):
        return jsonify({'error': 'user_id é obrigatório'}), 400
    
    # Verificar se o usuário existe
    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    # Verificar se já existe perfil de técnico para este usuário
    existing = Technician.query.filter_by(user_id=data['user_id']).first()
    if existing:
        return jsonify({'error': 'Usuário já possui perfil de técnico'}), 409
    
    # Verificar matrícula duplicada
    if data.get('registration_number'):
        existing_reg = Technician.query.filter_by(registration_number=data['registration_number']).first()
        if existing_reg:
            return jsonify({'error': 'Número de matrícula já existe'}), 409
    
    # Verificar equipe se fornecida
    if data.get('team_id'):
        team = Team.query.get(data['team_id'])
        if not team:
            return jsonify({'error': 'Equipe não encontrada'}), 404
    
    technician = Technician(
        user_id=data['user_id'],
        registration_number=data.get('registration_number'),
        specialty=data.get('specialty'),
        team_id=data.get('team_id')
    )
    
    db.session.add(technician)
    db.session.commit()
    
    return jsonify({
        'message': 'Técnico criado com sucesso',
        'technician': technician.to_dict(include_relations=True)
    }), 201


@technicians_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@role_required('superadmin', 'admin', 'coord', 'tecnico')
def get_technician(id):
    """Retorna detalhes de um técnico
    ---
    tags:
      - 🔧 GAT - Técnicos
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        type: integer
        required: true
    responses:
      200:
        description: Detalhes do técnico
      404:
        description: Técnico não encontrado
    """
    technician = Technician.query.get(id)
    
    if not technician:
        return jsonify({'error': 'Técnico não encontrado'}), 404
    
    return jsonify(technician.to_dict(include_relations=True)), 200


@technicians_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@role_required('superadmin', 'admin', 'coord')
def update_technician(id):
    """Atualiza um técnico
    ---
    tags:
      - 🔧 GAT - Técnicos
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
        description: Técnico atualizado
      404:
        description: Técnico não encontrado
    """
    technician = Technician.query.get(id)
    
    if not technician:
        return jsonify({'error': 'Técnico não encontrado'}), 404
    
    data = request.get_json()
    
    # Verificar matrícula duplicada
    if data.get('registration_number') and data['registration_number'] != technician.registration_number:
        existing = Technician.query.filter_by(registration_number=data['registration_number']).first()
        if existing:
            return jsonify({'error': 'Número de matrícula já existe'}), 409
    
    # Atualizar campos
    if 'registration_number' in data:
        technician.registration_number = data['registration_number']
    if 'specialty' in data:
        technician.specialty = data['specialty']
    if 'is_available' in data:
        technician.is_available = data['is_available']
    if 'team_id' in data:
        technician.team_id = data['team_id']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Técnico atualizado com sucesso',
        'technician': technician.to_dict(include_relations=True)
    }), 200


@technicians_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required('superadmin', 'admin')
def delete_technician(id):
    """Exclui um técnico
    ---
    tags:
      - 🔧 GAT - Técnicos
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        type: integer
        required: true
    responses:
      200:
        description: Técnico excluído
      404:
        description: Técnico não encontrado
    """
    technician = Technician.query.get(id)
    
    if not technician:
        return jsonify({'error': 'Técnico não encontrado'}), 404
    
    db.session.delete(technician)
    db.session.commit()
    
    return jsonify({'message': 'Técnico excluído com sucesso'}), 200
