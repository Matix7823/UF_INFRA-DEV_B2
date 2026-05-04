from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime
from bson import ObjectId

load_dotenv()
client = MongoClient(os.getenv('MONGO_URI', 'mongodb://localhost:27017/ymmo'))
db = client['ymmo']

class Property:
    @staticmethod
    def create(data):
        data['created_at'] = datetime.now()
        result = db.properties.insert_one(data)
        return result.inserted_id
    
    @staticmethod
    def find(query):
        return db.properties.find(query)
    
    @staticmethod
    def find_by_id(property_id):
        return db.properties.find_one({'_id': ObjectId(property_id)})
