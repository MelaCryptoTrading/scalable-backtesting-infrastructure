from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 6, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'recapitalize_index_fund',
    default_args=default_args,
    description='A simple DAG to recapitalize the crypto index fund monthly',
    schedule_interval='@monthly',
)

recapitalize_task = SimpleHttpOperator(
    task_id='recapitalize_index',
    method='POST',
    http_conn_id='flask_app',
    endpoint='/index-fund/recapitalize',
    headers={"Content-Type": "application/json"},
    dag=dag,
)
