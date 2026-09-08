import logging
from airflow.operators.bash import BashOperator

logger = logging.getLogger(__name__)
SODA_PATH = "/opt/airflow/include/soda"
DATASOURCE = "pg_datasource"

def elt_api_data_quality(schema):
    try:
        task = BashOperator(
            task_id=f"test_data_quality_in_schema_{schema}",
            bash_command=f"soda scan -d {DATASOURCE} -c {SODA_PATH}/configuration.yml -v SCHEMA={schema} {SODA_PATH}/checks.yml"
        )
        return task
    except Exception as e:
        logger.error(f"Error running test data quality in schema {schema}")
        raise e