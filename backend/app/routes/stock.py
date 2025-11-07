# app/routes/stock.py
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from app import db
from app.models.stock_movement import StockMovement
from app.models.product import Product

stock_bp = Blueprint('stock', __name__)

# ===============================================================
# 📋 Obtener todos los movimientos de stock
# ===============================================================
@stock_bp.route('/api/admin/stock/movements', methods=['GET', 'OPTIONS'])
@cross_origin(origin='http://localhost:8080', supports_credentials=True)
def get_stock_movements():
    # Respuesta preflight
    if request.method == 'OPTIONS':
        return '', 200

    try:
        movimientos = StockMovement.query.order_by(StockMovement.fecha_movimiento.desc()).all()
        data = [m.to_dict() for m in movimientos]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ===============================================================
# ➕ Registrar un nuevo movimiento y actualizar stock
# ===============================================================
@stock_bp.route('/api/admin/stock/movements', methods=['POST', 'OPTIONS'])
@cross_origin(origin='http://localhost:8080', supports_credentials=True)
def create_stock_movement():
    if request.method == 'OPTIONS':
        return '', 200  # Respuesta preflight

    try:
        data = request.get_json()
        if not data or 'producto_id' not in data:
            return jsonify({'error': 'Datos incompletos'}), 400

        producto = Product.query.get(data['producto_id'])
        if not producto:
            return jsonify({'error': 'Producto no encontrado'}), 404

        # Validar cantidad
        try:
            cantidad = int(data.get('cantidad', 0))
        except ValueError:
            return jsonify({'error': 'La cantidad debe ser un número entero'}), 400

        tipo = data.get('tipo', 'ajuste')
        motivo = str(data.get('motivo', '')).strip()
        usuario_id = data.get('usuario_id')

        movimiento = StockMovement(
            producto_id=producto.id,
            tipo=tipo,
            cantidad=cantidad,
            motivo=motivo,
            usuario_id=usuario_id
        )

        # 🔹 Actualizar stock según el tipo
        if tipo == 'entrada':
            producto.stock += cantidad
        elif tipo == 'salida':
            producto.stock = max(0, producto.stock - cantidad)
        elif tipo == 'ajuste':
            producto.stock = max(0, cantidad)

        db.session.add(movimiento)
        db.session.commit()

        return jsonify({'message': 'Movimiento registrado y stock actualizado correctamente'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
