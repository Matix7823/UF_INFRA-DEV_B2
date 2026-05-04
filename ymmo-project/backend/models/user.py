from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()
client = MongoClient(os.getenv('MONGO_URI', 'mongodb://localhost:27017/ymmo'))
db = client['ymmo']

class User:
    @staticmethod
    def create(email, password_hash, nom, prenom, role='client'):
        user_data = {
            'email': email,
            'password_hash': password_hash,
            'nom': nom,
            'prenom': prenom,
            'role': role,
            'created_at': datetime.now()
        }
        result = db.users.insert_one(user_data)
        return result.inserted_id
    
    @staticmethod
    def find_by_email(email):
        return db.users.find_one({'email': email})
    
    @staticmethod
    def find_by_id(user_id):
        from bson import ObjectId
        return db.users.find_one({'_id': ObjectId(user_id)})
