# PFERDE ATELIER – TEXT – SYSTEM 4 – ARBEITSPROTOKOLL 2026-09-14

## STATUS

System 4 wurde nach wiederholten Live-Abbrüchen ursächlich nachgeschärft. Schwerpunkt: reparierbare Fehler dürfen nicht pauschal den gesamten Artikel beenden, sondern müssen zur zuständigen Maschinenstufe zurückgeroutet werden.

## URSÄCHLICH GESCHLOSSENE FEHLERKLASSEN

### 1. Stage-aware Rückgabe
Bekanntes Fehlermuster:
- eine frühere Maschinenstufe erzeugt/bindet einen Wert;
- ein späterer echter Prüfer beanstandet diesen Wert;
- bisher führte das trotz Reparierbarkeit teilweise zum terminalen Abbruch.

Zentrale Rückroute:
- Titel / Kategorie / Slot -> Parent-Maschine;
- Links -> Context-Binder;
- Quellen / Facts -> Research-Stufe;
- Textkörper -> Same-Article-Repair.

Ziel: reparierbarer Fehler -> zuständige Vorstufe -> Reparatur/Neubindung -> erneute echte Prüfung -> Weiterlauf desselben Artikels. Nur echt nicht reparierbare Fehler dürfen terminal blockieren.

### 2. Feldloser PPM-Inhaltsfehler
Im realen Artikel `Pferdeanhänger richtig beladen und Gewicht sicher verteilen` trat nach mehreren zulässigen Same-Article-Reparaturen ein PPM-Hardblock auf:
`PPM679_VALIDATOR_BLOCKED:BLOCKED_KNOWN_REGRESSION_PATTERN`.

Ursache im System: `_ppm_repair_findings()` behandelte nur wenige fest verdrahtete PPM-Fehlerpräfixe als reparierbar. Ein erfolgreich ausgeführter PPM-Inhaltsvalidator ohne Feldangabe fiel deshalb pauschal in terminalen Hard-Stop.

Ursächliche neue Regel:
- erfolgreich ausgeführter PPM-Inhaltsvalidator lehnt Inhalt ab -> reparierbarer/routbarer Prüferbefund, auch ohne Feldangabe;
- technische PPM-Ausführungsfehler, Integritätsfehler, Hash-/Manipulationsfehler bleiben terminal fail-closed.

Damit wird nicht `BLOCKED_KNOWN_REGRESSION_PATTERN` einzeln gepatcht, sondern die Klasse `Inhaltsablehnung ohne Feldadresse` zentral behandelt.

## FRISCHER KOMPLETTER ARTIKELTEST POSITIV / NEGATIV

Frisch neu ausgeführt, kein alter PASS übernommen.

Aktueller Volltest-Run: `34886610523` auf Test-Head `5f6b3a530a9eeba5eeeea65f305a92879786b97a`.

PASS:
- Python syntax;
- feldlose PPM-Inhaltsfehler positiv/negativ;
- technische/integritätsbezogene PPM-Fehler bleiben terminal;
- Stage-aware Repair Router;
- Repair Continuity inklusive Mehrfach-Repair;
- gesamte bestehende System-4-Suite;
- exaktes LanguageTool 6.8;
- echter LT-6.8 / PPM-6.7.9-Korridor;
- drei neue Realthemen;
- 1 Artikel Start -> Datei/Handoff;
- 3 Artikel Start -> Datei/Handoff.

Gesamter frischer GitHub-Volltest: **PASS**.

Wichtig: ein separater lokaler Lauf konnte in der verfügbaren lokalen Umgebung wegen fehlender GitHub/DNS-Erreichbarkeit nicht belastbar ausgeführt werden. `lokal PASS` wird deshalb ausdrücklich nicht behauptet.

## PRODUKTIONSSTAND

PR: `#259`
Branch: `hobbyroom/system4-parent-start-token-clean-v1`
Produktions-Head: `a9cb5e3a7500cf4ba5e4551591ffd79cae57e36e`

Immutable Base Hardlock auf exakt diesem Head:
Run `34886245170` -> **PASS**.

Vergleich Test-Head `5f6b3a5...` gegen Produktions-Head `a9cb5e3...`:
- Produktcode identisch;
- einzige Unterschiede: zwei reine Test-Workflow-Dateien unter `.github/workflows/`.

Damit ist der grün getestete Produktcode bytegleich auf dem Produktionsstand vorhanden.

## REALER CODEX-ARTIKEL

Thema:
`Pferdeanhänger richtig beladen und Gewicht sicher verteilen`

Target Keyword:
`Pferdeanhänger richtig beladen`

Artikeltyp:
`Beratung`

Kategorie:
`checklisten-fuer-pferdeanhaenger-beratung`

Gebundene/versiegelte Quellen:
- FN / Pferdetransport;
- § 22 StVO;
- § 34 StVZO;
- § 44 StVZO.

Historischer Realabbruch dieses Artikels:
- mehrere Same-Article-Reparaturen bis Revision 4;
- danach PPM `BLOCKED_KNOWN_REGRESSION_PATTERN`;
- Batch/V2/Inline wurden nicht erreicht.

Nach ursächlichem Fix wurde genau dieser reale Produktionslauf erneut auf PR #259 gestartet.

Neuer Codex-Auftrag:
Kommentar `5675455629`.

Codex-Connector-Reaktion:
`eyes` -> Auftrag angenommen.

Verwendeter gebundener Einstieg:
`python3 isolated_system4/parent_start.py start-bound isolated_system4/bound_launches/real_article_pferdeanhaenger_20260914.json ca3d56b2f6c9aa1668cb9503c7b21ce13dd0ec36a48cbc2adb55d73c544c190a /tmp/system4-parent-runtime`

Vorgabe:
- gleicher Artikel;
- kein Merge;
- kein Publish;
- `publish_allowed=false`;
- reparierbare Validatorbefunde müssen zurückgeroutet und erneut geprüft werden;
- technische/integritätsbezogene Fehler bleiben terminal;
- echter LT 6.8 -> echter PPM 6.7.9 -> Batch -> V2-Handoff -> Inline-Pack/Unpack -> bytegleiche Enddatei.

## AKTUELLER OFFENER PUNKT

Der erneute reale Codex-Lauf ist gestartet und vom Connector angenommen. Zum Zeitpunkt dieser Protokollierung liegt noch **kein terminales Endergebnis** vor.

Daher ausdrücklich:
- kein Produktions-PASS behauptet;
- kein zweiter Parallel-Lauf;
- kein Merge;
- kein Publish;
- `publish_allowed=false`.

## NEXT ACTION

Nur den bereits angenommenen realen Codex-Lauf zu Kommentar `5675455629` auswerten.

Bei PASS: echten End-to-End-Nachweis bis Batch Gate, V2-Handoff, Inline-Pack/Unpack und bytegleicher Rekonstruktion dokumentieren.

Bei Fehler: exakt erste fehlschlagende Stufe, Fehlercode, Feld falls vorhanden, Ist/Soll und zuständige Reparaturroute dokumentieren; keinen Symptom-Patch und keinen Parallel-/Ausweichlauf starten.
