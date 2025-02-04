from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
import os
from cosmos import DbtDag, ProjectConfig, ProfileConfig, RenderConfig, LoadMode
from pathlib import Path
from cosmos.profiles import SnowflakeUserPasswordProfileMapping

# Default DBT root path
DEFAULT_DBT_ROOT_PATH = Path(__file__).parent.parent / "dags" / "dbt" / "my_project"

# DBT root path from environment variable or default
DBT_ROOT_PATH = Path(os.getenv("DBT_ROOT_PATH", DEFAULT_DBT_ROOT_PATH))

# Profile configuration for the DBT project
profile_config = ProfileConfig(
    profile_name="my_project",
    target_name="demo",
    profile_mapping=SnowflakeUserPasswordProfileMapping(
        conn_id="snowflake_conn_prod"
    )
)

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 5, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1
}

# Define the DBT task
hello_task = DbtDag(
    project_config=ProjectConfig(DBT_ROOT_PATH),
    operator_args={"install_deps": True},
    profile_config=profile_config,
    start_date=datetime(2023, 9, 10),
    dag_id="dbt_snowflake_dag",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
    render_config=RenderConfig(
        selector="only_mart",  # this selector must be defined in your dbt project
        load_method=LoadMode.DBT_LS,
    )
)

# Set the task dependencies
hello_task
