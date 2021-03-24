import requests
from traceback import print_exc

from server.datastore.webhooks import get_target_url_for_bug_level_project_id

def trigger(projectid, bug):
    try:
        if not bug or not projectid:
            return
        data = get_target_url_for_bug_level_project_id(bug['buglevel'], projectid)
        target_url = None
        if data and len(data) > 0:
            target_url = data[0]
        if not target_url:
            return
        r = requests.post(target_url, json=bug, headers={"Content-Type": "application/json"})
        if r.status_code > 300:
            return False
        return True
    except Exception as e:
        print_exc()
        return
