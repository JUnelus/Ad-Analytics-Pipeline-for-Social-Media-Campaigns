# Configure the Google Cloud provider
provider "google" {
  project = "partner-data-pipeline"  # Replace with your GCP project ID
  region  = "us-central1"      # Set your preferred region
}

# Create a BigQuery dataset
resource "google_bigquery_dataset" "reddit_dataset" {
  dataset_id = "reddit_dataset"  # Replace with your dataset ID
  location   = "US"
}

# Create a BigQuery table within the dataset
resource "google_bigquery_table" "reddit_table" {
  dataset_id = google_bigquery_dataset.reddit_dataset.dataset_id
  table_id   = "reddit_table"
  schema     = <<EOF
[
  {
    "name": "title",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "score",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "comments",
    "type": "INTEGER",
    "mode": "NULLABLE"
  }
]
EOF
}

# Create a Google Cloud Storage bucket
resource "google_storage_bucket" "reddit_data_bucket" {
  name     = "social-media-campaigns2-bucket"  # Replace with a unique bucket name
  location = "US"
}

# Grant BigQuery Data Editor and Storage Object Viewer roles to a service account
resource "google_project_iam_member" "service_account_bigquery" {
  project = "partner-data-pipeline"
  role    = "roles/bigquery.dataEditor"
  member  = "serviceAccount:5817495091-compute@developer.gserviceaccount.com"
}

resource "google_project_iam_member" "service_account_storage" {
  project = "partner-data-pipeline"
  role    = "roles/storage.objectViewer"
  member  = "serviceAccount:5817495091-compute@developer.gserviceaccount.com"
}
