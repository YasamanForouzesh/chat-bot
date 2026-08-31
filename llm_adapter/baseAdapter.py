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