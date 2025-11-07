# backend/app/routes/facturas.py
from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.factura import Factura
from app.models.venta import Venta
from app.auth.decorators import cliente_required, admin_required
import io

facturas_bp = Blueprint('facturas', __name__)

# GET /api/facturas/venta/<int:venta_id> - Obtener factura de una venta
@facturas_bp.route('/venta/<int:venta_id>', methods=['GET'])
@jwt_required()
@cliente_required
def get_factura_venta(venta_id):
    try:
        current_user_id = get_jwt_identity()
        
        # Verificar que la venta pertenece al usuario
        venta = Venta.query.filter_by(id=venta_id, cliente_id=current_user_id).first_or_404()
        
        factura = Factura.query.filter_by(venta_id=venta_id).first()
        if not factura:
            return jsonify({'error': 'No se encontró factura para esta venta'}), 404
            
        return jsonify({
            'factura': factura.to_dict()
        }), 200
        
    except Exception as e:
        print(f"ERROR (GET FACTURA): {e}")
        return jsonify({'error': str(e)}), 500

# GET /api/facturas/usuario - Facturas del usuario
@facturas_bp.route('/usuario', methods=['GET'])
@jwt_required()
@cliente_required
def get_facturas_usuario():
    try:
        current_user_id = get_jwt_identity()
        
        # Obtener facturas a través de las ventas del usuario
        facturas = db.session.query(Factura).join(Venta).filter(
            Venta.cliente_id == current_user_id
        ).order_by(Factura.fecha_factura.desc()).all()
        
        return jsonify({
            'facturas': [factura.to_dict() for factura in facturas]
        }), 200
        
    except Exception as e:
        print(f"ERROR (FACTURAS USUARIO): {e}")
        return jsonify({'error': str(e)}), 500

# POST /api/facturas/generar - Generar factura (admin)
@facturas_bp.route('/generar', methods=['POST'])
@jwt_required()
@admin_required
def generar_factura():
    try:
        data = request.get_json()
        venta_id = data.get('venta_id')
        
        venta = Venta.query.get_or_404(venta_id)
        
        # Generar número de factura (en producción usaría DIAN)
        ultima_factura = Factura.query.order_by(Factura.id.desc()).first()
        nuevo_numero = f"FAC{str(ultima_factura.id + 1 if ultima_factura else 1).zfill(6)}"
        
        factura = Factura(
            venta_id=venta_id,
            numero_factura=nuevo_numero,
            prefijo="FAC",
            cliente_nombre=venta.cliente.nombre,
            cliente_tipo_documento="CC",
            cliente_documento="123456789",
            cliente_email=venta.cliente.email,
            empresa_nombre="Granja CBC",
            empresa_nit="900123456-1",
            empresa_direccion="Calle 123 #45-67, Bogotá",
            empresa_telefono="+57 1 1234567",
            empresa_resolucion_dian="18764000000001",
            subtotal=venta.total * 0.81,  # Asumiendo 19% IVA
            iva=venta.total * 0.19,
            total=venta.total,
            estado="generada"
        )
        
        db.session.add(factura)
        db.session.commit()
        
        return jsonify({
            'message': 'Factura generada exitosamente',
            'factura': factura.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"ERROR (GENERAR FACTURA): {e}")
        return jsonify({'error': 'Error generando factura'}), 500