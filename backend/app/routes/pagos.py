# backend/app/routes/pagos.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.pago import Pago
from app.models.metodo_pago import MetodoPago
from app.models.venta import Venta
from app.auth.decorators import cliente_required, admin_required

pagos_bp = Blueprint('pagos', __name__)

# --- FUNCIÓN DE AYUDA PARA VALIDACIÓN ---
def get_float_from_data(data, key):
    value = data.get(key)
    if value is None or value == '':
        raise ValueError(f"El campo '{key}' es obligatorio.")
    
    try:
        final_value = float(value)
    except (ValueError, TypeError):
        raise TypeError(f"El campo '{key}' debe ser un número válido.")
    
    if final_value <= 0:
        raise ValueError(f"El campo '{key}' debe ser un número positivo.")
        
    return final_value

# GET /api/pagos/metodos - Obtener métodos de pago disponibles
@pagos_bp.route('/metodos', methods=['GET'])
def get_metodos_pago():
    try:
        metodos = MetodoPago.query.filter_by(activo=True).all()
        return jsonify({
            'metodos_pago': [metodo.to_dict() for metodo in metodos]
        }), 200
    except Exception as e:
        print(f"ERROR (GET METODOS PAGO): {e}")
        return jsonify({'error': str(e)}), 500

# POST /api/pagos/procesar - Procesar un pago
@pagos_bp.route('/procesar', methods=['POST'])
@jwt_required()
@cliente_required
def procesar_pago():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validaciones
        venta_id = data.get('venta_id')
        metodo_pago_id = data.get('metodo_pago_id')
        monto = get_float_from_data(data, 'monto')
        
        # Verificar venta
        venta = Venta.query.filter_by(id=venta_id, cliente_id=current_user_id).first_or_404()
        
        # Verificar método de pago
        metodo_pago = MetodoPago.query.filter_by(id=metodo_pago_id, activo=True).first_or_404()
        
        # Crear pago
        nuevo_pago = Pago(
            venta_id=venta_id,
            metodo_pago_id=metodo_pago_id,
            monto=monto,
            estado='pendiente',
            banco=data.get('banco'),
            tipo_cuenta=data.get('tipo_cuenta'),
            numero_cuenta=data.get('numero_cuenta'),
            telefono_nequi=data.get('telefono_nequi'),
            email_pago=data.get('email_pago')
        )
        
        db.session.add(nuevo_pago)
        db.session.commit()
        
        # Aquí integrarías con la pasarela de pago real (Wompi, PayU, etc.)
        # Por ahora simulamos éxito
        nuevo_pago.estado = 'aprobado'
        nuevo_pago.codigo_autorizacion = 'SIM' + str(nuevo_pago.id).zfill(6)
        nuevo_pago.referencia_externa = 'REF' + str(nuevo_pago.id).zfill(8)
        
        # Actualizar estado de la venta
        venta.estado = 'pagado'
        
        db.session.commit()
        
        return jsonify({
            'message': 'Pago procesado exitosamente',
            'pago': nuevo_pago.to_dict()
        }), 201
        
    except (ValueError, TypeError) as e:
        print(f"ERROR 422 (VALIDACIÓN PAGO): {e}")
        return jsonify({'error': str(e)}), 422
    except Exception as e:
        db.session.rollback()
        print(f"ERROR 500 (PROCESAR PAGO): {e}")
        return jsonify({'error': 'Error procesando el pago'}), 500

# GET /api/pagos/historial - Historial de pagos del usuario
@pagos_bp.route('/historial', methods=['GET'])
@jwt_required()
@cliente_required
def get_historial_pagos():
    try:
        current_user_id = get_jwt_identity()
        
        # Obtener pagos a través de las ventas del usuario
        pagos = db.session.query(Pago).join(Venta).filter(
            Venta.cliente_id == current_user_id
        ).order_by(Pago.fecha_creacion.desc()).all()
        
        return jsonify({
            'pagos': [pago.to_dict() for pago in pagos]
        }), 200
        
    except Exception as e:
        print(f"ERROR (HISTORIAL PAGOS): {e}")
        return jsonify({'error': str(e)}), 500