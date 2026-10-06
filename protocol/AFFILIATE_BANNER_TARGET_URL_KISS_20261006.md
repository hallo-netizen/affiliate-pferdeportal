# Affiliate-Banner – Ziel-URL-KISS-Vertrag

Datum: 06.10.2026

Rolle: dauerhafte WAS/WARUM-Entscheidung. Keine CURRENT-Wahrheit.
Aktueller Status und genau eine NEXT ACTION stehen ausschließlich in:
`control/release-governance/CURRENT_RELEASE.json`.

## Zielvertrag

HARD RULE für automatische Banner:

`Import -> Ziel-URL -> einmalige Zuordnung zu festen Portalzielen -> speichern`

Danach gilt:
- Runtime liest ausschließlich die gespeicherte feste Portalziel-Zuordnung.
- Keine Ziel-URL-Neuklassifikation im Frontend.
- Kein Provider-Thema als Runtime-Vorrang.
- Kein allgemeiner Banner-Fallback.
- Ohne gespeicherte feste Zielzuordnung: keine automatische Bannerausspielung.

## Warum

Die frühere Kombination aus Ziel-URL-Evidenz, Provider-Themen und allgemeinen Fallbacks konnte trotz lokal korrekter Rankingtests fachlich falsche Live-Banner zulassen. Der KISS-Vertrag reduziert die Entscheidung auf einen einmaligen Import-/Planungsschritt und macht die spätere Ausspielung deterministisch.

## Performance- und Datenbank-Hardlocks

- keine neue Tabelle;
- keine neue Spalte;
- keine URL-Historie;
- kein Frontend-HTTP zur Zielbestimmung;
- keine neue Frontend-DB-Abfrage;
- nach einem Importbatch genau eine gebündelte Abfrage der betroffenen Banner;
- Zielzuordnung wird in der vorhandenen Creative-Library gespeichert;
- Wiederholung erzeugt keine zusätzlichen Creative-Zeilen oder Target-Records.

## Umsetzung

Version 6.72.190:
- Importpfad ermittelt bzw. übernimmt die reale Ziel-URL.
- Nach dem Importbatch werden betroffene Banner einmal gebündelt geladen.
- Für jeden Banner werden feste Portalziele einmalig aus der Ziel-URL abgeleitet und in `topic_targets` gespeichert.
- Runtime-Funktion für Banner verwendet nur noch diese gespeicherte Map.
- Fehlt die Map, wird fail-closed nicht ausgespielt.
- eigener versionsgebundener 6.72.190-Nachlauf, damit frühere 6.72.189-done-Zustände den Neuaufbau nicht unterdrücken.

## Nachweis

Real WordPress/MariaDB:
- Run 37443761578: PASS.
- Run 37444152532: PASS einschließlich finalem ZIP-Build.

Belegt:
- Reithelme-Ziel-URL -> festes Portalziel Reithelme;
- Schabracken-Ziel-URL -> festes Portalziel Schabracken;
- fehlende gespeicherte Zielkarte -> keine Runtime-Ermittlung/keine Ausspielung;
- Wiederholung -> keine zusätzlichen Target-Records;
- keine zusätzliche Creative-Zeile;
- keine neue Tabelle/Spalte.

Evidence:
`release/affiliate-zentrale/evidence/affiliate_router_v672190_hard_kiss_banner_target_map_20261006.md`

Finaler Installer:
`release/affiliate-zentrale/artifacts/final/AFFILIATE_ZENTRALE_6.72.190.zip`

SHA-256:
`1a4939c91f60a7f526bc713f63719cb1cd3da88d575b7b2ec79cf063f530c1e3`

## Nicht wiederholen

- Ziel-URL nicht bei jedem Seitenaufruf neu auswerten.
- Keine Banner-Kategorie-/Provider-Metadaten vor die gespeicherte Zielkarte setzen.
- Kein allgemeiner Fallback für Banner ohne gespeicherte Zielkarte.
- Kein neuer Poller.
- Keine neue Banner-Datenbank.
- Keine neue URL-Historie.
- Kein Portal-Live-Test als Ersatz für den Import-/Persistenzvertrag.

## Tarifcheck

Tarifcheck wurde in diesem Arbeitsstrang nur konzeptionell angesprochen und NICHT implementiert.
Die gezeigten Tarifcheck-Codes sind kein Bestandteil von 6.72.190 und keine NEXT ACTION dieses Scopes.
