from uuid import uuid4
from time import time

from server.datastore import bugs as bugs_db
from server.exceptions import NoProjectUnderOrganisationException, UnidentifiedException

def create_bug(project_id, bug_level, bug_location, bug_text, organization_id):
    bug = {
        "bug_id": str(uuid4()),
        "project_id": project_id,
        "bug_level": bug_level,
        "bug_location": bug_location,
        "bug_text": bug_text,
        "ts": str(int(time()))
    }
    check = bugs_db.insert_bug(bug, organization_id)
    if check[0]:
        return bug
    else:
        if check[1] == "NO_PROJ_UNDER_ORG":
            raise NoProjectUnderOrganisationException
        else:
            raise UnidentifiedException

def get_all_bugs(project_id, organization_id):
    data_raw = bugs_db.select_all_bugs(project_id, organization_id)
    data = []
    for bug_raw in data_raw:
        data.append({
            "bug_id": bug_raw[0],
            "bug_level": bug_raw[1],
            "bug_location": bug_raw[2],
            "ts": bug_raw[3]
        })
    return data

def get_specific_bug(bug_id, organization_id):
    bug_raw = bugs_db.select_specific_bug(bug_id, organization_id)
    bug = {
            "bug_id": bug_raw[0],
            "bug_level": bug_raw[1],
            "bug_location": bug_raw[2],
            "bug_text": bug_raw[3],
            "ts": bug_raw[4]
        }
    return bug
