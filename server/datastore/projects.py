from server.properties import get_pg_connection

QUERY_INSERT_PROJECT = "INSERT INTO projects(project_id, organization_id, title, details, created_ts) VALUES (%s, %s, %s, %s, %s)"

QUERY_GET_ALL_PROJECTS = "SELECT (project_id, title, details, created_ts, bug_count) FROM projects WHERE organization_id = %s INNER JOIN \
                        (SELECT project_id, COUNT(bug_id) FROM bugs GROUP BY project_id) \
                        ON projects.project_id = bugs.project_id"

QUERY_GET_SPECIFIC_PROJECT = "SELECT (project_id, title, details, created_ts, bug_count) FROM projects WHERE project_id = %s AND organization_id = %s INNER JOIN \
                        (SELECT project_id, COUNT(bug_id) FROM bugs) \
                        ON projects.project_id = bugs.project_id"

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
