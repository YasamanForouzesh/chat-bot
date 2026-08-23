from .baseAdapter import BaseAdapter
from openai import OpenAI


class OpenAIAdapter(BaseAdapter):
    def __init__(self, model: str):
        super().__init__(model)
        self.client = OpenAI()

    def generate(
        self,
        prompt: str,
        system_prompt: str | None = None
    ):
        messages = []

        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })

        messages.append({
            "role": "user",
            "content": prompt
        })

        response = self.client.responses.create(
            model=self.model,
            input=messages,
        )

        return response.output_text