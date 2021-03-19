from flask import request, jsonify
from functools import wraps

from server import utils
from server.properties import get_site_secret_key

def get_decoded_token_from_header(request_header):
    if 'token' in request_header:
        obj = utils.get_object_from_token(request_header['token'], get_site_secret_key())
        return obj

def error_report_access_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            obj = get_decoded_token_from_header(request.headers)
            if "ERR_REPORT" in obj['ACCESS_RIGHTS']:
                return f(obj['PROJ_ID'], obj['ORG_ID'])
            return jsonify({ "STATUS" : "FAIL", "MSG": "Contact Organization Owner to Provide Access." }), 401
        except:
            return jsonify({"STATUS": "FAIL", "MSG": "ERROR IN AUTHENTICATION"}), 401
    return decorated_function

def error_view_access_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            obj = get_decoded_token_from_header(request.headers)
            if "ERR_VIEW" in obj['ACCESS_RIGHTS']:
                return f(obj['PROJ_ID'], obj['ORG_ID'])
            return jsonify({ "STATUS" : "FAIL", "MSG": "Contact Organization Owner to Provide Access." }), 401
        except:
            return jsonify({"STATUS": "FAIL", "MSG": "ERROR IN AUTHENTICATION"}), 401
    return decorated_function