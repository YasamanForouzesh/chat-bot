from llm_adapter.helper import llmFactory
from llm_adapter.baseAdapter import prompt
from dotenv import load_dotenv
from prompt_loader import promptLoader
load_dotenv()


def chat():
    systemPrompt = promptLoader("v1", "backend")
    llm = llmFactory("gpt-4.1-nano", "openai")
    rsp = llm.generate([
        prompt(
            role="user",
            content="Try to write a function to solve the Fibonacci sequence."
        )
    ], systemPrompt)
    return rsp


def main():
    print(chat())


if __name__ == "__main__":
    main()
