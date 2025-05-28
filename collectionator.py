import os
import weaviate
from weaviate.classes.init import Auth
from weaviate.agents.query import QueryAgent
import csv

os.environ["WEAVIATE_URL"] = "<YOUR_SECRET_VALUE>"
os.environ['WEAVIATE_API_KEY'] = '<YOUR_SECRET_VALUE>'
os.environ[
    'YOUR_INFERENCE_PROVIDER_KEY'] = "<YOUR_SECRET_VALUE>"

headers = {
    # Provide your required API key(s), e.g. Cohere, OpenAI, etc. for the configured vectorizer(s)
    "X-INFERENCE-PROVIDER-API-KEY": os.environ.get("YOUR_INFERENCE_PROVIDER_KEY", ""),
}

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=os.environ.get("WEAVIATE_URL"),
    auth_credentials=Auth.api_key(os.environ.get("WEAVIATE_API_KEY")),
    headers=headers,
)

data_rows = []
with open("GlobalLandTemperaturesByMajorCity.csv", "r") as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        data_rows.append(row)

collection = client.collections.get("GlobalLandTemperaturesByMajorCity")

with collection.batch.fixed_size(batch_size=200) as batch:
    for data_row in data_rows:
        batch.add_object(
            properties=data_row,
        )
        if batch.number_errors > 10:
            print("Batch import stopped due to excessive errors.")
            break

failed_objects = collection.batch.failed_objects
if failed_objects:
    print(f"Number of failed imports: {len(failed_objects)}")
    print(f"First failed object: {failed_objects[0]}")
