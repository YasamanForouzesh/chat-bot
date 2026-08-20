from .anthropic import Anthropic
from .openai_adapter import OpenAIAdapter


def llm_helper(model: str, provider: str):
    if provider == "anthropic":
        return Anthropic(model)
    if provider == "openai":
        return OpenAIAdapter(model)
    raise ValueError("Unknown provider")