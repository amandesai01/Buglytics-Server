from BuglyticsServer.properties import get_services_to_deploy, get_site_secret_key

SERVICES = get_services_to_deploy()

if not SERVICES:
    print("No Service to Deploy.")
    raise SystemExit

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = get_site_secret_key()

CORS(app)

if "ERRSERVICE" in SERVICES:
    from BuglyticsServer.Services.error_reporting_service import app as err_service
    app.register_blueprint(err_service)
    print("Registered ERRSERVICE.")

if "AUTHSERVICE" in SERVICES:
    from BuglyticsServer.Services.authentication_service import app as auth_service
    app.register_blueprint(auth_service)
    print("Registered AUTHSERVICE.")

if "DASHSERVICE" in SERVICES:
    from BuglyticsServer.Services.dashboard_service import app as dash_service
    app.register_blueprint(dash_service)
    print("Registered DASHSERVICE.")