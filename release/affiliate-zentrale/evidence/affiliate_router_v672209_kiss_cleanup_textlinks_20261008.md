# Affiliate-Zentrale 6.72.209 – KISS-Cleanup + generische Textlink-Platzhalter

Datum: 2026-10-08

## Ziel

Bestehenden funktionierenden Affiliate-Prozess nicht umbauen. Nur nachweislich tote interne Altlasten entfernen, Backend-Navigation vereinfachen und einen allgemeinen zentralen Textlink-Platzhalterweg analog zu den Tarifrechnern ergänzen.

Autoritative Zielquelle:
`protocol/AFFILIATE_RELEASE_BANNER_IMPORT_BASIS_TARGET_20261007.md`, insbesondere Abschnitte 11 und 12.

## Source

Version: `6.72.209`

Source-Manifest:
`e88439cdc9a6fa1cfd4c1a21b156317cae178d99c9d1082e627c803f78721a5f`

Source-Dateien: 28

Getesteter Head:
`818f26becf39d96315d3f4d68b25728b39d41535`

## KISS-Cleanup

- tote Legacy-Konstante `OPTION_EBAY_EXTERNAL_TICK_KEY` entfernt;
- nur intern private Hilfsmethoden mit 0 Aufrufern im gesamten aktuellen Plugin entfernt;
- keine öffentliche Fachfunktion entfernt;
- alte Fachseiten werden direkt unsichtbar registriert statt zuerst sichtbar angelegt und anschließend per `remove_submenu_page()` entfernt;
- alte CSS-Verstecklogik bleibt entfernt;
- keine Änderung an Bannerimport, Creative Library-Fachlogik, Zielzuordnung, Ranking, Produktlogik, Rechnerlogik, Providerlogik, Automation, Reconcile, Health oder Frontend-Runtime.

## Allgemeine Textlinks

Textlinks sind providerneutral und kein LeadAlliance-Sonderweg.

Backend:
- gemeinsamer Bereich `Rechner & Textlinks`;
- Partner/Programm;
- interne Bezeichnung;
- sichtbarer Linktext;
- Affiliate-/Tracking-Link;
- optionale reale Ziel-URL nur zur Dokumentation;
- aktiv/inaktiv;
- stabiler Platzhalter `[affiliate_textlink id="<id>"]`;
- aktive Platzhalter als kopierbare Writer-Liste;
- bearbeiten und löschen.

Runtime:
- unbekannt/inaktiv/ungültig -> leere Ausgabe;
- aktiver Textlink -> zentral gespeicherter Linktext + zentral gespeicherter Tracking-Link;
- `rel="sponsored nofollow noopener"`;
- keine automatische Keyword-Verlinkung;
- kein Frontend-HTTP;
- keine neue Tabelle;
- kein Cron;
- kein Provideradapter;
- eine kleine nicht-autoloadende Option mit Request-Cache.

LeadAlliance wurde im Test lediglich als Beispielpartner verwendet. Es ist nicht im Code fest verdrahtet.

## Tests

Erster Lauf:
`37779116971`

Ergebnis: rot ausschließlich im neuen Textlink-Ausgabetest.

Ursache:
Testfixture verwendete `tracking.example.test`. WordPress akzeptierte diese Test-Domain nicht über `wp_http_validate_url()`. Speicherung, Writer-Registry, Inaktiv-/Negativfälle und alle vorherigen Schritte waren bereits PASS. Plugin-Source wurde nicht geändert.

Korrektur:
Nur Workflow-Testdaten auf eine von WordPress gültige HTTPS-Testadresse geändert. Source-Manifest blieb unverändert.

Finaler Lauf:
`37779421162`

Ergebnis:
**54 PASS / 0 FAIL**

Zusätzlich:
- Exact source and bounded KISS delta: PASS
- Automation/Health invariants unchanged: PASS
- Fresh WordPress + MariaDB: PASS
- Backend navigation positive/negative: PASS
- Textlink Speicherung: PASS
- Textlink Option nicht autoloaded: PASS
- Writer-Registry aktiv/inaktiv: PASS
- stabiler Platzhalter: PASS
- sichtbarer Linktext: PASS
- Tracking-Link-Ausgabe: PASS
- sponsored/nofollow/noopener: PASS
- optionale Ziel-URL nicht in Runtime-Ausgabe: PASS
- unbekannter Textlink leer: PASS
- inaktiver Textlink leer: PASS
- realer WordPress-Shortcode-Render: PASS
- zentrale Linkänderung wirkt: PASS
- Deaktivierung wirkt: PASS
- keine neue Tabelle: PASS
- bestehender Tarifrechner-Shortcode: PASS
- alter abgeschlossener Automation-Job wird gelöscht: PASS
- offener Job bleibt erhalten: PASS
- obsolete Recovery-Optionen werden entfernt: PASS
- PHP-Syntax: PASS
- ZIP-Source-Identität 28/28: PASS

## Exakt getesteter Installer

Datei:
`AFFILIATE_ZENTRALE_6.72.209.zip`

SHA256:
`0d312d16afeb91c8886e513d85327c828a622b4c16dea1fbb071665561a012b7`

Bytes:
`810707`

Workflow Artifact-ID:
`11551770130`

Workflow-Run:
`37779421162`

ZIP-Integrität:
PASS

## Ergebnis

6.72.209 ist als exakter KISS-Cleanup-/Textlink-Kandidat technisch PASS. Keine neue Architektur, keine neue Tabelle, kein Frontend-HTTP und keine zusätzliche Frontend-DB-Abfrage für Banner-/Rankingpfade.
