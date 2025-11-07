from app.database import db
from datetime import datetime

class Factura(db.Model):
    """Modelo para registrar las facturas asociadas a una venta."""
    __tablename__ = 'factura'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Columna de la llave foránea: apunta a la tabla 'venta'
    venta_id = db.Column(db.Integer, db.ForeignKey('venta.id'), nullable=False, unique=True)
    
    # Número de factura (puede ser autogenerado o manual)
    numero_factura = db.Column(db.String(50), unique=True, nullable=False)
    
    # Campo para la fecha de emisión de la factura
    fecha_emision = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Total facturado
    total_factura = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Estado (ej. 'pendiente', 'pagada', 'anulada')
    estado = db.Column(db.String(50), nullable=False, default='pendiente')
    
    # Relación: ¡La corrección clave es usar 'Venta' como string!
    # Esto permite a SQLAlchemy resolver la clase después de que todos los modelos se carguen.
    # Usamos backref='factura' (singular) porque una venta solo debería tener una factura.
    venta = db.relationship('Venta', backref=db.backref('factura', uselist=False), lazy=True) 

    def __init__(self, venta_id, numero_factura, total_factura, estado='pendiente'):
        self.venta_id = venta_id
        self.numero_factura = numero_factura
        self.total_factura = total_factura
        self.estado = estado

    def to_dict(self):
        """Convierte el objeto Factura a un diccionario para respuestas JSON."""
        return {
            'id': self.id,
            'venta_id': self.venta_id,
            'numero_factura': self.numero_factura,
            'fecha_emision': self.fecha_emision.isoformat() if self.fecha_emision else None,
            'total_factura': float(self.total_factura),
            'estado': self.estado,
        }