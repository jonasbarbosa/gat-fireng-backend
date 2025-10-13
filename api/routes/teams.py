from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Team
from decorators import role_required

teams_bp = Blueprint('teams', __name__)

@teams_bp.route('', methods=['GET'])
@jwt_required()
@role_required('superadmin', 'admin', 'coord')
def list_teams():
    """Lista todas as equipes
    ---
    tags:
      - 👥 GAT - Equipes
    security:
      - Bearer: []
    parameters:
      - in: query
        name: is_active
        type: boolean
        description: Filtrar por status ativo/inativo
    responses:
      200:
        description: Lista de equipes
    """
    is_active = request.args.get('is_active', type=lambda v: v.lower() == 'true')
    
    query = Team.query
    
    if is_active is not None:
        query = query.filter_by(is_active=is_active)
    
    teams = query.all()
    
    return jsonify({
        'teams': [team.to_dict(include_relations=True) for team in teams]
    }), 200


@teams_bp.route('', methods=['POST'])
@jwt_required()
@role_required('superadmin', 'admin', 'coord')
def create_team():
    """Cria uma nova equipe
    ---
    tags:
      - 👥 GAT - Equipes
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
          properties:
            name:
              type: string
            description:
              type: string
    responses:
      201:
        description: Equipe criada com sucesso
      400:
        description: Dados inválidos
      409:
        description: Nome de equipe já existe
    """
    data = request.get_json()
    
    # Validação
    if not data.get('name'):
        return jsonify({'error': 'Nome é obrigatório'}), 400
    
    # Verificar nome duplicado
    existing = Team.query.filter_by(name=data['name']).first()
    if existing:
        return jsonify({'error': 'Nome de equipe já existe'}), 409
    
    team = Team(
        name=data['name'],
        description=data.get('description'),
        specialization=data.get('specialization'),
        coordinator_id=data.get('coordinator_id')
    )
    
    db.session.add(team)
    db.session.commit()
    
    return jsonify({
        'message': 'Equipe criada com sucesso',
        'team': team.to_dict(include_relations=True)
    }), 201


@teams_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@role_required('superadmin', 'admin', 'coord', 'tecnico')
def get_team(id):
    """Retorna detalhes de uma equipe
    ---
    tags:
      - 👥 GAT - Equipes
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID da equipe
      - in: query
        name: include_relations
        type: boolean
        description: Incluir relacionamentos (técnicos, coordenador)
    responses:
      200:
        description: Detalhes da equipe
      404:
        description: Equipe não encontrada
    """
    include_relations = request.args.get('include_relations', type=lambda v: v.lower() == 'true')
    
    team = Team.query.get(id)
    
    if not team:
        return jsonify({'error': 'Equipe não encontrada'}), 404
    
    return jsonify({
        'team': team.to_dict(include_relations=include_relations)
    }), 200


@teams_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@role_required('superadmin', 'admin', 'coord')
def update_team(id):
    """Atualiza uma equipe
    ---
    tags:
      - 👥 GAT - Equipes
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
        description: Equipe atualizada
      404:
        description: Equipe não encontrada
    """
    team = Team.query.get(id)
    
    if not team:
        return jsonify({'error': 'Equipe não encontrada'}), 404
    
    data = request.get_json()
    
    # Verificar nome duplicado
    if data.get('name') and data['name'] != team.name:
        existing = Team.query.filter_by(name=data['name']).first()
        if existing:
            return jsonify({'error': 'Nome de equipe já existe'}), 409
    
    # Atualizar campos
    if 'name' in data:
        team.name = data['name']
    if 'description' in data:
        team.description = data['description']
    if 'specialization' in data:
        team.specialization = data['specialization']
    if 'coordinator_id' in data:
        team.coordinator_id = data['coordinator_id']
    if 'is_active' in data:
        team.is_active = data['is_active']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Equipe atualizada com sucesso',
        'team': team.to_dict(include_relations=True)
    }), 200


@teams_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required('superadmin', 'admin')
def delete_team(id):
    """Exclui uma equipe
    ---
    tags:
      - 👥 GAT - Equipes
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        type: integer
        required: true
    responses:
      200:
        description: Equipe excluída
      404:
        description: Equipe não encontrada
    """
    team = Team.query.get(id)
    
    if not team:
        return jsonify({'error': 'Equipe não encontrada'}), 404
    
    db.session.delete(team)
    db.session.commit()
    
    return jsonify({'message': 'Equipe excluída com sucesso'}), 200
