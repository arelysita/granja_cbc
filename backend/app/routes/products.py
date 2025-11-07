from flask import Blueprint, request, jsonify, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from app import db, photos 
from app.models.product import Product
from app.models.category import Category
from app.models.review import Review
from app.auth.decorators import admin_required
import os
import decimal

products_bp = Blueprint('products', __name__)

@products_bp.route('/', methods=['GET'])
def get_products():
    # ... (código GET sin cambios, solo para contexto)
    try:
        # Filtros
        categoria_id = request.args.get('categoria_id', type=int)
        search = request.args.get('search', '')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 12, type=int)
        
        query = Product.query.filter_by(activo=True)
        
        if categoria_id:
            query = query.filter_by(categoria_id=categoria_id)
        
        if search:
            query = query.filter(Product.nombre.ilike(f'%{search}%'))
        
        products = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'products': [product.to_dict() for product in products.items],
            'total': products.total,
            'pages': products.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    # ... (código GET sin cambios, solo para contexto)
    try:
        product = Product.query.get_or_404(product_id)
        
        if not product.activo:
            return jsonify({'error': 'Producto no disponible'}), 404
        
        return jsonify({'product': product.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@products_bp.route('/', methods=['POST'])
# Recuerda DESCOMENTAR estos decoradores una vez que el problema del body se resuelva
# @jwt_required() 
# @admin_required
def create_product():
    """
    Ruta para crear un producto.
    CORRECCIÓN: Se usa request.form para obtener datos de texto y request.files para la imagen.
    """
    try:
        # Esto lee todos los campos de texto del FormData (incluyendo 'nombre', 'precio', 'etc')
        data = request.form.to_dict()
        
        # Validar campos esenciales
        required_fields = ['nombre', 'precio', 'stock', 'categoria_id']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'El campo {field} es obligatorio.'}), 400

        # Validar categoría
        categoria = Category.query.get(data.get('categoria_id'))
        if not categoria:
            return jsonify({'error': 'Categoría no válida'}), 400
            
        # 1. CONVERSIÓN DE TIPOS CRUCIAL
        # Aseguramos que los valores sean numéricos o booleanos, lo que evita errores de DB.
        precio = decimal.Decimal(data['precio'])
        stock = int(data['stock'])
        # El frontend envía 'true' o 'false' como string.
        activo = data.get('activo', '1').lower() in ('true', '1', 'on')

        # 2. Manejar imagen
        image_to_save = '' 
        if 'imagen' in request.files and request.files['imagen'].filename:
            # 1. Guardar el archivo físico
            filename = photos.save(request.files['imagen'])
            # 2. Guardar SOLO EL NOMBRE DEL ARCHIVO en la base de datos
            image_to_save = filename
        
        # 3. Crear producto
        product = Product(
            nombre=data['nombre'],
            descripcion=data.get('descripcion', ''),
            precio=precio, # Usar el Decimal
            stock=stock, # Usar el int
            categoria_id=int(data['categoria_id']),
            activo=activo, # Usar el booleano
            imagen_url=image_to_save 
        )
        
        db.session.add(product)
        db.session.commit()
        
        return jsonify({
            'message': 'Producto creado exitosamente. Vuelve a activar JWT!',
            'product': product.to_dict()
        }), 201
        
    except decimal.InvalidOperation:
         db.session.rollback()
         return jsonify({'error': 'Error de formato: El precio debe ser un número válido.'}), 400
    except ValueError as ve:
        db.session.rollback()
        return jsonify({'error': f'Error de formato en stock o categoría: {ve}'}), 400
    except Exception as e:
        db.session.rollback()
        # En caso de otros errores, como problemas de DB
        return jsonify({'error': str(e)}), 500

@products_bp.route('/<int:product_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_product(product_id):
    """
    Ruta para actualizar un producto.
    Sigue usando request.form porque la edición también puede incluir una nueva imagen.
    """
    try:
        product = Product.query.get_or_404(product_id)
        # Esto lee todos los campos de texto del FormData o x-www-form-urlencoded
        data = request.form.to_dict()
        
        if 'nombre' in data:
            product.nombre = data['nombre']
        if 'descripcion' in data:
            product.descripcion = data['descripcion']
            
        if 'precio' in data:
            try:
                # Usar Decimal para precisión monetaria
                product.precio = decimal.Decimal(data['precio'])
            except decimal.InvalidOperation:
                return jsonify({'error': 'El precio debe ser un número válido.'}), 400
                
        if 'stock' in data:
            try:
                product.stock = int(data['stock'])
            except ValueError:
                return jsonify({'error': 'El stock debe ser un número entero válido.'}), 400

        if 'categoria_id' in data:
            categoria = Category.query.get(data['categoria_id'])
            if not categoria:
                return jsonify({'error': 'Categoría no válida'}), 400
            product.categoria_id = int(data['categoria_id'])
            
        if 'activo' in data:
            # Convierte el string 'true'/'false' a booleano
            product.activo = data['activo'].lower() == 'true'
        
        # Actualizar imagen
        if 'imagen' in request.files and request.files['imagen'].filename:
            # Lógica para eliminar la imagen vieja si es necesario
            # ...
            filename = photos.save(request.files['imagen'])
            product.imagen_url = filename
            
        # Si se envía el campo 'delete_image' con 'true', se elimina la URL
        elif data.get('delete_image') == 'true':
            product.imagen_url = ''
            
        db.session.commit()
        
        return jsonify({
            'message': 'Producto actualizado exitosamente',
            'product': product.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@products_bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_product(product_id):
# ... (código DELETE sin cambios)
    try:
        product = Product.query.get_or_404(product_id)
        
        # En lugar de eliminar, desactivar
        product.activo = False
        db.session.commit()
        
        return jsonify({'message': 'Producto desactivado exitosamente'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@products_bp.route('/<int:product_id>/reviews', methods=['GET'])
def get_product_reviews(product_id):
# ... (código reviews sin cambios)
    try:
        product = Product.query.get_or_404(product_id)
        reviews = Review.query.filter_by(
            producto_id=product_id, 
            aprobada=True
        ).all()
        
        return jsonify({
            'reviews': [review.to_dict() for review in reviews]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
