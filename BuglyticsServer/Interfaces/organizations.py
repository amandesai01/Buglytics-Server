from uuid import uuid4
from time import time
from hashlib import sha256

from psycopg2 import errors as pgerrors

from BuglyticsServer.Datastore import organizations as org_db
from BuglyticsServer.validations import validate_secret
from BuglyticsServer.exceptions import EmailAlreadyExistsException

def create_organization(title, email, secret):
    try:
        validate_secret(secret)
        organization = {
            "organization_id": str(uuid4()),
            "title": title,
            "created_ts": str(int(time())),
            "secret": sha256(secret.encode('utf-8')).hexdigest(),
            "email": email
        }
        org_db.insert_organization(organization)
        organization['total_projects'] = 0
        return organization
    except pgerrors.UniqueViolation:
        raise EmailAlreadyExistsException

def get_organization_details(organization_id):
    data = org_db.select_organization(organization_id)
    data_project_count = org_db.select_organization_project_count(organization_id)
    organization = {
        "organization_id": organization_id,
        "title": data[0],
        "created_ts": data[1],
        "total_projects": data_project_count[0]
    }
    return organization