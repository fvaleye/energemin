import vertexai

from vertexai.generative_models import GenerativeModel
from vertexai.generative_models import Tool
from vertexai.generative_models import grounding


def config_vertex_ai():
    """
    Configure the Vertex AI project and location
    """
    vertexai.init(location="us-central1")

async def call_vertex_ai_gemini(prompt :str, model_name: str = "gemini-1.5-pro-002"):
    """
    Call the Vertex AI Gemini model

    Args:
        prompt (str): The prompt to send to the model
        model_name (str): The name of the model to use

    Returns:
        str: The response from the model
    """
    config_vertex_ai()

    generation_config = {
        "max_output_tokens": 8192,
        "temperature": 1,
        "top_p": 0.95,
    }
    model = GenerativeModel(
        model_name,
    )

    responses = model.generate_content(
        [prompt],
        generation_config=generation_config,
        tools=[Tool.from_google_search_retrieval(
        google_search_retrieval=grounding.GoogleSearchRetrieval())],
        stream=True,
    )

    for response in responses:
        yield response.text
