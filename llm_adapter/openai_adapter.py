from .baseAdapter import BaseAdapter
from openai import OpenAI


class OpenAIAdapter(BaseAdapter):
    def __init__(self, model: str):
        super().__init__(model)
        self.client = OpenAI()

    def generate(self, prompt):
        response = self.client.responses.create(
            model=self.model,
            input=prompt,
        )

        return response