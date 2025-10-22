from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flasgger import swag_from
from ..models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Registra um novo usuário
    ---
    tags:
      - 🔐 Compartilhado - Autenticação
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
              example: "usuario@example.com"
            password:
              type: string
              example: "senha123"
            name:
              type: string
              example: "João Silva"
            role:
              type: string
              enum: [superadmin, admin, tecnico, cliente]
              example: "tecnico"
            phone:
              type: string
              example: "(11) 98765-4321"
    responses:
      201:
        description: Usuário criado com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
            user:
              type: object
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
    db.session.commit()
    
    return jsonify({
        'message': 'Usuário criado com sucesso',
        'user': user.to_dict()
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """Autentica um usuário e retorna tokens JWT
    ---
    tags:
      - 🔐 Compartilhado - Autenticação
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              example: "usuario@example.com"
            password:
              type: string
              example: "senha123"
    responses:
      200:
        description: Login realizado com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
            access_token:
              type: string
            refresh_token:
              type: string
            user:
              type: object
      400:
        description: Email e senha são obrigatórios
      401:
        description: Credenciais inválidas
      403:
        description: Usuário inativo
    """
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email e senha são obrigatórios'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Credenciais inválidas'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'Usuário inativo'}), 403
        
        # Gerar tokens (identity deve ser string)
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        
        return jsonify({
            'message': 'Login realizado com sucesso',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }), 200
    except Exception as e:
        print(f"Erro no login: {str(e)}")
        return jsonify({
            'error': 'Erro interno do servidor',
            'message': str(e)
        }), 500


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Gera um novo access token usando o refresh token
    ---
    tags:
      - 🔐 Compartilhado - Autenticação
    security:
      - Bearer: []
    responses:
      200:
        description: Novo token gerado com sucesso
        schema:
          type: object
          properties:
            access_token:
              type: string
      401:
        description: Token inválido ou expirado
    """
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)
    
    return jsonify({
        'access_token': access_token
    }), 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Retorna informações do usuário autenticado
    ---
    tags:
      - 🔐 Compartilhado - Autenticação
    security:
      - Bearer: []
    responses:
      200:
        description: Dados do usuário
        schema:
          type: object
          properties:
            id:
              type: integer
            email:
              type: string
            name:
              type: string
            role:
              type: string
            phone:
              type: string
            is_active:
              type: boolean
      401:
        description: Token inválido ou expirado
      404:
        description: Usuário não encontrado
    """
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    return jsonify(user.to_dict()), 200


@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Altera a senha do usuário autenticado
    ---
    tags:
      - 🔐 Compartilhado - Autenticação
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - current_password
            - new_password
          properties:
            current_password:
              type: string
              example: "senha_antiga"
            new_password:
              type: string
              example: "senha_nova"
    responses:
      200:
        description: Senha alterada com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
      400:
        description: Dados inválidos
      401:
        description: Senha atual incorreta ou token inválido
      404:
        description: Usuário não encontrado
    """
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    data = request.get_json()
    
    if not data.get('current_password') or not data.get('new_password'):
        return jsonify({'error': 'Senha atual e nova senha são obrigatórias'}), 400
    
    if not user.check_password(data['current_password']):
        return jsonify({'error': 'Senha atual incorreta'}), 401
    
    user.set_password(data['new_password'])
    db.session.commit()
    
    return jsonify({'message': 'Senha alterada com sucesso'}), 200

