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


## Arbeits-/Fehlerprotokoll dieses Strangs

1. **6.72.189 war noch kein harter KISS-Vertrag.**
   - Ziel-URL wurde zwar importseitig ermittelt/gespeichert.
   - Runtime enthielt weiterhin eigene URL-Semantik, Provider-Themen-Vorrang und allgemeinen Banner-Fallback.
   - Folge: Der Nutzerhinweis „Ziel-URL einmal zuordnen und danach nur speichern/lesen“ war nicht vollständig umgesetzt.
   - Status: abgelöst durch 6.72.190.

2. **ADCELL-Kategorien-API war ein unnötiger Zwischenweg.**
   - Der Weg über Promotion-Kategorien löste nicht den gewünschten einfachen Ziel-URL-Vertrag.
   - Status: für den Hard-KISS-Bannerweg verworfen.

3. **Lokaler MariaDB-Nachladeweg war unnötig.**
   - Der Container besaß keine passende DB-Laufzeit.
   - Statt neue Infrastruktur zu bauen wurde der vorhandene GitHub-WordPress/MariaDB-Runner wiederverwendet.
   - Status: korrigiert; keine neue Testarchitektur.

4. **Final-ZIP-Test hatte einen temporären Shell-Tippfehler.**
   - Die OK-Zählzeile im temporären Workflow war falsch formuliert.
   - Nur Testworkflow betroffen, kein Produktcode.
   - Status: korrigiert; Final-R2 Run 37444152532 PASS.

5. **Unnötiger Live-Read-only-Probe-Versuch nach Nutzerkritik.**
   - Der Probe-Weg war nicht erforderlich, um den vom Nutzer verlangten Hard-KISS-Vertrag zu definieren.
   - Kein Produktiv-Schreibzugriff und kein Live-Ergebnis als Fixbeweis verwendet.
   - Status: verworfen; nicht Teil der Abnahme.

6. **Current Generation 221 enthielt eine guard-ungültige freie NEXT-ACTION-Konstante.**
   - `MANUAL_WORDPRESS_INSTALL_6_72_190` in `authorized_next_action`.
   - Negativ: Run 37444424717 -> `AUTHORIZED_NEXT_ACTION_INVALID`.
   - Fix: Generation 222 -> `RUN_BOUND_RELEASE_GATES`; konkrete manuelle Installation nur in `bound_user_scope_action`.
   - Positiv: Run 37445573248 -> Affiliate governance check PASS.

## Plugin-Referenz

Plugin-ID / Verzeichnis:
`affiliate-portal-router`

Name:
Affiliate-Zentrale / Pferdeportal Affiliate Router

Änderung:
6.72.189 -> 6.72.190

WARUM:
HARD RULE vollständig erzwingen: Import -> Ziel-URL -> einmalige feste Portalziel-Zuordnung -> speichern; Runtime ausschließlich gespeicherte Zielkarte.

Aktuelles Release-Artefakt:
`release/affiliate-zentrale/artifacts/final/AFFILIATE_ZENTRALE_6.72.190.zip`

SHA-256:
`1a4939c91f60a7f526bc713f63719cb1cd3da88d575b7b2ec79cf063f530c1e3`

Vorheriger 6.72.189-Installer:
`release/affiliate-zentrale/artifacts/final/AFFILIATE_ZENTRALE_6.72.189.zip`

6.72.189 SHA-256:
`0589746569fcbec900cfae6e46ad501ea9f5a0311b04762caea3e9b2e8a60b94`

Rollback:
Nur auf den exakt gebundenen vorherigen Installer zurückgehen; keine Mischstände einzelner Dateien.

Hinweis:
Die technische Release-/Live-Wahrheit bleibt in der Affiliate-Release-Autorität. Eine separate PLUGINS-Büro-Ausgabekopie ist hier nicht als zweite Current-Wahrheit zu behandeln.
