from llm_adapter.helper import llmFactory
from llm_adapter.baseAdapter import prompt
from dotenv import load_dotenv
from prompt_loader import prompt_loader
from decorators import tool
from typing import Annotated
from pydantic import Field

load_dotenv()


def chat():
    systemPrompt = prompt_loader("backend", "v1")
    llm = llmFactory("gpt-4.1-nano", "openai")
    rsp = llm.generate([
        prompt(
            role="user",
            content="I have trip to la in two days what type of clothes should I take ?"
        )
    ], systemPrompt, tools=[get_weather.to_dict()])
    # rsp = get_weather("tehran", 3)
    # print(get_weather.to_dict())
    return rsp
@tool()
def get_weather( location: Annotated[
        str,
        Field(description="City and state, e.g. San Francisco, CA")
    ], days: int = 1):
    """Get wather information for a city."""
    return f"Weather for {location} for {days} is hot"

def main():
    print(chat())


if __name__ == "__main__":
    main()
