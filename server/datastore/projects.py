from server.properties import get_pg_connection

QUERY_INSERT_PROJECT = "INSERT INTO projects(project_id, organization_id, title, details, created_ts) VALUES (%s, %s, %s, %s, %s)"

QUERY_GET_ALL_PROJECTS = "SELECT * FROM \
        (SELECT project_id, title, details, created_ts FROM projects WHERE organization_id = %s) t1 \
        INNER JOIN \
        (SELECT project_id, COUNT(bug_id) as bug_count FROM bugs AS bugs GROUP BY project_id) t2 \
        ON t1.project_id = t2.project_id"

QUERY_GET_SPECIFIC_PROJECT = "SELECT * FROM \
        (SELECT project_id, title, details, created_ts FROM projects WHERE project_id = %s AND organization_id = %s) t1 \
        INNER JOIN \
        (SELECT project_id, COUNT(bug_id) as bug_count FROM bugs AS bugs GROUP BY project_id) t2 \
        ON t1.project_id = t2.project_id"

db = get_pg_connection()

def insert_project(project, organization_id):
    values = (project['project_id'], organization_id, project['title'], project['details'], project['created_ts'])
    with db:
        with db.cursor() as cursor:
            cursor.execute(QUERY_INSERT_PROJECT, values)

def select_all_projects(organization_id):
    values = (organization_id,)
    with db:
        with db.cursor() as cursor:
            cursor.execute(QUERY_GET_ALL_PROJECTS, values)
            return cursor.fetchall()

def select_specific_project(project_id, organization_id):
    values = (project_id, organization_id)
    with db:
        with db.cursor() as cursor:
            cursor.execute(QUERY_GET_SPECIFIC_PROJECT, values)
            return cursor.fetchone()
