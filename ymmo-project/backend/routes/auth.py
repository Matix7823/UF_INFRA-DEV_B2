from flask import Blueprint, request, jsonify
from models.user import User
import bcrypt
import jwt
import os

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    nom = data.get('nom')
    
    # Validation
    if not email or not password:
        return {'error': 'Email et password requis'}, 400
    
    # Hash password
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    
    # Créer user
    user_id = User.create(email, hashed, nom, data.get('prenom'))
    
    return {'user_id': str(user_id)}, 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    user = User.find_by_email(email)
    if not user or not bcrypt.checkpw(password.encode(), user['password_hash']):
        return {'error': 'Invalid credentials'}, 401
    
    token = jwt.encode(
        {'user_id': str(user['_id']), 'email': email},
        os.getenv('SECRET_KEY', 'dev-secret-key'),
        algorithm='HS256'
    )
    
    return {'token': token}, 200
