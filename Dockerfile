FROM quay.io/astronomer/astro-runtime:12.6.0

WORKDIR "/usr/local/airflow"

RUN python -m venv /usr/local/airflow/dbt_venv && \
    /usr/local/airflow/dbt_venv/bin/pip install --no-cache-dir dbt-snowflake

ENV DBT_BIN="/usr/local/airflow/dbt_venv/bin/dbt"
