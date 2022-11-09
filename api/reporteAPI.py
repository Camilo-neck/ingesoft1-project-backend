import uuid
from flask import Blueprint, request, jsonify
from firebase_admin import firestore

db = firestore.client()

reporteAPI = Blueprint("reporteAPI", __name__)

#Agregar comentario por metodo POST
@reporteAPI.route('/add', methods=['POST'])
def create():
    ''' Insert new report in database '''

    try:
        # Create a unique id for the report
        id = uuid.uuid4()
        # Insert report in firestone database
        db.collection('reporte').document(id.hex).set(request.json) 
        return jsonify({"success": True}), 200  # Get success message
    except Exception as e:
        return f"An error has ocurred: {e}"