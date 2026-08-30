import inspect
from pydantic import create_model
from models import Tool


def tool(*, strict: bool = False):

    def decorator(func):

        signature = inspect.signature(func)

        fields = {}

        for name, param in signature.parameters.items():

            # Example:
            # city: str
            annotation = param.annotation

            if annotation is inspect.Parameter.empty:
                annotation = str

            # No default means required
            if param.default is inspect.Parameter.empty:
                default = ...
            else:
                default = param.default

            fields[name] = (
                annotation,
                default,
            )

        input_model = create_model(
            f"{func.__name__.title()}Input",
            **fields,
        )

        parameters = input_model.model_json_schema()

        return Tool(
            name=func.__name__,
            description=func.__doc__ or "",
            parameters=parameters,
            func=func,
            strict=strict,
        )

    return decorator