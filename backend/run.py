# Archivo: run.py
import os
from app import create_app
from flask import jsonify

# Crear la instancia de Flask desde la fábrica
app = create_app()

# ✅ Ruta raíz para verificar que el backend está funcionando
@app.route('/')
def home():
    return jsonify({
        "message": "API Granja CBC funcionando correctamente ✅"
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
