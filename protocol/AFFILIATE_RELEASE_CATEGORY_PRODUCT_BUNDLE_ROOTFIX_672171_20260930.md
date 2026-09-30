# Affiliate-Zentrale 6.72.171 – Category-Product Bundle Performance Rootfix

Datum: 2026-09-30

## Realer Auslöser

Nach 6.72.170 ist der 6.72.169-eBay-Regressionsteil beseitigt, aber die strukturelle Restlatenz bleibt:
- Hub-1 /ausruestung/: ca. 1.44 s
- Hub-2 /ausruestung/ausruestung-sattel/: ca. 8.85 s
- Hub-2 /ausruestung/ausruestung-trensen-und-gebisse/: ca. 8.91 s
- Ebene 3 /.../trensen/: ca. 8.62 s
- Ebene 3 /.../pferdesaettel/: ca. 9.09 s

Template-Vertrag:
- Hub-1 rendert einen realen Partnerbanner.
- Hub-2 sowie Kategorie/Leaf rendern zusätzlich drei Produktplätze category_product_1..3.
- Der Router rankt diese drei Produktplätze bisher jeweils separat.

## Root Cause

Die drei category_product_* Slots sind fachlich ein gemeinsames 3er-Produktbundle derselben Seite. Trotzdem läuft der teure Kontext-/Target-Rankingpfad pro Slot erneut. Request-Caches vermeiden einzelne Rohdaten-/Normalisierungsschritte, aber nicht die komplette dreifache Ziel-/Eligibility-/Health-Auswertung.

## Fixziel

Den gemeinsamen fachlichen Ranking-Basislauf pro Seitenkontext genau einmal durchführen. Aus dieser unveränderten Rangbasis werden category_product_1, _2 und _3 anschließend jeweils mit ihren bisherigen slot-spezifischen Placement-, Control-, Provider- und Positionsregeln abgeleitet.

Kein gemeinsames "ein Ergebnis für alle Slots": slot-spezifische Bindungen/Vetos bleiben erhalten.

## Nicht ändern

- Kampagnenauswahl fachlich
- Reihenfolge
- Relevanzstufen
- PRIVATE/BUSINESS
- Providerstrategie und Provider-Mix
- Slot-Placement
- Control/Veto pro Slot
- Health
- Produktbild-Gate
- Affiliate-Tracking
- Design / Template Kit
- Admin/Cron/REST/WP-CLI-Verhalten

## Pflichtsimulation vor jeder Freigabe

Gleiche lokale WordPress-7.1.2/MariaDB-Instanz und identischer synthetischer Datenbestand, Baseline 6.72.170 gegen Kandidat 6.72.171:

POSITIV:
- Hub-1: Banneroutput identisch.
- Hub-2: Banner + category_product_1..3 Auswahl/HTML-Hash identisch.
- Kategorie/Leaf: Banner + category_product_1..3 identisch.
- Direktbindung.
- Parent-Bindung mit descendant.
- Generic category_product placement.
- slot-spezifische category_product_1/_2/_3 placements.
- eBay + idealo + Awin/OTTO Provider-Mix.

NEGATIV:
- falsches Target bleibt ausgeschlossen.
- falscher Slot bleibt ausgeschlossen.
- slot-spezifisches Veto bleibt gesperrt.
- inaktiver/ungültiger Kandidat bleibt ausgeschlossen.
- kein Kandidat bleibt leer.
- Admin/REST/Cron/WP-CLI fallen nicht in den Frontend-Bundlecache.

PERFORMANCE:
- exakt gleicher Datenbestand und gleiche vier Slot-Aufrufe.
- Baseline und Kandidat jeweils mehrere Läufe, Median vergleichen.
- mindestens 3x weniger vollständige category_product Kontext-Rankings; Ziel: genau 1 statt 3.
- keine Mehrabfragen.
- identischer fachlicher Output ist Voraussetzung; Performancegewinn ohne Outputgleichheit zählt nicht.

Erst bei PASS darf ein Installer gebaut werden.
