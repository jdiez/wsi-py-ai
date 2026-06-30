"""Safety guardrails for the multi-agent WSI pipeline."""

from __future__ import annotations

from pydantic import BaseModel


class AgentGuardrails(BaseModel, frozen=True):
    """Safety constraints for the agent system.

    These guardrails are non-negotiable pipeline rules that agents
    cannot override regardless of their instructions or confidence level.

    Attributes:
        never_delete_raw_slides: Raw slide files are immutable — never delete originals.
        never_skip_deid: De-identification is mandatory before any data leaves the system.
        min_confidence_threshold: Minimum confidence for autonomous action (0.0-1.0).
        max_retries_before_escalate: Maximum retry attempts before escalating to human.
        require_human_for_deid_failure: Deid failures always require human review.
        require_human_for_low_confidence: Escalate when confidence below threshold.
        max_concurrent_agents: Maximum agents running simultaneously.
        audit_all_decisions: Log every agent decision for compliance.
    """

    never_delete_raw_slides: bool = True
    never_skip_deid: bool = True
    min_confidence_threshold: float = 0.85
    max_retries_before_escalate: int = 3
    require_human_for_deid_failure: bool = True
    require_human_for_low_confidence: bool = True
    max_concurrent_agents: int = 5
    audit_all_decisions: bool = True

    def allows_autonomous_action(self, confidence: float) -> bool:
        """Check if the confidence level permits autonomous action.

        Args:
            confidence: Agent's confidence in its decision (0.0-1.0).

        Returns:
            True if the agent can proceed without human approval.
        """
        return confidence >= self.min_confidence_threshold

    def should_escalate(self, retries: int) -> bool:
        """Check if the failure count warrants human escalation.

        Args:
            retries: Number of retries attempted so far.

        Returns:
            True if the agent should escalate to human review.
        """
        return retries >= self.max_retries_before_escalate
