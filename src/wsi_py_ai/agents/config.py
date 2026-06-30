"""Model configuration for the multi-agent system."""

from pydantic import BaseModel


class AgentModelConfig(BaseModel, frozen=True):
    """Cloud model assignments per agent role.

    Attributes:
        planner: Model for the coordinator agent (strongest reasoning).
        qa: Model for QA assessment and diagnosis.
        qa_vision: Model for visual slide reasoning tasks.
        deid: Model for de-identification verification.
        ingest: Model for ingestion edge case handling.
        registry: Model for metadata enrichment and curation.
        training: Model for optimization strategy.
        recovery: Model for failure diagnosis and retry.
    """

    planner: str = "claude-sonnet-4-6"
    qa: str = "claude-sonnet-4-6"
    qa_vision: str = "claude-sonnet-4-6"
    deid: str = "claude-haiku-4-5"
    ingest: str = "claude-haiku-4-5"
    registry: str = "claude-sonnet-4-6"
    training: str = "claude-sonnet-4-6"
    recovery: str = "claude-sonnet-4-6"


class LocalAgentModelConfig(AgentModelConfig, frozen=True):
    """On-premise model assignments using local inference.

    Attributes:
        inference_server: Local inference backend (ollama, vllm, tgi).
        inference_url: URL of the local inference server.
    """

    planner: str = "llama3.1:70b-instruct"
    qa: str = "llama3.2-vision:90b"
    qa_vision: str = "llama3.2-vision:90b"
    deid: str = "llama3.1:8b-instruct"
    ingest: str = "llama3.1:8b-instruct"
    registry: str = "llama3.1:70b-instruct"
    training: str = "llama3.1:70b-instruct"
    recovery: str = "llama3.1:8b-instruct"
    inference_server: str = "ollama"
    inference_url: str = "http://localhost:11434"
