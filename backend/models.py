from datetime import datetime
from flask_sqlalchemy import SQLAlchemy 

# IMPORTANTE: Debes asegurarte de que 'db' se inicialice
# en tu archivo principal de la aplicación (ej: app.py)
# Si no has definido 'db' aún, hazlo así:
# db = SQLAlchemy()
# Y luego, en tu app.py o __init__.py:
# db.init_app(app)

db = SQLAlchemy()

# =============================================
# TABLA usuarios
# =============================================
class User(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(50), default='cliente')
    nombre = db.Column(db.String(100))
    direccion = db.Column(db.Text)
    telefono = db.Column(db.String(20))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)

    # Relaciones
    ventas = db.relationship('Venta', backref='cliente', lazy=True)
    cart_items = db.relationship('CartItem', backref='user', lazy=True) 
    reseñas = db.relationship('Reseña', backref='usuario', lazy=True)
    movimientos_stock = db.relationship('MovimientoStock', backref='usuario', lazy=True)


# =============================================
# TABLA categorias
# =============================================
class Categoria(db.Model):
    __tablename__ = 'categorias'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    descripcion = db.Column(db.Text)
    imagen_url = db.Column(db.String(500))
    activa = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    productos = db.relationship('Product', backref='categoria', lazy=True)


# =============================================
# TABLA productos
# =============================================
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
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    detalles_venta = db.relationship('DetalleVenta', backref='producto', lazy=True)
    carts = db.relationship('CartItem', backref='product', lazy=True)
    reseñas = db.relationship('Reseña', backref='producto', lazy=True)
    movimientos_stock = db.relationship('MovimientoStock', backref='producto', lazy=True)


# =============================================
# TABLA carrito (¡CORREGIDA PARA COINCIDIR CON TU BD!)
# =============================================
class CartItem(db.Model):
    __tablename__ = 'carrito' # Debe ser 'carrito'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False) # Debe ser 'usuario_id'
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False) 
    cantidad = db.Column(db.Integer, nullable=False, default=1)
    fecha_agregado = db.Column(db.DateTime, default=datetime.utcnow) # Debe ser 'fecha_agregado'

    # Opción de unicidad para evitar duplicados, si la necesitas:
    __table_args__ = (
        db.UniqueConstraint('usuario_id', 'producto_id', name='uq_carrito_item'),
    )


# =============================================
# TABLA ventas (Campos existentes + Pago Colombiano)
# =============================================
class Venta(db.Model):
    __tablename__ = 'ventas'
    
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Campos que ya tienes en tu BD:
    estado = db.Column(db.String(50), default='pendiente') 
    metodo_pago = db.Column(db.String(100)) 
    direccion_envio = db.Column(db.Text) 
    notas = db.Column(db.Text) # Visto en tu esquema SQL
    
    # Nuevos campos sugeridos (si no existen, los tendrás que añadir con SQL)
    referencia_transaccion = db.Column(db.String(255))
    ciudad_envio = db.Column(db.String(100))
    costo_envio = db.Column(db.Numeric(10, 2), default=0.00)
    
    fecha_venta = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow)

    detalles = db.relationship('DetalleVenta', backref='venta', lazy=True)


# =============================================
# TABLA detalles_venta
# =============================================
class DetalleVenta(db.Model):
    __tablename__ = 'detalles_venta'
    
    id = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column(db.Integer, db.ForeignKey('ventas.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    
# =============================================
# TABLA movimientos_stock
# =============================================
class MovimientoStock(db.Model):
    __tablename__ = 'movimientos_stock'
    
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    tipo = db.Column(db.String(20), nullable=False) 
    cantidad = db.Column(db.Integer, nullable=False)
    motivo = db.Column(db.String(255))
    fecha_movimiento = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))


# =============================================
# TABLA reseñas
# =============================================
class Reseña(db.Model):
    __tablename__ = 'reseñas'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    calificacion = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.Text)
    aprobada = db.Column(db.Boolean, default=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)