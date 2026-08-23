from llm_adapter.helper import llmFactory
from dotenv import load_dotenv
load_dotenv()
def chat():
    llm = llmFactory("gpt-4.1-nano", "openai")
    rsp = llm.generate("hello tell one small and quick joke for who immigrate from Iran to USA to undrestand LA culcutre.")
    return rsp


def main():
    print(chat())



if __name__ == "__main__":
    main()
