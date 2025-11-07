# app/models/cart.py
from app import db
from datetime import datetime

class CartItem(db.Model):
    __tablename__ = 'carrito'  # usa el nombre real de tu tabla si es otro

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=1)
    fecha_agregado = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación (asegúrate que Product está definido)
    product = db.relationship('Product', backref='cart_items', lazy=True)

    def to_dict(self):
        # Construye una salida exactamente con los keys que usa el frontend
        producto = None
        if self.product:
            # usa la lógica que tengas en Product.to_dict para imagen_url si aplica
            imagen = self.product.imagen_url
            if imagen and not imagen.startswith('/'):
                imagen = f'/static/uploads/{imagen}'
            producto = {
                'id': self.product.id,
                'nombre': self.product.nombre,
                'precio': float(self.product.precio),
                'imagen_url': imagen,
                'stock': self.product.stock
            }

        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'producto_id': self.producto_id,
            # keys usados por tu frontend:
            'producto_imagen': producto['imagen_url'] if producto else None,
            'producto_nombre': producto['nombre'] if producto else 'Desconocido',
            'producto_precio': producto['precio'] if producto else 0.0,
            'producto_stock': producto['stock'] if producto else 0,
            'cantidad': self.cantidad,
            'subtotal': float(self.cantidad * producto['precio']) if producto else 0.0,
            'fecha_agregado': self.fecha_agregado.isoformat() if self.fecha_agregado else None
        }
