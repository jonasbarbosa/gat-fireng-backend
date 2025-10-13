from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..models import db, Branch, Client
from ..decorators import role_required

branches_bp = Blueprint('branches', __name__)

@branches_bp.route('', methods=['GET'])
@jwt_required()
@role_required('superadmin', 'admin', 'coord')
def list_branches():
    """Lista todas as filiais
    ---
    tags:
      - 🏢 GAT - Filiais
    security:
      - Bearer: []
    parameters:
      - in: query
        name: company_id
        type: integer
        description: Filtrar por empresa
      - in: query
        name: is_active
        type: boolean
        description: Filtrar por status ativo/inativo
    responses:
      200:
        description: Lista de filiais
    """
    company_id = request.args.get('company_id', type=int)
    is_active = request.args.get('is_active', type=lambda v: v.lower() == 'true')
    
    query = Branch.query
    
    if company_id:
        query = query.filter_by(company_id=company_id)
    if is_active is not None:
        query = query.filter_by(is_active=is_active)
    
    branches = query.all()
    
    return jsonify({
        'branches': [branch.to_dict(include_relations=True) for branch in branches]
    }), 200


@branches_bp.route('', methods=['POST'])
@jwt_required()
@role_required('superadmin', 'admin', 'coord')
def create_branch():
    """Cria uma nova filial
    ---
    tags:
      - 🏢 GAT - Filiais
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
            - company_id
          properties:
            name:
              type: string
            cnpj:
              type: string
            address:
              type: string
            city:
              type: string
            state:
              type: string
            zip_code:
              type: string
            phone:
              type: string
            email:
              type: string
            company_id:
              type: integer
            notes:
              type: string
    responses:
      201:
        description: Filial criada com sucesso
      400:
        description: Dados inválidos
      404:
        description: Empresa não encontrada
    """
    data = request.get_json()
    
    # Validação
    if not data.get('name') or not data.get('company_id'):
        return jsonify({'error': 'Nome e empresa são obrigatórios'}), 400
    
    # Verificar se a empresa existe
    company = Client.query.get(data['company_id'])
    if not company:
        return jsonify({'error': 'Empresa não encontrada'}), 404
    
    # Verificar CNPJ duplicado
    if data.get('cnpj'):
        existing = Branch.query.filter_by(cnpj=data['cnpj']).first()
        if existing:
            return jsonify({'error': 'CNPJ já cadastrado'}), 409
    
    branch = Branch(
        name=data['name'],
        cnpj=data.get('cnpj'),
        address=data.get('address'),
        city=data.get('city'),
        state=data.get('state'),
        zip_code=data.get('zip_code'),
        phone=data.get('phone'),
        email=data.get('email'),
        company_id=data['company_id'],
        notes=data.get('notes')
    )
    
    db.session.add(branch)
    db.session.commit()
    
    return jsonify({
        'message': 'Filial criada com sucesso',
        'branch': branch.to_dict(include_relations=True)
    }), 201


@branches_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@role_required('superadmin', 'admin', 'coord', 'tecnico')
def get_branch(id):
    """Retorna detalhes de uma filial
    ---
    tags:
      - 🏢 GAT - Filiais
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        type: integer
        required: true
    responses:
      200:
        description: Detalhes da filial
      404:
        description: Filial não encontrada
    """
    branch = Branch.query.get(id)
    
    if not branch:
        return jsonify({'error': 'Filial não encontrada'}), 404
    
    return jsonify(branch.to_dict(include_relations=True)), 200


@branches_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@role_required('superadmin', 'admin', 'coord')
def update_branch(id):
    """Atualiza uma filial
    ---
    tags:
      - 🏢 GAT - Filiais
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
        description: Filial atualizada
      404:
        description: Filial não encontrada
    """
    branch = Branch.query.get(id)
    
    if not branch:
        return jsonify({'error': 'Filial não encontrada'}), 404
    
    data = request.get_json()
    
    # Verificar CNPJ duplicado
    if data.get('cnpj') and data['cnpj'] != branch.cnpj:
        existing = Branch.query.filter_by(cnpj=data['cnpj']).first()
        if existing:
            return jsonify({'error': 'CNPJ já cadastrado'}), 409
    
    # Atualizar campos
    if 'name' in data:
        branch.name = data['name']
    if 'cnpj' in data:
        branch.cnpj = data['cnpj']
    if 'address' in data:
        branch.address = data['address']
    if 'city' in data:
        branch.city = data['city']
    if 'state' in data:
        branch.state = data['state']
    if 'zip_code' in data:
        branch.zip_code = data['zip_code']
    if 'phone' in data:
        branch.phone = data['phone']
    if 'email' in data:
        branch.email = data['email']
    if 'is_active' in data:
        branch.is_active = data['is_active']
    if 'notes' in data:
        branch.notes = data['notes']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Filial atualizada com sucesso',
        'branch': branch.to_dict(include_relations=True)
    }), 200


@branches_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required('superadmin', 'admin')
def delete_branch(id):
    """Exclui uma filial
    ---
    tags:
      - 🏢 GAT - Filiais
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        type: integer
        required: true
    responses:
      200:
        description: Filial excluída
      404:
        description: Filial não encontrada
    """
    branch = Branch.query.get(id)
    
    if not branch:
        return jsonify({'error': 'Filial não encontrada'}), 404
    
    db.session.delete(branch)
    db.session.commit()
    
    return jsonify({'message': 'Filial excluída com sucesso'}), 200
