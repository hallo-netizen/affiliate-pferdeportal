# Wassertechnik – echter WordPress-Export / SEO-Qualitätsgate
**Stand 14.11.2026.** Daten: zwei original vom Nutzer exportierte JSON-Dateien (unverändert unter `WORDPRESS_TEST_20261114/`). Vollständig gelesen und lokal auf Struktur geprüft.

## Wo stehen wir?
- Ausführende Test-URL aus WordPress-Bestandsbericht: `https://wasser.oliver-beil.de/`; Plugin-Version **0.1.1**, Modus `READ_ONLY_INVENTORY`.
- WordPress meldet **2 Seiten, 1 Beitrag und 1 Kategorie**. Konkret: Seiten „Beispielseite“ (veröffentlicht), „Datenschutzerklärung“ (Entwurf), Beitrag „Hallo Welt!“ und Kategorie „Allgemein“. Keine Wassertechnik-Kategorieobjekte gemeldet.
- HivePress Listings/Kategorien jeweils `NOT_CONFIGURED`; Journal-/Affiliate- und Forschungsanschluss `NOT_CONNECTED` bzw. `NOT_MAPPED`. Das ist auf einer jungfräulichen Testseite kein unerklärter Fehler.
- Kostenloser W4-Preflight: **218/218** eindeutige Owner, genau **8** Hauptseiten, **19** Gruppen, **1** Industrie-Hub, **6** Industrielandings, **79** Produktseiten, **105** Rubriken. 0 verworfen, 0 Duplikat-Owner, 0 `review_holds`. Ausgabezeit `2026-11-14T12:29:04+00:00`, Report-Fingerprint `18db2da41da0a576cc07275766862606039dd630c963beb2e2caed05123c5b0f`.
- Der Preflight verweist auf dasselbe W4-Quellprofil wie das installierte WT001-0.1.1-ZIP (`source_sha256=ba70d1f5e67715ad4b93c80dca043579f8da23ef8da5652ff13eb37b9601f28f`); der GitHub-W4-Fachbaum besteht aus 79 Produktseiten/105 Rubriken. **Echte WP-Admin-Exportfunktion funktioniert.** Keine Aussage über andere nicht ausgeführte Pluginfunktionen.

## Problem: kein SEMANTISCHER SEO-PASS
`review_holds: 0` heißt nur: **keine technischen Sperren**, nicht „alle Suchbegriffe fachlich richtig“. Das WP-Bestandsformat bestätigt dies selbst durch `no_semantic_or_keyword_audit: true` und `keyword_research_status: NOT_CONNECTED`.

Bei den 218 Einträgen sind:
- **124** automatische Zusammenfügungen (19 Gruppen, 105 WP-Rubriken). Beispiel: „feinfilter filterpraxis“, „pumpen & druck druckversorgung“. Diese müssen redaktionell auf echte Nutzerfragen umgestellt, zusammengeführt oder als reine Strukturtitel belassen werden, bevor sie kostenpflichtig recherchiert werden.
- **4** weitere Menütitel mit zu prüfendem Suchwortlaut: „pumpen & druck“, „kühl- & kreislaufwasser“, „messung, regelung & dosierung“, „kommunale/großanlagen“.
- **90** übrige fachliche Startbegriffe, darunter 79 konkrete Produktbezeichnungen. Auch diese **sind noch nicht SEO-validiert**.

**Ein wichtiger Unterschied:** Die obigen Markierungen sind nur eine Qualitätskontrolle der Suchwortform, keine Keywordrecherche. Keine Keywordvolumina, SERPs oder Provisionen wurden ermittelt.

## Konkrete KISS-Reihenfolge
1. W4-Fachbaum und **genau eine** daraus abgeleitete redaktionelle Keywordzuordnung als Eigentümerbasis erhalten. Keine neuen oder doppelten Kategorieentscheidungen durch Plugins.
2. In `W4_KEYWORD_QUALITAET_218_20261114.csv` die 124 automatischen und vier Sammelbegriffe fachlich überarbeiten. Das kann anhand der 356 bereits angedachten Artikelschwerpunkte geschehen; **keine** kostenpflichtige Recherche oder erfundene Nachfrage.
3. Danach das SEO-Profil **zentral einmal** überarbeiten und im Wassertechnik-Kategorieplugin entsprechend anzeigen (keine zweite freie Keywordliste). Kostenlosen 218-Owner-Preflight erneut durchführen: jeder Owner vorhanden; reine Menütitel dürfen außerhalb bezahlter Keywords bleiben.
4. Erst nach separater Kostenfreigabe: DataForSEO im WordPress-Kategorieplugin, zuerst ausgewählte kaufnahe Produktbegriffe; Kostenkontrolle, Rückführung der Ergebnisse in den einen W4-Baum. Die aktuelle Testversion besitzt bewusst **keine** bezahlte SEO-Schnittstelle.
5. Sobald der gesamte Baum fachlich und SEO-seitig freigegeben ist, einmaliger geplanter WordPress-Import. Aktuell **kein** Import/kein Löschen der WordPress-Standardseiten notwendig.

**Status:** `ECHTER_WP_EXPORT_PASS; SEO-QUALITÄTSGATE_OFFEN; BEZAHLTE_ABFRAGE_GESPERRT; WP-IMPORT_GESPERRT`.
