import time
from google.cloud import storage, bigquery
import json

PROJECT_ID = "partner-data-pipeline"  # Replace with your actual project ID

def create_dataset_and_table(dataset_name, table_name):
    bq_client = bigquery.Client(project=PROJECT_ID)

    # Create dataset if it doesn't exist
    dataset_ref = bigquery.Dataset(f"{PROJECT_ID}.{dataset_name}")
    try:
        bq_client.get_dataset(dataset_ref)  # Check if dataset exists
    except Exception:
        bq_client.create_dataset(dataset_ref)
        print(f"Created dataset {dataset_name}")

    # Define schema to match Reddit data fields
    schema = [
        bigquery.SchemaField("title", "STRING"),
        bigquery.SchemaField("score", "INTEGER"),
        bigquery.SchemaField("comments", "INTEGER"),
    ]
    table_ref = bq_client.dataset(dataset_name).table(table_name)
    table = bigquery.Table(table_ref, schema=schema)

    try:
        bq_client.get_table(table)  # Check if table exists
    except Exception:
        bq_client.create_table(table)
        print(f"Created table {table_name}")

    # Wait and confirm table creation
    for attempt in range(5):
        try:
            bq_client.get_table(table_ref)  # Check if table exists
            print(f"Confirmed table {table_name} exists.")
            break
        except Exception:
            print("Waiting for table to be fully created...")
            time.sleep(2)  # Delay before checking again

def load_and_transform_data(file_name, dataset_name, table_name):
    # Ensure dataset and table exist
    create_dataset_and_table(dataset_name, table_name)

    # Fetch data from GCS
    gcs_client = storage.Client()
    bucket = gcs_client.bucket("social-media-campaigns1-bucket")
    blob = bucket.blob(file_name)
    data = json.loads(blob.download_as_text())

    # Print the raw data from the JSON file
    print("Raw data from GCS:", data[:5])  # Print the first 5 items

    # Transform data to match BigQuery schema
    transformed_data = []
    for item in data:
        transformed_entry = {
            "title": item.get("title"),
            "score": item.get("score"),
            "comments": item.get("comments")
        }
        transformed_data.append(transformed_entry)

    # Print the transformed data before loading into BigQuery
    print("Transformed data:", transformed_data[:5])  # Print the first 5 items

    # Load data into BigQuery
    bq_client = bigquery.Client(project=PROJECT_ID)
    table_id = f"{PROJECT_ID}.{dataset_name}.{table_name}"
    bq_client.insert_rows_json(table_id, transformed_data)

if __name__ == "__main__":
    load_and_transform_data("reddit_data.json", "your_dataset", "reddit_table")