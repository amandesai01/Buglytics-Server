from uuid import uuid4

from server.datastore import webhooks as webhk_db

def create_webhook(project_id, target_url, bug_level):
    webhook = {
        "webhook_id": str(uuid4()),
        "project_id": project_id,
        "target_url": target_url,
        "bug_level": bug_level
    }
    webhk_db.insert_webhook(webhook['webhook_id'], project_id, target_url, bug_level)
    return webhook

def get_all_webhooks(project_id):
    data_raw = webhk_db.select_all_webhooks_from_project(project_id)
    data = []
    for webh_raw in data_raw:
        data.append({
            "webhook_id": webh_raw[0],
            "target_url": webh_raw[1],
            "bug_level": webh_raw[2]
        })
    return data

def delete_webhook(webhook_id, project_id):
    webhk_db.delete_webhook(webhook_id, project_id)