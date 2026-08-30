from typing import Annotated
from pydantic import Field
from decorators import tool

@tool()
def get_weather( location: Annotated[
        str,
        Field(description="City and state, e.g. San Francisco, CA")
    ], days: int = 1):
    """Get wather information for a city."""
    return f"Weather for {location} for {days} is hot"