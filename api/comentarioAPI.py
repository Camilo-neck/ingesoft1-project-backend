import uuid
from flask import Blueprint, request, jsonify
from firebase_admin import firestore
from .utils import sentiment_analysis
from statistics import mean

db = firestore.client()

comentarioAPI = Blueprint("comentarioAPI", __name__)

#Agregar comentario por metodo POST
@comentarioAPI.route('/add', methods=['POST'])
def create():
    comentario_ref = db.collection('comentario')
    chazas_ref = db.collection('chaza')
    try:
        data = request.json
        comentario = data
        chazaId = data['chazaId']
        # comment_sentiment = sentiment_analysis(comentario['contenido'])
        # data['sentiment'] = comment_sentiment
        # print(data)
        id = uuid.uuid4()
        comentario_ref.document(id.hex).set(comentario)
        if comentario["estrellas"] == None: comentario["estrellas"] = 0
        chaza_dict = chazas_ref.document(chazaId).get().to_dict()
        if len(chaza_dict["comentarios"]) == 0: promedio = comentario["estrellas"]
        else: promedio = (float(chaza_dict["calificacion"])+float(comentario["estrellas"]))/2
        
        print(chaza_dict["calificacion"])
        print(comentario["estrellas"])
        print(promedio)

        chazas_ref.document(chazaId).update({
            'comentarios': firestore.ArrayUnion([id.hex]),
            'calificacion' : promedio
        })

        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An error has ocurred: {e}"


@comentarioAPI.route('/increaseCommentUpvotes/<id>', methods=['POST'])
def increaseUpvotes(id=None):
    ''' Increases by 1 the comment upvotes given a comment id

    Args:
        id: Firestone database comment id
    '''
    selected_comment = db.collection('comentario').document(id)
    if selected_comment.get().exists:
        selected_comment.update({'upvotes': firestore.Increment(1)})
        return jsonify({"success": True}), 200
    else:
        return 'The selected comment does not exist'


@comentarioAPI.route('/<id>', methods=['GET'])
def getCommentSummary(id=None):
    ''' Get .JSON containing all the comment attributes

    Args:
        id: Firestone database comment id
    '''
    selected_comment = db.collection('comentario').document(id).get()
    if selected_comment.exists:
        return jsonify(selected_comment.to_dict())
    else:
        return 'The selected comment does not exist'

@comentarioAPI.route('/delete/<id>', methods=['GET'])
def deleteComment(id=None):
    '''Delete a comment given its id
    
    i.e : localhost:5000/comentario/delete/c3fe24df5a6d4bdbb8f3e33af21183bf
    where c3fe24df5a6d4bdbb8f3e33af21183bf is the id of the comment

    '''
    try:
        db.collection('comentario').document(id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An error has ocurred: {e}"


@comentarioAPI.route('/getCommentReports/<commentID>', methods=['GET'])
def getCommentReports(commentID=None):
    '''Get all reports related to a comment
    
    Args:
        commentID: Given firestone comment unique id
    '''

    # Database query
    matching_reports = db.collection('reporte').where('comentarioID', '==', commentID)

    try:
        # Return JSON with all matching comments
        return jsonify([doc.to_dict() for doc in matching_reports.stream()]), 200  
    except Exception as e:
        return f"An error has ocurred: {e}"