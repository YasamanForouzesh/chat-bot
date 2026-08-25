
from pathlib import Path


def prompt_loader(agent: str, version: str)-> str:
    path = Path("prompts") / agent /f"{version}.md"
    return path.read_text(encoding="utf-8")