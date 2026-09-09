# AFFILIATE RELEASE — OTTO/AWIN FEED-VALIDIERUNG 2026-09-09

Workstream: `AFFILIATE_ZENTRALE`
Branch: `affiliate-release-current`
Advertiser: `OTTO DE / Awin 14336`
Status: `ROOTFIX_PENDING / AUTOMATION_OFF`

## Tatsächlich ausgeführte Live-/Dateiprüfungen

1. WordPress-Live-Lauf mit gebundenem Create-a-Feed abgeschlossen:
   - 298 Feedzeilen vollständig geprüft
   - 1 importiert
   - 297 blockiert
   - 0 aktualisiert
2. Exakt verwendete Nutzerdatei `datafeed_2990695.csv.gz` vollständig geprüft:
   - 211 Skincare / Gesichtspflege
   - 31 Cosmetics / Make-up
   - 28 Basketball
   - 22 Garden / Sonnenschutz
   - 6 Football
   - 0 belastbare Pferde-/Reitsportzeilen
3. Der einzige Import ist falsch positiv:
   - `aw_product_id=45749237798`
   - Titel enthält WPC-Gartenzaun / Sichtschutz / `Windschutz`
   - Root Cause: der OTTO-Gate setzt synthetisch `FeedScope=Pferdebedarf`; der gemeinsame Klassifikator behandelt `pferdebedarf` als starkes Pferdesignal und kann dadurch `Windschutz` gegen das Portal-Konzept `Windschutz für Pferde` routen.
4. Nutzerdatei `datafeeds.csv` vollständig auf OTTO 14336 geprüft. Aktuell exakt drei aktive Feeddatensätze:
   - 54165 — Wohnen, Spielzeug und Baumarkt — 317451 Produkte
   - 54179 — Technik und Sport — 90547 Produkte
   - 54183 — Kategorien: Mode und Beauty — 347642 Produkte
   - Kein separater Pferde-/Tierbedarf-/Schuhe-Feed in dieser aktuellen Feedliste.

Hinweis: Feed-Download-URLs enthalten einen privaten Awin-Schlüssel und werden deshalb bewusst **nicht** in GitHub protokolliert.

## WAS / WARUM

- Die bisherige Annahme, ein als `portal_filtered` bestätigter Feed könne zusätzlich als Fachbeweis in der Einzelzeilenklassifikation dienen, ist verworfen.
- Source-Scope und Produktrelevanz werden strikt getrennt:
  - Scope bestätigt nur die erlaubte Quelle.
  - Fachrelevanz muss aus realen Produktzeilen stammen.
- Awin-Feedwahl darf nur aus den drei real belegten OTTO-Feeds erfolgen; keine erfundenen Zusatzfeeds.

## NEXT ACTION

1. Awin-Auswahl innerhalb der realen drei OTTO-Feeds fachlich neu eingrenzen.
2. Minimaler Code-Rootfix: `FeedScope` nicht mehr als Pferde-Domain-Evidence in den Klassifikator einspeisen.
3. Vor neuem Plugin zwingend:
   - POSITIV: reales Pferde-/Reitsportprodukt wird belastbar erkannt;
   - NEGATIV: belegter WPC-`Windschutz`-Datensatz bleibt blockiert;
   - NEGATIV: weitere fachfremde Skincare/Cosmetics/Teamsport-Zeilen bleiben blockiert;
   - Gesamtworkflow/Regressionen/Manifest/Byte-Scope/Error-Register-Postcheck.
4. Automatische Synchronisierung bleibt bis zum Beleg AUS.

## Nicht geändert

- Keine Produktions-PHP-Datei in diesem Abschlussblock geändert.
- Keine neue Pluginversion gebaut.
- Kein Release-/Live-PASS für den Rootfix behauptet.
