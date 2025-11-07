from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(50), default='cliente')
    nombre = db.Column(db.String(100))
    direccion = db.Column(db.Text)
    telefono = db.Column(db.String(20))
    fecha_creacion = db.Column(db.DateTime, default=db.func.now())
    activo = db.Column(db.Boolean, default=True)
    
    # ELIMINAMOS TODAS LAS RELACIONES por ahora
    # ventas = db.relationship('Sale', backref='cliente', lazy=True)
    # carrito = db.relationship('CartItem', backref='usuario', lazy=True)
    # reseñas = db.relationship('Review', backref='usuario', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'rol': self.rol,
            'nombre': self.nombre,
            'telefono': self.telefono,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }