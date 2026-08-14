from airflow.providers.postgres.hooks.postgres import PostgresHook
from psycopg2.extras import RealDictCursor

table = 'api_elt'

def get_conn_cursor():
    hook = PostgresHook(postgres_conn_id="postgres_db_yt_elt", database='elt_db')
    conn = hook.get_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    return conn, cur

def close_conn_cursor(conn, cur):
    cur.close()
    conn.close()
    
def create_schema(schema):
    conn, cur = get_conn_cursor()
    request = f"CREATE SCHEMA IF NOT EXISTS {schema};"
    cur.execute(request)
    conn.commit()
    close_conn_cursor(conn, cur)
    
def create_table(schema):
    conn, cur = get_conn_cursor()
    
    if schema == "staging":
        cur.execute(f"""CREATE TABLE IF NOT EXISTS {schema}.{table}(
        "Video_Id" VARCHAR(12) PRIMARY KEY NOT NULL,
        "Video_Title" TEXT NOT NULL,
        "Uploads_Date" TIMESTAMP NOT NULL,
        "Duration" VARCHAR(12) NOT NULL,
        "View_Count" INT,
        "Like_Count" INT,
        "Comment_Count" INT
    );
    """)
    else:
        cur.execute(f"""CREATE TABLE IF NOT EXISTS {schema}.{table}(
        "Video_Id" VARCHAR(12) PRIMARY KEY NOT NULL,
        "Video_Title" TEXT NOT NULL,
        "Uploads_Date" TIMESTAMP NOT NULL,
        "Duration" VARCHAR(12) NOT NULL,
        "View_Count" INT,
        "Like_Count" INT,
        "Comment_Count" INT,
        "Type" VARCHAR(10)
    );
    """)
    conn.commit()
    close_conn_cursor(conn, cur)
    
def get_videos_ids(cur, schema):
    request = f"""
        SELECT "Video_Id" FROM {schema}.{table};
    """
    cur.execute(request)
    ids = cur.fetchall()
    videos_ids = [row['Video_Id'] for row in ids]
    return videos_ids