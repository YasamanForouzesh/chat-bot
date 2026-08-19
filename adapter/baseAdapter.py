from abc import ABC, abstractmethod


class BaseAdapter(ABC):
    def __init__(self, model):
        self.model = model
    @abstractmethod
    def generate(self, prompt):
        pass