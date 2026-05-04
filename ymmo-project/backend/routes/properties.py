from flask import Blueprint, request, jsonify
from models.property import Property
from bson import ObjectId

properties_bp = Blueprint('properties', __name__, url_prefix='/api/properties')

@properties_bp.route('', methods=['GET'])
def list_properties():
    # Filtres optionnels
    prix_min = request.args.get('prix_min', type=int)
    prix_max = request.args.get('prix_max', type=int)
    
    query = {}
    if prix_min:
        query['prix'] = {'$gte': prix_min}
    if prix_max:
        if 'prix' in query:
            query['prix']['$lte'] = prix_max
        else:
            query['prix'] = {'$lte': prix_max}
    
    properties = list(Property.find(query))
    for p in properties:
        p['_id'] = str(p['_id'])
    return {'properties': properties}, 200

@properties_bp.route('', methods=['POST'])
def create_property():
    data = request.json
    prop_id = Property.create(data)
    return {'property_id': str(prop_id)}, 201

@properties_bp.route('/<property_id>', methods=['GET'])
def get_property(property_id):
    prop = Property.find_by_id(ObjectId(property_id))
    if not prop:
        return {'error': 'Not found'}, 404
    prop['_id'] = str(prop['_id'])
    return {'property': prop}, 200
