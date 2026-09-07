# AFFILIATE – HOBBYRAUM

STAND: 2026-09-07
STATUS: AKTIV

## 1-KLICK-ÜBERSICHT

**AKTUELLER AUFTRAG:**  
OTTO über den bestehenden Awin-Weg vollständig real abnehmen: Produktfeed + automatische Zuordnung + Exact Product Match + reale Bannerquelle.

**BEREITS STRUKTURELL UMGESETZT:**  
Awin/OTTO-Verteilung, 1/2/3-Produktplätze, Beitragsprodukte, Productwissen-Exact-Consumer, Verkäufer-Gate und automatische Zuordnung realer importierter Banner.

**NICHT TUN:**  
kein eigenes OTTO-Plugin; keine zweite Providerarchitektur; keine Productwissen-Tabellen direkt lesen/schreiben; kein ähnlich passendes Ersatzprodukt für Exact Match; kein Produktbild als Banner; Digistore24 nicht nebenbei öffnen.

## NEXT ACTION – NUR DIESER WEG

1. Gebundenen Affiliate-Hobbyraum-Test real ausführen:
   `AFFILIATE_HOBBYRAUM/TASK.current.json`
   inklusive `php test_otto_automation.php`.
2. Im eigenen Awin-Zugang OTTO Advertiser **14336** real nachweisen.
3. echten OTTO-Produktfeed prüfen:
   - Feed eindeutig?
   - reale Felder?
   - Verkäufer-Spalte exakt bestimmen;
   - nichts raten.
4. echten Produktfeed durch WordPress/MariaDB laufen lassen.
5. real prüfen:
   - Hub Produkt 1/2/3;
   - Kategorie Produkt 1/2/3;
   - normaler Beitrag;
   - Productwissen Exact Match / kein Ersatz.
6. realen OTTO/Awin-Bannerbestand bzw. belegten Export/API-Zugang bestimmen.
7. mindestens ein echtes OTTO-Banner importieren/holen und die vorhandene automatische Ziel-/Slotzuordnung real prüfen.
8. Erst danach Release-Gates weiterführen.

## PRODUCTWISSEN-GRENZE

Produktwissen ist fachliche Identitätsquelle.
Affiliate ist Commerce-Schicht.

Schnittstelle:
`ppar_affiliate_exact_product_requirements`

Kein Exact Match = keine Karte.
Kein Affiliate-Ersatzmodell.

## BANNER-GRENZE

Zuordnung ist automatisiert.
Beschaffung ist erst automatisiert, wenn ein realer maschinenlesbarer Awin-/OTTO-Creative-Weg belegt ist.

Bis dahin:
real importiertes Creative → automatisch prüfen/zuordnen/aktivieren.
Kein reales Creative → kein Banner.

## TECHNISCHE AUTORITÄTEN

- `control/release-governance/CURRENT_RELEASE.json`
- `release/affiliate-zentrale/AGENTS.md`
- `release/affiliate-zentrale/current/affiliate-portal-router/`
- `release/affiliate-zentrale/CURRENT_SOURCE_SHA256.txt`
- `protocol/AFFILIATE_RELEASE_OTTO_AUTOMATION_CONCEPT_20260907.md`

## OFFENE RELEASE-GRENZE

GitHub Kandidat: 6.72.1  
WordPress-Livebeleg: 6.72.2

Vor realem Release auflösen; nicht still ignorieren.

Digistore24 bleibt zurückgestellt.
