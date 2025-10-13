from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from models import User

def role_required(*roles):
    """
    Decorator para verificar se o usuário possui uma das roles especificadas
    Uso: @role_required('admin', 'superadmin')
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = User.query.get(int(user_id))
            
            if not user:
                return jsonify({'error': 'Usuário não encontrado'}), 404
            
            if not user.is_active:
                return jsonify({'error': 'Usuário inativo'}), 403
            
            if not user.has_role(*roles):
                return jsonify({
                    'error': 'Acesso negado',
                    'message': f'Requer uma das seguintes permissões: {", ".join(roles)}'
                }), 403
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def get_current_user():
    """Retorna o usuário atual autenticado"""
    verify_jwt_in_request()
    user_id = get_jwt_identity()
    return User.query.get(int(user_id))

