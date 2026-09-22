# Affiliate Performance Cleanup – Zielvertrag 2026-09-22

Rolle: autoritative Zielquelle für den aktuell eingeschobenen Performance-Auftrag.
Diese Datei ist KEINE Status-/CURRENT-/NEXT-ACTION-Quelle. Der dynamische Stand liegt ausschließlich in `control/release-governance/CURRENT_RELEASE.json`.

## Ziel

Die zwei eigenen, im Frontend gemeinsam wirkenden Plugins werden global bereinigt, ohne Fachlogik, Daten, Design oder Affiliate-Entscheidungen zu verändern:

1. PPA-001 – Affiliate-Zentrale / Affiliate Portal Router
   - bereits live bewiesene 6.72.145-SQL-Batchbereinigung erhalten;
   - verbleibende unnötige CPU-Wiederholungen in zentralen eBay-/Rankingpfaden beseitigen;
   - Wirkung global für Kategorieebenen, Portalseiten und Einzelbeiträge;
   - keine Änderung an Veto, Approval, Slots, Targets, BUSINESS/PRIVATE, Providertransport, Tracking, Bannerregeln, CSS oder JS.

2. PPA-013 – Pferde Atelier Design / Affiliate Portal Template Kit
   - doppelten teuren Menü-Setup-/Metadata-Aufwand des gemeinsamen Headers reduzieren;
   - Desktop- und Mobile-Ausgabe sowie ihre unterschiedlichen Filter vollständig erhalten;
   - Wirkung global auf alle Seitentypen, die den gemeinsamen Header nutzen;
   - keine Layout-/Inhalts-/Navigationsregel verändern.

## Abnahme

PPA-001:
- Positiv/Negativ-/Semantikgleichheit;
- bestehender 6.72.145 DB-Batchvertrag unverändert PASS;
- Banner-/Rankingregression PASS;
- echtes WordPress/MariaDB-Gate PASS;
- installierbarer Kandidat mit ZIP-/Fresh-Unpack-/SHA-Prüfung;
- anschließend echter Live-Performance-Readback.

PPA-013:
- beide originalen Desktop-/Mobile-Menürenderpfade bleiben erhalten;
- HTML-Ausgabe vor/nach Fix byteidentisch;
- bestehende Desktop-/Mobile-Filter bleiben erhalten;
- zweiter Menü-Setup-Pfad reduziert Metadata-Hooklast deutlich;
- echter WordPress-Test PASS;
- vor einem installierbaren Paket muss der exakt aktuelle Live-Vollstand des Plugins gebunden werden; kein historisches Vollpaket darf den Live-Stand überschreiben.

## Reihenfolge / Out of scope

1. Erst PPA-001 und PPA-013 sauber abschließen.
2. Danach Kubio separat behandeln.
3. Erst danach ein alternatives Theme isoliert testen.

Bis zum Abschluss der zwei Pluginbereinigungen:
- Kubio NICHT verändern.
- Astra/Theme NICHT verändern.
- Bannerarbeit 6.72.143 bleibt pausiert.
- 6.72.142 GOLDMASTER bleibt unveränderlicher Router-Rollbackanker.
