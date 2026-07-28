"""Append-only Audit-Log: jede Entscheidung wird nachvollziehbar protokolliert,
statt nur das Endergebnis zu zeigen.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(frozen=True)
class AuditEntry:
    """Ein einzelner, unveraenderlicher Eintrag im Audit-Trail."""

    actor: str
    action: str
    reason: str
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


class AuditLog:
    """Sammelt Audit-Eintraege. Bewusst append-only: keine update()/delete()-
    Methode, damit ein einmal geschriebener Eintrag nicht mehr veraendert
    werden kann.
    """

    def __init__(self) -> None:
        self._entries: list[AuditEntry] = []

    def record(self, actor: str, action: str, reason: str) -> AuditEntry:
        entry = AuditEntry(actor=actor, action=action, reason=reason)
        self._entries.append(entry)
        return entry

    @property
    def entries(self) -> list[AuditEntry]:
        return list(self._entries)

    def __len__(self) -> int:
        return len(self._entries)
