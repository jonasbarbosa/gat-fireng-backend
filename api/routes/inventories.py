from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..models import db, Inventory, Branch
from ..decorators import role_required

inventories_bp = Blueprint('inventories', __name__)

@inventories_bp.route('', methods=['GET'])
@jwt_required()
@role_required('superadmin', 'admin', 'coord', 'tecnico')
def list_inventories():
    """Lista todos os inventários
    ---
    tags:
      - 📦 GAT - Inventários
    security:
      - Bearer: []
    parameters:
      - in: query
        name: branch_id
        type: integer
        description: Filtrar por filial
    responses:
      200:
        description: Lista de inventários
    """
    branch_id = request.args.get('branch_id', type=int)
    
    query = Inventory.query
    
    if branch_id:
        query = query.filter_by(branch_id=branch_id)
    
    inventories = query.all()
    
    return jsonify({
        'inventories': [inv.to_dict(include_relations=True) for inv in inventories]
    }), 200


@inventories_bp.route('', methods=['POST'])
@jwt_required()
@role_required('superadmin', 'admin', 'coord')
def create_inventory():
    """Cria um novo inventário
    ---
    tags:
      - 📦 GAT - Inventários
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - branch_id
          properties:
            branch_id:
              type: integer
            status:
              type: string
            notes:
              type: string
    responses:
      201:
        description: Inventário criado com sucesso
      400:
        description: Dados inválidos
      404:
        description: Filial não encontrada
      409:
        description: Filial já possui inventário
    """
    data = request.get_json()
    
    # Validação
    if not data.get('branch_id'):
        return jsonify({'error': 'Filial é obrigatória'}), 400
    
    # Verificar se a filial existe
    branch = Branch.query.get(data['branch_id'])
    if not branch:
        return jsonify({'error': 'Filial não encontrada'}), 404
    
    # Verificar se já existe inventário para esta filial
    existing = Inventory.query.filter_by(branch_id=data['branch_id']).first()
    if existing:
        return jsonify({'error': 'Filial já possui inventário'}), 409
    
    inventory = Inventory(
        branch_id=data['branch_id'],
        status=data.get('status', 'atualizado'),
        notes=data.get('notes', '')
    )
    
    db.session.add(inventory)
    db.session.commit()
    
    return jsonify({
        'message': 'Inventário criado com sucesso',
        'inventory': inventory.to_dict(include_relations=True)
    }), 201


@inventories_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@role_required('superadmin', 'admin', 'coord', 'tecnico')
def get_inventory(id):
    """Retorna detalhes de um inventário
    ---
    tags:
      - 📦 GAT - Inventários
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        type: integer
        required: true
    responses:
      200:
        description: Detalhes do inventário
      404:
        description: Inventário não encontrado
    """
    inventory = Inventory.query.get(id)
    
    if not inventory:
        return jsonify({'error': 'Inventário não encontrado'}), 404
    
    return jsonify(inventory.to_dict(include_relations=True)), 200


@inventories_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@role_required('superadmin', 'admin', 'coord')
def update_inventory(id):
    """Atualiza um inventário
    ---
    tags:
      - 📦 GAT - Inventários
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
        description: Inventário atualizado
      404:
        description: Inventário não encontrado
    """
    inventory = Inventory.query.get(id)
    
    if not inventory:
        return jsonify({'error': 'Inventário não encontrado'}), 404
    
    data = request.get_json()
    
    # Atualizar campos
    if 'name' in data:
        inventory.name = data['name']
    if 'description' in data:
        inventory.description = data['description']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Inventário atualizado com sucesso',
        'inventory': inventory.to_dict(include_relations=True)
    }), 200


@inventories_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required('superadmin', 'admin')
def delete_inventory(id):
    """Exclui um inventário
    ---
    tags:
      - 📦 GAT - Inventários
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        type: integer
        required: true
    responses:
      200:
        description: Inventário excluído
      404:
        description: Inventário não encontrado
    """
    inventory = Inventory.query.get(id)
    
    if not inventory:
        return jsonify({'error': 'Inventário não encontrado'}), 404
    
    db.session.delete(inventory)
    db.session.commit()
    
    return jsonify({'message': 'Inventário excluído com sucesso'}), 200
