"""Writer-Profile für die zwei Concept-Agent-Varianten."""

from dataclasses import dataclass


@dataclass(frozen=True)
class WriterProfile:
    name: str
    mode: str
    automatic: bool
    external_connection_required: bool


CHAT_PROFILE = WriterProfile(
    name="Chat Writer",
    mode="CHAT_MANUAL_ORCHESTRATED",
    automatic=False,
    external_connection_required=False,
)

CLAUDE_PROFILE = WriterProfile(
    name="Claude Writer",
    mode="CLAUDE_API_OPTIONAL",
    automatic=True,
    external_connection_required=True,
)
