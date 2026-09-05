from abc import ABC, abstractmethod
from typing import Literal
from pydantic import BaseModel
from typing import Type
import models as m

class BaseAdapter(ABC):
    def __init__(self, model: str):
        self.model = model

    @abstractmethod
    def generate(
        self,
        prompt: list[m.prompt | m.ToolResult],
        system_prompt: str | None = None,
        output_schema: Type[BaseModel] | None = None,
        tools: list[m.Tool | dict] | None = None
    )-> m.LLMResponse:
        pass

    def agent(
        self,
        prompt: list[m.prompt | m.ToolCall | m.ToolResult],
        system_prompt: str | None = None,
        output_schema: Type[BaseModel] | None = None,
        tools: list[m.Tool | dict] | None = None,
    ) -> str | BaseModel:

        while True:
            response = self.generate(
                prompt=prompt,
                system_prompt=system_prompt,
                output_schema=output_schema,
                tools=tools,
            )

            # no tool calls -> final answer
            if not response.tool_calls:
                return response.parsed or response.text

            tool_results = []

            for tool_call in response.tool_calls:
                result = self.execute_tool(
                    tool_call=tool_call,
                    tools=tools,
                )

                tool_results.append(result)

            # model needs to see both:
            # what it called + what the tool returned
            prompt.extend(response.tool_calls)
            prompt.extend(tool_results)
    # @abstractmethod
    # def web_search(
    #     self,
    #     config: WebSearchConfig,
    # ) -> dict:
    #     pass

    @staticmethod
    @abstractmethod
    def tool_normalizer(
        tools: list,
    ) -> list[dict]:
        pass


    def execute_tool(
        self,
        tool_call: m.ToolCall,
        tools: list[m.Tool | dict], 
    ) -> m.ToolResult:

        for tool in tools:
            if not isinstance(tool, m.Tool): 
                continue
            if tool_call.name == tool.name:
                result = tool.func(**tool_call.arguments)
                return m.ToolResult(
                    call_id=tool_call.id,
                    name=tool_call.name,
                    result=result
                )
        raise ValueError(
            f"Tool '{tool_call.name}' not found."
        )