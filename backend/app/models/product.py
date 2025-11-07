from app import db
import os

class Product(db.Model):
    __tablename__ = 'productos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, default=0)
    imagen_url = db.Column(db.String(500))
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=db.func.now())
    
    # ✅ Relación con carrito (solo aquí, NO en cart.py)
    
    def to_dict(self):
        # Construcción de URL de imagen
        image_path = self.imagen_url
        
        if image_path:
            if not image_path.startswith('/'):
                final_imagen_url = f'/static/uploads/{image_path}'
            else:
                final_imagen_url = image_path
        else:
            final_imagen_url = '/static/uploads/default.jpg'
            
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': float(self.precio),
            'stock': self.stock,
            'imagen_url': final_imagen_url,
            'categoria_id': self.categoria_id,
            'activo': self.activo,
            'fecha_creacion': self.fecha_creacion.isoformat(),
            'categoria_nombre': self.categoria.nombre if hasattr(self, 'categoria') and self.categoria else None
        }
