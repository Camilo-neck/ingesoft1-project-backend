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


@comentarioAPI.route('/increaseCommentUpvotes/<id>', methods=['POST'])
def increaseUpvotes(id=None):
    ''' Increases by 1 the comment upvotes given a comment id

    Args:
        id: Firestone database comment id
    '''
    selected_comment = db.collection('comentario').document(id)
    if selected_comment.get().exists:
        selected_comment.update({'upvotes': firestore.Increment(1)})
    else:
        print('The selected comment does not exist')
    return '' # Dummy return which must be changed


@comentarioAPI.route('/<id>', methods=['GET'])
def getCommentSummary(id=None):
    ''' Get .JSON containing all the comment attributes

    Args:
        id: Firestone database comment id
    '''
    selected_comment = db.collection('comentario').document(id).get()
    if selected_comment.exists:
        return f'{selected_comment.to_dict()}'
    else:
        return 'The selected comment does not exist'