from langchain.chat_models import init_chat_model

def get_llm(model_id="gemini-2.5-flash-preview-05-20", model_provider="google_vertexai", **kwargs):
    """
    Returns an initialized LLM object.
    You can pass model_id, provider, and any additional keyword arguments.
    """
    return init_chat_model(model=model_id, model_provider=model_provider, **kwargs)
