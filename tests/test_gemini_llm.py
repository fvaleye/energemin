import pytest
from unittest.mock import patch, MagicMock
import asyncio

from src.gemini_llm import call_vertex_ai_gemini, config_vertex_ai

@pytest.fixture
def mock_vertex_response():
    mock_response = MagicMock()
    mock_response.text = "This is a test response"
    return [mock_response]

@pytest.fixture
def mock_generative_model():
    with patch('src.gemini_llm.GenerativeModel') as mock:
        model_instance = MagicMock()
        mock.return_value = model_instance
        yield mock

@pytest.fixture
def mock_vertexai():
    with patch('src.gemini_llm.vertexai') as mock:
        yield mock

def test_config_vertex_ai(mock_vertexai):
    config_vertex_ai()
    mock_vertexai.init.assert_called_once_with(location="us-central1")

@pytest.mark.asyncio
async def test_call_vertex_ai_gemini_default_model(mock_generative_model, mock_vertex_response):
    model_instance = mock_generative_model.return_value
    model_instance.generate_content.return_value = mock_vertex_response

    responses = []
    async for response in call_vertex_ai_gemini("Test prompt"):
        responses.append(response)

    assert responses == ["This is a test response"]
    mock_generative_model.assert_called_once_with("gemini-1.5-pro-002")
    
@pytest.mark.asyncio
async def test_call_vertex_ai_gemini_custom_model(mock_generative_model, mock_vertex_response):
    model_instance = mock_generative_model.return_value
    model_instance.generate_content.return_value = mock_vertex_response

    responses = []
    async for response in call_vertex_ai_gemini("Test prompt", model_name="custom-model"):
        responses.append(response)

    assert responses == ["This is a test response"]
    mock_generative_model.assert_called_once_with("custom-model")

@pytest.mark.asyncio
async def test_call_vertex_ai_gemini_generation_config(mock_generative_model, mock_vertex_response):
    model_instance = mock_generative_model.return_value
    model_instance.generate_content.return_value = mock_vertex_response

    expected_config = {
        "max_output_tokens": 8192,
        "temperature": 1,
        "top_p": 0.95,
    }

    async for _ in call_vertex_ai_gemini("Test prompt"):
        pass

    # Verify the generation config was passed correctly
    call_kwargs = model_instance.generate_content.call_args[1]
    assert call_kwargs["generation_config"] == expected_config
    assert call_kwargs["stream"] is True

@pytest.mark.asyncio
async def test_call_vertex_ai_gemini_multiple_responses(mock_generative_model):
    model_instance = mock_generative_model.return_value
    
    # Create multiple mock responses
    mock_responses = [
        MagicMock(text="Response 1"),
        MagicMock(text="Response 2"),
        MagicMock(text="Response 3"),
    ]
    model_instance.generate_content.return_value = mock_responses

    responses = []
    async for response in call_vertex_ai_gemini("Test prompt"):
        responses.append(response)

    assert responses == ["Response 1", "Response 2", "Response 3"]