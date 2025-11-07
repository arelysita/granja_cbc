from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.auth.decorators import admin_required
from app.models.user import User
from app.models.product import Product
from app.models.category import Category

admin_bp = Blueprint('admin', __name__)

# ===============================================================
# 🔹 Endpoint: Listar Todos los Usuarios (GET /api/admin/users)
# ===============================================================
@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required
def get_all_users():
    """Requiere JWT y rol 'administrador'."""
    try:
        users = User.query.all()
        
        # Se requiere el método .to_dict() en el modelo User
        return jsonify({
            'users': [user.to_dict() for user in users]
        }), 200
        
    except Exception as e:
        print(f"❌ Error al listar usuarios: {e}")
        return jsonify({'error': str(e)}), 500

# ===============================================================
# 🔹 Endpoint: Métricas del Dashboard (GET /api/admin/metrics)
# ===============================================================
@admin_bp.route('/metrics', methods=['GET'])
@jwt_required()
@admin_required
def get_dashboard_metrics():
    """Proporciona métricas básicas para el panel de administración."""
    try:
        # Contamos las entidades básicas
        user_count = User.query.count()
        product_count = Product.query.count()
        category_count = Category.query.count()
        
        # Contamos productos activos
        active_products_count = Product.query.filter_by(activo=True).count()
        
        return jsonify({
            'total_users': user_count,
            'total_products': product_count,
            'active_products': active_products_count,
            'total_categories': category_count
        }), 200
        
    except Exception as e:
        print(f"❌ Error al obtener métricas: {e}")
        return jsonify({'error': 'Error al conectar con la base de datos para métricas'}), 500