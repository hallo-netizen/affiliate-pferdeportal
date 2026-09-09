# PRODUKTVERGLEICH -> SEO/TEXT -> ACM – ÜBERGABEKONZEPT V1

Stand: 2026-09-09
Status: KONZEPT / KEINE PRODUKTIONSADOPTION
Arbeitsbasis Produktvergleich: `hobbyroom/productvergleich-workflow-v070-20260908` @ `5d6863a9fe9b9082c1111debc22cde96191a34eb`

## Ziel

Produktvergleich wird als neue gebundene Beitragsart an die vorhandene Textmaschine/Fachworkflow-Kette angeschlossen, ohne eine zweite Textmaschine, einen zweiten Controller oder ein zweites Produktions-Handoff zu bauen.

Zielkette:

`Produktwissen -> Produktvergleichsdossier -> SEO/TEXT-Fachworkflow -> bestehende FACHWORKFLOW_HANDOFF_REQUEST.json -> ACM -> externe Signatur -> WordPress-DRAFT -> Readback/DOM -> Nutzerreview -> STOP`

Kein Auto-Publish.

## 1. Büro PRODUKTVERGLEICH – Fachpaket

Verantwortet ausschließlich die produktvergleichsspezifische Fachwahrheit:

- exakte Produkte/Varianten;
- Herstellerfakten und Quellenstatus;
- Vergleichbarkeit;
- erlaubte Vergleichsmerkmale;
- erlaubte Bedarfszuordnungen;
- verbotene/unbelegte Schlussfolgerungen;
- Vergleichsregeln/Ruleset;
- Produktvergleichs-spezifische SEO-Eignung als gebundenes Signal.

Ausgabe:
ein vollständig gebundenes Produktvergleichsdossier plus Ruleset-/Versions-/Hashbindung.

PRODUKTVERGLEICH schreibt im Zielbetrieb nicht den fertigen Artikel und erzeugt keinen eigenen produktiven WordPress-Draft.

## 2. Büro SEO/TEXT – Beitragsart und Textproduktion

Verantwortet:

- Artikeltyp-Vertrag `Produktvergleich`;
- Aufbau/Abschnittsreihenfolge;
- Überschriften-/Tabellenvertrag;
- Sprach-/Stilregeln;
- SEO/Target Keyword;
- interne Links;
- LanguageTool;
- Dubletten/Kannibalisierung;
- bestehende allgemeine Textmaschinen- und Qualitätsregeln.

Es liest das gebundene Produktvergleichsdossier als Fachinput.

Ausgabe:
der normale Fachworkflow mit den bestehenden Stage-Proofs und der bestehenden Produktionsübergabe.

Hard Rule:
Bestehende Beitragsarten und bestehende Textmaschinenregeln werden nicht verändert. Produktvergleich wird als neuer gebundener Artikeltyp ergänzt.

## 3. Übergabepunkt SEO/TEXT -> ACM

Einzige Produktions-Eingangswahrheit bleibt:

`FACHWORKFLOW_HANDOFF_REQUEST.json`

Vertrag:
`PFERDE_ATELIER_FACHWORKFLOW_HANDOFF_REQUEST_V1`

Keine 17. Top-Level-Eigenschaft.
Kein neues Jobmanifest.
Kein zweites Handoff-Format.

Der Vergleichskontext muss innerhalb der bereits vorhandenen Produktionskontexte gebunden werden, insbesondere `fact_pack` und/oder `production_plan_item`. Die exakte interne Zuordnung wird erst nach Schema-/Fixture-Prüfung im SEO/TEXT-Büro festgelegt und positiv/negativ getestet.

## 4. Büro ACM – Transport/Orchestrierung

ACM entscheidet nichts Fachliches.

Es nimmt ausschließlich die bestehende Handoff-Datei an und führt die gebundene technische Reihenfolge aus:

`Handoff -> PPM prepare(no write) -> externe Signatur -> WordPress-Verifikation -> Draft -> Readback/DOM -> STOP`

ACM darf weder Produkte, Fakten, Artikeltyp, Regeln, Text, Route, Validator noch Publishstatus frei wählen.

## 5. Büro AFFILIATE – Commerce-Schicht

Affiliate ist nicht Teil der fachlichen Textwahrheit.

Es liest nur exakte Produktidentitäten und liefert separat:

- aktuelles Angebot;
- Preis;
- Verfügbarkeit;
- Händler;
- Tracking/Affiliate-Link.

Affiliate darf Produktvergleich, Herstellerfakten oder Textregeln nicht verändern.

## 6. Testverantwortung – keine Doppelprüfung

### PRODUKTVERGLEICH testet seinen Ausgang
Positiv:
- exakte Identitäten;
- vollständige belegte Vergleichsfakten;
- gültiges Ruleset;
- erlaubte Bedarfszuordnung.

Negativ:
- Identitätsdrift;
- Fakten-/Ruleset-Hashdrift;
- nicht vergleichbare Produkte;
- Quellenkonflikt/fehlende Pflichtinformation;
- unbelegte Schlussfolgerung;
- SEO nicht geeignet -> kein Produktionsauftrag.

### SEO/TEXT testet seine Verarbeitung
Positiv:
- Produktvergleichsdossier wird als gebundener Input angenommen;
- Artikeltyp `Produktvergleich` erzeugt regelkonformen Text;
- alle bestehenden Qualitätsgates PASS.

Negativ:
- Pflichtdossier fehlt;
- Artikeltyp/Dossier passen nicht;
- ungebundene Fakten oder freie Textstruktur;
- LanguageTool/SEO/Links/Tabelle/etc. nicht PASS -> BLOCK.

### ACM testet nur die technische Übergabe
Positiv:
- exakte bestehende 16-Feld-Handoff-Datei -> gebundener Prepare/Sign/Write/Readback-Weg.

Negativ:
- Feld fehlt/zusätzlich;
- Identitäts-/plan_slot-Drift;
- Hash-/Signaturfehler;
- zusätzliche/geänderte Datei;
- Replay;
- Publishversuch -> BLOCK.

### Integrationsabnahme
Ein realer Produktvergleich läuft einmal vollständig durch:
`Produktvergleich -> SEO/TEXT -> bestehender Handoff -> ACM -> signierter WordPress-DRAFT -> Readback`.

Erst dieser Lauf ist Gesamt-PASS.

## 7. Kommunikation zwischen den Büros

Chats kommunizieren nicht direkt miteinander und sind keine Wissensquelle.

Der GitHub-Aktenbestand ist der Briefkasten.

Ablauf:
1. sendendes Büro schreibt seinen freigegebenen Vertrag/Befund in seinen Aktenschrank;
2. Nutzer gibt dem empfangenden Chat nur den Verweis: Büro + Branch + Dateipfad;
3. empfangender Chat liest die Datei selbst direkt aus GitHub, nicht aus Chat-Erinnerung;
4. empfangendes Büro dokumentiert ACCEPTED oder BLOCKED mit Begründung in seinem eigenen Aktenschrank;
5. keine gegenseitigen Branch-Änderungen;
6. erst nach beidseitig geprüftem Vertrag erfolgt ein kontrollierter Integrationsschritt.

Praktischer Übergabesatz an den Nachbarchat:

`Campus -> Pferde Atelier -> SEO/TEXT/ACM. Lies den Produktvergleich-Übergabevertrag read-only aus branch hobbyroom/productvergleich-workflow-v070-20260908 unter protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/PRODUKTVERGLEICH/AKTENSCHRANK/01_UEBERGABEKONZEPT_PRODUKTVERGLEICH_TEXT_ACM_V1.md. Prüfe ihn gegen den aktuellen autoritativen SEO/TEXT-/ACM-Stand. Produktvergleich-Branch nicht verändern. Ergebnis ACCEPTED oder BLOCKED in deinem eigenen Aktenschrank dokumentieren.`

## 8. Reihenfolge ab jetzt

1. Im PRODUKTVERGLEICH-Büro die noch offenen Fach-/Artikelanforderungen schließen.
2. Noch keinen produktiven Writer-/WordPress-Weg weiterbauen.
3. ACM/SEO-TEXT im Nachbarbüro vollständig abschließen und hart testen.
4. Nachbarbüro liest diesen Vertrag und prüft Anschlussfähigkeit.
5. SEO/TEXT ergänzt den gebundenen Artikeltyp `Produktvergleich` und die minimale Dossier-Abbildung in den bestehenden Handoff.
6. Positive/negative Fach- und Schnittstellentests.
7. Ein vollständiger Realtest bis WordPress-DRAFT/Readback.
8. Erst danach Produktionsadoption/ggf. Mergeentscheidung.

## Leitsatz

**Produktvergleich liefert die geprüften Zutaten. SEO/TEXT kocht nach festem Rezept. ACM transportiert nur. Der bestehende Handoff ist die einzige Tür.**
