from llm_adapter.helper import llm_helper
from dotenv import load_dotenv
load_dotenv()
def chat():
    llm = llm_helper("gpt-4.1-nano", "openai")
    rsp = llm.generate("hello tell one small and quick joke for who immigrate from Iran to USA to undrestand LA culcutre.")
    return rsp.output_text


def main():
    print(chat())



if __name__ == "__main__":
    main()
