from abc import ABC, abstractmethod
from typing import Literal
from pydantic import BaseModel
from typing import Type
from models import WebSearchConfig, WebFetchConfig

class prompt(BaseModel):
    role: Literal["user", "assistant", "developer"]
    content: str




class BaseAdapter(ABC):
    def __init__(self, model: str):
        self.model = model

    @abstractmethod
    def generate(
        self,
        prompt: list[prompt],
        system_prompt: str | None = None,
        output_schema: Type[BaseModel] | None = None
    )-> str | BaseModel:
        pass



    @abstractmethod
    def web_search(
        self,
        config: WebSearchConfig,
    ) -> dict:
        pass

    @abstractmethod
    def tool_normalizer(
        self,
        tools: list,
    ) -> list[dict]:
        pass