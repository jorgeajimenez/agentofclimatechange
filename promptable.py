import os
import weaviate
from weaviate.classes.init import Auth
from weaviate.agents.query import QueryAgent

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

# Instantiate a new agent object
qa = QueryAgent(
    client=client, collections=["GlobalTemperatures"]
)

query_response = qa.run('is LandAverageTemperature increasing over time?')

print(query_response)
