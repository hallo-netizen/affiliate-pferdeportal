# HOBBYRAUSCH – KONZEPT – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-09-30
STATUS: BUCHBINDEN E2E OWNERSHIP LOKAL PASS / V1.9.1 + PSTE 0.57.14 TECHNISCH VERKETTET / PROBLEME + FAQ DATENLÜCKE / LIVE-ABNAHME OFFEN

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

Lokaler Realtest mit vorhandenen DataForSEO-Daten:
`BUCHBINDEN_E2E_OWNERSHIP_REALTEST_20260930.md`

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

`HOBBYRAUSCH/TEXT_REDAKTION` ist jetzt auf **PSTE 0.57.14 Editorial Ownership Gate / lokal HARD PASS** gebunden.

Der allgemeine Downstream-Artikelgate ist damit lokal implementiert für:
- eindeutigen `owner_concept_id`;
- verpflichtenden `semantic_intent_key` vor Artikelpromotion;
- semantisch gleiche Intents mit anderer Formulierung;
- bestehende exakte/answer-equivalente Dubletten;
- Frageform ohne automatische FAQ-Owner-Autorität.

Lokaler End-to-End-Test V1.9.1 → PSTE 0.57.14 mit realen Buchbinden-Keywords: PASS.

Belegt:
- richtige Owner passieren;
- falsche FAQ-Zuordnung wird bei exakter oder semantischer Doppelbelegung BLOCKED;
- Frageform besitzt keine FAQ-Autorität;
- fehlender `semantic_intent_key` wird fail-closed blockiert.

DataForSEO-Befund aus dem vorhandenen 50-Keyword-Buchbinden-Set:
- Einstieg: Evidenz vorhanden;
- Ausrüstung: Evidenz vorhanden;
- Material: Mindestbreite vorhanden;
- Techniken/Praxis: Evidenz vorhanden;
- Fragen/Probleme: DATA GAP;
- FAQ: DATA GAP.

FAQ-Tragfähigkeit bleibt daher offen: mindestens 3, bevorzugt 4+, eigenständige Restintents müssen real belegt werden; sonst nicht künstlich auffüllen.

Die reale WordPress-Abnahme des technischen Anschlusses ist weiterhin offen.

## Erster offener Blocker

Kein Entwicklungsblocker mehr im Kategorie- oder Ownership-Gate.

Technischer lokaler E2E-Blocker besteht nicht mehr.

Offen sind jetzt:
1. reale WordPress-Abnahme V1.9.1 → PSTE 0.57.14;
2. gezielte Nachrecherche für **Fragen/Probleme** und **FAQ**, weil der vorhandene DataForSEO-Bestand dort noch keine ausreichende Tragfähigkeit belegt.

## NEXT ACTION

Kein weiteres Plugin bauen.

Als Nächstes keine weitere Pluginentwicklung.

1. V1.9.1 live sauber zurückrollen/retesten und Editorial-Handoff in PSTE 0.57.14 importieren.
2. Parallel nur die fehlenden Buchbinden-Research-Räume **Fragen/Probleme** und **FAQ-Restintents** nachrecherchieren.
3. Erst danach finale Buchbinden-Leaf-Freigabe.
