from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from data_ingestion.fetch_data_reddit import fetch_reddit_data
from data_transformation.transform_data import load_and_transform_data

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG("ad_analytics_pipeline", default_args=default_args, schedule_interval="0 6 * * *", start_date=datetime(2023, 1, 1)) as dag:
    fetch_reddit = PythonOperator(task_id="fetch_reddit", python_callable=fetch_reddit_data)
    load_data = PythonOperator(task_id="load_data", python_callable=load_and_transform_data,
                               op_kwargs={"file_name": "twitter_data.json", "dataset_name": "your_dataset", "table_name": "twitter_table"})

    fetch_reddit >> load_data
