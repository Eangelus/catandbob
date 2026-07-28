"""Minimaler Workflow: Anfrage -> Plan -> Risiko-Gate -> Ausfuehrung.

Zeigt das Grundmuster von Cat & Bob (Planung und Ausfuehrung als getrennte
Rollen, mit einem Freigabe-Gate dazwischen) als eigenstaendige,
unabhaengige Neuimplementierung -- kein Auszug aus dem produktiven System.
"""

from dataclasses import dataclass
from enum import Enum

from .audit import AuditLog
from .risk import RiskLevel, TaskProfile, classify_risk, requires_human_approval


@dataclass
class Plan:
    """Ergebnis der Planungsphase: was soll getan werden, mit welchem Risiko."""

    request: str
    profile: TaskProfile
    risk_level: RiskLevel


class DecisionStatus(str, Enum):
    AUTO_APPROVED = "auto_approved"
    PENDING_HUMAN = "pending_human"
    REJECTED = "rejected"


@dataclass
class Decision:
    status: DecisionStatus
    risk_level: RiskLevel
    reason: str


class Planner:
    """Entspricht der Rolle "Cat": erstellt einen Plan, generiert selbst
    keine Ausfuehrung.
    """

    def __init__(self, audit: AuditLog) -> None:
        self._audit = audit

    def plan(self, request: str, profile: TaskProfile) -> Plan:
        risk_level = classify_risk(profile)
        self._audit.record(
            actor="planner",
            action="plan_created",
            reason=f"request={request!r} risk={risk_level.name}",
        )
        return Plan(request=request, profile=profile, risk_level=risk_level)


class Gate:
    """Freigabe-Gate zwischen Planung und Ausfuehrung. Ab R2 ist eine
    explizite menschliche Freigabe zwingend -- der Gate selbst kann sie
    nicht erteilen, nur einfordern.
    """

    def __init__(self, audit: AuditLog) -> None:
        self._audit = audit

    def decide(self, plan: Plan, human_approved: bool = False) -> Decision:
        if not requires_human_approval(plan.risk_level):
            decision = Decision(
                status=DecisionStatus.AUTO_APPROVED,
                risk_level=plan.risk_level,
                reason=f"{plan.risk_level.name} erlaubt autonome Ausfuehrung",
            )
        elif human_approved:
            decision = Decision(
                status=DecisionStatus.AUTO_APPROVED,
                risk_level=plan.risk_level,
                reason=f"{plan.risk_level.name} -- menschliche Freigabe erteilt",
            )
        else:
            decision = Decision(
                status=DecisionStatus.PENDING_HUMAN,
                risk_level=plan.risk_level,
                reason=f"{plan.risk_level.name} erfordert menschliche Freigabe",
            )

        self._audit.record(
            actor="gate",
            action=decision.status.value,
            reason=decision.reason,
        )
        return decision


class Executor:
    """Entspricht der Rolle "Bob": fuehrt einen freigegebenen Plan aus.
    Verweigert die Ausfuehrung strukturell, wenn keine Freigabe vorliegt --
    nicht nur per Konvention, sondern als Vorbedingung im Code.
    """

    def __init__(self, audit: AuditLog) -> None:
        self._audit = audit

    def execute(self, plan: Plan, decision: Decision) -> str | None:
        if decision.status != DecisionStatus.AUTO_APPROVED:
            self._audit.record(
                actor="executor",
                action="execution_blocked",
                reason=f"status={decision.status.value}",
            )
            return None

        result = f"erledigt: {plan.request}"
        self._audit.record(
            actor="executor",
            action="execution_completed",
            reason=result,
        )
        return result
