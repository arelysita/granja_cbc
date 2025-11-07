# Script para ELIMINAR PERMANENTEMENTE todos los registros de la tabla 'products'.

from app import create_app, db
from app.models.product import Product
from sqlalchemy.exc import IntegrityError
import os

def delete_all_products():
    # Creamos la instancia de la aplicación Flask
    app = create_app()
    
    with app.app_context():
        print("Iniciando proceso de eliminación de TODOS los productos...")
        
        try:
            # 1. Eliminar todos los productos.
            # Esta línea borra TODAS las filas de la tabla 'product'.
            # Usar 'synchronize_session=False' es necesario para algunos ORMs.
            count = db.session.query(Product).delete(synchronize_session=False)
            db.session.commit()
            
            print(f"✅ Éxito: Se eliminaron {count} productos de la base de datos.")
            
            # Opcional: Si deseas que los IDs empiecen desde 1 de nuevo (solo en SQLite)
            # Para SQLite, resetear la secuencia (autoincremento)
            if db.engine.url.drivername == 'sqlite':
                 db.session.execute(db.text("UPDATE sqlite_sequence SET seq = 0 WHERE name='product'"))
                 db.session.commit()
                 print("✅ Secuencia de ID de la tabla 'product' reseteada.")

        except IntegrityError as e:
            db.session.rollback()
            print("\n❌ ERROR DE INTEGRIDAD: La eliminación falló.")
            print("Esto significa que hay otras tablas (reseñas, pedidos, etc.) que dependen de estos productos.")
            print("Debes eliminar primero los registros relacionados en esas otras tablas.")
            print(f"Detalles del error: {e}")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ ERROR INESPERADO al eliminar productos: {e}")
        
if __name__ == '__main__':
    delete_all_products()
