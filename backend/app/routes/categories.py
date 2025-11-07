from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models.category import Category
from app.models.product import Product
from app.auth.decorators import admin_required

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/', methods=['GET'])
def get_categories():
    try:
        categories = Category.query.filter_by(activa=True).all()
        return jsonify({
            'categories': [category.to_dict() for category in categories]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@categories_bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    try:
        category = Category.query.get_or_404(category_id)
        return jsonify({'category': category.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@categories_bp.route('/<int:category_id>/products', methods=['GET'])
def get_category_products(category_id):
    try:
        category = Category.query.get_or_404(category_id)
        products = Product.query.filter_by(
            categoria_id=category_id, 
            activo=True
        ).all()
        
        return jsonify({
            'products': [product.to_dict() for product in products]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@categories_bp.route('/', methods=['POST'])
@jwt_required()
@admin_required
def create_category():
    try:
        data = request.get_json()
        
        category = Category(
            nombre=data['nombre'],
            descripcion=data.get('descripcion', ''),
            imagen_url=data.get('imagen_url', '')
        )
        
        db.session.add(category)
        db.session.commit()
        
        return jsonify({
            'message': 'Categoría creada exitosamente',
            'category': category.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@categories_bp.route('/<int:category_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_category(category_id):
    try:
        category = Category.query.get_or_404(category_id)
        data = request.get_json()
        
        if 'nombre' in data:
            category.nombre = data['nombre']
        if 'descripcion' in data:
            category.descripcion = data['descripcion']
        if 'imagen_url' in data:
            category.imagen_url = data['imagen_url']
        if 'activa' in data:
            category.activa = data['activa']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Categoría actualizada exitosamente',
            'category': category.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500