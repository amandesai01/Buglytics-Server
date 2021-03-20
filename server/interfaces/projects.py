from uuid import uuid4
from time import time

from server.datastore import projects as proj_db
from server.exceptions import ProjectNotFoundException

def create_project(title, details, organization_id):
    project = {
        "project_id": str(uuid4()),
        "title": title,
        "details": details,
        "created_ts": str(int(time()))
    }
    proj_db.insert_project(project, organization_id)
    return project

def get_all_projects(organization_id):
    data_raw = proj_db.select_all_projects(organization_id)
    data = []
    for proj_raw in data_raw:
        data.append({
            "project_id": proj_raw[0],
            "title": proj_raw[1],
            "details": proj_raw[2],
            "created_ts": proj_raw[3],
            "bug_count": proj_raw[5]
        })
    return data

def get_selected_project(project_id, organization_id):
    proj_raw = proj_db.select_specific_project(project_id, organization_id)
    if not proj_raw:
        raise ProjectNotFoundException
    project = {
            "project_id": proj_raw[0],
            "title": proj_raw[1],
            "details": proj_raw[2],
            "created_ts": proj_raw[3],
            "bug_count": proj_raw[4]
        }
    return project
