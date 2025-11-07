# Archivo creado automáticamente
from app import db

class Category(db.Model):
    __tablename__ = 'categorias'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    imagen_url = db.Column(db.String(500))
    activa = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=db.func.now())
    
    # Relaciones
    productos = db.relationship('Product', backref='categoria', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'imagen_url': self.imagen_url,
            'activa': self.activa,
            'fecha_creacion': self.fecha_creacion.isoformat(),
            'cantidad_productos': len(self.productos)
        }