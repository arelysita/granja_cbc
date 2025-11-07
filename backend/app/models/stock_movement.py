from app import db

class StockMovement(db.Model):
    __tablename__ = 'movimientos_stock'
    
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # entrada, salida, ajuste
    cantidad = db.Column(db.Integer, nullable=False)
    motivo = db.Column(db.String(255))
    fecha_movimiento = db.Column(db.DateTime, default=db.func.now())
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

    # ✅ Relación con el producto
    producto = db.relationship('Product', backref='movimientos_stock', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'producto_id': self.producto_id,
            'producto_nombre': self.producto.nombre if self.producto else None,
            'tipo': self.tipo,
            'cantidad': self.cantidad,
            'motivo': self.motivo,
            'fecha_movimiento': self.fecha_movimiento.isoformat(),
            'usuario_id': self.usuario_id
        }
