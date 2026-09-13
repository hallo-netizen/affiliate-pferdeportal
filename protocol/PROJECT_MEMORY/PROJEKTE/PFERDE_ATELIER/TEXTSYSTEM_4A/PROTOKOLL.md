# TEXTSYSTEM 4A – PROTOKOLL

## 2026-09-13 – Büroanlage / Architekturprüfung

### Frisch geprüfter System-4-Stand
- PR #238 offen, Draft, nicht gemergt.
- Branch `hobbyroom/system4-true-single-room-v1`.
- Head bei Prüfung: `77c02a9df1745a28157fcc27f65f74e9c4fb1153`.
- Aktueller Status laut System-4-README: BLOCKED bis kompletter aktueller Unittest- und E2E-Nachweis.
- Einzelartikelkern inzwischen: kanonischer State, feste Phasen, Research/Facts/Context/Draft/Fullcheck/Repair, Same-Article-Repair, Content-/Design-Guard intern, echter Production-Fullcheck zentral.

### Wichtige Korrektur gegenüber früherer 4a-Idee
Separate Python-Module sind nicht automatisch echte Handoffs. `content_guard` und `design_guard` werden im aktuellen System-4-Controller direkt als interne Prüfer aufgerufen. Die Existenz mehrerer Dateien allein ist daher kein ausreichender Grund für 4a.

### Korrektur nach Nutzerprüfung
Die aktuell in System 4 noch vorhandene feste Bindung auf sieben Artikel und `Beratung` ist **kein Entscheidungskriterium für 4a**. Diese Bindungen werden in System 4 separat entfernt und dürfen daher nicht als struktureller Vorteil von 4a gewertet werden.

### Gültiger 4a-Prüfmaßstab
4a muss gegen ein **bereinigtes System 4** bestehen. Maßgeblich sind nur:
1. echte Laufzeit-/Zustandsautoritäten;
2. echte Übergabegrenzen mit Re-Bindungs-/Interpretationsrisiko;
3. Außenfreiheit bzw. Möglichkeit externer Workflow-Steuerung;
4. Vollständigkeit des Weges Produktionsanstoß → Recherche → Fakten → Text → echte Prüfer → Repair → Querschnitt → WordPress-Datei → Elternchat;
5. unveränderte Inhalts-, Design- und Qualitätsautorität;
6. Flexibilität für neue Beitragsarten;
7. Automatisierbarkeit und Wiederanlauf ohne Neustart des Gesamtprozesses.

### Historische Sackgassen, die nicht wiederholt werden dürfen
1. H7/H8: starke Ein-Tür-Sicherheit, aber viele Räume/Tokens/Receipts/Packages und dadurch neue Übergabeprobleme.
2. Signer-/Producer-Schleifen: derselbe fehlende Anschluss wurde unter neuen Namen wiederholt gesucht; Erklärung wurde mit Fortschritt verwechselt.
3. Alte Workflowgenerationen: neue Runner/Gates/Signer als Reaktion auf einzelne Blocker führten zu Schutzarchitektur statt Produktion.
4. Chat-Drift: textuelle Verbote reichten nicht; der ausführende Chat übernahm trotzdem Planungshoheit.
5. Schlechter früher System-4-7er-Lauf: zu schwache Recherche-/Fact-Pack-Bindung plus artikelübergreifende Textschablonen; Einzelartikelprüfer allein reichten nicht.
6. Falsche Autoritätsinterpretation: statische Hinweise wurden zeitweise stärker gewichtet als der tatsächlich gebundene aktuelle Prüferzustand.

### Neuer struktureller Befund im aktuellen System-4-Controller
Der Controller bietet technisch mehrere Produktions-/Ausgangswege an:
- BASIC: `check` → `release`;
- FULL: `fullcheck` → `OUTPUT_GATE_REQUIRED`;
- SIGNED: `prepare-release` → `SIGNATURE_REQUIRED` → `finalize-signed`.

Der verbindliche System-4-Zielvertrag beschreibt dagegen nur den FULL-Weg mit anschließendem Batch-/Direct-Import-Handoff und erklärt Signing für diesen Pfad ausdrücklich als ausgeschaltet.

**Folgerung:** Der relevante Härtungsbedarf ist nicht eine neue 4a-Maschine, sondern die Entfernung technisch erreichbarer Parallelstraßen aus Konzept 4.

### WordPress-Importer 0.28.23 frisch geprüft
Library-ZIP:
`portal-seo-editorial-plan-compiler_0.28.23_SYSTEM4_DIRECT_IMPORT.zip`

SHA-256:
`22a8459b64db488852841d894d887ec51e531a0872ee5f33afdd64e43a8a8c7f`

Ergebnis:
- generischer Zielvertrag `SYSTEM4_WORDPRESS_HANDOFF_V1` bereits vorhanden;
- Importer verlangt mindestens einen Artikel, keine feste 7er-Grenze;
- `article_type` ist gebunden, aber nicht auf `Beratung` hardcodiert;
- vor erstem Write werden Kategorie, Slug und Kollisionen aller Artikel geprüft;
- nur WordPress-Drafts;
- finaler Content-Hash und Metadaten werden per Readback kontrolliert;
- bei Fehler werden bereits erzeugte Posts des Imports zurückgerollt;
- Redaktionsplan wird weder gelesen noch beschrieben;
- `publish_allowed=false`.

Der vorgelagerte `PSERC_TEXTMACHINE_METADATA_BATCH_V2` übergibt exakt fünf skalare Felder (`title`, `target_keyword`, `category`, `article_type`, `plan_slot`), verbietet Inhalts-/Design-/Promptpayload und setzt Artikelgrenzen auf 0 = unbegrenzt.

Details dauerhaft in `WORDPRESS_HANDOFF.md`.

### Architekturentscheidung
**Ein eigenständiges 4a-System wird aktuell verworfen.**

Die 4a-Zielidee bleibt als Audit-/Härtungsmaßstab bestehen. Konzept 4 soll selbst auf folgende Form reduziert werden:
`1 Controller + N Artikelzustände + unveränderte Prüfer als interne Aufrufe + 1 finaler generischer WordPress-Ausgang`.

Das ist keine fünfte Textmaschine, sondern die Bereinigung des bereits weitgehend passenden Konzept 4.

### Teststatus
Noch kein neuer System-4-Gesamt-PASS. Diese Architekturprüfung und die WordPress-Codeprüfung sind kein Produktionsfreigabenachweis.
