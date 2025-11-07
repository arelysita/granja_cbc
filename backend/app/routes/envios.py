# Contenido de backend/app/routes/envios.py

from flask import Blueprint, jsonify

# Define la Blueprint con el nombre 'envios_bp' que se importa en __init__.py
envios_bp = Blueprint('envios_bp', __name__, url_prefix='/api/envios')

# (Opcional) Una ruta de prueba para asegurar que funciona
@envios_bp.route('/', methods=['GET'])
def get_envios():
    return jsonify({"mensaje": "Rutas de envíos cargadas correctamente"})