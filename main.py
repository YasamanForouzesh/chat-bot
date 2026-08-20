from llm_adapter.helper import llm_helper


def chat():
    llm = llm_helper("gpt-4.1-nano", "openai")
    return llm.generate("hello tell one small and quick joke for who immigrate from Iran to USA to undrestand LA culcutre.")


def main():
    print(chat())



if __name__ == "__main__":
    main()
