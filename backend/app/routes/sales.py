from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.sale import Sale, SaleDetail
from app.models.cart import CartItem
from app.models.product import Product
from app.models.stock_movement import StockMovement
from app.auth.decorators import cliente_required, admin_required
from datetime import datetime

sales_bp = Blueprint('sales', __name__)

@sales_bp.route('/', methods=['POST'])
@jwt_required()
@cliente_required
def create_sale():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Obtener items del carrito
        cart_items = CartItem.query.filter_by(usuario_id=current_user_id).all()
        
        if not cart_items:
            return jsonify({'error': 'El carrito está vacío'}), 400
        
        # Calcular total y verificar stock
        total = 0
        for item in cart_items:
            if item.producto.stock < item.cantidad:
                return jsonify({
                    'error': f'Stock insuficiente para {item.producto.nombre}'
                }), 400
            total += item.cantidad * item.producto.precio
        
        # Crear venta
        sale = Sale(
            cliente_id=current_user_id,
            total=total,
            metodo_pago=data.get('metodo_pago', 'contra_entrega'),
            direccion_envio=data.get('direccion_envio', ''),
            notas=data.get('notas', '')
        )
        
        db.session.add(sale)
        db.session.flush()  # Para obtener el ID de la venta
        
        # Crear detalles de venta y actualizar stock
        for item in cart_items:
            # Detalle de venta
            detail = SaleDetail(
                venta_id=sale.id,
                producto_id=item.producto_id,
                cantidad=item.cantidad,
                precio_unitario=item.producto.precio
            )
            db.session.add(detail)
            
            # Actualizar stock
            item.producto.stock -= item.cantidad
            
            # Registrar movimiento de stock
            movement = StockMovement(
                producto_id=item.producto_id,
                tipo='salida',
                cantidad=item.cantidad,
                motivo=f'Venta #{sale.id}',
                usuario_id=current_user_id
            )
            db.session.add(movement)
        
        # Vaciar carrito
        CartItem.query.filter_by(usuario_id=current_user_id).delete()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Venta creada exitosamente',
            'sale': sale.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@sales_bp.route('/my-orders', methods=['GET'])
@jwt_required()
@cliente_required
def get_my_orders():
    try:
        current_user_id = get_jwt_identity()
        
        sales = Sale.query.filter_by(cliente_id=current_user_id)\
                         .order_by(Sale.fecha_venta.desc())\
                         .all()
        
        return jsonify({
            'sales': [sale.to_dict() for sale in sales]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sales_bp.route('/<int:sale_id>', methods=['GET'])
@jwt_required()
def get_sale(sale_id):
    try:
        current_user_id = get_jwt_identity()
        
        sale = Sale.query.get_or_404(sale_id)
        
        # Verificar permisos
        user = User.query.get(current_user_id)
        if sale.cliente_id != current_user_id and user.rol != 'administrador':
            return jsonify({'error': 'No autorizado'}), 403
        
        return jsonify({'sale': sale.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500