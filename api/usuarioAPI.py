import uuid
from flask import Blueprint, request, jsonify
from firebase_admin import firestore

db = firestore.client()

usuarioAPI = Blueprint("usuarioAPI", __name__)


@usuarioAPI.route('/add', methods=['POST'])
def create():
    usuario_ref = db.collection('usuario')
    try:
        usuario_ref.document(request.json['uid']).set(request.json)
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

@usuarioAPI.route('/<id_usuario>/newchaza', methods=['POST'])
def agregarChaza(id_usuario=None):
    chaza_ref = db.collection('chaza')
    usuario_ref = db.collection('usuario').document(id_usuario)
    try:
        id_chaza = uuid.uuid4()
        #request.json["chazasPropias"].push(id_chaza.hex)
        request.json["propietario"] = id_usuario
        chaza_ref.document(id_chaza.hex).set(request.json)
        usuario_ref.update({"chazasPropias": firestore.ArrayUnion([id_chaza.hex])})
        
        return jsonify({"success": True}), 200

    except Exception as e:
        return f"An error has ocurred: {e}"

@usuarioAPI.route('/<id_usuario>/listchazas', methods=['GET'])
def listarChazas(id_usuario=None):
    chaza_ref = db.collection('chaza')
    try:
        return jsonify([summarizeChaza(chaza_doc) for chaza_doc in chaza_ref.where('propietario', '==', id_usuario).stream()])

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
        return jsonify(usuario.to_dict()), 200
    else:
        return jsonify({'log' : 'El usuario no existe'}), 404

def summarizeChaza(chaza_doc):
    chaza = chaza_doc.to_dict()
    return {
        "id" : chaza_doc.id,
        "nombre" : chaza["nombre"],
        "urlImagen" : chaza["urlImagen"],
        "calificacion" : chaza["calificacion"],
        "categorias" : chaza["categorias"],
        "ubicacion" : chaza["ubicacion"],
        "telefono" : chaza["telefono"]
    }