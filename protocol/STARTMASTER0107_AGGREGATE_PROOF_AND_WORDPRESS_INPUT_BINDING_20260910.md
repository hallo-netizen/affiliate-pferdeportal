# STARTMASTER0107 – Aggregate Proof / WordPress-Input-Bindung – Protokoll 2026-09-10

**STATUS DIESER DATEI:** HISTORISCHES PROTOKOLL / WAS-WARUM-NACHWEIS. **KEINE CURRENT-AUTORITÄT.** Aktueller Status ausschließlich in `control/startmaster0107/CURRENT_STATE.json`.

## Belastbarer Stand

- PR #217 `Hobbyraum: Gesamtbeleg statt 12 externe Stage-Proofs` wurde in `main` gemergt: `7fcae6ad09e002903d44ff3800e6f22d9679d92e`.
- Der Rootfix entfernt die fachlich falsche Konstruktion von Worker-authored Stage-PASS-Zetteln. `stage_proofs` muss leer sein; Worker/Codex besitzt keine PASS-Autorität. Der Gesamtbeleg entsteht ausschließlich aus hash-gebundenem Handoff und vorhandenen Validatoren.
- Keine Inhalts-, Qualitäts-, Textmaschinen-, PPM-, PSERC-, PSTE-, LanguageTool-, SEO-, Design-, Publish- oder Endstempel-Regel wurde mit PR217 geändert.
- GitHub-Actions-Nachweis auf PR217: M01–M36 = PASS; letzter Regressionstest = PASS; `codex_current_action.py selftest` = PASS; `fachworkflow_proof_handoff.py selftest` = PASS; finaler PR217-Head hatte `hardlock` und `hardlock-base` = SUCCESS.
- Ein echter post-merge 7/7-Lauf auf genau diesem Main wurde gestartet und stoppte am ersten echten Blocker `BOUND_RAW_FACHWORKFLOW_OUTPUT_CONTRACTS_MISSING` (PR107, issuecomment-5623141641). 7/7 ist daher **NICHT PASS**.

## Neuer belegter Fehler / Ursache

Der aktuelle 107007-Pfad verlangt `fact_pack`, `production_plan_item`, `production_plan_header`, `workflow_release_item` und `workflow_release_metadata`, bindet aber die Quelle dieser Rohdaten nicht vollständig in R_001 ein. Der Handoff validiert und konsumiert diese Werte; er ist nicht deren Erzeuger.

Autoritative Fachklarstellung für den nächsten Lauf:

- Die Rohquelle ist **eine frische, vom Nutzer bereitgestellte WordPress-Datei**.
- Für **jeden neuen Lauf muss eine neue Datei** als konkrete Eingabe gebunden werden.
- Es ist **kein interner Rohdaten-Generator** zu bauen.
- Der Worker darf diese WordPress-Rohdaten nicht frei rekonstruieren, ersetzen oder selbst beglaubigen.

Der bestehende `runtime_inbox/incoming`-Pfad zeigt bereits das Prinzip einer gebundenen Quellprojektion für einen 7er-Batch. Gleichzeitig enthält das derzeit gebundene `PRODUCTION_PACKAGE.json` leere `fact_pack_bundle.fact_packs` und leere `production_plan.items`; deshalb kann der gegenwärtige Paketstand die fünf vollständigen Rohkontexte nicht liefern.

## Verbindliche NEXT ACTION

KISS-Ursachenfix im bestehenden Intake/R_001-Weg:

1. Die jeweils frische Nutzer-/WordPress-Datei als **eine konkrete per-run Eingabe** mit Dateiidentität und SHA-256 binden.
2. Die fünf benötigten Rohwerte ausschließlich aus dieser gebundenen Quelle bzw. ihrer bereits vorgesehenen Intake/Lifecycle-Projektion beziehen.
3. Fehlende, alte, fremde oder veränderte Datei sowie falscher Hash, Batch, `plan_slot`, `canonical_article_id` oder abgeleiteter Kontext müssen fail-closed blockieren.
4. Keine neue Architektur: kein neuer Runner, Gate, Controller, Sidecar, Fallback, Schlüssel oder Parallelweg.
5. Keine freie Workflow-/Regel-/PASS-Autorität für Worker, Chat oder Codex.
6. Danach genau ein realer positiver Gesamtpfad `frische WordPress-Datei -> gebundener Intake/R_001 -> Handoff -> Aggregate-PASS -> Consumer` und die nötigen negativen Source-/Hash-/Identity-Manipulationen.
7. Erst danach frischer echter 7/7-Lauf bis 107008; dort vor Publish stoppen.

## Sicherheits-/Architekturfolge

Allgemeingültiges Prinzip für zukünftige Büros/Projekte: **Quelleigentümer-Daten werden pro Lauf als unveränderliche, hash-gebundene Eingabe übernommen; ein Worker darf sie nicht als Ersatzquelle rekonstruieren.** Diese Regel darf erst in einen Campus-/Neubaustandard übernommen werden, wenn dessen autoritative Standardquelle eindeutig bestimmt ist. Diese Protokolldatei ist kein Ersatz für einen Campus-Standard.

## Nicht anfassen

Textmaschine, Artikeltyp-/Inhalts-/Qualitätsregeln, PPM 6.7.9, PSERC, PSTE, LanguageTool-Regeln, SEO/Links/Tabellen/Dubletten/Design, WordPress-Fachlogik, Endstempel-/Publish-Sicherheit, offizieller Cloud-Entry und bestehende Single-Door-Navigation. `publish_allowed=false` bleibt zwingend.
