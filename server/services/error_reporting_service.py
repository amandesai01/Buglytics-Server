from traceback import print_exc

from flask import Blueprint, jsonify, request

from server.interfaces import bugs as bug_service
from server.middlewares import error_report_access_required, error_view_access_required
from server.exceptions import BuglyticsException

app = Blueprint("error_reporting_service", __name__)

@app.route('/errors/create', methods=['POST'])
@error_report_access_required
def create_error(project_id, organization_id):
    try:
        data = request.get_json()
        bug_level = data['buglevel']
        bug_location = data['buglocation']
        bug_text = data['bugtext']
        bug = bug_service.create_bug(project_id, bug_level, bug_location, bug_text, organization_id)
        return jsonify({"STATUS": "OK", "DATA": bug})
    except KeyError as e:
        return jsonify({"STATUS": "FAIL", "MSG": "Incomplete Data: " + str(e)})
    except BuglyticsException as e:
        return jsonify({"STATUS": "FAIL", "MSG": str(e)})
    except Exception as e:
        print_exc()
        return jsonify({"STATUS": "FAIL", "MSG": "Server Error"}), 501
