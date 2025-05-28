from weaviate.agents.classes import Operations

import os
import weaviate
from weaviate.classes.init import Auth
from weaviate.agents.query import QueryAgent
from weaviate.collections.classes.config import DataType
from weaviate_agents.transformation import TransformationAgent

os.environ["WEAVIATE_URL"] = "<YOUR_SECRET_VALUE>"
os.environ['WEAVIATE_API_KEY'] = "<YOUR_SECRET_VALUE>"
os.environ[
    "X-INFERENCE-PROVIDER-API-KEY"] = "<YOUR_SECRET_VALUE>"

headers = {
    # Provide your required API key(s), e.g. Cohere, OpenAI, etc. for the configured vectorizer(s)
    "X-INFERENCE-PROVIDER-API-KEY": os.environ.get("X-INFERENCE-PROVIDER-API-KEY", ""),
}

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=os.environ.get("WEAVIATE_URL"),
    auth_credentials=Auth.api_key(os.environ.get("WEAVIATE_API_KEY")),
    headers=headers,
)
add_fahrenheit_conversion = Operations.append_property(
    property_name="fahrenheit_transformation",
    data_type=DataType.TEXT_ARRAY,
    view_properties=["LandAverageTemperature"],
    instruction="""There are temperatures given in Celsius in the column LandAverageTemperature. Find the equivalent Fahrenheit temperature""",
)

agent = TransformationAgent(
    client=client,
    collection="GlobalTemperatures",
    operations=[add_fahrenheit_conversion],
)

response = agent.update_all()  # The response is a TransformationResponse object

agent.get_status(workflow_id=response.workflow_id)  # Use the workflow_id to check the status of each workflow
