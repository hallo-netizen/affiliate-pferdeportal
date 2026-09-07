# AFFILIATE – HOBBYRAUM

STAND: 2026-09-07
STATUS: AKTIV

## 1-KLICK-ÜBERSICHT

**AKTUELLER AUFTRAG:**  
OTTO real abnehmen: Produktfeed + Productwissen-Exact-Match + reale Bannerquelle + automatische anteilsgesteuerte Bannerverteilung + manuelle Reparaturprobe.

**BEREITS STRUKTURELL UMGESETZT:**  
Awin/OTTO-Produkte, 1/2/3-Produktplätze, Exact-Consumer, Verkäufer-Gate, automatische Bannerziel-/Slotzuordnung, Relevance-First-Anteilssystem und Reparaturinstanz.

**NICHT TUN:**  
kein eigenes OTTO-Plugin; keine zweite Providerarchitektur; keine direkte Productwissen-Tabellenkopplung; kein Ersatzprodukt bei Exact Match; kein Produktbild als Banner; keine Quote vor Relevanz; Digistore24 nicht nebenbei öffnen.

## BANNERVERTEILUNG – AKTUELLER VERTRAG

Startanteile:
- OTTO 40
- Awin andere 25
- ADCELL 20
- Direkt 15
- Digistore24 0
- Sonstige 0

Regel:
**Relevanz/Sicherheit zuerst, Anteil nur zwischen gleich relevanten Möglichkeiten.**

Fehlende Quelle:
Anteile automatisch unter den verfügbaren gleich relevanten Quellen normalisieren.

Verteilungseinheit:
Bannerplätze, nicht abrechnungsgenaue Impressionen.

Stabilität:
Kalenderwoche + Kontext + Slot.

## REPARATURINSTANZ

Normalzustand = Automatik.

Intern möglich:
- fest auswählen;
- nicht anzeigen;
- Vererbung auf Unterseiten;
- zurück zur Automatik.

Zusätzlich Control-/Veto-Ebenen und Notabschaltung.

## NEXT ACTION – NUR DIESER WEG

0. Schnellprüfung ohne Docker, sobald ein Repo-Checkout vorhanden ist:
   `bash AFFILIATE_HOBBYRAUM/run_otto_checks.sh`

1. Gebundenen Hobbyraum-Test real ausführen:
   `AFFILIATE_HOBBYRAUM/TASK.current.json`
   inklusive `php test_otto_automation.php`.
2. Im eigenen Awin-Zugang OTTO Advertiser **14336** real nachweisen.
3. echten OTTO-Produktfeed prüfen und reale Verkäufer-Spalte bestimmen.
4. Produktfeed durch WordPress/MariaDB laufen lassen.
5. real prüfen:
   - Hub Produkt 1/2/3;
   - Kategorie Produkt 1/2/3;
   - Beitrag;
   - Productwissen Exact Match;
   - fehlender Exact Match = kein Ersatz.
6. realen OTTO/Awin-Bannerbestand oder belegten Export/API-Zugang bestimmen.
7. reale Banner importieren/holen.
8. reale automatische Bannerprüfung:
   - Ziel;
   - Relevanz;
   - Slot/Format;
   - Anteil;
   - Aktivierung.
9. über genügend Seiten/Slots reale Verteilung gegen Zielanteile prüfen.
10. mindestens eine bewusste Fehlzuordnung intern reparieren:
    - fest/none oder Veto;
    - danach auf Automatik zurücksetzen;
    - Rückkehr zur Automatik belegen.
11. Erst danach Release-Gates weiterführen.

## PRODUCTWISSEN-GRENZE

`ppar_affiliate_exact_product_requirements`

Produktwissen = fachlich.
Affiliate = Commerce.

Kein Exact Match = keine Karte.

## BANNERQUELLEN-GRENZE

Zuordnung, Anteilssystem, 0-Anteil-Sperre, Mehrfachplatz-Deduplizierung und manuelle Reparatur sind strukturell vorhanden.

Beschaffung ist erst vollständig automatisiert, wenn ein realer maschinenlesbarer OTTO/Awin-Creative-Weg belegt ist.

Bis dahin:
reales Creative → Automatik.
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

Vor Release auflösen.

Digistore24 bleibt zurückgestellt.


## REALER BANNERQUELLEN-ANSCHLUSS

Technische Anschlussstelle:
`ppar_affiliate_awin_static_creatives`

Nur reale Bannerzeilen:
Advertiser-ID + Creative-ID + Titel + Bild + Tracking.

Ungebunden → vorhandene Banner bleiben erhalten.
Gebunden und leer → `['bound'=>true,'rows'=>[]]` erlaubt kontrollierte Reconciliation.
Kein erfundener Awin-API-Weg.
