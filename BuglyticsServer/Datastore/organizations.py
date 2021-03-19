from BuglyticsServer.properties import get_pg_connection

QUERY_INSERT_ORGANIZATION = "INSERT INTO organizations(organization_id, title, created_ts, secret_key, organization_email) VALUES (%s, %s, %s, %s, %s)"

QUERY_SELECT_ORGANIZATION = "SELECT title, created_ts FROM organizations WHERE organization_id = %s"

QUERY_SELECT_PROJECT_COUNT_ORGANIZATION = "SELECT COUNT(project_id) FROM projects WHERE organization_is = %s"

db = get_pg_connection()

def insert_organization(organization):
    values = (organization['organization_id'], organization['title'], organization['created_ts'], organization['secret'], organization['email'])
    with db:
        with db.cursor() as cursor:
            cursor.execute(QUERY_INSERT_ORGANIZATION, values)

def select_organization(organization_id):
    values = (organization_id,)
    with db:
        with db.cursor() as cursor:
            cursor.execute(QUERY_SELECT_ORGANIZATION, values)

def select_organization_project_count(organization_id):
    values = (organization_id,)
    with db:
        with db.cursor() as cursor:
            cursor.execute(QUERY_SELECT_PROJECT_COUNT_ORGANIZATION, values)
