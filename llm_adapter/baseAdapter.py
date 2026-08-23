from abc import ABC, abstractmethod


class BaseAdapter(ABC):
    def __init__(self, model: str):
        self.model = model

    @abstractmethod
    def generate(
        self,
        prompt: str,
        system_prompt: str | None = None
    ):
        pass