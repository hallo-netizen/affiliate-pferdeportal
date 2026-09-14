# PROTOKOLL — SYSTEM 4 SINGLE-BUTTON FULL ROUTE — 14.09.2026

## Zweck

Dauerhafte WAS/WARUM-/Testdokumentation des am 14.09.2026 auf dem isolierten System-4-Hobbyraum-Branch aufgebauten und remote geprüften Startknopf-bis-Datei-Kandidaten.

Diese Datei ist **kein CURRENT_STATE und kein zweiter Zielvertrag**. Aktuelle System-4-Statuswahrheit bleibt `isolated_system4/README.md`. Aktueller Zielvertrag bleibt `isolated_system4/ZIELVERTRAG_SYSTEM4_MACHINE_POINT0_CODEX_WRITER_20260914.md`. Offizieller Campus-/LIVE-Stand bleibt `control/startmaster0107/CURRENT_STATE.json`.

## Ausgangsproblem

Frühere Teststrecken konnten grün werden, obwohl wesentliche Live-Übergänge separat oder erst später geprüft wurden. Wiederkehrende Fehlerklassen betrafen insbesondere falsche Einstiegspunkte, vorbereitete Zwischenzustände, ungebundene Research-/Fact-/Context-Daten, Artikelindex-/Batchabweichungen, echte LT-/PPM-Lücken und Handoff-Abweichungen.

Zusätzlich war der Worker-/Codex-Start zunächst nicht Bestandteil des einen Startknopfs. Das widersprach dem Ziel „vom Startknopf bis zur finalen Datei dieselbe Strecke“.

## WAS geändert wurde

1. Point-0 zweistufig gebunden: `PREPARED -> Quellenbindung -> FINAL`.
2. Root/Supervisor/Receipt/Worker-Dispatch binden Head, Manifest, Source-Pool und Artikelindex.
3. `full_route_start.py` als ein Startknopf ergänzt und in die kritische Root-Identität aufgenommen.
4. Worker-Start ist Teil derselben Route; kein separater manueller Worker-Start wird für den Test benötigt.
5. Route ist phasentreu: Research -> Maschinenprüfung -> Facts -> Maschinen-Context/Authoring-Contract -> Draft -> Fullcheck.
6. Kategorie, Quality-Binding und exakt drei interne Links werden maschinell gebunden; externe Vorbelegung ist fail-closed verboten.
7. Alte Direkt-/Legacy-Eingänge bleiben negativ gesperrt.
8. Echter LanguageTool-6.8-Bestand 43 wird hashgebunden wiederhergestellt und ausgeführt.
9. Echter PPM 6.7.9 wird ausschließlich über `controller fullcheck` ausgeführt.
10. Batch -> V2-Handoff -> Inline-Pack/Unpack -> SHA-/Bytegleichheit ist Teil der Abnahme.
11. Für den vollständigen Testpfad wurde ein eigener Hard-Boundary-Test ergänzt, der direkte und indirekte Abhängigkeiten zu dem ausdrücklich verbotenen SEO-Provider DataForSEO im ausgeführten Startknopf-/Worker-/Workflow-Pfad blockiert. Der bestehende, fachfremde SEO/PAA-TODO außerhalb dieser Route bleibt historische/andere Facharbeit und ist keine Runtime-Abhängigkeit.
12. Der frühere Zielvertrag vom 13.09. wurde ausdrücklich als historisch abgelöst markiert; `CODEX_LIVE_TASK.md` verweist jetzt ausschließlich auf den Zielvertrag vom 14.09.

## WARUM

Die Teststrecke darf nicht wieder an einer Stelle beginnen, die im echten Lauf erst später erreicht wird. Deshalb ist die Abnahme nur belastbar, wenn der eine Einstieg selbst Root, Supervisor, Worker-Grenze, maschinelle Bindungen, echte Prüfer und den finalen Dateitransport umfasst.

Der Worker darf keine Route, Prüfer, Kategorie, Links oder PASS bestimmen. Er liefert nur die fachlichen Worker-Artefakte an den jeweils freigegebenen Phasen. Bekannte Anforderungen werden vor dem Schreiben maschinell gebunden, soweit sie vorab bestimmbar sind.

## Tatsächlich ausgeführte Prüfungen

### Remote-Code-Head

`8e1a03361b8a59aa76f12e0a0ff985b3688e0cb5`

### GitHub Actions

Run `34865422904` -> **SUCCESS**.

Auf genau diesem Code-Head vollständig ausgeführt:

- Python-Syntax: PASS;
- Point-0 PREPARED->FINAL hard boundary: PASS;
- Point-0/Supervisor/Controller hard boundary: PASS;
- Maschinen-Produktionsbindung: PASS;
- Single-Button harte Negativstrecke: PASS;
- verbotener SEO-Provider hard boundary: PASS;
- kompletter bestehender System-4-Unittestbestand: PASS;
- exakter LanguageTool 6.8 / Bestand 43: PASS;
- echter LT-6.8-/PPM-6.7.9-Real-Korridor: PASS;
- separater Drei-neue-Themen-Real-Korridor: PASS;
- Single-Button ein weiterer neuer Artikel bis Datei: PASS;
- Single-Button drei weitere neue Artikel bis Datei: PASS;
- Batch/Handoff/Inline-Unpack/Bytegleichheit: PASS.

### Zusätzliche neue Startknopf-Themen

Einzelartikel:
- `Haftpflicht für Pferde bei Pflegebeteiligung`.

Anschließender separater Dreier-Batch:
- `Fliegenmasken für Pferde an sonnigen Tagen`;
- `Pellets aus Luzerne für Pferde im Winter`;
- `Haftpflicht für Pferde bei Betreuung im Urlaub`.

## Neue Fehler dieses Arbeitslaufs

### 1. Worker-Start lag zunächst außerhalb des vollständigen Startknopfwegs

Status: **BEHOBEN**.

Ursache: Der Worker-Einstieg war als separate Grenzfunktion vorhanden, wurde aber nicht vom einen Full-Route-Start selbst durchfahren.

Fix: Worker-Start und die phasengetrennten Worker-Aufrufe wurden in `full_route_start.py` eingebunden. Negativfälle für fehlenden Worker und ungebundene Worker-Research-Ausgabe wurden ergänzt.

### 2. Mehrartikel-Einstieg war zunächst nicht durchgehend artikelindexgebunden

Status: **BEHOBEN**.

Fix: Artikelindex wird durch Root -> Supervisor -> Receipt -> Worker-Dispatch -> Controller gegen den gebundenen Snapshot geprüft. Out-of-range blockiert vor gültigem Controller-State.

### 3. Neue Dreier-Abnahme: `BLOCKED_WAVE2_CONCLUSION_BALANCE`

Status: **BEHOBEN**.

Befund: Der erste Artikel des zuletzt neu gewählten Dreier-Testbatches erreichte echten PPM 6.7.9 und wurde wegen Fazitbalance korrekt blockiert.

Fix: Ausschließlich der kontrollierte Test-Worker-Draft wurde im Conclusion-Block verlängert und danach erneut gegen den unveränderten Authoring-Contract validiert. PPM/Textmaschine/Grenzwerte wurden nicht verändert. Gesamter Workflow anschließend PASS.

## Negativregressionen

Weiterhin fail-closed gebunden sind insbesondere:

- Legacy-/Direktstart;
- Root-/Head-/Manifest-/Critical-File-Abweichung;
- Source-Hash-/Source-Pool-Manipulation;
- ungebundene Research-Ausgabe;
- fehlender Worker;
- falsche Quellenanzahl;
- falscher Artikelindex;
- unbekannte oder unbelegte Fact-IDs;
- Context-/Authoring-Contract-Manipulation;
- externe Quality-/Link-Bindung;
- Designabweichung;
- zu breite Repair-Umschreibung;
- Batch-Mismatch / Wiederholung;
- Handoff-/Inline-/Hash-/Byte-Manipulation;
- verbotene Provider-Abhängigkeit im ausgeführten Full-Route-Testpfad.

## Abgrenzung zum offiziellen LIVE-Stand

`control/CURRENT_STARTMASTER.json` zeigt weiterhin auf STARTMASTER0107 und dessen `control/startmaster0107/CURRENT_STATE.json`. Diese LIVE-Wahrheit wurde in diesem Hobbyraum-Chat nicht geändert oder als PASS überschrieben.

Der hier bewiesene System-4-Stand ist ein isolierter Remote-Testkandidat. Kein Merge und kein Publish wurden ausgeführt. `publish_allowed=false` bleibt verbindlich.

## Offener Beweis / NEXT ACTION

Der Single-Button-Abnahmetest verwendet einen kontrollierten Test-Worker an derselben gebundenen Worker-Schnittstelle. Ein realer Codex-Produktionsarbeiter wurde in diesem Abschlusslauf **nicht** ausgeführt.

NEXT ACTION ist deshalb ausschließlich: auf dem unveränderten, vollständig vorgeprüften Kandidaten genau einen real gebundenen Codex-Artikel über dieselbe Worker-Schnittstelle laufen lassen; keine Architekturänderung davor. Nur mit ausdrücklicher Nutzerfreigabe. Bei einem echten Fehler fail-closed und nur Same-Article-Repair gemäß bestehendem Vertrag.

## Nicht betroffen

Keine Pluginentwicklung und kein Pluginupdate in diesem Arbeitslauf. Das PLUGINS-Büro bleibt unverändert.
