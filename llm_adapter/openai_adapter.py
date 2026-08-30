from .baseAdapter import BaseAdapter, prompt
from openai import OpenAI
from pydantic import BaseModel
from typing import Type
from models import Tool

class OpenAIAdapter(BaseAdapter):
    def __init__(self, model: str):
        super().__init__(model)
        self.client = OpenAI()

    @staticmethod
    def validate_messages(messages: list[prompt]) -> list[prompt]:
        allowed_roles = {"user", "assistant", "developer"}

        if not messages:
            raise ValueError("At least one message is required.")

        for index, message in enumerate(messages):
            if message.role not in allowed_roles:
                raise ValueError(
                    f"Invalid role '{message.role}' at index {index}. "
                    "OpenAI supports: user, assistant, developer."
                )

            if index == 0 and message.role == "assistant":
                raise ValueError("The first OpenAI message cannot be from assistant.")

        return messages

    @staticmethod
    def tool_normalizer(tools:list)-> list[dict]:
        normalized = []
        for tool in tools:
            if isinstance(tool,Tool):
                normalized.append({
                    "type": "function",
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters,
                    "strict": tool.strict,
                })
            elif isinstance(tool, dict):
                normalized.append(tool)

            else:
                raise TypeError(f"Unsupported tool type: {type(tool)}")

        return normalized


    
    def generate(
        self,
        prompt: list[prompt],
        system_prompt: str | None = None,
        output_schema: Type[BaseModel] | None = None,
        tools: list[dict] | None = None
    )-> str | BaseModel:
        validated_messages = self.validate_messages(prompt)
        messages = [p.model_dump() for p in validated_messages]

        if system_prompt:
            messages.insert(0, {
                "role": "system",
                "content": system_prompt,
            })
        
        request_args = {
                    "model": self.model,
                    "input": messages,
                }
        if tools:
            request_args["tools"] = tools

        if not output_schema:
            response = self.client.responses.create(**request_args)
            print(response)
            return response.output_text
        else: 
            request_args["text_format"]= output_schema
            response = self.client.responses.parse(**request_args)
            print(response)
            return response.output_parsed
