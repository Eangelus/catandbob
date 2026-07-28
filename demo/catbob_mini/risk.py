"""Risikoklassifikation: entscheidet, wie viel menschliche Aufsicht eine
Aufgabe braucht, bevor sie ausgefuehrt werden darf.

Dies ist eine eigenstaendige, stark vereinfachte Demo-Implementierung des
Grundmusters aus Cat & Bob (siehe https://catandbob.de) -- keine Kopie der
produktiven Risikologik.
"""

from dataclasses import dataclass, field
from enum import IntEnum


class RiskLevel(IntEnum):
    """R0 (unkritisch) bis R4 (zwingend menschliche Freigabe)."""

    R0 = 0
    R1 = 1
    R2 = 2
    R3 = 3
    R4 = 4


@dataclass
class TaskProfile:
    """Merkmale einer Aufgabe, die die Risikoeinstufung beeinflussen."""

    touches_auth: bool = False
    touches_billing: bool = False
    touches_production_data: bool = False
    has_tests: bool = True
    reversible: bool = True
    notes: str = field(default="")


def classify_risk(task: TaskProfile) -> RiskLevel:
    """Ordnet ein Aufgabenprofil einem Risikolevel zu.

    Die Regeln sind bewusst einfach gehalten, um das Muster zu zeigen
    (mehrere unabhaengige Signale erhoehen das Level additiv, ein
    einzelner harter Ausschluss -- irreversibel + Produktionsdaten --
    erzwingt sofort die hoechste Stufe).
    """
    if task.touches_production_data and not task.reversible:
        return RiskLevel.R4

    level = RiskLevel.R0
    if not task.has_tests:
        level = RiskLevel(min(level + 1, RiskLevel.R4))
    if task.touches_billing:
        level = RiskLevel(min(level + 2, RiskLevel.R4))
    if task.touches_auth:
        level = RiskLevel(min(level + 2, RiskLevel.R4))
    if task.touches_production_data:
        level = RiskLevel(min(level + 1, RiskLevel.R4))
    if not task.reversible:
        level = RiskLevel(min(level + 1, RiskLevel.R4))

    return level


def requires_human_approval(level: RiskLevel) -> bool:
    """Ab R2 ist eine menschliche Freigabe zwingend, nicht nur optional."""
    return level >= RiskLevel.R2
