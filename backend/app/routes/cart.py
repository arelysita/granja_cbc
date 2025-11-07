from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.cart import CartItem
from app.models.product import Product
from app.auth.decorators import cliente_required
from sqlalchemy.orm import joinedload # IMPORTACIÓN NECESARIA

cart_bp = Blueprint('cart', __name__)

# --- FUNCIÓN DE AYUDA DEFINITIVA PARA VALIDACIÓN DE 422 ---
def get_int_from_data(data, key):
    """
    Intenta obtener y validar un entero positivo del JSON de entrada.
    Lanza excepción para ser capturada y devolver 422.
    """
    value = data.get(key)
    if value is None or value == '':
        raise ValueError(f"El campo '{key}' es obligatorio.")
    
    try:
        final_value = int(value)
    except (ValueError, TypeError):
        raise TypeError(f"El campo '{key}' debe ser un número entero válido.")
    
    if final_value <= 0:
        raise ValueError(f"El campo '{key}' debe ser un número entero positivo.")
        
    return final_value
# --- FIN FUNCIÓN DE AYUDA ---

## RUTA: GET / - ¡MODIFICADA TEMPORALMENTE PARA DEBUG!
@cart_bp.route('/', methods=['GET'])
# @jwt_required()     # COMENTADO PARA LA PRUEBA
# @cliente_required   # COMENTADO PARA LA PRUEBA
def get_cart():
    # TEMPORAL: Usamos un ID fijo para que la lógica de la base de datos funcione.
    # *** USA EL MISMO ID DE USUARIO QUE USaste en /add (ej: 1) ***
    current_user_id = 1 
    
    try:
        # MODIFICACIÓN CLAVE: Usar joinedload para cargar la relación 'product'
        cart_items = db.session.query(CartItem).options(
            joinedload(CartItem.producto)
        ).filter(CartItem.usuario_id == current_user_id).all()
        
        # Cálculo del total
        total = sum(item.cantidad * item.product.precio for item in cart_items)
        
        return jsonify({
            'cart_items': [item.to_dict() for item in cart_items],
            'total': float(total)
        }), 200
        
    except Exception as e:
        print(f"DEBUG 500 (GET CART): {e}") 
        return jsonify({'error': str(e)}), 500

## RUTA: POST /add - MANTENEMOS LA MODIFICACIÓN DE DEBUG
@cart_bp.route('/add', methods=['POST'])
# @jwt_required()     # COMENTADO PARA LA PRUEBA
# @cliente_required   # COMENTADO PARA LA PRUEBA
def add_to_cart():
    # TEMPORAL: Usamos un ID fijo para que la lógica de la base de datos funcione.
    current_user_id = 1 
    
    try:
        data = request.get_json()
        final_product_id = get_int_from_data(data, 'producto_id')
        final_cantidad = get_int_from_data(data, 'cantidad')
        
    except (ValueError, TypeError) as e:
        print(f"DEBUG 422 (VALIDACIÓN DE ENTRADA): {e}") 
        return jsonify({'error': str(e)}), 422
    
    except Exception as e:
        if request.get_json(silent=True) is None:
            print("DEBUG 422 (JSON INVÁLIDO): Cuerpo de solicitud no es un JSON válido.")
            return jsonify({'error': 'La solicitud debe contener un cuerpo JSON válido.'}), 422
        
        print(f"DEBUG INESPERADO: {e}")
        return jsonify({'error': 'Error interno al procesar la solicitud.'}), 500
    
    # Lógica de negocio
    product = Product.query.get(final_product_id)
    if not product or not product.activo:
        return jsonify({'error': 'Producto no disponible'}), 400
    
    if product.stock < final_cantidad:
        return jsonify({'error': 'Stock insuficiente'}), 400
    
    try:
        existing_item = CartItem.query.filter_by(
            usuario_id=current_user_id,
            producto_id=final_product_id
        ).first()
        
        if existing_item:
            if product.stock < existing_item.cantidad + final_cantidad:
                return jsonify({'error': 'Stock insuficiente para la cantidad total'}), 400
            
            existing_item.cantidad += final_cantidad
        else:
            new_item = CartItem(
                usuario_id=current_user_id,
                producto_id=final_product_id,
                cantidad=final_cantidad
            )
            db.session.add(new_item)
        
        db.session.commit()
        
        return jsonify({'message': 'Producto agregado al carrito'}), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"DEBUG 500 (BASE DE DATOS/SERVIDOR): {e}") 
        return jsonify({'error': 'Error en el servidor al guardar el ítem'}), 500
    

## RUTA: PUT /update/<int:item_id>
@cart_bp.route('/update/<int:item_id>', methods=['PUT'])
@jwt_required()
@cliente_required
def update_cart_item(item_id):
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        cart_item = CartItem.query.filter_by(
            id=item_id,
            usuario_id=current_user_id
        ).first_or_404()
        
        nueva_cantidad = data.get('cantidad')
        
        try:
            final_nueva_cantidad = int(nueva_cantidad)
        except (ValueError, TypeError):
            return jsonify({'error': 'La cantidad debe ser un número entero válido.'}), 422

        if final_nueva_cantidad < 0:
            return jsonify({'error': 'La cantidad debe ser un número entero no negativo.'}), 422
        
        if final_nueva_cantidad == 0:
            db.session.delete(cart_item)
        else:
            if cart_item.product.stock < final_nueva_cantidad:
                return jsonify({'error': 'Stock insuficiente'}), 400
            cart_item.cantidad = final_nueva_cantidad
        
        db.session.commit()
        
        return jsonify({'message': 'Carrito actualizado'}), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"DEBUG 500 (UPDATE CART): {e}") 
        return jsonify({'error': str(e)}), 500

## RUTA: DELETE /remove/<int:item_id>
@cart_bp.route('/remove/<int:item_id>', methods=['DELETE'])
@jwt_required()
@cliente_required
def remove_from_cart(item_id):
    try:
        current_user_id = get_jwt_identity()
        
        cart_item = CartItem.query.filter_by(
            id=item_id,
            usuario_id=current_user_id
        ).first_or_404()
        
        db.session.delete(cart_item)
        db.session.commit()
        
        return jsonify({'message': 'Producto removido del carrito'}), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"DEBUG 500 (REMOVE CART): {e}") 
        return jsonify({'error': str(e)}), 500

## RUTA: DELETE /clear
@cart_bp.route('/clear', methods=['DELETE'])
@jwt_required()
@cliente_required
def clear_cart():
    try:
        current_user_id = get_jwt_identity()
        
        CartItem.query.filter_by(usuario_id=current_user_id).delete()
        db.session.commit()
        
        return jsonify({'message': 'Carrito vaciado'}), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"DEBUG 500 (CLEAR CART): {e}") 
        return jsonify({'error': str(e)}), 500
