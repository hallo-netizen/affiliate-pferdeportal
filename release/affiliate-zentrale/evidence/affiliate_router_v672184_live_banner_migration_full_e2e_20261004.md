# Affiliate Router 6.72.184 – Live-Banner-Migration – Full E2E

Datum: 2026-10-04
Workstream: AFFILIATE_ZENTRALE
Version: 6.72.184
Branch: affiliate-release-current

## Reale Ausgangslage

Auf der echten Schabracken-Seite war unter 6.72.183 weiterhin ein fachlich falscher SanoVet-Fütterungsbanner sichtbar. Damit war 6.72.183 live NICHT bestanden.

Root Cause:
- 6.72.183 machte die Creative-Library zwar für neu/materialisiert erzeugte Banner zur gespeicherten Ziel-URL-Wahrheit.
- Historische automatische Bannerkampagnen durften aber weiterhin parallel am Frontend-Ranking teilnehmen.
- Zusätzlich existierte kein gezielter Upgrade-Lauf, der den vorhandenen Bannerbestand einmalig durch die neue Ziel-URL-Sammelstelle zieht.
- Der generische Versions-Nachlauf würde stattdessen den gesamten Creative-Pool inklusive Produktzeilen erneut bearbeiten.

## KISS-Fix 6.72.184

1. Automatische Bannerquelle ist ausschließlich `source=output_object_v4`, also die Creative-Library-Materialisierung.
2. Historische/manuelle Kampagnen dürfen den automatischen Bannerpool nicht mehr parallel überstimmen.
3. Feste manuelle Bannerzuordnungen bleiben über den bestehenden Fixed-Pfad wirksam.
4. Ein eigener Banner-only-Migrationsworker verarbeitet nur aktive Banner aus der Creative-Library.
5. Der generische Vollpool-Nachlauf wird für dieses reine Bannerrelease nicht gestartet.
6. eBay-/Idealo-/Produktkampagnen werden nicht neu geplant.
7. Frontend-Hotpath: keine neue DB-Abfrage, kein Remoteaufruf, keine URL-Neuanalyse.

## Source Upgrade E2E

Run: 37223477984
Ergebnis: SUCCESS

Auf derselben WordPress-7.1.2/MariaDB-Installation:
- 6.72.183 reproduziert falschen Legacy-Banner: PASS
- relevanter Banner liegt unmaterialisiert in Creative-Library: PASS
- Upgrade auf 6.72.184: PASS
- Legacy-Automatik wird vor Migration ausgeschlossen: PASS
- alter Vollpool-Event/Cursor entfernt, kein Rescan: PASS
- Banner-only-Migration vollständig: PASS
- relevanter Schabracken-Banner danach sichtbar: PASS
- falscher SanoVet-Banner danach nicht sichtbar: PASS
- gespeicherte Schabracken-Zielkante vorhanden: PASS
- feste Legacy-Ausnahme bleibt sichtbar: PASS
- feste Legacy-Ausnahme mischt nicht in Automatik: PASS
- eBay-Produktkampagne bytegleich: PASS
- Idealo-Produktkampagne bytegleich: PASS
- zukünftiger Banner nutzt dieselbe Sammelstelle: PASS
- keine Remoteaufrufe: PASS

Gesamt: 20/20 PASS.

## Finales ZIP E2E

Run: 37223792210
Ergebnis: SUCCESS

Artifact:
`release/affiliate-zentrale/artifacts/final/AFFILIATE_ZENTRALE_6.72.184.zip`

SHA-256:
`bc101bd7dc06aa3ecbf085165914440e28e0b7aaefe6786d1e7db33fc7f8fe06`

Bytes:
`792763`

Git blob:
`21acf77857298b59cf1c9de085a37a71c763ad13`

Nachweise:
- ZIP 27/27 Manifest-Byteidentität: PASS
- PHP lint 21/21: PASS
- Performance-KISS-Hardlock: PASS
- exaktes Upgrade 6.72.183 -> installiertes ZIP 6.72.184: 20/20 PASS
- frischer kompletter Bannerpfad mit Library-Quelle: 21/21 PASS
- frische Ziel-URL-Sammelstelle: 26/26 PASS
- keine Remoteaufrufe im Frontend-/Migrationstest: PASS
- eBay und Idealo im Upgrade unverändert: PASS

## Testhistorie

Der erste ZIP-Gate-Lauf 37223643412 wurde absichtlich nicht abgenommen: Der historische 21er-Test erzeugte automatische Banner direkt als Legacy-Kampagnen außerhalb der Creative-Library. 6.72.184 blockiert genau diese parallele Quelle; deshalb wurde der Testfixture auf den neuen verbindlichen Vertrag umgestellt und der komplette Gate erneut ausgeführt. Erst Run 37223792210 wurde als finaler PASS verwendet.

## Live-Status

Produktiv auf pferde-atelier.de wurde 6.72.184 noch nicht installiert/readback-geprüft.

`release_allowed=false`

Nächste Aktion:
6.72.184 auf dem echten WordPress installieren und die reale Schabracken-Seite sowie weitere Bannerplätze zurücklesen.