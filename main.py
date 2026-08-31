from llm_adapter.helper import llmFactory
from dotenv import load_dotenv
from prompt_loader import prompt_loader
from tools import get_weather
from models import ToolResult, prompt
load_dotenv()


def chat():
    system_prompt = prompt_loader("backend", "v1")
    llm = llmFactory("gpt-4.1-nano", "openai")

    messages = [
        prompt(
            role="user",
            content="I have a trip to LA in two days. What type of clothes should I take?"
        )
    ]

    rsp = llm.generate(
        messages,
        system_prompt,
        tools=[get_weather]
    )

    messages.extend(rsp.tool_calls)

    for tool_call in rsp.tool_calls:
        if tool_call.name == "get_weather":
            tool_resp = get_weather(**tool_call.arguments)

            messages.append(
                ToolResult(
                    call_id=tool_call.id,
                    result=tool_resp
                )
            )

    rsp = llm.generate(
        messages,
        system_prompt,
        tools=[get_weather]
    )

    return rsp


def main():
    print(chat())


if __name__ == "__main__":
    main()
