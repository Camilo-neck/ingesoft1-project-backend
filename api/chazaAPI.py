import uuid
from flask import Blueprint, request, jsonify
from firebase_admin import firestore
from statistics import mean

db = firestore.client()

chazaAPI = Blueprint("chazaAPI", __name__)

# @chazaAPI.route('/update', methods=['GET'])
# def update():
#     comentario_ref = db.collection('comentario')
#     chazas_ref = db.collection('chaza')

#     for chaza in chazas_ref.stream():

#         chazaId = chaza.id
#         estrellas = [float(doc.to_dict()["estrellas"]) for doc in comentario_ref.where('chazaId', '==', chazaId).stream()]
#         if len(estrellas) == 0: promedio = 0 
#         else: promedio = mean(estrellas)

#         chazas_ref.document(chazaId).update({
#             'calificacion' : promedio
#         })
#         print(promedio, chazaId)
#     return "YES", 200
    

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


@chazaAPI.route('/edit/<id>', methods=['POST'])
def edit(id=None):
    chaza_ref = db.collection('chaza').document(id)
    try:
        chaza_ref.update(request.json)
        return jsonify({"success": True}), 200

    except Exception as e:
        return f"An error has ocurred: {e}"



@chazaAPI.route('/getChazaReports/<chazaID>', methods=['GET'])
def getChazaReports(chazaID=None):
    '''Get all reports related to a Chaza

    Reports have a 'chazaID' attribute and this function filters by this field.
    
    Args:
        chazaID: Given firestone chaza unique id
    '''

    # Database query
    reports_ref  = db.collection('reporte')

    user_ref = db.collection('usuario')

    all_users = {}
    for doc in user_ref.stream():
        usr = doc.to_dict()
        all_users[doc.id] = usr

    try:
        # Return JSON with all matching reports
        return jsonify([addUser(report_doc, all_users) for report_doc in reports_ref.where('chazaId', '==', chazaID).stream()]), 200
    except Exception as e:
        return jsonify({'log': f"An error has ocurred: {e}"})

@chazaAPI.route('/getChazaComments/<chazaID>', methods=['GET'])
def getChazaComments(chazaID=None):
    '''Get all comments related to a Chaza

    Comments have a 'chazaID' attribute and this function filters by this field.
    
    Args:
        chazaID: Given firestone chaza unique id
    '''

    # Database query
    comments_ref  = db.collection('comentario')
    user_ref = db.collection('usuario')

    all_users = {}
    for doc in user_ref.stream():
        usr = doc.to_dict()
        all_users[doc.id] = usr


    try:
        # Return JSON with all matching comments
        return jsonify([addUser(comment_doc, all_users) for comment_doc in comments_ref.where('chazaId', '==', chazaID).stream()]), 200
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

#estadisticas de rating
@chazaAPI.route('/rating', methods=['GET'])
def rating():
    chaza_ref = db.collection('chaza')
    categoryRating = []

    categories = ["Mercado", "Vivero", "Comida", "Comidas rapidas", "Ropa", "Bisuteria", "Papeleria", "Dulces", "Otros"]
    for category in categories:

        categoryRating.append({
            "tipo" : category,
            "4-5 estrellas": 0,
            "3-4 estrellas": 0,
            "2-3 estrellas": 0,
            "1-2 estrellas": 0,
            "0-1 estrellas": 0
         })

    try:
    
        for doc in chaza_ref.stream():
            chaza = doc.to_dict()
            rate = float(chaza["calificacion"])

            for cat in chaza["categorias"]: 
                if rate>4 and rate <=5: categoryRating[categories.index(cat)]["4-5 estrellas"] +=1; continue
                if rate>3 and rate <=4: categoryRating[categories.index(cat)]["3-4 estrellas"] +=1; continue
                if rate>2 and rate <=3: categoryRating[categories.index(cat)]["2-3 estrellas"] +=1; continue
                if rate>1 and rate <=2: categoryRating[categories.index(cat)]["1-2 estrellas"] +=1; continue
                categoryRating[categories.index(cat)]["0-1 estrellas"] +=1
            

        return jsonify(categoryRating), 200
        
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

#Agregar info basica de usuario a comentario/reporte 
def addUser(document, all_users):
    d_doc = document.to_dict()
    user_id = d_doc["usuario"]
    if user_id not in all_users.keys(): return d_doc
    owner = all_users[user_id]

    d_doc["id"] = document.id
    d_doc["usuario"] = {
        "id" : user_id,
        "urlFotoPerfil" : owner["urlFotoPerfil"],
        "nombre" : owner["nombre"]
    }
    return d_doc
