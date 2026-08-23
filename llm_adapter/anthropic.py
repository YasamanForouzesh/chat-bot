from .baseAdapter import BaseAdapter
import anthropic


class Anthropic(BaseAdapter):
    def __init__(self, model: str):
        super().__init__(model)
        self.client = anthropic.Anthropic()

    def generate(self, prompt: str, system_prompt):
        message = self.client.messages.create(
            model=self.model,
            messages=prompt,
        )
        return response.content[0].text