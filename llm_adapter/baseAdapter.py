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

    @abstractmethod
    def agent(
        self,
        prompt: list[m.prompt | m.ToolCall | m.ToolResult],
        system_prompt: str | None = None,
        output_schema: Type[BaseModel] | None = None,
        tools: list[m.Tool | dict] | None = None,
    ) -> str | BaseModel:
        pass
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