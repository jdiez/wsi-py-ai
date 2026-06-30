"""Decision audit log for regulatory compliance."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import structlog
from pydantic import BaseModel

from wsi_py_ai.agents.base import AgentDecision, AgentRole

logger: structlog.stdlib.BoundLogger = structlog.get_logger("wsi_py_ai.memory.audit")


class AuditEntry(BaseModel, frozen=True):
    """Single audit log entry.

    Attributes:
        timestamp: UTC timestamp of the decision.
        agent_role: Which agent made the decision.
        decision: The decision details.
        context: Additional context for the audit trail.
    """

    timestamp: str
    agent_role: AgentRole
    decision: AgentDecision
    context: dict[str, Any] = {}


class DecisionAuditLog:
    """Append-only audit log for agent decisions.

    Writes JSONL entries for regulatory compliance and traceability.
    All agent decisions are logged with timestamps, reasoning, and confidence.
    """

    def __init__(self, log_dir: Path) -> None:
        """Initialize the audit log.

        Args:
            log_dir: Directory to store audit log files.
        """
        self._log_dir = log_dir
        self._log_dir.mkdir(parents=True, exist_ok=True)
        self._log_file = self._log_dir / "decisions.jsonl"

    def record(
        self,
        agent_role: AgentRole,
        decision: AgentDecision,
        context: dict[str, Any] | None = None,
    ) -> AuditEntry:
        """Record a decision to the audit log.

        Args:
            agent_role: The agent that made this decision.
            decision: The decision with action, reasoning, and confidence.
            context: Optional additional context.

        Returns:
            The created audit entry.
        """
        entry = AuditEntry(
            timestamp=datetime.now(tz=timezone.utc).isoformat(),
            agent_role=agent_role,
            decision=decision,
            context=context or {},
        )

        with self._log_file.open("a") as f:
            f.write(json.dumps(entry.model_dump(), default=str) + "\n")

        logger.info(
            "decision.recorded",
            agent=agent_role.value,
            decision=decision.decision,
            confidence=decision.confidence,
        )
        return entry

    def query(
        self,
        agent_role: AgentRole | None = None,
        since: str | None = None,
    ) -> list[AuditEntry]:
        """Query audit log entries.

        Args:
            agent_role: Filter by agent role (optional).
            since: ISO timestamp — return entries after this time (optional).

        Returns:
            List of matching audit entries.
        """
        if not self._log_file.exists():
            return []

        entries: list[AuditEntry] = []
        with self._log_file.open() as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                data = json.loads(line)
                entry = AuditEntry.model_validate(data)

                if agent_role and entry.agent_role != agent_role:
                    continue
                if since and entry.timestamp < since:
                    continue

                entries.append(entry)

        return entries
