import uuid
from flask import Blueprint, request, jsonify
from firebase_admin import firestore

db = firestore.client()

chazaAPI = Blueprint("chazaAPI", __name__)

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
        return jsonify(chaza.to_dict())
    else:
        return 'La chaza no existe'

# For example:   localhost:5000/chaza/getRatingByCategory/Comida
@chazaAPI.route('/getRatingByCategory/<categoryName>', methods=['GET'])
def getRatingByCategory(categoryName=None):
    '''Here goes the code you asked for Nata'''
    result_dict = dict()
    for i in range(1, 6):
        collection = db.collection('chaza').where('categorias', 'array_contains', categoryName).where('calificacion', '==', i)
        shops_by_score = [shop.to_dict() for shop in collection.stream()]
        result_dict[str(i)] = str(len(shops_by_score))
    # Convert result dictionary to JSON
    resp = jsonify(result_dict)
    resp.status_code = 200
    return resp


@chazaAPI.route('/getChazaReports/<chazaID>', methods=['GET'])
def getChazaReports(chazaID=None):
    '''Get all reports related to a Chaza

    Reports have a 'chazaID' attribute and this function filters by this field.
    
    Args:
        chazaID: Given firestone chaza unique id
    '''

    # Database query
    matching_comments = db.collection('reporte').where('chazaID', '==', chazaID)

    try:
        # Return JSON with all matching comments
        return jsonify([doc.to_dict() for doc in matching_comments.stream()]), 200  
    except Exception as e:
        return f"An error has ocurred: {e}"

@chazaAPI.route('/getChazaComments/<chazaID>', methods=['GET'])
def getChazaComments(chazaID=None):
    '''Get all comments related to a Chaza

    Comments have a 'chazaID' attribute and this function filters by this field.
    
    Args:
        chazaID: Given firestone chaza unique id
    '''

    # Database query
    print(chazaID)
    comments_ref  = db.collection('comentario')
    user_ref = db.collection('usuario')

    all_users = {}
    for doc in user_ref.stream():
        usr = doc.to_dict()
        all_users[doc.id] = usr
    return jsonify([addUserToComment(comment_doc,all_users) for comment_doc in comments_ref.where('chazaId', '==', chazaID).stream()]), 200
    try:
        # Return JSON with all matching comments
        return jsonify([addUserToComment(comment_doc,all_users) for comment_doc in comments_ref.where('chazaId', '==', chazaID).stream()]), 200
    except Exception as e:
        return jsonify({'log': f"An error has ocurred: {e}"})

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
        "categorias" : chaza["categorias"],
        "ubicacion" : chaza["ubicacion"],
        "telefono" : chaza["telefono"]
    }


def addUserToComment(comment_doc, all_users):
    comment = comment_doc.to_dict()
    user_id = comment["usuario"]
    #owner = user_ref.document(user_id).get().to_dict()
    if user_id not in all_users.keys(): return comment
    owner = all_users[user_id]
    print(owner)
    comment["usuario"] = {
        "id" : user_id,
        "urlFotoPerfil" : owner["urlFotoPerfil"],
        "nombre" : owner["nombre"]
    }
    return comment