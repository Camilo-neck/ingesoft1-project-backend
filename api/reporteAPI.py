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

@reporteAPI.route('/resolve/<id>', methods=['POST'])
def resolveReport(id):
    ''' Marks a given report as resolved

    Args:
        id: Firestone database report id
    '''
    selected_report = db.collection('reporte').document(id)
    if selected_report.get().exists:
        selected_report.update({"estado_resuelto": "true"})
        return jsonify({"success": True}), 200
    else:
        return 'The selected report does not exist'


@reporteAPI.route('/getUnresolvedReports', methods=['GET'])
def getUnresolvedReports():
    '''Gets all the unresolved reports in JSON format'''

    # Database query
    unresolved_reports = db.collection('reporte').where('estado_resuelto', '==', 'false')

    try:
        # Return JSON with all matching reports
        unresolved = []
        for doc in unresolved_reports.stream():
            d_dict = doc.to_dict()
            d_dict["id"] = doc.id
            unresolved.push(d_dict)

        return jsonify(unresolved), 200  
    except Exception as e:
        return f"An error has ocurred: {e}"

@reporteAPI.route('/delete/<id>', methods=['GET'])
def deleteReport(id=None):
    '''Delete a report given its id
    
    i.e : localhost:5000/report/delete/61e298308ba74f3e8bedf5e7fa9a0789
    where 61e298308ba74f3e8bedf5e7fa9a0789 is the id of the comment

    '''
    try:
        db.collection('reporte').document(id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An error has ocurred: {e}"