from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..models import db, Client
from ..decorators import role_required

clients_bp = Blueprint('clients', __name__)

@clients_bp.route('', methods=['GET'])
@jwt_required()
def list_clients():
    """Lista todos os clientes"""
    is_active = request.args.get('is_active')
    search = request.args.get('search')
    
    query = Client.query
    
    if is_active is not None:
        is_active_bool = is_active.lower() == 'true'
        query = query.filter_by(is_active=is_active_bool)
    
    if search:
        search_pattern = f'%{search}%'
        query = query.filter(
            db.or_(
                Client.name.ilike(search_pattern),
                Client.email.ilike(search_pattern),
                Client.cpf_cnpj.ilike(search_pattern)
            )
        )
    
    clients = query.all()
    
    return jsonify({
        'clients': [client.to_dict() for client in clients],
        'total': len(clients)
    }), 200


@clients_bp.route('/<int:client_id>', methods=['GET'])
@jwt_required()
def get_client(client_id):
    """Obtém detalhes de um cliente específico"""
    client = Client.query.get(client_id)
    
    if not client:
        return jsonify({'error': 'Cliente não encontrado'}), 404
    
    return jsonify(client.to_dict()), 200


@clients_bp.route('', methods=['POST'])
@jwt_required()
@role_required('superadmin', 'admin', 'coord')
def create_client():
    """Cria um novo cliente"""
    data = request.get_json()
    
    # Validação básica
    required_fields = ['name', 'email']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Campo obrigatório: {field}'}), 400
    
    # Verificar se o email já existe
    if Client.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email já cadastrado'}), 409
    
    # Verificar se o CPF/CNPJ já existe
    if data.get('cpf_cnpj'):
        if Client.query.filter_by(cpf_cnpj=data['cpf_cnpj']).first():
            return jsonify({'error': 'CPF/CNPJ já cadastrado'}), 409
    
    # Criar novo cliente
    client = Client(
        name=data['name'],
        email=data['email'],
        phone=data.get('phone'),
        cpf_cnpj=data.get('cpf_cnpj'),
        address=data.get('address'),
        city=data.get('city'),
        state=data.get('state'),
        zip_code=data.get('zip_code'),
        notes=data.get('notes')
    )
    
    db.session.add(client)
    db.session.commit()
    
    return jsonify({
        'message': 'Cliente criado com sucesso',
        'client': client.to_dict()
    }), 201


@clients_bp.route('/<int:client_id>', methods=['PUT'])
@jwt_required()
@role_required('superadmin', 'admin', 'coord')
def update_client(client_id):
    """Atualiza informações de um cliente"""
    client = Client.query.get(client_id)
    
    if not client:
        return jsonify({'error': 'Cliente não encontrado'}), 404
    
    data = request.get_json()
    
    # Atualizar campos
    if 'name' in data:
        client.name = data['name']
    
    if 'email' in data and data['email'] != client.email:
        # Verificar se o novo email já existe
        existing_client = Client.query.filter_by(email=data['email']).first()
        if existing_client:
            return jsonify({'error': 'Email já cadastrado'}), 409
        client.email = data['email']
    
    if 'cpf_cnpj' in data and data['cpf_cnpj'] != client.cpf_cnpj:
        # Verificar se o novo CPF/CNPJ já existe
        existing_client = Client.query.filter_by(cpf_cnpj=data['cpf_cnpj']).first()
        if existing_client:
            return jsonify({'error': 'CPF/CNPJ já cadastrado'}), 409
        client.cpf_cnpj = data['cpf_cnpj']
    
    if 'phone' in data:
        client.phone = data['phone']
    
    if 'address' in data:
        client.address = data['address']
    
    if 'city' in data:
        client.city = data['city']
    
    if 'state' in data:
        client.state = data['state']
    
    if 'zip_code' in data:
        client.zip_code = data['zip_code']
    
    if 'notes' in data:
        client.notes = data['notes']
    
    if 'is_active' in data:
        client.is_active = data['is_active']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Cliente atualizado com sucesso',
        'client': client.to_dict()
    }), 200


@clients_bp.route('/<int:client_id>', methods=['DELETE'])
@jwt_required()
@role_required('superadmin', 'admin')
def delete_client(client_id):
    """Desativa um cliente (soft delete)"""
    client = Client.query.get(client_id)
    
    if not client:
        return jsonify({'error': 'Cliente não encontrado'}), 404
    
    client.is_active = False
    db.session.commit()
    
    return jsonify({'message': 'Cliente desativado com sucesso'}), 200

