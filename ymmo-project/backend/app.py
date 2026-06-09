from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import bcrypt
import jwt
from datetime import datetime
import json
import sys

# Ajout du dossier services au path
sys.path.append(os.path.join(os.path.dirname(__file__), 'services'))
from db_service import DBService
from analytics_service import MarketAnalyzer

load_dotenv()

app = Flask(__name__)
CORS(app)
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-ultra-secure')

db_service = DBService()

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'server': 'IIS/WindowsServer', 'db': 'SQL Server 2025'}), 200

# --- AUTH ROUTES ---
# Note: Ces routes supposent une table 'Users' dans SQL Server
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    # Simuler un utilisateur pour le projet étudiant si la table n'est pas encore créée
    # Ou implémenter la recherche réelle
    if email == "admin@ymmo.fr" and password == "admin123":
        token = jwt.encode({'user_id': 1, 'email': email}, SECRET_KEY, algorithm='HS256')
        return jsonify({
            'message': 'Login success', 
            'token': token, 
            'user': {'id': 1, 'email': email, 'nom': 'Architecte Ymmo'}
        }), 200
    
    return jsonify({'error': 'Identifiants invalides (admin@ymmo.fr / admin123)'}), 401

# --- PROPERTY ROUTES ---

@app.route('/api/properties', methods=['GET'])
def get_properties():
    prix_min = request.args.get('prix_min', type=int)
    prix_max = request.args.get('prix_max', type=int)
    ville = request.args.get('ville', type=str)
    
    properties = db_service.fetch_all_properties(prix_min, prix_max, ville)
    return jsonify(properties), 200

@app.route('/api/properties/<int:prop_id>', methods=['GET'])
def get_property(prop_id):
    prop = db_service.fetch_property_by_id(prop_id)
    if not prop:
        return jsonify({'error': 'Bien non trouvé'}), 404
    return jsonify(prop), 200

@app.route('/api/properties', methods=['POST'])
def create_property():
    data = request.json
    # Mapping JSON frontend vers structure SQL
    property_data = {
        'titre': data.get('titre'),
        'ville': data.get('localisation', {}).get('ville', data.get('ville')),
        'prix': data.get('prix'),
        'type_bien': data.get('type_bien', 'Appartement'),
        'surface': data.get('surface'),
        'chambres': data.get('chambres'),
        'description': data.get('description'),
        'dpe': data.get('dpe', 'A'),
        'status': 'disponible'
    }
    
    new_id = db_service.add_property(property_data)
    if new_id:
        return jsonify({'message': 'Bien ajouté avec succès', 'id': new_id}), 201
    return jsonify({'error': 'Erreur lors de l\'ajout'}), 500

# --- ANALYTICS ROUTES ---

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    analyzer = MarketAnalyzer()
    stats = analyzer.get_market_trends()
    return jsonify(stats), 200

if __name__ == '__main__':
    print("\n[YMMO BACKEND] Serveur lancé pour environnement IIS")
    print("Base de données : SQL Server 2025 Express")
    app.run(debug=True, port=5000)
