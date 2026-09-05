from llm_adapter.helper import llmFactory
from dotenv import load_dotenv
from prompt_loader import prompt_loader
from tools import get_weather
from models import Prompt
load_dotenv()


def chat():
    system_prompt = prompt_loader("backend", "v1")
    llm = llmFactory("gpt-4.1-nano", "openai")

    messages = [
        Prompt(
            role="user",
            content="I have a trip to LA in two days. What type of clothes should I take?"
        )
    ]

    rsp = llm.agent(
        messages,
        system_prompt,
        tools=[get_weather]
    )


    return rsp


def main():
    print(chat())


if __name__ == "__main__":
    main()
