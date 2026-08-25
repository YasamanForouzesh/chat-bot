from abc import ABC, abstractmethod
from typing import Literal
from pydantic import BaseModel


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

