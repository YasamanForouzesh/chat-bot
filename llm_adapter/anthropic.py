from .baseAdapter import BaseAdapter
import anthropic
from pydantic import BaseModel
from typing import Type
import json
from anthropic import transform_schema
from pydantic import TypeAdapter
import models as m

class Anthropic(BaseAdapter):
    def __init__(self, model: str):
        super().__init__(model)
        self.client = anthropic.Anthropic()

    @staticmethod
    def validate_messages(messages: list[m.prompt]) -> list[m.prompt]:
        allowed_roles = {"user", "assistant"}
        cleaned_messages = []

        if not messages:
            raise ValueError("At least one message is required.")

        for index, message in enumerate(messages):
            if message.role == "developer":
                raise ValueError("Anthropic does not support the developer role.")

            if index == 0 and message.role != "user" :
                 raise ValueError("Anthropic first role has to be user.")
            
            if message.role not in allowed_roles:
                raise ValueError(
                    f"Invalid role '{message.role}' at index {index}. "
                    "Anthropic supports: user, assistant."
                )
            cleaned_messages.append(message)

            if index != 0:
                previous_role = cleaned_messages[index - 1].role
                current_role = cleaned_messages[index].role
                if previous_role == current_role:
                    raise ValueError(
                        "Anthropic message order must alternate between user and assistant."
                    )

        if not cleaned_messages:
            raise ValueError("Anthropic requires at least one user or assistant message.")


        return cleaned_messages


    def generate_schema_config(self, raw_schema: type[BaseModel]):
        

        # Optionally run Anthropic's transformer to fit Claude API constraints
        clean_schema = TypeAdapter(raw_schema).json_schema()
        clean_schema = transform_schema(clean_schema)

        return {
            "format": {
                "type": "json_schema",
                "schema": clean_schema,
            }
        }
    
    def generate(self, prompt: list[m.prompt], system_prompt: str | None = None,
                 output_schema: Type[BaseModel] | None = None)-> str | BaseModel:
        
        validated_messages = self.validate_messages(prompt)
        messages = [p.model_dump() for p in validated_messages]

        request_args = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "messages": messages,
        }

        if system_prompt:
            request_args["system"] = system_prompt


        if output_schema:
          request_args["output_config"] = self.generate_schema_config(output_schema)

        # the create use the output_config which we have to manually format that
        # the parse use output_format that we can pass pydantic 
        # for streaming we should use create
        response = self.client.messages.create(**request_args)

        raw_text = "".join(block.text for block in response.content if block.type == "text")
        if not raw_text:
            return None
        try:
            data = json.loads(raw_text)
        except (json.JSONDecodeError, TypeError):
            # Step 3: Fall back to treating it as plain prose
            data = raw_text
        return data



