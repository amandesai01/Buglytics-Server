from uuid import uuid4
from time import time

from BuglyticsServer.Datastore import organizations as org_db

def create_organization(title):
    organization = {
        "organization_id": str(uuid4()),
        "title": title,
        "created_ts": str(int(time()))
    }
    org_db.insert_organization(organization)
    organization['total_projects'] = 0
    return organization

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