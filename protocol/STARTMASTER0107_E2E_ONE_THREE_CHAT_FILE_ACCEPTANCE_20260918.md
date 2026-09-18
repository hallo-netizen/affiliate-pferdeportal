# STARTMASTER0107 — E2E-Abnahme 1 + 3 Artikel bis Chat-Datei

Stand: 18.09.2026

## Nutzerauftrag

Frische Abnahme der kompletten Teststrecke:
- zuerst exakt **1 Artikel**;
- danach exakt **3 Artikel** als Mehrartikeltest;
- vom gebundenen Chat-/System-4-Einstieg bis zur **downloadbaren finalen Datei im Parent-Chat**;
- Technik und Textqualität jeweils positiv und negativ;
- Struktur-/Validatorfehler und Textqualität bleiben getrennte Aussagen;
- kein Publish und keine WordPress-Schreibaktion.

## Positive Gesamtstrecke

Für beide Läufe gilt:
`Chat/System-4-Einstieg -> Point-0 -> Codex Research/Facts/Context/Draft -> echtes LanguageTool 6.8 -> echter PPM 6.7.9 -> Same-Article-Repair falls erforderlich -> OUTPUT_GATE_REQUIRED -> Batch Collect -> V2-Handoff -> 107008 -> PSERC -> GitHub-ENDSTEMPEL -> reale WordPress-Importformat-Prüfung -> byte-identische Finaldatei im Parent-Chat`.

Gesamt-PASS ist erst zulässig, wenn die im Chat ausgegebene Datei byte-identisch zu der unmittelbar davor geprüften finalen signierten Datei ist.

## Textqualität

Positiv:
- reale Codex-Texte;
- PPM `CONTENT_QUALITY_CHECK_OK`;
- keine historische Artikelkörper-Wiederverwendung;
- strukturelle/technische Befunde dürfen nicht als schlechte Textqualität umetikettiert werden.

Negativ:
- absichtlich schlechter Testtext muss von den zuständigen Qualitätsprüfungen blockiert werden;
- ein strukturfehlerhafter, aber inhaltlich guter Text darf nicht als Textqualitätsfehler bewertet werden.

Mocks, deterministische Testworker und vorbereitete Finaltexte dürfen keinen Beweis realer Codex-Textqualität liefern.

## Technik

Positiv:
- kanonischer Einstieg;
- richtige Artikelreihenfolge;
- gleicher Artikel/gleicher Workspace bei Repair;
- echte LT-/PPM-Rechecks;
- 1..N-Batch;
- bytegleicher Handoff;
- 107008/PSERC/ENDSTEMPEL;
- WordPress-Importformat;
- Chat-Datei.

Negativ mindestens:
- Tamper/Hash-Drift;
- `publish_allowed=true`;
- falscher Artikelindex/Reihenfolge;
- Body-/Handoff-Manipulation;
- falsches oder unvollständiges WordPress-Importformat;
- abweichende Chat-Dateibytes;
- nächster Artikel vor PASS des aktuellen Artikels.

Alle Negativfälle müssen fail-closed blockieren.

## Mehrartikelregel

Im 3-Artikel-Lauf:
- Artikel 0 muss PASS sein, bevor Artikel 1 startet;
- Artikel 1 muss PASS sein, bevor Artikel 2 startet;
- Repair bleibt auf exakt dem betroffenen Artikel;
- kein Cross-Item-Leak;
- Gesamtdatei enthält exakt drei geprüfte Artikel.

## Verboten

- Publish oder WordPress-Schreibaktion;
- Lockerung von LT, PPM, Text-, Design- oder Qualitätsregeln;
- Architekturumbau;
- historische Artikeltexte als NEW-Quelle;
- Mock/Testworker/Prebuilt-Final als Beweis realer Codex-Qualität;
- Gesamt-PASS ohne tatsächlich im Parent-Chat ausgegebene byte-identische Finaldatei.

## Hinweis zum vorherigen Repair-PASS

PR-107-Kommentar `5735784162` meldet einen realen Repair-PASS, ersetzt aber die drei geforderten Base64-Evidence-Felder durch Output-Limit-Platzhalter. Daher bleibt `REAL_CODEX_REPAIR_PROVEN=false`, bis ein dauerhaft rekonstruierbarer Beweis vorliegt.
