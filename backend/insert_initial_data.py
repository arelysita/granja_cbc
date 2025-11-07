# Este script inserta los 50 productos iniciales y sus URLs de imagen en la DB.
# Está modificado para BORRAR los datos existentes antes de reinsertar, 
# solucionando productos repetidos y asegurando URLs correctas.

from app import create_app, db
from app.models.product import Product
from app.models.category import Category
import os
from sqlalchemy.exc import IntegrityError

# Mapeo de Categorías (Asegúrate de que estas existan en tu tabla 'categorias'!)
CATEGORIES = [
    'Frutas', 'Verduras', 'Lacteos', 'Granja', 'Hierbas', 'Frutos Secos', 
    'Hongos', 'Ensaladas', 'Tuberculos', 'Citricos', 'Bayas'
]

# Datos de los 50 productos
PRODUCT_DATA = [
    # (Nombre, Descripción, Precio, Categoría, Stock, Nombre_Archivo_Imagen)
    ('Manzanas Rojas', 'Manzanas frescas rojas, dulces y crujientes', 3.99, 'Frutas', 100, 'manzanas_rojas.jpg'),
    ('Plátanos Maduros', 'Plátanos orgánicos, perfectamente maduros', 2.49, 'Frutas', 80, 'platanos.jpg'),
    ('Naranjas Valencia', 'Naranjas jugosas, ricas en vitamina C', 4.50, 'Frutas', 60, 'naranjas.jpg'),
    ('Fresas Frescas', 'Fresas dulces y aromáticas, recién cosechadas', 5.99, 'Frutas', 40, 'fresas.jpg'),
    ('Uvas Verdes', 'Uvas verdes sin semillas, dulces y refrescantes', 6.50, 'Frutas', 35, 'uvas_verdes.jpg'),
    ('Mangos Maduros', 'Mangos tropicales dulces y jugosos', 7.25, 'Frutas', 25, 'mangos.jpg'),
    ('Piñas Dulces', 'Piñas frescas, dulces y aromáticas', 8.99, 'Frutas', 20, 'pinas.jpg'),
    ('Limones Verdes', 'Limones verdes jugosos, perfectos para bebidas', 2.99, 'Frutas', 70, 'limones.jpg'),
    ('Aguacates Hass', 'Aguacates cremosos, listos para consumir', 4.75, 'Frutas', 45, 'aguacates.jpg'),
    ('Sandías', 'Sandías dulces y refrescantes, ideales para verano', 12.99, 'Frutas', 15, 'sandias.jpg'),
    ('Tomates Rojos', 'Tomates frescos rojos, perfectos para ensaladas', 2.99, 'Verduras', 90, 'tomates.jpg'),
    ('Zanahorias Frescas', 'Zanahorias crujientes y dulces', 1.99, 'Verduras', 120, 'zanahorias.jpg'),
    ('Lechuga Romana', 'Lechuga romana fresca y crujiente', 1.50, 'Verduras', 80, 'lechuga.jpg'),
    ('Cebollas Blancas', 'Cebollas blancas frescas, sabor suave', 2.25, 'Verduras', 110, 'cebollas.jpg'),
    ('Papas Amarillas', 'Papas amarillas, ideales para cocinar', 3.50, 'Verduras', 95, 'papas.jpg'),
    ('Brócoli Fresco', 'Brócoli orgánico, rico en nutrientes', 4.25, 'Verduras', 50, 'brocoli.jpg'),
    ('Espinacas', 'Espinacas frescas, perfectas para ensaladas', 2.75, 'Verduras', 45, 'espinacas.jpg'),
    ('Pimientos Rojos', 'Pimientos rojos dulces y jugosos', 3.99, 'Verduras', 40, 'pimientos.jpg'),
    ('Calabacines', 'Calabacines frescos, versátiles para cocinar', 2.50, 'Verduras', 35, 'calabacines.jpg'),
    ('Pepinos', 'Pepinos frescos y crujientes', 1.75, 'Verduras', 65, 'pepinos.jpg'),
    ('Huevos Frescos', 'Huevos frescos de gallinas criadas en libertad', 4.99, 'Lacteos', 200, 'huevos.jpg'),
    ('Leche Entera Fresca', 'Leche entera fresca, sin homogenizar', 3.25, 'Lacteos', 60, 'leche.jpg'),
    ('Queso Fresco', 'Queso fresco artesanal, suave y cremoso', 6.50, 'Lacteos', 30, 'queso_fresco.jpg'),
    ('Mantequilla Natural', 'Mantequilla natural sin sal añadida', 5.75, 'Lacteos', 25, 'mantequilla.jpg'),
    ('Yogurt Natural', 'Yogurt natural cremoso, sin azúcar añadida', 4.25, 'Lacteos', 40, 'yogurt.jpg'),
    ('Miel Pura', 'Miel 100% pura de abejas de la granja', 12.99, 'Granja', 35, 'miel.jpg'),
    ('Mermelada de Fresa', 'Mermelada artesanal de fresas naturales', 6.50, 'Granja', 28, 'mermelada_fresa.jpg'),
    ('Pan Casero', 'Pan artesanal recién horneado', 4.99, 'Granja', 20, 'pan_casero.jpg'),
    ('Aceite de Oliva', 'Aceite de oliva extra virgen, producción local', 15.99, 'Granja', 25, 'aceite_oliva.jpg'),
    ('Mazorcas de Maíz', 'Mazorcas de maíz dulce frescas', 2.99, 'Granja', 50, 'mazorcas.jpg'),
    ('Albahaca Fresca', 'Albahaca fresca recién cosechada', 2.25, 'Hierbas', 40, 'albahaca.jpg'),
    ('Cilantro', 'Cilantro fresco, perfecto para guisos', 1.99, 'Hierbas', 45, 'cilantro.jpg'),
    ('Perejil', 'Perejil fresco, ideal para decorar', 1.75, 'Hierbas', 50, 'perejil.jpg'),
    ('Romero', 'Romero fresco, aromático para carnes', 2.50, 'Hierbas', 30, 'romero.jpg'),
    ('Menta', 'Menta fresca, perfecta para bebidas', 2.25, 'Hierbas', 35, 'menta.jpg'),
    ('Almendras', 'Almendras crudas, ricas en proteínas', 8.99, 'Frutos Secos', 40, 'almendras.jpg'),
    ('Nueces', 'Nueces frescas, ideales para postres', 9.50, 'Frutos Secos', 35, 'nueces.jpg'),
    ('Avellanas', 'Avellanas tostadas, sabor intenso', 10.25, 'Frutos Secos', 25, 'avellanas.jpg'),
    ('Maní Tostado', 'Maní tostado sin sal, snack saludable', 5.99, 'Frutos Secos', 60, 'mani.jpg'),
    ('Pistachos', 'Pistachos salados, deliciosos y nutritivos', 12.99, 'Frutos Secos', 20, 'pistachos.jpg'),
    ('Champiñones Blancos', 'Champiñones frescos, versátiles en cocina', 4.50, 'Hongos', 30, 'champinones.jpg'),
    ('Portobello', 'Setas portobello grandes y carnosas', 6.75, 'Hongos', 20, 'portobello.jpg'),
    ('Shiitake', 'Hongos shiitake frescos, sabor umami', 8.25, 'Hongos', 15, 'shiitake.jpg'),
    ('Ensalada César', 'Ensalada César fresca con aderezo casero', 7.99, 'Ensaladas', 15, 'cesar.jpg'),
    ('Ensalada Griega', 'Ensalada griega con queso feta y aceitunas', 8.50, 'Ensaladas', 12, 'griega.jpg'),
    ('Zanahorias Baby', 'Zanahorias baby dulces y tiernas', 3.25, 'Tuberculos', 55, 'zanahorias_baby.jpg'),
    ('Rábanos', 'Rábanos frescos, picantes y crujientes', 2.99, 'Tuberculos', 40, 'rabanos.jpg'),
    ('Limones Amarillos', 'Limones amarillos jugosos y ácidos', 3.25, 'Citricos', 65, 'limones_amarillos.jpg'),
    ('Toronjas', 'Toronjas dulces y refrescantes', 4.75, 'Citricos', 25, 'toronjas.jpg'),
    ('Arándanos', 'Arándanos frescos, ricos en antioxidantes', 6.99, 'Bayas', 30, 'arandanos.jpg'),
    ('Frambuesas', 'Frambuesas rojas, dulces y aromáticas', 7.50, 'Bayas', 22, 'frambuesas.jpg'),
]

def insert_initial_data():
    app = create_app()
    
    with app.app_context():
        print("Iniciando proceso de limpieza e inserción de datos...")
        
        # 0. Limpieza: BORRAR TODOS LOS DATOS EXISTENTES PARA EVITAR DUPLICADOS
        try:
            # Es vital borrar primero productos, luego categorías por las llaves foráneas.
            db.session.query(Product).delete()
            print("✅ Productos antiguos borrados.")
            db.session.query(Category).delete()
            print("✅ Categorías antiguas borradas.")
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error al borrar datos: {e}. Asegúrate de que las tablas existan.")
            return

        # 1. Insertar Categorías
        for cat_name in CATEGORIES:
            db.session.add(Category(nombre=cat_name))
        try:
            db.session.commit()
            print("✅ Categorías insertadas.")
        except IntegrityError:
            db.session.rollback()
            print("❌ Error de integridad al insertar categorías. Revisar la tabla.")
            return

        # Obtener mapeo de nombre de categoría a ID
        category_map = {cat.nombre: cat.id for cat in Category.query.all()}
        
        # 2. Insertar Productos
        inserted_count = 0
        for name, desc, price, cat_name, stock, image_url in PRODUCT_DATA:
            # El producto no existe porque acabamos de borrar la tabla. Lo creamos.
            new_product = Product(
                nombre=name,
                descripcion=desc,
                precio=price,
                stock=stock,
                # Guardamos solo el nombre del archivo. El modelo to_dict() lo resolverá.
                imagen_url=image_url, 
                categoria_id=category_map.get(cat_name)
            )
            db.session.add(new_product)
            inserted_count += 1
                
        try:
            db.session.commit()
            print(f"\n✨ Proceso completado. Productos insertados: {inserted_count} nuevos productos.")
        except IntegrityError:
            db.session.rollback()
            print("❌ Error de integridad al insertar productos. Revisar las llaves foráneas.")


if __name__ == '__main__':
    # Este script asume que la estructura de la base de datos ya fue creada
    # por run.py o por comandos de Flask-Migrate.
    insert_initial_data()
