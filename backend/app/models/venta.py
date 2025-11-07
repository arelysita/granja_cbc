from app.database import db
from datetime import datetime

# Tabla intermedia para el detalle de la venta (muchos a muchos o uno a muchos)
# En este caso, usaremos un modelo explícito de detalle.

class DetalleVenta(db.Model):
    """Modelo para las líneas de una venta (qué productos se vendieron)."""
    __tablename__ = 'detalle_venta'
    
    id = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column(db.Integer, db.ForeignKey('venta.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    
    cantidad = db.Column(db.Integer, nullable=False, default=1)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Relación con Producto (asumiendo que tienes un modelo Producto)
    # producto = db.relationship('Producto', backref='detalles_venta') 

    def __init__(self, venta_id, producto_id, cantidad, precio_unitario):
        self.venta_id = venta_id
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.subtotal = cantidad * precio_unitario # Cálculo básico
        
    def to_dict(self):
        return {
            'id': self.id,
            'producto_id': self.producto_id,
            'cantidad': self.cantidad,
            'precio_unitario': float(self.precio_unitario),
            'subtotal': float(self.subtotal)
        }

class Venta(db.Model):
    """Modelo principal de la Venta."""
    __tablename__ = 'venta'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Campo para la fecha, usando la hora actual por defecto
    fecha_venta = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relación a un cliente (opcional)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=True)
    
    # Campo para el total de la venta
    total_venta = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    
    # Relación con DetalleVenta: 'cascade' asegura que los detalles se borren 
    # si se borra la venta.
    detalles = db.relationship('DetalleVenta', backref='venta', lazy='dynamic', cascade="all, delete-orphan")

    # Constructor: Soluciona el 'SyntaxError' al definir argumentos reales (o ninguno)
    def __init__(self, cliente_id=None, total_venta=0.00, **kwargs):
        self.cliente_id = cliente_id
        self.total_venta = total_venta
        # La fecha_venta se establece por defecto.
        super().__init__(**kwargs) 

    def to_dict(self):
        """Convierte el objeto Venta a un diccionario para respuestas JSON."""
        return {
            'id': self.id,
            'fecha_venta': self.fecha_venta.isoformat() if self.fecha_venta else None,
            'cliente_id': self.cliente_id,
            'total_venta': float(self.total_venta),
            # Incluir los detalles de la venta (si es necesario)
            'detalles': [detalle.to_dict() for detalle in self.detalles.all()]
        }