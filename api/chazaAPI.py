import uuid
from flask import Blueprint, request, jsonify
from firebase_admin import firestore

db = firestore.client()

chazaAPI = Blueprint("chazaAPI", __name__)

#Agregar chaza por metodo POST
@chazaAPI.route('/add', methods=['POST'])
def create():
    chaza_ref = db.collection('chaza')
    try:
        id = uuid.uuid4()
        chaza_ref.document(id.hex).set(request.json)
        return jsonify({"success": True}), 200

    except Exception as e:
        return f"An error has ocurred: {e}"

#Listar todas las chazas en la base de datos
@chazaAPI.route('/list', methods=['GET'])
def list():
    chaza_ref = db.collection('chaza')
    try:
        all_chazas = [doc.to_dict() for doc in chaza_ref.stream()]
        return jsonify(all_chazas), 200
        
    except Exception as e:
        return f"An error has ocurred: {e}"

#Obtener info completa de una chaza (ej: /chaza/1b15c3be71bc4875a10599ebb9c3d302)
@chazaAPI.route('/<id>', methods=['GET'])
def id(id=None):
    chaza_ref = db.collection('chaza').document(id)
    chaza = chaza_ref.get()
    if chaza.exists:
        return f'{chaza.to_dict()}'
    else:
        return 'La chaza no existe'

#Obtener y filtrar info resumida de las chazas por categoria y/o nombre
#(ej: /chaza/?categoria=Comida  |  /chaza/?nombre=Chaza1  |  /chaza/?categoria=Comida&nombre=Chaza3)
@chazaAPI.route('/', methods=['GET'])
def search():
    category = request.args.get('categoria')
    if category is None: category = "Todas"

    name = request.args.get('nombre')

    chaza_ref = db.collection('chaza')

    try:
        category_chazas = categoryQuery(chaza_ref,category,name)
        return jsonify(category_chazas), 200

    except Exception as e:
        return f"An error has ocurred: {e}"

def categoryQuery(chaza_ref,category,name):
    if category == "Todas":
        if name != None:
            return [summarizeChaza(chaza_doc) for chaza_doc in chaza_ref.where('nombre', '==', name).stream()]
        return [summarizeChaza(chaza_doc) for chaza_doc in chaza_ref.stream()]

    if name != None:
        return [summarizeChaza(chaza_doc) for chaza_doc in chaza_ref.where('categorias', 'array_contains', category).where('nombre', '==', name).stream()]
    return [summarizeChaza(chaza_doc) for chaza_doc in chaza_ref.where('categorias', 'array_contains', category).stream()]
    

#Retornar diccionario resumido de una chaza (para las categorias)
def summarizeChaza(chaza_doc):
    chaza = chaza_doc.to_dict()
    return {
        "id" : chaza_doc.id,
        "nombre" : chaza["nombre"],
        "urlImagen" : chaza["urlImagen"],
        "calificacion" : chaza["calificacion"],
        "categorias" : chaza["categorias"]
    }