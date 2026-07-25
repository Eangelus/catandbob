# Cat & Bob — Autonome Software-Fabrik

> **Showroom-Repository.** Dies ist eine kuratierte Projektübersicht ohne Quellcode.
> Das produktive System läuft unter [catandbob.de](https://catandbob.de);
> der vollständige Code liegt in einem privaten Repository.

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
  und ISO/IEC 12207 (Software-Lebenszyklus)

## Live

Das produktive System ist erreichbar unter **[catandbob.de](https://catandbob.de)**.

## Kontakt

**Thomas Bernecker**
[bernecker.thomas@gmx.de](mailto:bernecker.thomas@gmx.de)

---

*Dieses Repository dient ausschließlich der Projektvorstellung. Es enthält bewusst keinen
Quellcode, keine Infrastrukturdetails und keine Kundendaten.*
