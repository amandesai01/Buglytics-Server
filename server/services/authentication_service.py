from traceback import print_exc

from flask import Blueprint, jsonify, request

from server.interfaces import organizations as org_service
from server.middlewares import organization_required
from server.exceptions import BuglyticsException
from server.utils import get_object_from_token, get_token_from_object
from server.properties import get_site_secret_key

app = Blueprint("authentication_service", __name__)

@app.route('/authenticate/organization', methods=['POST'])
def authenticate_organization():
    try:
        data = request.get_json()
        email = data['email']
        password = data['password']
        organization_id = org_service.get_organization_id_from_email_password(email, password)
        token_contents = {
            "ORG_ID": organization_id,
            "TYPE": "ORGANIZATION"
        }
        token = get_token_from_object(token_contents, get_site_secret_key(), 7200)
        return jsonify({"STATUS": "OK", "TOKEN": token})
    except KeyError as e:
        return jsonify({"STATUS": "FAIL", "MSG": "Incomplete Data: " + str(e)})
    except BuglyticsException as e:
        return jsonify({"STATUS": "FAIL", "MSG": str(e)})
    except Exception as e:
        print_exc()
        return jsonify({"STATUS": "FAIL", "MSG": "Server Error"}), 501

@app.route('/authentication/tokens/create', methods=['POST'])
@organization_required
def create_access_token(organization_id):
    try:
        data = request.get_json()
        access_rights = data['access_rights']
        project_id = data['project_id']
        valid_till = data['valid_till']
        token_contents = {
            "ACCESS_RIGHTS": access_rights,
            "PROJ_ID": project_id,
            "ORG_ID": organization_id
        }
        if valid_till == "-":
            valid_till = None
        token = get_token_from_object(token_contents, get_site_secret_key(), valid_till)
        return jsonify({"STATUS": "OK", "TOKEN": token})
    except KeyError as e:
        return jsonify({"STATUS": "FAIL", "MSG": "Incomplete Data: " + str(e)})
    except BuglyticsException as e:
        return jsonify({"STATUS": "FAIL", "MSG": str(e)})
    except Exception as e:
        print_exc()
        return jsonify({"STATUS": "FAIL", "MSG": "Server Error"}), 501