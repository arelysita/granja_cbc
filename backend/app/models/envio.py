# backend/app/models/envio.py
from app import db
from datetime import datetime

class Envio(db.Model):
    __tablename__ = 'envios'

    id = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column(db.Integer, db.ForeignKey('ventas.id'), nullable=False)
    
    # Información del envío
    transportadora = db.Column(db.String(100))
    numero_guia = db.Column(db.String(100), unique=True)
    costo_envio = db.Column(db.Numeric(10, 2), default=0.00)
    
    # Dirección de envío
    direccion = db.Column(db.Text)
    ciudad = db.Column(db.String(100))
    departamento = db.Column(db.String(100))
    codigo_postal = db.Column(db.String(20))
    telefono_contacto = db.Column(db.String(20))
    persona_recibe = db.Column(db.String(100))
    
    # Seguimiento
    estado = db.Column(db.String(50), default='preparando')
    fecha_estimada_entrega = db.Column(db.DateTime)
    fecha_envio = db.Column(db.DateTime)
    fecha_entrega = db.Column(db.DateTime)
    
    url_seguimiento = db.Column(db.String(500))

    # Relación
    venta = db.relationship('Venta', backref='envios', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'venta_id': self.venta_id,
            'transportadora': self.transportadora,
            'numero_guia': self.numero_guia,
            'costo_envio': float(self.costo_envio) if self.costo_envio else 0.0,
            'direccion': self.direccion,
            'ciudad': self.ciudad,
            'departamento': self.departamento,
            'codigo_postal': self.codigo_postal,
            'telefono_contacto': self.telefono_contacto,
            'persona_recibe': self.persona_recibe,
            'estado': self.estado,
            'fecha_estimada_entrega': self.fecha_estimada_entrega.isoformat() if self.fecha_estimada_entrega else None,
            'fecha_envio': self.fecha_envio.isoformat() if self.fecha_envio else None,
            'fecha_entrega': self.fecha_entrega.isoformat() if self.fecha_entrega else None,
            'url_seguimiento': self.url_seguimiento
        }