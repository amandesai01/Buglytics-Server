from traceback import print_exc

from flask import Blueprint, jsonify, request

from server.interfaces import bugs as bug_service
from server.interfaces import projects as proj_service
from server.interfaces import webhooks as webh_service
from server.middlewares import error_report_access_required, error_view_access_required, organization_required
from server.exceptions import BuglyticsException

app = Blueprint("dashboard_service", __name__)

@app.route('/errors/all')
@organization_required
def get_all_errors(organization_id):
    try:
        project_id = request.args['projectid']
        data = bug_service.get_all_bugs(project_id, organization_id)
        return jsonify({"STATUS": "OK", "DATA": data})
    except BuglyticsException as e:
        return jsonify({"STATUS": "FAIL", "MSG": str(e)})
    except Exception as e:
        print_exc()
        return jsonify({"STATUS": "FAIL", "MSG": "Server Error"}), 501

@app.route('/errors')
@error_view_access_required
def get_error(_, organization_id):
    try:
        bug_id = request.args['bugid']
        data = bug_service.get_specific_bug(bug_id, organization_id)
        return jsonify({"STATUS": "OK", "DATA": data}) 
    except BuglyticsException as e:
        return jsonify({"STATUS": "FAIL", "MSG": str(e)})
    except Exception as e:
        print_exc()
        return jsonify({"STATUS": "FAIL", "MSG": "Server Error"}), 501

@app.route('/projects/create', methods=['POST'])
@organization_required
def create_project(organization_id):
    try:
        data = request.get_json()
        title = data['title']
        details = data['details']
        project = proj_service.create_project(title, details, organization_id)
        return jsonify({"STATUS": "OK", "PROJECT": project})
    except BuglyticsException as e:
        return jsonify({"STATUS": "FAIL", "MSG": str(e)})
    except Exception as e:
        print_exc()
        return jsonify({"STATUS": "FAIL", "MSG": "Server Error"}), 501

@app.route('/projects/all')
@organization_required
def get_all_projects(organization_id):
    try:
        data = proj_service.get_all_projects(organization_id)
        return jsonify({"STATUS": "OK", "DATA": data})
    except BuglyticsException as e:
        return jsonify({"STATUS": "FAIL", "MSG": str(e)})
    except Exception as e:
        print_exc()
        return jsonify({"STATUS": "FAIL", "MSG": "Server Error"}), 501

@app.route('/projects')
@organization_required
def get_a_project(organization_id):
    try:
        project_id = request.args['projectid']
        project = proj_service.get_selected_project(project_id, organization_id)
        return jsonify({"STATUS": "OK", "PROJECT": project})
    except BuglyticsException as e:
        return jsonify({"STATUS": "FAIL", "MSG": str(e)})
    except Exception as e:
        print_exc()
        return jsonify({"STATUS": "FAIL", "MSG": "Server Error"}), 501

@app.route('/webhooks/create', methods=['POST'])
@organization_required
def create_webhook(_):
    try:
        data = request.get_json()
        project_id = data['projectid']
        target_url = data['targeturl']
        bug_level = data['buglevel']
        webhook = webh_service.create_webhook(project_id, target_url, bug_level)
        return jsonify({"STATUS": "OK", "WEBHOOK": webhook})
    except BuglyticsException as e:
        return jsonify({"STATUS": "FAIL", "MSG": str(e)})
    except Exception as e:
        print_exc()
        return jsonify({"STATUS": "FAIL", "MSG": "Server Error"}), 501

@app.route('/webhooks/all')
@organization_required
def get_all_webhooks(_):
    try:
        projectid = request.args['projectid']
        data = webh_service.get_all_webhooks(projectid)
        return jsonify({"STATUS": "OK", "DATA": data})
    except BuglyticsException as e:
        return jsonify({"STATUS": "FAIL", "MSG": str(e)})
    except Exception as e:
        print_exc()
        return jsonify({"STATUS": "FAIL", "MSG": "Server Error"}), 501

@app.route('/webhooks/delete')
@organization_required
def delete_webhook(_):
    try:
        webhookid = request.args['webhookid']
        projectid = request.args['projectid']
        webh_service.delete_webhook(webhookid, projectid)
        return jsonify({"STATUS": "OK"})
    except BuglyticsException as e:
        return jsonify({"STATUS": "FAIL", "MSG": str(e)})
    except Exception as e:
        print_exc()
        return jsonify({"STATUS": "FAIL", "MSG": "Server Error"}), 501