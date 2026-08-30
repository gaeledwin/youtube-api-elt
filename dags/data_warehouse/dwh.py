from data_warehouse.data_utils import get_conn_cursor, close_conn_cursor, create_schema, create_table, get_videos_ids
from data_warehouse.data_load import load_data
from data_warehouse.data_modification import insert_row, update_row, delete_row
from data_warehouse.data_transformation import transform_data
from airflow.decorators import task
import logging

logger = logging.getLogger(__name__)
table = 'api_elt'

@task
def staging_table():
    schema = "staging"
    conn, cur = None, None
    try:
        conn, cur = get_conn_cursor()
        create_schema(schema)
        create_table(schema)
        video_ids = get_videos_ids(cur, schema)
        yt_data = load_data()
        for row in yt_data:
            if len(video_ids) == 0:
                insert_row(cur, conn, schema, row)
            else:
                if row['video_id'] in video_ids:
                    update_row(cur, conn, schema, row)
                else:
                    insert_row(cur, conn, schema, row)
            ids_in_json = {row['video_id'] for row in yt_data}
            ids_to_delete = set(video_ids) - ids_in_json
            if ids_to_delete:
                delete_row(conn, cur, schema, ids_to_delete)
            logger.info(f"{schema} table update row completed... ")
    except Exception as e:
        logger.error(f"An error occured during the update of {schema} table: {e} ")
        raise e
    finally:
        if conn and cur:
            close_conn_cursor(conn, cur)

@task
def core_table():
    schema = "core"
    conn, cur = None, None
    try:
        conn, cur = get_conn_cursor()
        create_schema(schema)
        create_table(schema)
        table_ids = get_videos_ids(cur, schema)
        current_video_ids = set()
        cur.execute(f"SELECT * FROM staging.{table}")
        rows = cur.fetchall()
        for row in rows:
            current_video_ids.add(row['Video_Id'])
            if len(table_ids) == 0:
                transform_row = transform_data(row)
                insert_row(cur, conn, schema, transform_row)
            else:
                transform_row = transform_data(row)
                if transform_row['Video_Id'] in table_ids:
                    update_row(cur, conn, schema, transform_row)
                else:
                    insert_row(cur, conn, schema, transform_row)
        ids_to_delete = set(table_ids) - current_video_ids
        if ids_to_delete:
            delete_row(conn, cur, schema, ids_to_delete)
        logger.info(f"{schema} table update row completed... ")
    except Exception as e:
        logger.error(f"An error occured during the update of {schema} table: {e} ")
        raise e
    finally:
        if conn and cur:
            close_conn_cursor(conn, cur)
        
        