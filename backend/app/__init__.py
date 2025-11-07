from flask import Flask, send_from_directory, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from flask_uploads import UploadSet, IMAGES, configure_uploads
from app.database import db
import os

# ----------------------------
# 🔧 Instancias globales
# ----------------------------
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
photos = UploadSet('photos', IMAGES)

# ----------------------------
# 🔹 Crear aplicación
# ----------------------------
def create_app():
    app = Flask(__name__)

    # ----------------------------
    # Configuración general
    # ----------------------------
    app.config['SECRET_KEY'] = 'granja-cbc-secret-key-2024'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///granja_cbc.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'jwt-secret-key-2024'

    # ----------------------------
    # Configuración subida de imágenes
    # ----------------------------
    upload_folder = os.path.join(app.root_path, '..', 'static', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)

    app.config['UPLOADED_PHOTOS_DEST'] = upload_folder
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB máx
    app.config['UPLOADED_PHOTOS_URL'] = '/static/uploads/'

    configure_uploads(app, photos)

    # ----------------------------
    # Inicializar extensiones
    # ----------------------------
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # ----------------------------
    # Configuración CORS
    # ----------------------------
    CORS(
        app,
        resources={r"/api/*": {"origins": "http://localhost:8080"}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        expose_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

    # ----------------------------
    # Permitir preflight OPTIONS sin auth
    # ----------------------------
    @app.before_request
    def handle_options():
        if request.method == 'OPTIONS':
            return '', 200

    # ----------------------------
    # Registrar Blueprints
    # ----------------------------
    from app.routes.auth import auth_bp
    from app.routes.products import products_bp
    from app.routes.categories import categories_bp
    from app.routes.cart import cart_bp
    from app.routes.stock import stock_bp
    from app.routes.admin import admin_bp
    from app.routes.sales import sales_bp
    from app.routes.pagos import pagos_bp
    from app.routes.facturas import facturas_bp
    from app.routes.envios import envios_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(products_bp, url_prefix='/api/products')
    app.register_blueprint(categories_bp, url_prefix='/api/categories')
    app.register_blueprint(cart_bp, url_prefix='/api/cart')
    app.register_blueprint(stock_bp)
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(sales_bp, url_prefix='/api/sales')
    app.register_blueprint(pagos_bp, url_prefix='/api/pagos')
    app.register_blueprint(facturas_bp, url_prefix='/api/facturas')
    app.register_blueprint(envios_bp, url_prefix='/api/envios')

    # ----------------------------
    # Ruta para archivos estáticos
    # ----------------------------
    @app.route('/static/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(upload_folder, filename)

    # ----------------------------
    # Inicializar Base de Datos y Admin por defecto
    # ----------------------------
    with app.app_context():
        db.create_all()
        print("✅ Base de datos inicializada")

        from app.models.user import User
        admin = User.query.filter_by(email='admin@granjacbc.com').first()
        if not admin:
            admin = User(
                email='admin@granjacbc.com',
                nombre='Administrador',
                rol='administrador'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✅ Usuario admin creado")

    return app
