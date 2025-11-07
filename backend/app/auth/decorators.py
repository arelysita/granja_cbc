# Archivo creado automáticamente
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from app.models.user import User

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or user.rol != 'administrador':
            return jsonify({'error': 'Se requieren privilegios de administrador'}), 403
        
        return f(*args, **kwargs)
    return decorated_function

def cliente_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or user.rol != 'cliente':
            return jsonify({'error': 'Acceso solo para clientes'}), 403
        
        return f(*args, **kwargs)
    return decorated_function