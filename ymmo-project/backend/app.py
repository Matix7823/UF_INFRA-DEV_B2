from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from dotenv import load_dotenv
import os
import bcrypt
import jwt
from datetime import datetime
import json

load_dotenv()

app = Flask(__name__)
CORS(app)
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-ultra-secure')
DB_PATH = 'ymmo.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                nom TEXT NOT NULL,
                role TEXT DEFAULT 'client',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Structure V2 pour Properties
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS properties (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titre TEXT NOT NULL,
                description TEXT,
                prix INTEGER NOT NULL,
                surface INTEGER NOT NULL,
                chambres INTEGER DEFAULT 0,
                ville TEXT NOT NULL,
                status TEXT DEFAULT 'disponible',
                dpe TEXT DEFAULT 'A',
                equipements TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

init_db()

@app.route('/api/health', methods=['GET'])
def health():
    return {'status': 'ok', 'version': 'v2', 'message': 'Backend Premium fonctionnel!'}, 200

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    nom = data.get('nom', 'Utilisateur')
    
    if not email or not password:
        return {'error': 'Email et password requis'}, 400
        
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (email, password_hash, nom) VALUES (?, ?, ?)', (email, hashed, nom))
            conn.commit()
            return {'message': 'User créé', 'user_id': cursor.lastrowid}, 201
    except sqlite3.IntegrityError:
        return {'error': 'Email déjà utilisé'}, 400
    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        
    if not user:
        return {'error': 'User not found'}, 404
        
    if not bcrypt.checkpw(password.encode(), user['password_hash'].encode()):
        return {'error': 'Invalid password'}, 401
        
    token = jwt.encode({'user_id': user['id'], 'email': email}, SECRET_KEY, algorithm='HS256')
    
    return {'message': 'Login success', 'token': token, 'user': {'id': user['id'], 'email': email, 'nom': user['nom']}}, 200

@app.route('/api/properties', methods=['GET'])
def get_properties():
    prix_min = request.args.get('prix_min', type=int)
    prix_max = request.args.get('prix_max', type=int)
    ville = request.args.get('ville', type=str)
    
    query = 'SELECT * FROM properties WHERE 1=1'
    params = []
    
    if prix_min:
        query += ' AND prix >= ?'
        params.append(prix_min)
    if prix_max:
        query += ' AND prix <= ?'
        params.append(prix_max)
    if ville:
        query += ' AND ville LIKE ?'
        params.append(f'%{ville}%')
        
    query += ' ORDER BY created_at DESC LIMIT 50'
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        properties = [dict(row) for row in cursor.fetchall()]
        
    return {'properties': properties}, 200

@app.route('/api/properties/<int:prop_id>', methods=['GET'])
def get_property(prop_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM properties WHERE id = ?', (prop_id,))
        row = cursor.fetchone()
        if not row:
            return {'error': 'Non trouvé'}, 404
        return {'property': dict(row)}, 200

@app.route('/api/properties', methods=['POST'])
def create_property():
    data = request.json
    required = ['titre', 'prix', 'surface', 'localisation']
    if not all(field in data for field in required):
        return {'error': 'Champs obligatoires manquants'}, 400
        
    titre = data.get('titre')
    description = data.get('description', '')
    prix = data.get('prix')
    surface = data.get('surface')
    chambres = data.get('chambres', 0)
    ville = data.get('localisation', {}).get('ville', '')
    dpe = data.get('dpe', 'A')
    equipements = json.dumps(data.get('equipements', []))
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO properties (titre, description, prix, surface, chambres, ville, dpe, equipements)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (titre, description, prix, surface, chambres, ville, dpe, equipements))
        conn.commit()
        return {'message': 'Propriété luxueuse créée', 'property_id': cursor.lastrowid}, 201

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    from analytics_service import MarketAnalyzer
    analyzer = MarketAnalyzer(DB_PATH)
    stats = analyzer.get_market_trends()
    return jsonify(stats), 200

if __name__ == '__main__':
    print("\n Serveur SQLAlchemy/SQLite V2 lance sur http://localhost:5000")
    print(" API docs: http://localhost:5000/api/health\n")
    app.run(debug=True, port=5000)
