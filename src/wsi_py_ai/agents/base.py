"""Base types for the multi-agentic system."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class AgentRole(str, Enum):
    """Roles in the multi-agent WSI system."""

    PLANNER = "planner"
    INGEST = "ingest"
    DEID = "deid"
    QA = "qa"
    REGISTRY = "registry"
    TRAINING = "training"
    RECOVERY = "recovery"


class Priority(str, Enum):
    """Message priority levels."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class AgentMessage(BaseModel, frozen=True):
    """Inter-agent communication message.

    Attributes:
        from_agent: Sender agent role.
        to_agent: Recipient agent role or "human" for escalation.
        action: Description of what happened or what's requested.
        payload: Structured data for the message.
        priority: Message urgency level.
        timestamp: When the message was created.
        trace_id: Links all messages in a pipeline run.
    """

    from_agent: AgentRole
    to_agent: str
    action: str
    payload: dict[str, object] = {}
    priority: Priority = Priority.NORMAL
    timestamp: datetime = datetime(2026, 1, 1)
    trace_id: str = ""


class AgentDecision(BaseModel, frozen=True):
    """Auditable record of an agent's autonomous decision.

    Attributes:
        agent: Which agent made the decision.
        decision: What was decided.
        reasoning: Why (auditable explanation).
        confidence: Confidence score 0-1; below threshold triggers escalation.
        alternatives_considered: Other options that were evaluated.
        trace_id: Pipeline run identifier.
        timestamp: When the decision was made.
    """

    agent: AgentRole
    decision: str
    reasoning: str
    confidence: float
    alternatives_considered: tuple[str, ...] = ()
    trace_id: str = ""
    timestamp: datetime = datetime(2026, 1, 1)
