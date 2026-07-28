# Cat & Bob — Autonome Software-Fabrik

> Kuratierte Projektübersicht ohne Quellcode. Das produktive System läuft unter
> [catandbob.de](https://catandbob.de); der vollständige Code liegt in einem privaten
> Repository.

Cat & Bob ist eine deterministische Multi-Agent-Plattform für Software-Engineering-Prozesse:
von der Anforderung über die Umsetzung bis zum getesteten, deploybaren Feature — mit
nachvollziehbarer Governance statt Blackbox-Automatisierung.

## Idee

Zwei spezialisierte Agenten mit klar getrennter Verantwortung:

- **Cat** — Planung & Governance. Erstellt Lastenhefte, Vorschläge und Freigabe-Workflows.
  Generiert selbst keinen Code.
- **Bob** — Umsetzung. Generiert Code, schreibt und führt Tests aus, arbeitet in isolierten
  Docker-Containern ohne Zugriff auf das Host-System.

Zwischen beiden steht ein **Risikomodell** (R0–R4), das automatisiert entscheidet, wie viel
menschliche bzw. Governance-Aufsicht ein Vorgang braucht — von vollautonomer Umsetzung bis
zur zwingenden menschlichen Freigabe.

## Architektur (High-Level)

```
Anfrage → Cat (Planung, Risikoeinstufung, Governance-Check)
            │
            ▼
        Freigabe-Gate (abhängig vom Risikolevel R0–R4)
            │
            ▼
        Bob (Codegenerierung, Tests, QA)
            │
            ▼
        Isolierte Ausführung (Docker, kein Host-Zugriff)
            │
            ▼
        Getestetes, dokumentiertes Ergebnis
```

- **Backend:** Python, FastAPI, modulare Engine-Pipeline
- **Frontend:** React + Vite
- **Persistenz:** SQL-Datenbank mit additiven, nachvollziehbaren Migrationen
- **Ausführung:** Docker-isolierte Sandboxes für generierten Code, keine direkte Host-Ausführung
- **Governance:** Audit-Logging, Policy-Engine, DSGVO-orientiertes Datenmodell (by Design)
- **Qualitätssicherung:** automatisierte Test-Suite (Backend + Frontend) als CI-Pflicht-Gate
  vor jedem Deploy

## Ausrichtung

- On-Premises-fähig — keine zwingende Cloud-Abhängigkeit für den Kern
- DSGVO by Design statt Nachrüstung
- Orientierung an ISO 9001 (Qualitätsmanagement), ISO/IEC 27001 (Informationssicherheit)
  und ISO/IEC 12207 (Software-Lebenszyklus) — **nicht** extern zertifiziert oder
  auditiert; gemeint sind die gelebten Prozesse (siehe unten), nicht ein Siegel.

## Was heißt das konkret — und wie lässt sich das prüfen?

Starke Begriffe ohne Beleg sind wertlos. Da der produktive Code privat bleibt
(siehe oben, bewusste Entscheidung gegen IP-Preisgabe), lässt sich hier nicht
alles zeigen — aber das, was öffentlich nachprüfbar ist:

| Begriff | Was er hier konkret bedeutet | Wo nachprüfbar |
|---|---|---|
| „Deterministisch" | Die Risikoeinstufung folgt festen, dokumentierten Regeln (kein Sampling, keine Blackbox-Entscheidung) — jede Regel ist einzeln benannt und testbar | [demo/](demo/) — `risk.py`, 8 Tests decken jede Regel einzeln ab |
| „Governance statt Blackbox" | Planung und Ausführung sind strukturell getrennte Rollen mit einem dazwischenliegenden Freigabe-Gate, nicht nur Konvention | [demo/](demo/) — `Gate.decide()` blockiert `Executor.execute()` strukturell, nicht per Absprache; siehe auch [DEEP-DIVE.md](DEEP-DIVE.md) für das echte Tool-Plugin-Interface |
| „Audit-Logging" | Jede Entscheidung (auch eine blockierte) erzeugt einen unveränderlichen Log-Eintrag, kein optionales Nice-to-have | [demo/](demo/) — `AuditLog` ist append-only (frozen Dataclass, keine update()-Methode) |
| „DSGVO by Design" | Datenschutzrelevante Entscheidungen (z. B. ob etwas ausgeführt werden darf) sind im selben Freigabe-Mechanismus verankert wie Sicherheitsentscheidungen, nicht separat nachgerüstet | Live-System: [catandbob.de](https://catandbob.de) — Impressum/Datenschutzerklärung sind Teil des ausgelieferten Produkts, nicht nur Marketingtext |
| „On-Premises-fähig" | Kern läuft containerisiert (Docker), ohne zwingenden Cloud-Dienst für die Kernfunktion | Docker-Image-basierter Deploy ist die einzige produktive Betriebsform (siehe Live-System) |

Was hier bewusst **nicht** behauptet wird: eine externe Zertifizierung, ein
unabhängiges Audit oder verifizierte Kunden-KPIs — dafür gibt es aktuell keinen
öffentlich prüfbaren Nachweis, und unbelegte Zahlen sind hier absichtlich
weggelassen.

## Code-Beispiel

→ [DEEP-DIVE.md](DEEP-DIVE.md) — ein konkreter Architektur-Ausschnitt (Tool-Plugin-System)
mit Code und Begründung, statt nur Fließtext.

→ [demo/](demo/) — eine eigenständige, lauffähige Mini-Demo des Governance-Gate-Musters
(Planner/Gate/Executor + Audit-Log), mit Tests und CI-Pipeline. Kein Auszug aus dem
produktiven Code.

## Live

Das produktive System ist erreichbar unter **[catandbob.de](https://catandbob.de)**.

## Kontakt

**Thomas Bernecker**
[bernecker.thomas@gmx.de](mailto:bernecker.thomas@gmx.de)

---

*Dieses Repository dient ausschließlich der Projektvorstellung. Es enthält bewusst keinen
Quellcode, keine Infrastrukturdetails und keine Kundendaten.*
