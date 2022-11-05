import uuid
from flask import Blueprint, request, jsonify
from firebase_admin import firestore

db = firestore.client()

userAPI = Blueprint("userAPI", __name__)

@userAPI.route('/add', methods=['POST'])
def create():
    user_ref = db.collection('user')
    try:
        # Identificador unico de cada documento de cada coleccion
        id = uuid.uuid4()
        user_ref.document(id.hex).set(request.json)
        return jsonify({"success": True}), 200

    except Exception as e:
        return f"An error has ocurred: {e}"

@userAPI.route('/list', methods=['GET'])
def list():
    user_ref = db.collection('user')
    try:
        all_users = [doc.to_dict() for doc in user_ref.stream()]
        return jsonify(all_users), 200
        
    except Exception as e:
        return f"An error has ocurred: {e}"

# No estoy seguro si esta es la manera correcta de hacer el read
@userAPI.route('/read', methods=['POST'])
def read():
    try:
        user_id = request.json["id"]
        user_ref = db.collection('user').where('id', '==', user_id)
        user = [doc.to_dict() for doc in user_ref.stream()]
        return jsonify(user), 200

    except Exception as e:
        return f"An error has ocurred: {e}"