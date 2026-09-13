# TEXTSYSTEM 4A – HOBBYRAUM

STAND: 2026-09-13
STATUS: AKTIV / ISOLIERTER GEGENPROTOTYP

## AKTUELLE ARBEITSBINDUNG

THEMA: `KONZEPT_4_GEGEN_4A_STATE_AUTHORITY`
STATUS: `ENTSCHEIDUNGSBEWEIS_AKTIV`

AUFTRAG:
Nicht eine neue Textmaschine bauen, sondern exakt einen strukturellen Punkt gegen das bereinigte Konzept 4 beweisen oder verwerfen:

**Kann ein außerhalb des Codex-Workers liegender Supervisor den kompletten Workflow-State allein besitzen, während Codex nur den jeweils erlaubten Fachauftrag ausführt und die vorhandenen realen Prüfer ausschließlich PASS/FAIL zurückgeben?**

## FRISCHER SYSTEM-4-BEFUND

Aktueller Vergleichshead:
`623510bf7a7c968ae24fcb9003cf2f5d12c75bcc`

Im realen System-4-Produktionsauftrag gilt weiterhin:
- alle Artikel-Workspaces/States liegen im selben Codex-Task;
- Codex ruft `controller.py ingress/research/facts/context/draft/fullcheck/repair` selbst auf;
- `state.json` wird zwischen diesen Aufrufen persistiert und wieder eingelesen;
- der Batch-Gate erhält am Ende diese State-Dateien.

Damit ist die State-/Workflow-Autorität noch nicht vollständig außerhalb des ausführenden Workers gekapselt.

## 4A-GEGENPROTOTYP

PR #255
Branch `hobbyroom/system4a-capsule-v1-20260913`

Aktueller Architekturstand:
- interner `CapsuleController` ist einziger State-Besitzer;
- Worker sieht keinen echten State;
- Worker erhält nur den gerade erlaubten Arbeitsauftrag;
- Worker-Rückgabe erlaubt ausschließlich Arbeitsinhalt;
- Route/PASS/Phase/Publish sind nicht worker-setzbar;
- FAIL → automatisch Same-Article-Repair → erneuter Fullcheck;
- HMAC-Checkpoint für Resume.

Lokaler Architekturbeweis: **13/13 PASS**, inklusive 1000 unabhängiger Mock-Kapseln.

Kein fachlicher Produktions-PASS daraus ableiten.

## JETZT VERBINDLICHE NEXT ACTION

1. 4A auf exakt aktuellen System-4-Head halten;
2. **keinen neuen Prüfer bauen**;
3. vorhandene System-4-Funktionen READ-ONLY anbinden:
   - Research-Evidence-Guard;
   - Facts-Evidence-Guard;
   - Fact-Pack-/Production-Context-Bindung;
   - Content-/Design-Guard;
   - realer FULL-Production-Check mit PPM/LT;
   - Repair-Continuity;
   - Batch-Distinctness/Repetition;
4. Prozessstufe `Production Context` in die Kapsel aufnehmen;
5. Worker darf weiterhin nur Arbeitsinhalt liefern und keine State-/Routefelder;
6. positiver Einzelartikel-E2E mit exakt denselben bestehenden Prüfern;
7. negativer Test: Worker versucht State-/Route-/PASS-Manipulation;
8. negativer Test: manipuliertes Research/Facts/Context/Draft;
9. nur wenn dieser Beweis grün ist: generischen vorhandenen `SYSTEM4_WORDPRESS_HANDOFF_V1` als finalen Ausgang anschließen;
10. danach 1/3/25/1000 und mehrere bereits freigegebene Beitragsarten.

## WORDPRESS

Keine neue Schnittstelle bauen.

Autoritative Prüfung: `WORDPRESS_HANDOFF.md`.
Der vorhandene Importer 0.28.23 kann den generischen `SYSTEM4_WORDPRESS_HANDOFF_V1` bereits verarbeiten.

## STOPPREGELN

- Keine neue Fach-/Text-/Design-/Qualitätsregel.
- Kein Ersatzprüfer.
- Keine neue WordPress-Schnittstelle.
- Keine Bewertung über 7er-/`Beratung`-Hardcodes.
- Kein zweiter Signer/Receipt-/Room-/Package-Weg.
- Keine zweite CURRENT_STATE-/Fehler-/Zielwahrheit.
- Kein Merge/Publish/Pluginbau aus diesem Büro.
- Wenn echte Supervisor-Trennung nur mit neuer Übergabekomplexität möglich ist: **4A STOPPEN und die Härtung in System 4 übernehmen.**
