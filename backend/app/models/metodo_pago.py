# backend/app/models/metodo_pago.py
from app import db
from datetime import datetime

class MetodoPago(db.Model):
    __tablename__ = 'metodos_pago'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    descripcion = db.Column(db.Text)
    activo = db.Column(db.Boolean, default=True)
    comision_porcentaje = db.Column(db.Numeric(5, 2), default=0.00)
    requiere_verificacion = db.Column(db.Boolean, default=False)
    tipo_billetera = db.Column(db.String(50))
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'codigo': self.codigo,
            'descripcion': self.descripcion,
            'activo': self.activo,
            'comision_porcentaje': float(self.comision_porcentaje) if self.comision_porcentaje else 0.0,
            'requiere_verificacion': self.requiere_verificacion,
            'tipo_billetera': self.tipo_billetera
        }