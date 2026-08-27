from dataclasses import dataclass


@dataclass
class WebSearchConfig:
    max_uses: int | None = None
    allowed_domains: list[str] | None = None
    blocked_domains: list[str] | None = None
    user_location: dict | None = None


@dataclass
class WebFetchConfig:
    max_uses: int | None = None
    allowed_domains: list[str] | None = None
    blocked_domains: list[str] | None = None
    citations: bool = True
    max_content_tokens: int | None = None