from llm_adapter.helper import llmFactory
from llm_adapter.baseAdapter import prompt
from dotenv import load_dotenv

load_dotenv()


def chat():
    llm = llmFactory("gpt-4.1-nano", "openai")
    rsp = llm.generate([
        prompt(
            role="user",
            content="hello tell one small and quick joke for someone who immigrated from Iran to the USA and wants to understand LA culture."
        )
    ])
    return rsp


def main():
    print(chat())


if __name__ == "__main__":
    main()
