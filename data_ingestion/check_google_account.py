from google.cloud import storage
from google.auth.exceptions import DefaultCredentialsError

try:
    # Instantiate the client, which should trigger authentication using the credentials file
    client = storage.Client()
    # List buckets to confirm access
    buckets = list(client.list_buckets())
    print("Successfully authenticated. Accessible buckets:", [bucket.name for bucket in buckets])
except DefaultCredentialsError as e:
    print("Authentication failed. Check credentials file path:", e)
except Exception as ex:
    print("An error occurred:", ex)