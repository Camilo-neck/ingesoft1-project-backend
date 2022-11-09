import uuid
from flask import Blueprint, request, jsonify
from firebase_admin import firestore

db = firestore.client()

comentarioAPI = Blueprint("comentarioAPI", __name__)

#Agregar comentario por metodo POST
@comentarioAPI.route('/add', methods=['POST'])
def create():
    comentario_ref = db.collection('comentario')
    try:
        id = uuid.uuid4()
        comentario_ref.document(id.hex).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An error has ocurred: {e}"
