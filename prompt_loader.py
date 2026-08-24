
from pathlib import Path


def promptLoader(version: str, agent: str)-> str:
    path = Path("prompts") / agent /f"{version}.md"
    print(path, "------------------")
    return path.read_text(encoding="utf-8")