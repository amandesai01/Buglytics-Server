from server.properties import get_pg_connection

QUERY_INSERT_BUG_INFO = "INSERT INTO bugs(bug_id, project_id, bug_level, bug_location, bug_text, bug_type, ts) \
                            VALUES (%s, %s, %s, %s, %s, %s, %s)"

QUERY_COUNT_PROJECT_ID_FOR_ORGANIZATION = "SELECT COUNT(project_id) FROM projects WHERE organization_id = %s AND project_id = %s"

# Subqueries to make sure only correct organisation can access it.

QUERY_GET_ALL_BUGS = "SELECT bug_id, bug_level, bug_location, bug_text, bug_type, ts FROM bugs WHERE project_id IN \
                        (SELECT project_id FROM projects WHERE organization_id = %s AND project_id = %s)"

QUERY_GET_SPECIFIC_BUG = "SELECT bug_id, bug_level, bug_location, bug_text, bug_type, ts FROM bugs WHERE bug_id = %s AND \
                            project_id IN (SELECT project_id FROM projects WHERE organization_id = %s)"

db = get_pg_connection()

def insert_bug(bug, organization_id):
    project_id_organization_tuple = (organization_id, bug['project_id'])
    bug_tuple = (bug['bug_id'], bug['project_id'], bug['bug_level'], bug['bug_location'], bug['bug_text'], bug['bug_type'], bug['ts'])
    with db:
        with db.cursor() as cursor:
            cursor.execute(QUERY_COUNT_PROJECT_ID_FOR_ORGANIZATION, project_id_organization_tuple)
            counts = cursor.fetchone()
            if counts[0] == 1:
                cursor.execute(QUERY_INSERT_BUG_INFO, bug_tuple)
                return True, None
            else:
                return False, "NO_PROJ_UNDER_ORG"
    return False, "CONN_NOT_ESTABLISHED"

def select_all_bugs(project_id, organization_id):
    values = (organization_id, project_id)
    with db:
        with db.cursor() as cursor:
            cursor.execute(QUERY_GET_ALL_BUGS, values)
            return cursor.fetchall()

def select_specific_bug(bug_id, organization_id):
    values = (bug_id, organization_id)
    with db:
        with db.cursor() as cursor:
            cursor.execute(QUERY_GET_SPECIFIC_BUG, values)
            return cursor.fetchone()
