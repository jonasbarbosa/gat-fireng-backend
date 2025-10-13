from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime
from ..models import db, Contract, Client, Team
from ..decorators import role_required

contracts_bp = Blueprint('contracts', __name__)

@contracts_bp.route('', methods=['GET'])
@jwt_required()
@role_required('superadmin', 'admin', 'coord')
def list_contracts():
    """Lista todos os contratos
    ---
    tags:
      - 📄 GAT - Contratos
    security:
      - Bearer: []
    parameters:
      - in: query
        name: company_id
        type: integer
        description: Filtrar por empresa
      - in: query
        name: status
        type: string
        description: Filtrar por status (ativo, inativo, expirado, suspenso)
    responses:
      200:
        description: Lista de contratos
    """
    company_id = request.args.get('company_id', type=int)
    status = request.args.get('status')
    
    query = Contract.query
    
    if company_id:
        query = query.filter_by(company_id=company_id)
    if status:
        query = query.filter_by(status=status)
    
    contracts = query.all()
    
    return jsonify({
        'contracts': [contract.to_dict(include_relations=True) for contract in contracts]
    }), 200


@contracts_bp.route('', methods=['POST'])
@jwt_required()
@role_required('superadmin', 'admin', 'coord')
def create_contract():
    """Cria um novo contrato
    ---
    tags:
      - 📄 GAT - Contratos
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - contract_number
            - company_id
            - start_date
          properties:
            contract_number:
              type: string
            description:
              type: string
            start_date:
              type: string
              format: date-time
            end_date:
              type: string
              format: date-time
            status:
              type: string
              enum: [ativo, inativo, expirado, suspenso]
            value:
              type: number
            company_id:
              type: integer
            branch_id:
              type: integer
            team_id:
              type: integer
    responses:
      201:
        description: Contrato criado com sucesso
      400:
        description: Dados inválidos
      404:
        description: Empresa não encontrada
      409:
        description: Número de contrato já existe
    """
    data = request.get_json()
    
    # Validação
    required_fields = ['contract_number', 'company_id', 'start_date']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} é obrigatório'}), 400
    
    # Verificar se a empresa existe
    company = Client.query.get(data['company_id'])
    if not company:
        return jsonify({'error': 'Empresa não encontrada'}), 404
    
    # Verificar número de contrato duplicado
    existing = Contract.query.filter_by(contract_number=data['contract_number']).first()
    if existing:
        return jsonify({'error': 'Número de contrato já existe'}), 409
    
    # Nota: branch_id não é usado no modelo Contract
    
    # Verificar equipe se fornecida
    if data.get('team_id'):
        team = Team.query.get(data['team_id'])
        if not team:
            return jsonify({'error': 'Equipe não encontrada'}), 404
    
    contract = Contract(
        contract_number=data['contract_number'],
        description=data.get('description'),
        start_date=datetime.fromisoformat(data['start_date'].replace('Z', '+00:00')),
        end_date=datetime.fromisoformat(data['end_date'].replace('Z', '+00:00')) if data.get('end_date') else None,
        status=data.get('status', 'ativo'),
        value=data.get('value'),
        company_id=data['company_id'],
        team_id=data.get('team_id')
    )
    
    db.session.add(contract)
    db.session.commit()
    
    return jsonify({
        'message': 'Contrato criado com sucesso',
        'contract': contract.to_dict(include_relations=True)
    }), 201


@contracts_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@role_required('superadmin', 'admin', 'coord', 'tecnico')
def get_contract(id):
    """Retorna detalhes de um contrato
    ---
    tags:
      - 📄 GAT - Contratos
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        type: integer
        required: true
    responses:
      200:
        description: Detalhes do contrato
      404:
        description: Contrato não encontrado
    """
    contract = Contract.query.get(id)
    
    if not contract:
        return jsonify({'error': 'Contrato não encontrado'}), 404
    
    return jsonify(contract.to_dict(include_relations=True)), 200


@contracts_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@role_required('superadmin', 'admin', 'coord')
def update_contract(id):
    """Atualiza um contrato
    ---
    tags:
      - 📄 GAT - Contratos
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
        description: Contrato atualizado
      404:
        description: Contrato não encontrado
    """
    contract = Contract.query.get(id)
    
    if not contract:
        return jsonify({'error': 'Contrato não encontrado'}), 404
    
    data = request.get_json()
    
    # Verificar número de contrato duplicado
    if data.get('contract_number') and data['contract_number'] != contract.contract_number:
        existing = Contract.query.filter_by(contract_number=data['contract_number']).first()
        if existing:
            return jsonify({'error': 'Número de contrato já existe'}), 409
    
    # Atualizar campos
    if 'contract_number' in data:
        contract.contract_number = data['contract_number']
    if 'description' in data:
        contract.description = data['description']
    if 'start_date' in data:
        contract.start_date = datetime.fromisoformat(data['start_date'].replace('Z', '+00:00'))
    if 'end_date' in data:
        contract.end_date = datetime.fromisoformat(data['end_date'].replace('Z', '+00:00')) if data['end_date'] else None
    if 'status' in data:
        contract.status = data['status']
    if 'value' in data:
        contract.value = data['value']
    # Nota: branch_id não é usado no modelo Contract
    if 'team_id' in data:
        contract.team_id = data['team_id']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Contrato atualizado com sucesso',
        'contract': contract.to_dict(include_relations=True)
    }), 200


@contracts_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required('superadmin', 'admin')
def delete_contract(id):
    """Exclui um contrato
    ---
    tags:
      - 📄 GAT - Contratos
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        type: integer
        required: true
    responses:
      200:
        description: Contrato excluído
      404:
        description: Contrato não encontrado
    """
    contract = Contract.query.get(id)
    
    if not contract:
        return jsonify({'error': 'Contrato não encontrado'}), 404
    
    db.session.delete(contract)
    db.session.commit()
    
    return jsonify({'message': 'Contrato excluído com sucesso'}), 200
