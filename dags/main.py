from airflow import DAG
from datetime import datetime, timedelta
import pendulum
from api.videos_api import get_playlist_id, get_videos_ids, extract_data_videos, save_to_json
from data_warehouse.dwh import staging_table, core_table
from data_quality.soda import elt_api_data_quality

locale_tz = pendulum.timezone('Indian/Antananarivo')
schema_staging =  "staging"
schema_core = "core"

default_args = {
    "owner": "dataengineers",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "gaeldewin@gmail.com",
    "max_active_runs": 1,
    "dagrun_timeout": timedelta(hours=1),
    "start_date": datetime(2026, 1, 1, tzinfo=locale_tz)
}

with DAG (
    dag_id = "produce.json",
    default_args = default_args,
    description = "Orchestration data pipeline",
    schedule="0 14 * * *",
    catchup=False
    ) as dag:
    
    playlist_id = get_playlist_id()
    videos_ids = get_videos_ids(playlist_id)
    extracted_data = extract_data_videos(videos_ids)
    save_to_json_task = save_to_json(extracted_data)
    
    playlist_id >> videos_ids >> extracted_data >> save_to_json_task
    
    with DAG (
    dag_id = "update_db",
    default_args = default_args,
    description = "update database",
    schedule="0 15 * * *",
    catchup=False
    ) as dag:
    
        #define task 
        update_staging = staging_table()
        update_core = core_table()
        
        #define dependencies
        update_staging >> update_core
        
    with DAG (
    dag_id = "soda_test",
    default_args = default_args,
    description = "test data quality",
    schedule="0 15 * * *",
    catchup=False
    ) as dag:
    
        #define task 
        data_test_staging_schema = elt_api_data_quality(schema_staging)
        data_test_core_schema = elt_api_data_quality(schema_core)
        
        #define dependencies
        data_test_staging_schema >> data_test_core_schema
    