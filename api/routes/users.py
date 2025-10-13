from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..models import db, User, Technician, Team
from ..decorators import role_required, get_current_user

users_bp = Blueprint('users', __name__)

@users_bp.route('', methods=['POST'])
@jwt_required()
@role_required('superadmin', 'admin', 'coord')
def create_user():
    """Cria um novo usuário
    ---
    tags:
      - 👤 GAT - Usuários
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
            - name
            - role
          properties:
            email:
              type: string
              example: "tecnico@fireng.com"
            password:
              type: string
              example: "senha123"
            name:
              type: string
              example: "João Silva"
            role:
              type: string
              enum: [superadmin, admin, coord, tecnico, cliente]
              example: "tecnico"
            phone:
              type: string
              example: "(11) 98765-4321"
    responses:
      201:
        description: Usuário criado com sucesso
      400:
        description: Dados inválidos
      409:
        description: Email já cadastrado
    """
    data = request.get_json()
    
    # Validação básica
    required_fields = ['email', 'password', 'name', 'role']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Campo obrigatório: {field}'}), 400
    
    # Validar role
    if not User.validate_role(data['role']):
        return jsonify({'error': f'Role inválida. Opções: {", ".join(User.ROLES)}'}), 400
    
    # Verificar se o email já existe
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email já cadastrado'}), 409
    
    # Criar novo usuário
    user = User(
        email=data['email'],
        name=data['name'],
        role=data['role'],
        phone=data.get('phone')
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.flush()  # Para obter o ID do usuário
    
    # Se for técnico, criar perfil de técnico também
    technician = None
    if data['role'] == 'tecnico':
        # Gerar matrícula automática se não fornecida
        registration_number = data.get('registration_number')
        if not registration_number:
            # Buscar o último número de técnico e incrementar
            last_tech = Technician.query.order_by(Technician.id.desc()).first()
            last_number = int(last_tech.registration_number.split('-')[-1]) if last_tech and last_tech.registration_number else 0
            registration_number = f"TEC-{str(last_number + 1).zfill(3)}"
        
        technician = Technician(
            user_id=user.id,
            registration_number=registration_number,
            specializations=str(data.get('specializations', [])),
            experience_years=data.get('experience_years'),
            team_id=data.get('team_id'),
            notes=data.get('notes', 'Técnico criado automaticamente')
        )
        db.session.add(technician)
    
    db.session.commit()
    
    response_data = {
        'message': 'Usuário criado com sucesso',
        'user': user.to_dict()
    }
    
    if technician:
        response_data['technician'] = technician.to_dict(include_relations=True)
    
    return jsonify(response_data), 201


@users_bp.route('', methods=['GET'])
@jwt_required()
@role_required('superadmin', 'admin', 'coord')
def list_users():
    """Lista todos os usuários (com filtros opcionais)"""
    role = request.args.get('role')
    is_active = request.args.get('is_active')
    
    query = User.query
    
    if role:
        query = query.filter_by(role=role)
    
    if is_active is not None:
        is_active_bool = is_active.lower() == 'true'
        query = query.filter_by(is_active=is_active_bool)
    
    users = query.all()
    
    return jsonify({
        'users': [user.to_dict() for user in users],
        'total': len(users)
    }), 200


@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
@role_required('superadmin', 'admin', 'coord')
def get_user(user_id):
    """Obtém detalhes de um usuário específico"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    return jsonify(user.to_dict()), 200


@users_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
@role_required('superadmin', 'admin')
def update_user(user_id):
    """Atualiza informações de um usuário"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    data = request.get_json()
    current_user = get_current_user()
    
    # Apenas superadmin pode alterar role de outros usuários
    if 'role' in data and data['role'] != user.role:
        if current_user.role != 'superadmin':
            return jsonify({'error': 'Apenas superadmin pode alterar roles'}), 403
        
        if not User.validate_role(data['role']):
            return jsonify({'error': f'Role inválida. Opções: {", ".join(User.ROLES)}'}), 400
        
        user.role = data['role']
    
    # Atualizar outros campos
    if 'name' in data:
        user.name = data['name']
    
    if 'email' in data and data['email'] != user.email:
        # Verificar se o novo email já existe
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'error': 'Email já cadastrado'}), 409
        user.email = data['email']
    
    if 'phone' in data:
        user.phone = data['phone']
    
    if 'is_active' in data:
        user.is_active = data['is_active']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Usuário atualizado com sucesso',
        'user': user.to_dict()
    }), 200


@users_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
@role_required('superadmin')
def delete_user(user_id):
    """Desativa um usuário (soft delete)"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    current_user = get_current_user()
    
    # Não permitir que o usuário desative a si mesmo
    if user.id == current_user.id:
        return jsonify({'error': 'Você não pode desativar sua própria conta'}), 400
    
    user.is_active = False
    db.session.commit()
    
    return jsonify({'message': 'Usuário desativado com sucesso'}), 200


@users_bp.route('/technicians', methods=['POST'])
@jwt_required()
@role_required('superadmin', 'admin', 'coord')
def create_technician():
    """Cria um novo técnico com perfil completo
    ---
    tags:
      - 👤 GAT - Usuários
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
            - name
            - registration_number
          properties:
            email:
              type: string
              example: "tecnico@fireng.com"
            password:
              type: string
              example: "senha123"
            name:
              type: string
              example: "João Silva"
            phone:
              type: string
              example: "(11) 98765-4321"
            registration_number:
              type: string
              example: "TEC001"
            specializations:
              type: array
              items:
                type: string
              example: ["sprinklers", "alarme", "extintores"]
            experience_years:
              type: integer
              example: 5
            team_id:
              type: integer
              example: 1
            notes:
              type: string
              example: "Técnico especializado em sistemas de sprinklers"
    responses:
      201:
        description: Técnico criado com sucesso
      400:
        description: Dados inválidos
      409:
        description: Email ou matrícula já cadastrados
    """
    data = request.get_json()
    
    # Validação básica
    required_fields = ['email', 'password', 'name', 'registration_number']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Campo obrigatório: {field}'}), 400
    
    # Verificar se o email já existe
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email já cadastrado'}), 409
    
    # Verificar se a matrícula já existe
    if Technician.query.filter_by(registration_number=data['registration_number']).first():
        return jsonify({'error': 'Número de matrícula já existe'}), 409
    
    # Verificar equipe se fornecida
    team_id = data.get('team_id')
    if team_id:
        team = Team.query.get(team_id)
        if not team:
            return jsonify({'error': 'Equipe não encontrada'}), 404
    
    # Criar usuário técnico
    user = User(
        email=data['email'],
        name=data['name'],
        role='tecnico',
        phone=data.get('phone')
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.flush()  # Para obter o ID do usuário
    
    # Criar perfil de técnico
    import json
    technician = Technician(
        user_id=user.id,
        registration_number=data['registration_number'],
        specializations=json.dumps(data.get('specializations', [])),
        experience_years=data.get('experience_years'),
        team_id=team_id,
        notes=data.get('notes')
    )
    
    db.session.add(technician)
    db.session.commit()
    
    return jsonify({
        'message': 'Técnico criado com sucesso',
        'user': user.to_dict(),
        'technician': technician.to_dict(include_relations=True)
    }), 201


@users_bp.route('/technicians/<int:technician_id>', methods=['PUT'])
@jwt_required()
@role_required('superadmin', 'admin', 'coord')
def update_technician(technician_id):
    """Atualiza informações de um técnico
    ---
    tags:
      - 👤 GAT - Usuários
    security:
      - Bearer: []
    parameters:
      - in: path
        name: technician_id
        type: integer
        required: true
      - in: body
        name: body
        schema:
          type: object
          properties:
            name:
              type: string
            phone:
              type: string
            registration_number:
              type: string
            specializations:
              type: array
              items:
                type: string
            experience_years:
              type: integer
            team_id:
              type: integer
            notes:
              type: string
    responses:
      200:
        description: Técnico atualizado com sucesso
      404:
        description: Técnico não encontrado
    """
    technician = Technician.query.get(technician_id)
    
    if not technician:
        return jsonify({'error': 'Técnico não encontrado'}), 404
    
    data = request.get_json()
    
    # Atualizar dados do usuário
    if 'name' in data:
        technician.user.name = data['name']
    if 'phone' in data:
        technician.user.phone = data['phone']
    
    # Atualizar dados do técnico
    if 'registration_number' in data and data['registration_number'] != technician.registration_number:
        # Verificar se a nova matrícula já existe
        existing = Technician.query.filter_by(registration_number=data['registration_number']).first()
        if existing:
            return jsonify({'error': 'Número de matrícula já existe'}), 409
        technician.registration_number = data['registration_number']
    
    if 'specializations' in data:
        import json
        technician.specializations = json.dumps(data['specializations'])
    
    if 'experience_years' in data:
        technician.experience_years = data['experience_years']
    
    if 'team_id' in data:
        if data['team_id']:
            team = Team.query.get(data['team_id'])
            if not team:
                return jsonify({'error': 'Equipe não encontrada'}), 404
        technician.team_id = data['team_id']
    
    if 'notes' in data:
        technician.notes = data['notes']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Técnico atualizado com sucesso',
        'technician': technician.to_dict(include_relations=True)
    }), 200


@users_bp.route('/technicians', methods=['GET'])
@jwt_required()
def list_technicians():
    """Lista todos os técnicos ativos com perfil completo"""
    technicians = Technician.query.join(User).filter(User.is_active == True).all()
    
    return jsonify({
        'technicians': [tech.to_dict(include_relations=True) for tech in technicians],
        'total': len(technicians)
    }), 200


@users_bp.route('/users/<int:user_id>/create-technician-profile', methods=['POST'])
@jwt_required()
@role_required('superadmin', 'admin', 'coord')
def create_technician_profile(user_id):
    """Cria perfil de técnico para um usuário existente com role 'tecnico'
    ---
    tags:
      - 👤 GAT - Usuários
    security:
      - Bearer: []
    parameters:
      - in: path
        name: user_id
        type: integer
        required: true
        description: ID do usuário
      - in: body
        name: body
        schema:
          type: object
          properties:
            registration_number:
              type: string
              example: "TEC001"
            specializations:
              type: array
              items:
                type: string
              example: ["sprinklers", "alarme"]
            experience_years:
              type: integer
              example: 5
            team_id:
              type: integer
              example: 1
            notes:
              type: string
              example: "Técnico especializado"
    responses:
      201:
        description: Perfil de técnico criado com sucesso
      400:
        description: Usuário não é técnico ou já possui perfil
      404:
        description: Usuário não encontrado
    """
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    if user.role != 'tecnico':
        return jsonify({'error': 'Usuário não é um técnico'}), 400
    
    # Verificar se já possui perfil de técnico
    existing_technician = Technician.query.filter_by(user_id=user_id).first()
    if existing_technician:
        return jsonify({'error': 'Usuário já possui perfil de técnico'}), 400
    
    data = request.get_json() or {}
    
    # Gerar matrícula automática se não fornecida
    registration_number = data.get('registration_number')
    if not registration_number:
        last_tech = Technician.query.order_by(Technician.id.desc()).first()
        last_number = int(last_tech.registration_number.split('-')[-1]) if last_tech and last_tech.registration_number else 0
        registration_number = f"TEC-{str(last_number + 1).zfill(3)}"
    
    # Verificar se a matrícula já existe
    if Technician.query.filter_by(registration_number=registration_number).first():
        return jsonify({'error': 'Número de matrícula já existe'}), 409
    
    # Verificar equipe se fornecida
    team_id = data.get('team_id')
    if team_id:
        team = Team.query.get(team_id)
        if not team:
            return jsonify({'error': 'Equipe não encontrada'}), 404
    
    # Criar perfil de técnico
    technician = Technician(
        user_id=user_id,
        registration_number=registration_number,
        specializations=data.get('specializations', []),
        experience_years=data.get('experience_years'),
        team_id=team_id,
        notes=data.get('notes', 'Perfil criado posteriormente')
    )
    
    db.session.add(technician)
    db.session.commit()
    
    return jsonify({
        'message': 'Perfil de técnico criado com sucesso',
        'technician': technician.to_dict(include_relations=True)
    }), 201

