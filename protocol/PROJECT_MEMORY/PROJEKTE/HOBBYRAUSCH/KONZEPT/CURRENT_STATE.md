# HOBBYRAUSCH – KONZEPT – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-09-30
STATUS: BUCHBINDEN INTENT-OWNERSHIP GESETZT / V1.9.1 OWNER-HANDOFF IMPLEMENTIERT / TEXT-DUBLETTENGATE + FAQ-DATENPRÜFUNG OFFEN

## Rolle

Einzige aktuelle Zustandsautorität des Scopes `HOBBYRAUSCH_KONZEPT`.

## Aktueller belastbarer Stand

Aktueller Markenname: **Hobby Depot**.

Verbindliche Arbeitsbasis:
`KATEGORIEN_ARBEITSBASIS_UND_PILOTREGELN_20260930.md`

Buchbinden-Pilot:
`BUCHBINDEN_INTENT_OWNERSHIP_MATRIX_20260930.md`

Technische Prüfung:
`BUCHBINDEN_TECHNISCHE_INTENT_ABSICHERUNG_20260930.md`

### Struktur

**Gestalten · Fertigen · Technik · Forschen · Pflanzen · Tiere · Bewegen · Sammeln**

Harte Tiefe:
**SEITE → SEITE → SEITE → KATEGORIE → BEITRÄGE**

Keine weitere Kategorieebene.

### Buchbinden – fachliche Owner-Regel

**Ein Beitrag = ein primärer Intent = ein eindeutiger Kategorie-Owner.**

Für Buchbinden gilt:
- Einstieg = Startentscheidung;
- Ausrüstung = Werkzeugentscheidung;
- Material = Materialentscheidung;
- Techniken/Praxis = Durchführung/Methodenwahl;
- Fragen/Probleme = Fehlerbehebung;
- FAQ = ausschließlich belegte Restfragen ohne anderen Owner.

**Eine Frageform macht noch keinen FAQ-Intent.**

### Technische Umsetzung – jetzt vorhanden

Kategorie-Workflow V1.9.1 derselben allgemeinen Pluginlinie ist lokal hart geprüft.

Neu:
- allgemeine Kategorie-Owner-Registry;
- `ARTICLE_ONLY` kann an `owner_concept_id` gebunden werden;
- gleicher exakter Artikel-Intent bei mehreren Ownern wird im Editorial-Handoff blockiert;
- ungebundene ARTICLE_ONLY-Intents bleiben sichtbar offen;
- Residual-Research wird nie automatisch Artikel;
- keine Hobby-Depot-Begriffe hardcodiert;
- kein neues Plugin.

Prüfung:
248/248 PASS, Fresh-Unpack 248/248 PASS.

### Noch offen

`HOBBYRAUSCH/TEXT_REDAKTION` ist weiterhin fachlich/technisch noch nicht als Produktionssystem gebunden.

Deshalb fehlt noch der **Downstream-Artikelgate** für:
- semantisch gleiche Intents mit anderer Formulierung;
- bereits geplante/vorhandene Artikel;
- Keyword-/Intent-Kannibalisierung vor Textproduktion.

FAQ-Tragfähigkeit bleibt datenoffen:
mindestens 3, bevorzugt 4+, eigenständige Restintents müssen real belegt werden; sonst nicht künstlich auffüllen.

## Erster offener Blocker

Nicht mehr das Kategorie-Plugin.

Offen ist jetzt die **allgemeingültige Text-/Redaktionsprüfung**, die den V1.9.1-Handoff konsumiert und vor Artikelerstellung semantische Dubletten/Kannibalisierung fail-closed blockiert.

## NEXT ACTION

Kein weiteres Kategorie-Plugin bauen.

Als Nächstes den allgemeinen Downstream-Artikelgate auf den V1.9.1-Handoff binden und danach Buchbinden als ersten Realfall durch DataForSEO-/SERP- und Ownership-Prüfung laufen lassen.
