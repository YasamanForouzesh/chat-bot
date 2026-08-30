from llm_adapter.helper import llmFactory
from llm_adapter.baseAdapter import prompt
from dotenv import load_dotenv
from prompt_loader import prompt_loader
from tools import get_weather

load_dotenv()


def chat():
    systemPrompt = prompt_loader("backend", "v1")
    llm = llmFactory("gpt-4.1-nano", "openai")
    rsp = llm.generate([
        prompt(
            role="user",
            content="I have trip to la in two days what type of clothes should I take ?"
        )
    ], systemPrompt, tools=[get_weather])
   
    return rsp


def main():
    print(chat())


if __name__ == "__main__":
    main()
