# HD-009 – HOBBY DEPOT AFFILIATE-ZENTRALE – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-26
STATUS: PORTIERUNG IN ARBEIT / NICHT INSTALLIERBAR / KEIN RELEASE

Plugin-ID: HD-009-AFFILIATE-ZENTRALE
Name: Hobby Depot Affiliate-Zentrale
Art: Portierung der Pferdeatelier Affiliate-Zentrale

Fach-Current:
../../../AFFILIATE/CURRENT_STATE.md

Arbeitsbranch:
`hobbyrausch/hd009-affiliate-port-20261026`

Arbeitsquelle:
`WORKSOURCE/affiliate-portal-router/`

## Exakte Ausgangsbasis

Quelle:
`affiliate-release-current:release/affiliate-zentrale/current/affiliate-portal-router/`

Pferdeatelier-Branch-Head bei Übernahme:
`7375bc46a57ac4c2ff2a74a6dd4919113defd009`

Formaler Pferdeatelier-Kandidat:
6.72.211 / RELEASE BLOCKED durch AFF-ERR-065.

Wichtig:
Die Hobby-Depot-Portierung übernimmt die technische Quelle als Ausgangsbasis, nicht den Pferdeatelier-Release-/Live-PASS-Status.

28/28 Quelldateien wurden zunächst byte-identisch kopiert.
Danach entfernt:
- Pferdeatelier eBay-Zielkatalog;
- Pferdeatelier Portalstruktur;
- historischer Pferdeatelier-Recovery-Produktbestand.

## Provider-Wahrheit

- eBay: aktiv implementiert.
- idealo: aktiv implementiert.
- Amazon: nur vorbereitet; kein realer Adapter vorhanden.
- Awin/ADCELL/Digistore24/Direktpartner-Engine bleibt zunächst Bestandteil der technischen Basis und wird nur fachlich bereinigt, nicht blind entfernt.

## Credentials

Keine Zugangsdaten werden in diese Akte oder Quellkopie hineindokumentiert.
Die vorhandenen Options-/Konstanten-/Secret-Schnittstellen bleiben als Mechanismus erhalten.
Ein späterer Live-Transfer bestehender Zugangsdaten ist ein separater Laufzeit-/WordPress-Schritt.

## Noch nicht freigegeben

- keine Installations-ZIP;
- kein CURRENT.zip;
- kein Liveeinsatz;
- keine Hobby-Depot-Produktdaten;
- keine Amazon-Produktrecherche behaupten;
- keine Pferdeatelier-Zielbestände wiederverwenden.

## Zwischen-Gates – Stand 2026-10-26

1. **GATE 1 – Pferdeatelier-Bereinigung: PASS**
   - Pferdeatelier-eBay-Zielkatalog entfernt.
   - Pferdeatelier-Portalstruktur entfernt.
   - historischer Pferdeatelier-Recovery-Produktbestand entfernt.
   - verbleibende PHP/JS/CSS-Dateien vollständig auf Pferd/Pferdeatelier/Horse/Equine/Pony/Fohlen/Hengst/Stute/Wallach/Rasse/Breed/Sattel/Schabracke/Huf/Trense/Zaum/Halfter gescannt.
   - aktive Pferde-Fachlogik: 0 Treffer; letzte reine Rassen-/Breed-Altkommentare entfernt.

2. **GATE 2 – Hobby-Depot-Zielquelle: PASS (Vertrag), LIVE noch nicht geprüft**
   - `class-hdar-hobby-depot-source.php` nutzt ausschließlich die read-only HD-004-Kategorie-Registry.
   - verwendete API `hd_category_registry_ready()`, `hd_category_registry_revision()`, `hd_category_registry_snapshot()` stimmt exakt mit `KATEGORIE_ZENTRALE/RUNTIME_API.md` überein.
   - fail-closed bei fehlender Registry, ungültigem Snapshot, != 8 CORE-Welten oder < 300 strukturell belegten Hobbyseiten.
   - keine zweite Kategorie-/Produkt-Masterdatenhaltung im Affiliate-Plugin.

3. **GATE 3 – Provider-Recherchepfade:** IN ARBEIT
   - eBay und idealo gegen die neue Hobby-Depot-Zielquelle end-to-end prüfen.
   - Amazon bleibt vorbereitet; kein Adapter erfinden.

4. **GATE 4 – Positiv/Negativ/Regression:** OFFEN
5. **GATE 5 – Installationspaket/CURRENT.zip:** OFFEN; vor Gate 4 verboten.

## ERSTER OFFENER BLOCKER

eBay- und idealo-Recherche-/Zuordnungspfade müssen jetzt gegen die neue Hobby-Depot-Zielquelle vollständig geprüft und bei Bedarf minimal angepasst werden.

## EXAKT EINE NEXT ACTION

GATE 3 ausführen: eBay- und idealo-Recherchepfade vollständig gegen `HDAR_Hobby_Depot_Source` prüfen, Positiv- und Negativpfade belegen und nur echte verbleibende Pferdeportal-Annahmen minimal ersetzen.
