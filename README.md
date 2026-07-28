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

## Ausrichtung — mit Mechanismus statt nur Begriff

Begriffe wie „deterministisch" oder „DSGVO by Design" sind ohne sichtbaren
Mechanismus reine Behauptung. Deshalb hier je ein konkretes Beispiel dafür,
*wie* das umgesetzt ist — nicht nur *dass* es umgesetzt ist.

**„Deterministisch" heißt: feste, benannte Regeln statt Modell-Entscheidung.**
Die Risikoeinstufung ist kein ML-Modell und kein Scoring mit Wahrscheinlichkeiten,
sondern eine Kette einzeln benannter, einzeln testbarer Regeln. Aus der
[Mini-Demo](demo/) (`demo/catbob_mini/risk.py`, echter Code, kein Auszug aus der
Produktivlogik, aber dasselbe Muster):

```python
def classify_risk(task: TaskProfile) -> RiskLevel:
    if task.touches_production_data and not task.reversible:
        return RiskLevel.R4          # harter Ausschluss, keine Abwaegung

    level = RiskLevel.R0
    if not task.has_tests:
        level = RiskLevel(min(level + 1, RiskLevel.R4))
    if task.touches_billing:
        level = RiskLevel(min(level + 2, RiskLevel.R4))
    if task.touches_auth:
        level = RiskLevel(min(level + 2, RiskLevel.R4))
    # ... jede Regel einzeln in tests/test_risk.py abgedeckt (8 Tests)
    return level
```

Zwei identische Eingaben ergeben immer dasselbe Ergebnis — das ist die gesamte
Definition von „deterministisch" hier, nicht mehr und nicht weniger.

**„Governance statt Blackbox" heißt: das Gate kann nicht umgangen werden, weil
die Ausführung es strukturell braucht.** Nicht Konvention („Bob hält sich an
die Regel"), sondern Code-Struktur: `Executor.execute()` bekommt eine
`Decision` als Pflichtparameter und verweigert die Arbeit, wenn deren Status
nicht `AUTO_APPROVED` ist — nachlesbar in [demo/`workflow.py`](demo/catbob_mini/workflow.py).
Für das echte, produktive Tool-Plugin-Interface siehe [DEEP-DIVE.md](DEEP-DIVE.md).

**„Audit-Logging" heißt: auch eine verweigerte Ausführung erzeugt einen
Eintrag.** Nicht nur Erfolge werden protokolliert — gerade das Blockieren ist
der sicherheitsrelevante Fall. Der `AuditLog` in der Demo ist ein `frozen`
Dataclass ohne `update()`-Methode: ein Eintrag lässt sich anhängen, aber nicht
nachträglich verändern.

**„DSGVO by Design" heißt konkret:** Einwilligung (Consent) wird als eigenes,
vom Nutzerkonto getrenntes Ereignis protokolliert (Zeitpunkt, akzeptierte
Dokumentversion, IP), nicht nur als Ja/Nein-Flag am Konto — dieselbe
Append-only-Logik wie beim Audit-Log oben, angewendet auf Einwilligungen statt
auf Ausführungsentscheidungen. Sichtbarer Teil davon: die produktiv
ausgelieferte Datenschutzerklärung unter [catandbob.de](https://catandbob.de)
ist Teil des Produkts, nicht nur eine separate Marketing-Seite.

**„ISO-orientiert" heißt hier: Nachvollziehbarkeit als Code-Zwang, nicht als
Prozess-Dokument.** Der Kern von ISO 9001 ist, dass Entscheidungen begründet
und nachvollziehbar sind — hier erzwungen dadurch, dass jede `Decision` ein
Pflichtfeld `reason` trägt (siehe Demo-Code oben) statt in einem separaten,
irgendwann veraltenden Handbuch zu stehen. **Das ist keine Zertifizierung** —
es gibt kein externes Audit und kein Siegel dafür. Gemeint ist ausschließlich
das gelebte Prinzip.

**On-Premises-fähig:** Der Kern läuft containerisiert (Docker); die einzige
produktive Betriebsform ist ein Docker-Image-Deploy, kein verstecktes
Cloud-Backend für die Kernfunktion.

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
