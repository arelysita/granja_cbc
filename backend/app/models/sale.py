# Archivo creado automáticamente
from app import db
from datetime import datetime

class Sale(db.Model):
    __tablename__ = 'ventas'
    
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    estado = db.Column(db.String(50), default='pendiente')  # pendiente, procesando, enviado, completado, cancelado
    metodo_pago = db.Column(db.String(100))
    direccion_envio = db.Column(db.Text)
    notas = db.Column(db.Text)
    fecha_venta = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    detalles = db.relationship('SaleDetail', backref='venta', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'cliente_nombre': self.cliente.nombre if self.cliente else None,
            'total': float(self.total),
            'estado': self.estado,
            'metodo_pago': self.metodo_pago,
            'direccion_envio': self.direccion_envio,
            'notas': self.notas,
            'fecha_venta': self.fecha_venta.isoformat(),
            'fecha_actualizacion': self.fecha_actualizacion.isoformat(),
            'detalles': [detalle.to_dict() for detalle in self.detalles]
        }

class SaleDetail(db.Model):
    __tablename__ = 'detalles_venta'
    
    id = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column(db.Integer, db.ForeignKey('ventas.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'venta_id': self.venta_id,
            'producto_id': self.producto_id,
            'producto_nombre': self.producto.nombre if self.producto else None,
            'cantidad': self.cantidad,
            'precio_unitario': float(self.precio_unitario),
            'subtotal': float(self.cantidad * self.precio_unitario)
        }