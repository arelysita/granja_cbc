from app.database import db
from datetime import datetime

class Pago(db.Model):
    """Modelo para registrar los pagos asociados a una venta."""
    __tablename__ = 'pago'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Columna de la llave foránea: apunta a la tabla 'venta'
    venta_id = db.Column(db.Integer, db.ForeignKey('venta.id'), nullable=False)
    
    monto = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Tipo de pago (ej. 'efectivo', 'tarjeta', 'transferencia')
    tipo_pago = db.Column(db.String(50), nullable=False)
    
    # Campo para la fecha del pago
    fecha_pago = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relación: ¡La corrección clave es usar 'Venta' como string!
    # Esto le permite a SQLAlchemy resolver la clase después de que todos los modelos se carguen.
    venta = db.relationship('Venta', backref='pagos', lazy=True)

    def __init__(self, venta_id, monto, tipo_pago):
        self.venta_id = venta_id
        self.monto = monto
        self.tipo_pago = tipo_pago

    def to_dict(self):
        """Convierte el objeto Pago a un diccionario para respuestas JSON."""
        return {
            'id': self.id,
            'venta_id': self.venta_id,
            'monto': float(self.monto),
            'tipo_pago': self.tipo_pago,
            'fecha_pago': self.fecha_pago.isoformat() if self.fecha_pago else None,
        }