from app import db

class Review(db.Model):
    __tablename__ = 'reseñas'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    #venta_id = db.Column(db.Integer, db.ForeignKey('ventas.id'), nullable=False)
    calificacion = db.Column(db.Integer, nullable=False)  # 1-5
    comentario = db.Column(db.Text)
    aprobada = db.Column(db.Boolean, default=False)
    fecha_creacion = db.Column(db.DateTime, default=db.func.now())
    
    def to_dict(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'usuario_nombre': self.usuario.nombre if self.usuario else None,
            'producto_id': self.producto_id,
            'producto_nombre': self.producto.nombre if self.producto else None,
            #'venta_id': self.venta_id,
            'calificacion': self.calificacion,
            'comentario': self.comentario,
            'aprobada': self.aprobada,
            'fecha_creacion': self.fecha_creacion.isoformat()
        }