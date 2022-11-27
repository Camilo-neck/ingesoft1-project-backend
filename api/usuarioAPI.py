import uuid
from flask import Blueprint, request, jsonify
from firebase_admin import firestore

db = firestore.client()

usuarioAPI = Blueprint("usuarioAPI", __name__)


@usuarioAPI.route('/add', methods=['POST'])
def create():
    usuario_ref = db.collection('usuario')
    try:
        id = uuid.uuid4()
        usuario_ref.document(id.hex).set(request.json)
        return jsonify({"success": True}), 200

    except Exception as e:
        return f"An error has ocurred: {e}"

@usuarioAPI.route('/edit/<id>', methods=['POST'])
def edit(id=None):
    usuario_ref = db.collection('usuario').document(id)
    try:
        usuario_ref.update(request.json)
        return jsonify({"success": True}), 200

    except Exception as e:
        return f"An error has ocurred: {e}"

@usuarioAPI.route('/<id>/newchaza', methods=['POST'])
def agregarChaza(id=None):
    chaza_ref = db.collection('chaza')
    usuario_ref = db.collection('usuario').document(id)
    try:
        id_chaza = uuid.uuid4()
        chaza_ref.document(id_chaza.hex).set(request.json)
        usuario_ref.update({"chazasPropias": firestore.ArrayUnion([id_chaza.hex])})
        return jsonify({"success": True}), 200

    except Exception as e:
        return f"An error has ocurred: {e}"


@usuarioAPI.route('/list', methods=['GET'])
def list():
    usuario_ref = db.collection('usuario')
    try:
        all_usuarios = [doc.to_dict() for doc in usuario_ref.stream()]
        return jsonify(all_usuarios), 200
        
    except Exception as e:
        return f"An error has ocurred: {e}"


@usuarioAPI.route('/<id>', methods=['GET'])
def id(id=None):
    usuario_ref = db.collection('usuario').document(id)
    usuario = usuario_ref.get()
    if usuario.exists:
        return f'{usuario.to_dict()}'
    else:
        return 'El usuario no existe'