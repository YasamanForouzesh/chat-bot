from .baseAdapter import BaseAdapter, prompt
import anthropic


class Anthropic(BaseAdapter):
    def __init__(self, model: str):
        super().__init__(model)
        self.client = anthropic.Anthropic()

    @staticmethod
    def validate_messages(messages: list[prompt]) -> list[prompt]:
        allowed_roles = {"user", "assistant"}
        cleaned_messages = []

        if not messages:
            raise ValueError("At least one message is required.")

        for index, message in enumerate(messages):
            if message.role == "developer":
                raise ValueError("Anthropic does not support the developer role.")

            if index != 0 and message.role == "user" :
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

    def generate(self, prompt: list[prompt], system_prompt: str | None = None):
        validated_messages = self.validate_messages(prompt)
        messages = [p.model_dump() for p in validated_messages]

        response = self.client.messages.create(
            model=self.model,
            system=system_prompt,
            messages=messages,
        )
        return response.content[0].text