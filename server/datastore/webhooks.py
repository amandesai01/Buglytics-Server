from server.properties import get_pg_connection

QUERY_INSERT_WEBHOOK = "INSERT INTO webhooks(webhook_id, project_id, target_url, bug_level) VALUES (%s, %s, %s, %s)"

QUERY_SELECT_ALL_WEBHOOKS_FOR_PROJECT = "SELECT webhook_id, target_url, bug_level FROM webhooks WHERE project_id = %s"

QUERY_DELETE_WEBHOOK = "DELETE FROM webhooks WHERE webhook_id = %s AND project_id = %s"

QUERY_GET_TARGET_URL = "SELECT target_url FROM webhooks WHERE bug_level <= %s AND project_id = %s ORDER BY bug_level DESC"

db = get_pg_connection()

def insert_webhook(webhook_id, project_id, target_url, bug_level):
    values = (webhook_id, project_id, target_url, bug_level)
    with db:
        with db.cursor() as cursor:
            cursor.execute(QUERY_INSERT_WEBHOOK, values)

def select_all_webhooks_from_project(project_id):
    values = (project_id,)
    with db:
        with db.cursor() as cursor:
            cursor.execute(QUERY_SELECT_ALL_WEBHOOKS_FOR_PROJECT, values)
            return cursor.fetchall()

def delete_webhook(webhook_id, project_id):
    values = (webhook_id, project_id)
    with db:
        with db.cursor() as cursor:
            cursor.execute(QUERY_DELETE_WEBHOOK, values)

def get_target_url_for_bug_level_project_id(bug_level, project_id):
    values = (bug_level, project_id)
    with db:
        with db.cursor() as cursor:
            cursor.execute(QUERY_GET_TARGET_URL, values)
            return cursor.fetchone()