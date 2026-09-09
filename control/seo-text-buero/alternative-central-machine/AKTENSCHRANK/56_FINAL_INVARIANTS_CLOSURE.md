# ACM – ABSCHLUSS OFFENE PUNKTE / HARTE INVARIANTEN

Stand: 2026-09-09
Status: TECHNISCHE ABSCHLUSSPRÜFUNG PASS – KEINE PRODUKTIONSFREIGABE

## Verbindliche Entscheidungen

### 1. Artikelzahl
ACM besitzt kein fachliches oder architektonisches 7-Artikel-Limit.

Ziel:
- beliebige endliche Batchgröße
- Begrenzung ausschließlich durch reale Ressourcen
- Verarbeitung itemweise wiederholbar
- keine feste Artikelzahl im Controller

Bereits bewiesen:
- P34 akzeptiert einen signierten 1000-Item-Batch
- kein MAX_ITEMS/MAX_ARTICLES/BATCH_LIMIT in der ACM-Batchlogik
- 7/7 war ausschließlich Regression gegen den historischen Goldstand

Der vorhandene allgemeine Endstempel-Finalizer berechnet article_count dynamisch aus dem gebundenen Receipt.
Sein historischer Dateiname enthält noch "7_ARTIKEL"; dieser Name darf bei ACM-Produktionsübernahme nicht als Mengenvertrag übernommen werden.

Verbindliches ACM-Ziel für die Enddatei:
- neutraler, artikelzahlunabhängiger Dateiname
- Inhalt/Manifest bindet die tatsächliche article_count

### 2. Chat-/Codex-Freiheit
Verbindlich:
- ChatGPT/Codex besitzt keinerlei freie Workflow-, Navigations-, State-, Projektresultat- oder Publish-Autorität
- keine Auswahl von Route, Validator, Worker, Engine oder Reparaturpfad
- all_other_actions=DENY
- nächster Schritt ausschließlich technisch gebunden
- BLOCKED bedeutet Stop, keine Ersatzroute

Codex-Rolle:
- aktueller Codex-Prozess ist der gebundene Fachworkflow-Worker
- Codex erzeugt im gebundenen Item die realen Facharbeitsprodukte, einschließlich Recherche/fact_pack und finalem Artikel
- Codex darf PASS nicht selbst attestieren
- feste Validatoren und nachfolgende Gates entscheiden PASS/BLOCKED

### 3. Textmaschine / Qualität
Unverändert und autoritativ:
- bestehende Textmaschine
- Artikeltyp-/Strukturregeln
- Recherche/Fact-Pack
- SEO/Target Keyword
- Tabellen
- interne Links
- LanguageTool
- Dubletten/Kannibalisierung
- PPM
- PSERC
- PSTE
- Design/DOM/Readback
- Publish-Sicherheit

Keine ACM-Regel ersetzt oder vereinfacht diese Fachregeln.

### 4. LanguageTool
LanguageTool bleibt pro Artikel verbindlicher Qualitätsbestandteil.

Bestehender Vertrag verlangt:
- LanguageTool 6.8 / Bestand 43
- vollständiger sichtbarer Text
- exakte Raw Evidence
- null ungelöste Findings

ACM darf dieses Gate weder auslassen noch stichprobenartig ausführen.

### 5. Signierung / WordPress
Produktionsziel:
- vorhandener allgemeiner Endstempel-Mechanismus wiederverwenden
- privater Ed25519-Schlüssel ausschließlich externer/GitHub-Signer
- Producer und WordPress besitzen keinen privaten Schlüssel
- WordPress besitzt nur fest vertrauenswürdigen Public Key
- Manifest bindet Batch, Receipt, exaktes Dateiset, Byte-Länge und SHA-256 jedes Artikels
- WordPress verifiziert vor erstem Content-Write
- falscher Schlüssel, falsche Signatur, geändertes Byte, fehlende/zusätzliche Datei, Replay => kompletter BLOCK
- Import atomar/fail-closed
- publish_allowed=false

### 6. Beitragsarten
ACM-Controller ist beitragsart-unabhängig.

Daher sind zusätzliche Beitragsarten grundsätzlich einfacher anschließbar:
- keine Änderung am Zentralcontroller erforderlich, sofern der bestehende Fachworkflow die Beitragsart über seine gebundenen Templates/Contracts kennt
- neue Beitragsart braucht weiterhin einen vollständig definierten Textmaschinen-/Artikeltyp-Vertrag sowie positive/negative Fachtests
- keine freie Beitragsartwahl durch Chat/Codex

Die Erleichterung liegt in der Orchestrierung, nicht in einer Absenkung der Qualitätsanforderungen.

### 7. Menschliche Stichprobe
Später zulässig:
- menschliche Sichtprüfung stichprobenartig

Niemals stichprobenartig:
- Recherche-/Fact-Pack-Gates
- Textmaschinenregeln
- SEO
- LanguageTool
- Links/Tabellen
- Dubletten/Kannibalisierung
- PPM/PSERC/PSTE
- Signatur/Hash
- WordPress-Preimport
- Readback/DOM

## Noch separat vor Produktionsübernahme
- Zielvertrag: Position der externen Signatur offiziell vereinheitlichen
- neutralen finalen Dateinamen festlegen
- realen Workflow-Handoff durch die komplette ACM-Kette testen

Keine neue Architektur erforderlich.


## Harte Abschlussbeweise 2026-09-09

Getesteter ACM-Head:
`9612c7574e20db27bd6295af0c005e3df590cabc`

GitHub Actions:
- Alternative SEO Text P3 Isolated Lab: Run `34335572795` -> SUCCESS
- Alternative SEO Text P8 Signer Isolation Lab: Run `34335572775` -> SUCCESS

Zusätzlicher Endstempel-/WordPress-Test:
`ENDSTEMPEL_FIXED_TESTS_PASS`

Positiv:
- gültiger gebundener Endstempel -> WordPress-Preimport PASS

Negativ jeweils BLOCK:
- ein Zeichen verändert
- falscher Batch
- Datei fehlt
- zusätzliche Datei
- falsche Signiereridentität
- falsche Signatur
- bereits importierter Batch / Replay
- simuliertes Importversagen -> null committed content writes

Weitere bereits im selben grünen Lauf bestätigte Invarianten:
- P34: signierter 1000-Item-Batch akzeptiert
- kein architektonisches Artikelzahl-Limit
- zentrale Steuerung ohne Domainlogik
- keine vom Aufrufer wählbare Route/Validator
- P27: aktueller Codex ist gebundener Fachworkflow-Worker
- Feldsatz des Handoffs nicht zur Laufzeit wählbar
- Content-/Quality-Authority der technischen Steuerung = NONE
- LanguageTool in bestehender Hard-Rule-/Language-Evidence-Struktur gebunden
- LanguageTool required engine: LanguageTool 6.8 / Bestand 43
- vollständiger sichtbarer Text benötigt exakte LanguageTool-Raw-Evidence mit null ungelösten Findings
- erster vollständiger ACM-Einartikeltest weiterhin PASS
- kein Publish

### Ergebnis

Offene technische Konzeptpunkte Signatur, WordPress-Preimport, beliebige Artikelzahl, Chat-/Codex-Autorität und LanguageTool sind für den Prototyp geschlossen.

Noch keine Produktionsübernahme.
Vor Produktionsübernahme bleiben ausschließlich:
1. formale Vereinheitlichung der Signaturposition im Zielvertrag,
2. neutraler artikelzahlunabhängiger Enddateiname,
3. erster realer workflow-produzierter Handoff durch die unveränderte ACM-Kette.
