import uuid
from flask import Blueprint, request, jsonify
from firebase_admin import firestore

db = firestore.client()

reporteAPI = Blueprint("reporteAPI", __name__)


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


@reporteAPI.route('/<id>', methods=['GET'])
def getReportSummary(id=None):
    ''' Get .JSON containing all the comment attributes

    Args:
        id: Firestone database report id
    '''
    selected_report = db.collection('reporte').document(id).get()
    if selected_report.exists:
        return f'{selected_report.to_dict()}'
    else:
        return 'The selected report does not exist'